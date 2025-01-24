import logging
from contextlib import closing
from pathlib import Path
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl
from typing import Any
from pyhive import hive
import thrift
import time
import re

logger = logging.getLogger('mcp_hive_server')
logger.info("Starting MCP Hive Server")

PROMPT_TEMPLATE = """Welcome to the Hive MCP Server! This powerful tool enables you to interact with your Hive data warehouse through the Model Context Protocol (MCP).

Important Notes:
1. Data Understanding (Required First Steps):
   - Before querying, please understand the data structure and relationships
   - Use list_tables to see all available tables in {database}
   - Use describe_table to examine table schemas: {database}.table_name
   - Ask about table relationships and field meanings
   - Review sample data before complex queries

2. Query Execution Rules:
   - ONLY SELECT queries are allowed
   - Always use fully qualified table names: {database}.table_name
   - Example: SELECT * FROM {database}.users WHERE id = 1
   - DO NOT use semicolons (;) in queries
   - DO NOT use multiple statements in one query
   - DO NOT use comments (-- or /* */) in queries
   - Start with simple queries to verify data
   - Consider data volume and query performance

3. Query Restrictions:
   Forbidden Operations:
   - No DDL operations (CREATE, DROP, ALTER, TRUNCATE)
   - No DML operations (INSERT, UPDATE, DELETE, MERGE)
   - No privilege operations (GRANT, REVOKE)
   - No system operations (SET, ADD, RELOAD, REFRESH)
   - No data loading operations (LOAD, EXPORT, IMPORT, MSCK)

4. Error Handling:
   Common Error Types:
   - Permission errors: Check if you have access to the requested table
   - Syntax errors: Verify query format and date formats
   - Connection errors: System will auto-retry on connection issues
   - Semantic errors: Verify table names and field names

5. Best Practices:
   - Understand table relationships before joining
   - Verify field meanings and data types
   - Test queries with LIMIT clause first
   - Document your findings about data structure
   - Use appropriate date formats in queries
   - Always check table permissions before querying

6. Available Tools:
   - list_tables: View all available tables in {database}
   - describe_table: View table schema (use as: {database}.table_name)
   - read_query: Execute SELECT queries after understanding data

7. Security Features:
   - SQL injection protection
   - SELECT-only query restrictions
   - Automatic reconnection mechanism
   - Query validation and sanitization
   - Permission verification

Selected topic: {topic}

Recommended Workflow:
1. First, list available tables:
   - Use list_tables to see what's available
2. Then, understand table structures:
   - Use describe_table for each relevant table
   - Ask about field meanings and relationships 
3. Finally, build your query:
   - Start with simple SELECT statements
   - Test with LIMIT clause
   - Gradually add complexity as needed
   - Ensure compliance with query rules

Remember:
- Always prefix table names with '{database}.'
- Understand data before querying
- Ask questions about data structure
- Verify relationships between tables
- Test queries incrementally
- Follow all query restrictions
- Handle errors appropriately

Feel free to ask questions about:
- Table structures and relationships
- Field meanings and data types
- Best practices for specific queries
- Data quality and constraints
- Error messages and troubleshooting
- Query optimization suggestions

Let's start by understanding your data structure. What would you like to explore first?"""

