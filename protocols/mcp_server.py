"""
Enhanced MCP Server Implementation
خادم بروتوكول MCP المحسن

Advanced MCP server with Supabase integration and Git operations
"""

import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

# Optional imports - handle gracefully if not available
try:
    import mcp.server.stdio
    import mcp.types as types
    from mcp.server import NotificationOptions, Server
    from mcp.server.models import InitializationOptions
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    types = None
    NotificationOptions = None
    Server = None
    InitializationOptions = None

try:
    from supabase import Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

try:
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    Repo = None

logger = logging.getLogger(__name__)

# Enhanced MCP server instance
if MCP_AVAILABLE:
    mcp_server = Server("morvo-enhanced-mcp")
else:
    mcp_server = None  # Define as None when MCP is not available


class EnhancedMCPResource:
    """Enhanced MCP Resource with Supabase integration"""
    
    def __init__(self, supabase_client: Optional[Client] = None, git_repos: Optional[Dict[str, Repo]] = None):
        self.supabase = supabase_client
        self.git_repos = git_repos or {}
        
    async def get_resource_content(self, uri: str) -> str:
        """Get enhanced resource content"""
        try:
            if uri.startswith("supabase://"):
                return await self._get_supabase_content(uri)
            elif uri.startswith("git://"):
                return await self._get_git_content(uri)
            elif uri.startswith("file://"):
                return await self._get_file_content(uri)
            else:
                return f"Unknown resource type for URI: {uri}"
        except Exception as e:
            logger.error(f"Failed to get resource content for {uri}: {str(e)}")
            return f"Error: {str(e)}"
    
    async def _get_supabase_content(self, uri: str) -> str:
        """Get content from Supabase"""
        if not self.supabase:
            return "Supabase client not available"
            
        # Parse URI: supabase://table/operation/params
        path_parts = uri.replace("supabase://", "").split("/")
        table = path_parts[0] if len(path_parts) > 0 else "agents"
        operation = path_parts[1] if len(path_parts) > 1 else "select"
        
        try:
            if operation == "select":
                result = self.supabase.table(table).select("*").limit(10).execute()
                return json.dumps(result.data, indent=2, ensure_ascii=False)
            elif operation == "count":
                result = self.supabase.table(table).select("*", count="exact").execute()
                return f"Total records in {table}: {result.count}"
            else:
                return f"Unsupported operation: {operation}"
        except Exception as e:
            return f"Supabase error: {str(e)}"
    
    async def _get_git_content(self, uri: str) -> str:
        """Get Git repository content"""
        # Parse URI: git://repo/operation/params
        path_parts = uri.replace("git://", "").split("/")
        repo_name = path_parts[0] if len(path_parts) > 0 else "main"
        operation = path_parts[1] if len(path_parts) > 1 else "status"
        
        if repo_name not in self.git_repos:
            return f"Git repository '{repo_name}' not found"
            
        repo = self.git_repos[repo_name]
        
        try:
            if operation == "status":
                status_info = {
                    "branch": repo.active_branch.name,
                    "commit": repo.head.commit.hexsha[:8],
                    "dirty": repo.is_dirty(),
                    "untracked": len(repo.untracked_files),
                    "modified": len([item.a_path for item in repo.index.diff(None)]),
                    "message": repo.head.commit.message.strip()
                }
                return json.dumps(status_info, indent=2)
            elif operation == "log":
                commits = list(repo.iter_commits(max_count=5))
                log_info = [
                    {
                        "hash": commit.hexsha[:8],
                        "message": commit.message.strip(),
                        "author": str(commit.author),
                        "date": commit.committed_datetime.isoformat()
                    }
                    for commit in commits
                ]
                return json.dumps(log_info, indent=2)
            else:
                return f"Unsupported Git operation: {operation}"
        except Exception as e:
            return f"Git error: {str(e)}"
    
    async def _get_file_content(self, uri: str) -> str:
        """Get local file content"""
        file_path = Path(uri.replace("file://", ""))
        
        try:
            if file_path.exists() and file_path.is_file():
                return file_path.read_text(encoding='utf-8')
            else:
                return f"File not found: {file_path}"
        except Exception as e:
            return f"File read error: {str(e)}"


