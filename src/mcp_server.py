import asyncio
import json
from src.github_client import GitHubClient

class GitHubMCPServer:
    """MCP Server for GitHub operations following Model Context Protocol"""
    
    def __init__(self):
        self.github_client = GitHubClient()
        self.tools = self._define_tools()
        print("🔧 MCP Server initialized with GitHub tools")
    
    def _define_tools(self):
        """Define available MCP tools for GitHub operations"""
        return {
            "create_repository": {
                "description": "Create a new GitHub repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Repository name"},
                        "description": {"type": "string", "description": "Repository description"},
                        "private": {"type": "boolean", "description": "Make repository private"}
                    },
                    "required": ["name"]
                }
            },
            "list_repositories": {
                "description": "List user repositories",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            "get_repository_info": {
                "description": "Get detailed repository information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"}
                    },
                    "required": ["repo_name"]
                }
            },
            "create_issue": {
                "description": "Create an issue in a repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"},
                        "title": {"type": "string", "description": "Issue title"},
                        "body": {"type": "string", "description": "Issue description"}
                    },
                    "required": ["repo_name", "title"]
                }
            },
            "list_issues": {
                "description": "List issues in a repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"}
                    },
                    "required": ["repo_name"]
                }
            },
            "create_branch": {
                "description": "Create a new branch in a repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"},
                        "branch_name": {"type": "string", "description": "New branch name"},
                        "source_branch": {"type": "string", "description": "Source branch (default: main)"}
                    },
                    "required": ["repo_name", "branch_name"]
                }
            },
            "get_repository_stats": {
                "description": "Get repository statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"}
                    },
                    "required": ["repo_name"]
                }
            },
            "create_pull_request": {
                "description": "Create a pull request in a repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"},
                        "title": {"type": "string", "description": "Pull request title"},
                        "head": {"type": "string", "description": "Branch with your changes"},
                        "base": {"type": "string", "description": "Branch to merge into"},
                        "body": {"type": "string", "description": "Pull request description (optional)"}
                    },
                    "required": ["repo_name", "title", "head", "base"]
                }
            }
        }
    
    async def call_tool(self, tool_name: str, parameters: dict) -> dict:
        """Execute a tool call through MCP protocol"""
        try:
            print(f"🔧 MCP Tool Call: {tool_name} with {parameters}")
            
            if tool_name == "create_repository":
                result = self.github_client.create_repository(
                    name=parameters["name"],
                    description=parameters.get("description", ""),
                    private=parameters.get("private", False)
                )
            
            elif tool_name == "list_repositories":
                result = self.github_client.list_repositories()
            
            elif tool_name == "get_repository_info":
                result = self.github_client.get_repo_info(parameters["repo_name"])
            
            elif tool_name == "create_issue":
                result = self.github_client.create_issue(
                    repo_name=parameters["repo_name"],
                    title=parameters["title"],
                    body=parameters.get("body", "")
                )
            
            elif tool_name == "list_issues":
                result = self.github_client.list_issues(parameters["repo_name"])
            
            elif tool_name == "create_branch":
                result = self.github_client.create_branch(
                    repo_name=parameters["repo_name"],
                    branch_name=parameters["branch_name"],
                    source_branch=parameters.get("source_branch", "main")
                )
            
            elif tool_name == "get_repository_stats":
                result = self.github_client.get_repo_stats(parameters["repo_name"])
            
            elif tool_name == "create_pull_request":
                repo = self.github_client.get_repo_object(parameters["repo_name"])
                if not repo:
                    return {"success": False, "error": f"Repository '{parameters['repo_name']}' not found"}
                result = self.github_client.create_pull_request(
                    repo=repo,
                    title=parameters["title"],
                    head=parameters["head"],
                    base=parameters["base"],
                    body=parameters.get("body", "")
                )
            
            else:
                result = {"success": False, "error": f"Unknown tool: {tool_name}"}
            
            print(f"🔧 MCP Result: {result}")
            return result
            
        except Exception as e:
            error_result = {"success": False, "error": f"MCP tool execution failed: {str(e)}"}
            print(f"🚨 MCP Error: {error_result}")
            return error_result
    
    def get_available_tools(self) -> dict:
        """Return available tools for MCP discovery"""
        return self.tools
    
    async def handle_mcp_request(self, request: dict) -> dict:
        """Handle incoming MCP protocol requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {"name": name, **info} 
                            for name, info in self.tools.items()
                        ]
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                
                result = await self.call_tool(tool_name, tool_params)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