class HiveDatabase:
    def __init__(self, args):
        self.args = args
        self.conn = None
        self.max_retries = 2
        self._init_database()

    def _check_connection(self) -> bool:
        """检查数据库连接是否有效"""
        if not self.conn:
            return False
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            return False

    def _init_database(self):
        """Initialize connection to the Hive database"""
        logger.debug("Initializing database connection")
        # 验证必要参数
        required_params = ['host', 'port', 'username', 'password', 'database']
        for param in required_params:
            if not getattr(self.args, param):
                raise ValueError(f"Missing required parameter: {param}")
        
        retry_count = 0
        last_error = None
        
        while retry_count < self.max_retries:
            try:
                configuration = {}
                if self.args.configuration:
                    for param in self.args.configuration.split(';'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            configuration[key.strip()] = value.strip()
                
                self.conn = hive.Connection(
                    host=self.args.host,
                    port=self.args.port,
                    username=self.args.username,
                    password=self.args.password,
                    database=self.args.database,
                    configuration=configuration,
                    auth='CUSTOM'
                )
                logger.info("Successfully connected to Hive database")
                return
            except Exception as e:
                last_error = e
                retry_count += 1
                logger.warning(f"Connection attempt {retry_count}/{self.max_retries} failed: {e}")
                if retry_count < self.max_retries:
                    time.sleep(1)  # 等待1秒后重试
        
        logger.error(f"Failed to connect to Hive database after {self.max_retries} attempts")
        raise last_error

    def _reconnect_if_needed(self):
        """检查连接并在需要时重连"""
        if not self._check_connection():
            logger.info("Connection lost, attempting to reconnect")
            self._init_database()

    def _validate_select_query(self, query: str) -> bool:
        """验证查询的合法性，使用黑名单机制"""
        # 转换为大写并移除多余空格
        normalized_query = ' '.join(query.strip().upper().split())
        
        # 危险操作黑名单
        dangerous_keywords = {
            # DDL 操作
            'CREATE', 'DROP', 'ALTER', 'TRUNCATE', 
            # DML 操作
            'INSERT', 'UPDATE', 'DELETE', 'MERGE',
            # 权限操作
            'GRANT', 'REVOKE',
            # 系统操作
            'SET', 'ADD', 'RELOAD', 'REFRESH',
            # 其他危险操作
            'LOAD', 'EXPORT', 'IMPORT', 'MSCK'
        }
        
        # 检查是否包含危险关键字（按单词匹配）
        query_words = set(normalized_query.split())
        if any(keyword in query_words for keyword in dangerous_keywords):
            logger.warning(f"Query contains dangerous keyword: {query}")
            return False
            
        # 检查是否包含注释符号(防止 SQL 注入)
        if any(comment in normalized_query for comment in ['--', '/*', '*/']):
            logger.warning(f"Query contains comment symbols: {query}")
            return False

        # 检查是否是SELECT语句
        if not normalized_query.strip().startswith('SELECT'):
            logger.warning(f"Query must start with SELECT: {query}")
            return False

        # 检查分号使用
        if normalized_query.count(';') > 0:
            logger.warning(f"Query contains semicolon, which is not allowed: {query}")
            return False
            
        # 允许所有其他查询
        return True

    def _format_error_message(self, error: Exception) -> str:
        """格式化错误消息，提供更友好的错误提示"""
        if isinstance(error, thrift.transport.TTransport.TTransportException):
            return "数据库连接错误，请检查网络连接和数据库状态"
        
        error_msg = str(error)
        
        # 处理权限错误
        if "unauthorized db table operation" in error_msg:
            table_match = re.search(r'table=([^,\]]+)', error_msg)
            if table_match:
                table_name = table_match.group(1)
                return f"没有权限访问表 {table_name}，请确认您有正确的访问权限"
            return "权限错误：没有足够的权限执行此操作"
            
        # 处理语法错误
        if "ParseException" in error_msg:
            if "cannot recognize input near" in error_msg:
                return "SQL语法错误：请检查日期格式或引号使用是否正确"
            return "SQL语法错误：请检查查询语句的语法"
            
        # 处理其他常见错误
        if "SemanticException" in error_msg:
            return "语义错误：请检查表名、字段名是否正确，以及查询逻辑是否合理"
            
        return f"执行查询时发生错误: {error_msg}"

    def _execute_query(self, query: str) -> list[dict[str, Any]]:
        """Execute a HQL query and return results as a list of dictionaries"""
        logger.debug(f"Executing query: {query}")
        try:
            # 验证查询
            if not self._validate_select_query(query):
                raise ValueError(f"Invalid or unsafe query detected: {query}")
            
            # 检查连接状态
            self._reconnect_if_needed()
            
            retry_count = 0
            last_error = None
            
            while retry_count < self.max_retries:
                try:
                    with closing(self.conn.cursor()) as cursor:
                        cursor.execute(query)
                        if cursor.description:
                            columns = [col[0] for col in cursor.description]
                            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                            logger.debug(f"Read query returned {len(results)} rows")
                            return results
                        return []
                except thrift.transport.TTransport.TTransportException as e:
                    last_error = e
                    retry_count += 1
                    logger.warning(f"Query attempt {retry_count}/{self.max_retries} failed: {e}")
                    if retry_count < self.max_retries:
                        self._reconnect_if_needed()
                        time.sleep(1)  # 等待1秒后重试
                except Exception as e:
                    error_msg = self._format_error_message(e)
                    logger.error(f"Query execution error: {error_msg}")
                    raise ValueError(error_msg)
            
            error_msg = self._format_error_message(last_error)
            logger.error(f"Query failed after {self.max_retries} attempts: {error_msg}")
            raise last_error
                
        except Exception as e:
            error_msg = self._format_error_message(e)
            logger.error(f"Database error executing query: {error_msg}")
            raise ValueError(error_msg)

async def main(args):
    logger.info(f"Starting Hive MCP Server with connection parameters: host={args.host}, port={args.port}, database={args.database}")

    db = HiveDatabase(args)
    server = Server(
        "hive"
    )

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        logger.debug("Handling list_prompts request")
        return [
            types.Prompt(
                name="mcp-demo",
                description="A prompt to demonstrate what you can do with a Hive MCP Server + Claude",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Topic to analyze in the Hive database",
                        required=True,
                    )
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        logger.debug(f"Handling get_prompt request for {name} with args {arguments}")
        if name != "mcp-demo":
            logger.error(f"Unknown prompt: {name}")
            raise ValueError(f"Unknown prompt: {name}")

        if not arguments or "topic" not in arguments:
            logger.error("Missing required argument: topic")
            raise ValueError("Missing required argument: topic")

        topic = arguments["topic"]
        prompt = PROMPT_TEMPLATE.format(topic=topic)

        logger.debug(f"Generated prompt template for topic: {topic}")
        return types.GetPromptResult(
            description=f"Demo template for {topic}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(type="text", text=prompt.strip()),
                )
            ],
        )

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="read_query",
                description="Execute a SELECT query on the Hive database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SELECT HQL query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="list_tables",
                description="List all tables in the Hive database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="describe_table",
                description="Get the schema information for a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name of the table to describe"},
                    },
                    "required": ["table_name"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "list_tables":
                results = db._execute_query(
                    "SHOW TABLES"
                )
                return [types.TextContent(type="text", text=str(results))]

            elif name == "describe_table":
                if not arguments or "table_name" not in arguments:
                    raise ValueError("Missing table_name argument")
                    
                # 验证表名防止注入
                table_name = arguments["table_name"].strip()
                if not table_name.isalnum() and not all(c in '_' for c in table_name if not c.isalnum()):
                    raise ValueError("Invalid table name")
                    
                results = db._execute_query(
                    f"DESCRIBE {table_name}"
                )
                return [types.TextContent(type="text", text=str(results))]

            if not arguments:
                raise ValueError("Missing arguments")

            if name == "read_query":
                if not arguments["query"]:
                    raise ValueError("Empty query")
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hive",
                server_version="0.6.3",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