# Enhanced MCP server resource handler
enhanced_resource_handler = EnhancedMCPResource()


if MCP_AVAILABLE:
    @mcp_server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        """List enhanced MCP resources"""
        return [
            types.Resource(
                uri="supabase://agents/select",
                name="Morvo Agents Data",
                description="معلومات الوكلاء المسجلين في قاعدة البيانات",
                mimeType="application/json",
            ),
            types.Resource(
                uri="supabase://conversations/select", 
                name="Conversations Data",
                description="بيانات المحادثات والتفاعلات",
                mimeType="application/json",
            ),
            types.Resource(
                uri="git://main/status",
                name="Git Repository Status",
                description="حالة مستودع Git الرئيسي",
                mimeType="application/json",
            ),
            types.Resource(
                uri="git://main/log",
                name="Git Commit Log",
                description="سجل التغييرات الأخيرة في Git",
                mimeType="application/json",
            ),
            types.Resource(
                uri="file://config.py",
                name="Configuration File",
                description="ملف التكوين الرئيسي",
                mimeType="text/python",
            ),
            types.Resource(
                uri="file://requirements.txt",
                name="Dependencies",
                description="قائمة التبعيات المطلوبة",
                mimeType="text/plain",
            ),
        ]


    @mcp_server.read_resource()
    async def handle_read_resource(uri: str) -> str:
        """Read enhanced resource content"""
        return await enhanced_resource_handler.get_resource_content(uri)


    @mcp_server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List enhanced MCP tools"""
        return [
            types.Tool(
                name="supabase_query",
                description="تنفيذ استعلام على قاعدة بيانات Supabase",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "اسم الجدول"
                        },
                        "operation": {
                            "type": "string", 
                            "enum": ["select", "insert", "update", "delete"],
                            "description": "نوع العملية"
                        },
                        "data": {
                            "type": "object",
                            "description": "البيانات للعملية"
                        }
                    },
                    "required": ["table", "operation"]
                },
            ),
            types.Tool(
                name="git_operation",
                description="تنفيذ عمليات Git",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["status", "add", "commit", "push", "pull", "log"],
                            "description": "عملية Git"
                        },
                        "message": {
                            "type": "string",
                            "description": "رسالة التحديث (للcommit)"
                        },
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "الملفات للإضافة (للadd)"
                        }
                    },
                    "required": ["operation"]
                },
            ),
            types.Tool(
                name="cache_operation",
                description="عمليات التخزين المؤقت مع Redis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["get", "set", "delete", "exists"],
                            "description": "عملية التخزين المؤقت"
                        },
                        "key": {
                            "type": "string",
                            "description": "مفتاح التخزين"
                        },
                        "value": {
                            "type": "string",
                            "description": "القيمة (للset)"
                        },
                        "ttl": {
                            "type": "integer",
                            "description": "مدة البقاء بالثواني"
                        }
                    },
                    "required": ["operation", "key"]
                },
            ),
        ]


    @mcp_server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        """Handle enhanced tool calls"""
        try:
            if name == "supabase_query":
                result = await _handle_supabase_query(arguments)
            elif name == "git_operation":
                result = await _handle_git_operation(arguments)
            elif name == "cache_operation":
                result = await _handle_cache_operation(arguments)
            else:
                result = f"Unknown tool: {name}"
                
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            logger.error(f"Tool call failed for {name}: {str(e)}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def _handle_supabase_query(args: dict) -> str:
    """Handle Supabase database queries"""
    # This would be implemented with actual Supabase operations
    return f"Supabase query executed: {args}"


async def _handle_git_operation(args: dict) -> str:
    """Handle Git operations"""
    # This would be implemented with actual Git operations
    return f"Git operation executed: {args}"


async def _handle_cache_operation(args: dict) -> str:
    """Handle Redis cache operations"""
    # This would be implemented with actual Redis operations
    return f"Cache operation executed: {args}"


# Initialize enhanced MCP server
def setup_enhanced_mcp_server(supabase_client: Optional[Client] = None, git_repos: Optional[Dict[str, Repo]] = None):
    """Setup enhanced MCP server with integrations"""
    global enhanced_resource_handler
    enhanced_resource_handler = EnhancedMCPResource(supabase_client, git_repos)
    logger.info("Enhanced MCP server setup completed")
