import unittest
import pytest
import pytest_asyncio
from unittest.mock import Mock, patch, AsyncMock
import argparse
from mcp_server_hive.server import HiveDatabase, PROMPT_TEMPLATE
from mcp.server.models import InitializationOptions
import mcp.types as types
from pydantic import AnyUrl
from typing import Any

class TestHiveDatabase(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.args = argparse.Namespace(
            host="localhost",
            port=10000,
            username="test_user",
            password="",  # 空密码用于测试
            database="test_db",
            configuration=""
        )
        
        # Mock Hive connection
        self.conn_patcher = patch('mcp_server_hive.server.hive.Connection')
        self.mock_conn = self.conn_patcher.start()
        
        # Mock cursor with context manager
        self.mock_cursor = Mock()
        self.mock_cursor.__enter__ = Mock(return_value=self.mock_cursor)
        self.mock_cursor.__exit__ = Mock(return_value=None)
        self.mock_conn.return_value.cursor.return_value = self.mock_cursor
        
        # 设置查询结果
        self.mock_cursor.execute.return_value = None
        self.mock_cursor.description = [('col1',), ('col2',)]
        self.mock_cursor.fetchall.return_value = [(1, 'a'), (2, 'b')]
        
        # 创建数据库实例
        self.db = HiveDatabase(self.args)
        
    def tearDown(self):
        """清理测试环境"""
        self.conn_patcher.stop()
        
    def test_init_database(self):
        """测试数据库初始化"""
        self.mock_conn.assert_called_once_with(
            host="localhost",
            port=10000,
            username="test_user",
            password="",  # 空密码用于测试
            database="test_db",
            configuration="",
            auth="CUSTOM"
        )
        
    def test_validate_select_query_valid(self):
        """测试有效的 SELECT 查询验证"""
        valid_queries = [
            "SELECT * FROM test_table",
            "SELECT col1, col2 FROM test_table WHERE col1 > 0",
            "SELECT COUNT(*) FROM test_table GROUP BY col1",
            "  SELECT  *  FROM  test_table  ",  # 空格测试
        ]
        
        for query in valid_queries:
            with self.subTest(query=query):
                self.assertTrue(self.db._validate_select_query(query))
                
    def test_validate_select_query_invalid(self):
        """测试无效的查询验证"""
        invalid_queries = [
            "INSERT INTO test_table VALUES (1, 2)",
            "DELETE FROM test_table",
            "DROP TABLE test_table",
            "SELECT * FROM test_table; DROP TABLE test_table",
            "SELECT * FROM test_table -- comment",
            "/* comment */ SELECT * FROM test_table",
            "UPDATE test_table SET col1 = 1",
            "",  # 空查询
            "MERGE INTO test_table",
        ]
        
        for query in invalid_queries:
            with self.subTest(query=query):
                self.assertFalse(self.db._validate_select_query(query))
                
    def test_execute_query_results(self):
        """测试查询执行和结果处理"""
        # 设置模拟返回值
        self.mock_cursor.description = [('col1',), ('col2',)]
        self.mock_cursor.fetchall.return_value = [(1, 'a'), (2, 'b')]
        
        # 执行查询
        results = self.db._execute_query("SELECT col1, col2 FROM test_table")
        
        # 验证结果
        expected_results = [
            {'col1': 1, 'col2': 'a'},
            {'col1': 2, 'col2': 'b'}
        ]
        self.assertEqual(results, expected_results)
        
        # 验证查询执行
        self.mock_cursor.execute.assert_called_once_with("SELECT col1, col2 FROM test_table")
        
    def test_execute_query_connection_retry(self):
        """测试连接断开时的重试机制"""
        # 设置第一次执行失败,第二次成功
        self.mock_cursor.execute.side_effect = [
            Mock(side_effect=Exception("Connection lost")),
            None
        ]
        
        # 执行查询
        try:
            self.db._execute_query("SELECT * FROM test_table")
        except Exception:
            self.fail("Query execution with retry failed")
            
    def test_synthesize_memo(self):
        """测试备忘录生成"""
        # 添加一些见解
        self.db.insights = [
            "First insight",
            "Second insight"
        ]
        
        memo = self.db._synthesize_memo()
        
        # 验证备忘录格式
        self.assertIn("Business Intelligence Memo", memo)
        self.assertIn("First insight", memo)
        self.assertIn("Second insight", memo)
        self.assertIn("Analysis has revealed 2 key business insights", memo)
        
    def test_empty_memo(self):
        """测试空备忘录"""
        memo = self.db._synthesize_memo()
        self.assertEqual(memo, "No business insights have been discovered yet.")

@pytest.mark.asyncio
class TestMCPServer:
    @pytest_asyncio.fixture
    async def server_setup(self):
        """设置服务器测试环境"""
        args = argparse.Namespace(
            host="localhost",
            port=10000,
            username="test_user",
            password="",  # 空密码用于测试
            database="test_db",
            configuration=""
        )
        
        # Mock 数据库
        with patch('mcp_server_hive.server.HiveDatabase') as mock_db_class:
            mock_db_instance = Mock()
            mock_db_class.return_value = mock_db_instance
            mock_db_instance._synthesize_memo.return_value = "Test memo"
            mock_db_instance._execute_query.return_value = [{"result": "test"}]
            mock_db_instance.insights = []
            
            # Mock 连接和游标
            mock_db_instance.conn = Mock()
            mock_cursor = Mock()
            mock_cursor.__enter__ = Mock(return_value=mock_cursor)
            mock_cursor.__exit__ = Mock(return_value=None)
            mock_db_instance.conn.cursor.return_value = mock_cursor
            mock_cursor.description = [('result',)]
            mock_cursor.fetchall.return_value = [("test",)]
            
            # 创建服务器实例
            from mcp_server_hive.server import Server
            server = Server("hive")
            
            # 设置初始化选项
            server._initialization_options = InitializationOptions(
                server_name="hive",
                server_version="0.6.3",
                capabilities={},
            )
            
            # 注册处理程序
            @server.list_resources()
            async def handle_list_resources() -> list[types.Resource]:
                return [
                    types.Resource(
                        uri=AnyUrl("memo://insights"),
                        name="Business Insights Memo",
                        description="A living document of discovered business insights",
                        mimeType="text/plain",
                    )
                ]
            
            @server.read_resource()
            async def handle_read_resource(uri: AnyUrl) -> str:
                if uri.scheme != "memo":
                    raise ValueError(f"Unsupported URI scheme: {uri.scheme}")
                path = str(uri).replace("memo://", "")
                if not path or path != "insights":
                    raise ValueError(f"Unknown resource path: {path}")
                return mock_db_instance._synthesize_memo()
            
            @server.list_tools()
            async def handle_list_tools() -> list[types.Tool]:
                return [
                    types.Tool(
                        name="read_query",
                        description="Execute a SELECT query on the Hive database",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "SELECT SQL query to execute"},
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
                    types.Tool(
                        name="append_insight",
                        description="Add a business insight to the memo",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "insight": {"type": "string", "description": "Business insight discovered from data analysis"},
                            },
                            "required": ["insight"],
                        },
                    ),
                ]
            
            @server.call_tool()
            async def handle_call_tool(
                name: str, arguments: dict[str, Any] | None
            ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
                if name == "read_query":
                    results = mock_db_instance._execute_query(arguments["query"])
                    return [types.TextContent(type="text", text=str(results))]
                elif name == "append_insight":
                    mock_db_instance.insights.append(arguments["insight"])
                    return [types.TextContent(type="text", text="Insight added")]
                else:
                    raise ValueError(f"Unknown tool: {name}")
            
            return server, mock_db_instance
            
    async def test_list_resources(self, server_setup):
        """测试资源列表功能"""
        server, _ = server_setup
        
        resources = await server.list_resources()
        assert len(resources) == 1
        assert resources[0].uri == AnyUrl("memo://insights")
        assert resources[0].name == "Business Insights Memo"
        
    async def test_read_resource(self, server_setup):
        """测试读取资源功能"""
        server, mock_db = server_setup
        
        result = await server.read_resource(AnyUrl("memo://insights"))
        assert result == "Test memo"
        
        with pytest.raises(ValueError):
            await server.read_resource(AnyUrl("invalid://resource"))
            
    async def test_list_tools(self, server_setup):
        """测试工具列表功能"""
        server, _ = server_setup
        
        tools = await server.list_tools()
        tool_names = {tool.name for tool in tools}
        assert tool_names == {"read_query", "list_tables", "describe_table", "append_insight"}
        
    async def test_call_tool(self, server_setup):
        """测试工具调用功能"""
        server, mock_db = server_setup
        
        # 测试 read_query
        result = await server.call_tool("read_query", {"query": "SELECT * FROM test"})
        assert str([{"result": "test"}]) in result[0].text
        
        # 测试无效查询
        with pytest.raises(ValueError):
            await server.call_tool("read_query", {"query": "DELETE FROM test"})
            
        # 测试未知工具
        with pytest.raises(ValueError):
            await server.call_tool("unknown_tool", {}) 