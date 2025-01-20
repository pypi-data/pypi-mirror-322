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

logger = logging.getLogger('mcp_hive_server')
logger.info("Starting MCP Hive Server")

PROMPT_TEMPLATE = """Welcome to the Hive MCP Server! This powerful tool enables you to interact with your Hive data warehouse through the Model Context Protocol (MCP).
This MCP server provides the following core functionalities:
1. Data Querying:
   - Execute SELECT queries (read_query tool)
   - List all available tables (list_tables tool)
   - View table schemas (describe_table tool)
2. Security Features:
   - SQL injection protection
   - SELECT-only query restrictions
   - Automatic reconnection mechanism
You have selected the topic: {topic}
Let's start exploring your data! You can:
- Use list_tables to see available data tables
- Use describe_table to understand table structures
- Use read_query to execute queries
Feel free to ask me about any data you'd like to explore!"""

class HiveDatabase:
    def __init__(self, args):
        self.args = args
        self._init_database()

    def _init_database(self):
        """Initialize connection to the Hive database"""
        logger.debug("Initializing database connection")
        # 验证必要参数
        required_params = ['host', 'port', 'username', 'password', 'database']
        for param in required_params:
            if not getattr(self.args, param):
                raise ValueError(f"Missing required parameter: {param}")
            
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
        except Exception as e:
            logger.error(f"Failed to connect to Hive database: {e}")
            raise

    def _validate_select_query(self, query: str) -> bool:
        """验证 SELECT 查询的合法性"""
        # 转换为大写并移除多余空格
        normalized_query = ' '.join(query.strip().upper().split())
        
        # 基本语法检查
        if not normalized_query.startswith('SELECT'):
            return False
            
        # 禁止危险操作
        dangerous_keywords = {'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE', 'MERGE'}
        if any(keyword in normalized_query for keyword in dangerous_keywords):
            return False
            
        # 检查是否包含注释符号(防止 SQL 注入)
        if any(comment in normalized_query for comment in ['--', '/*', '*/']):
            return False
            
        return True

    def _execute_query(self, query: str) -> list[dict[str, Any]]:
        """Execute a HQL query and return results as a list of dictionaries"""
        logger.debug(f"Executing query: {query}")
        try:
            # 验证查询
            if not self._validate_select_query(query):
                raise ValueError("Invalid or unsafe query detected")
                
            with closing(self.conn.cursor()) as cursor:
                try:
                    cursor.execute(query)
                except thrift.transport.TTransport.TTransportException as e:
                    logger.error(f"Hive connection error: {e}")
                    self._init_database()  # 重新连接
                    cursor.execute(query)
                except Exception as e:
                    logger.error(f"Query execution error: {e}")
                    raise
                
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    logger.debug(f"Read query returned {len(results)} rows")
                    return results
                return []
                
        except Exception as e:
            logger.error(f"Database error executing query: {e}")
            raise

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
