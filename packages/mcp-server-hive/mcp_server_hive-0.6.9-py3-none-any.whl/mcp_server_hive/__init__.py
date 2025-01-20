from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Hive MCP Server')
    parser.add_argument('--username', 
                       default="hive",
                       help='Hive username')
    parser.add_argument('--password',
                       default="",
                       help='Hive password') 
    parser.add_argument('--host',
                       default="localhost",
                       help='Hive server hostname')
    parser.add_argument('--port',
                       type=int,
                       default=10000,
                       help='Hive server port')
    parser.add_argument('--database',
                       default="default",
                       help='Hive database name')
    parser.add_argument('--configuration',
                       default="",
                       help='Additional configuration string for Hive connection')
    
    args = parser.parse_args()
    asyncio.run(server.main(args))


# Optionally expose other important items at package level
__all__ = ["main", "server"]
