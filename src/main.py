import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_interface import LLMInterface
from src.mcp_server import GitHubMCPServer

class GitHubInterface:
    def __init__(self):
        """Initialize the enhanced GitHub interface with LLM and MCP"""
        try:
            print("Initializing GitHub MCP Integration...")
            self.mcp_server = GitHubMCPServer()
            self.llm_interface = LLMInterface()
            print("Ready!")
        except Exception as e:
            print(f"Initialization failed: {e}")
            print("Check your .env file has GITHUB_TOKEN and OPENAI_API_KEY")
            raise
    
    async def process_natural_language_request(self, user_input):
        """Process user request through LLM → MCP → GitHub pipeline"""
        try:
            # Parse with LLM
            parsed_intent = self.llm_interface.parse_natural_language(user_input)
            
            if "error" in parsed_intent:
                return {"success": False, "error": parsed_intent["error"]}
            
            action = parsed_intent.get("action")
            parameters = parsed_intent.get("parameters", {})
            
            if action == "unknown":
                return {"success": False, "error": "Could not understand the request"}
            
            # Execute through MCP
            result = await self.mcp_server.call_tool(action, parameters)
            
            # Generate response
            response = self.llm_interface.generate_response(result, user_input)
            
            return {
                "success": result.get("success", False),
                "llm_response": response,
                "raw_result": result,
                "parsed_intent": parsed_intent
            }
            
        except Exception as e:
            return {"success": False, "error": f"Processing failed: {str(e)}"}
    
    def display_result(self, result):
        """Display the result in a user-friendly way"""
        if result["success"]:
            print(f"\n{result['llm_response']}")
            
            raw_result = result.get("raw_result", {})
            
            # Show URL if available
            if "url" in raw_result:
                print(f"Link: {raw_result['url']}")
            
            # Show repositories
            if "repositories" in raw_result:
                repos = raw_result['repositories'][:3]  # Show first 3
                for repo in repos:
                    print(f"• {repo['name']}: {repo['url']}")
            
            # Show issues
            if "issues" in raw_result:
                issues = raw_result['issues'][:3]  # Show first 3
                for issue in issues:
                    print(f"• {issue['title']}: {issue['url']}")
            
            # Show stats
            if "stars" in raw_result:
                print(f"⭐ {raw_result['stars']} stars, 🍴 {raw_result['forks']} forks")
                
        else:
            print(f"\nError: {result.get('llm_response', result.get('error', 'Unknown error'))}")
    
    async def run_interactive_mode(self):
        """Run the interactive chat interface"""
        print("\nGitHub MCP Integration")
        print("Commands: 'create repo', 'list repos', 'create issue', 'quit'")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nWhat would you like to do? ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                result = await self.process_natural_language_request(user_input)
                self.display_result(result)
                
                # Debug mode
                if os.getenv('DEBUG', '').lower() == 'true':
                    print(f"Debug - Intent: {result.get('parsed_intent', {})}")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_demo_mode(self):
        """Run a demonstration of the system capabilities"""
        print("Demo Mode")
        
        demo_commands = [
            "Show me all my repositories",
            "Get information about Face-Recognition-CNN",
            "Create a repository called demo-project",
            "Create an issue in demo-project about adding README"
        ]
        
        for i, command in enumerate(demo_commands, 1):
            print(f"\nDemo {i}: {command}")
            input("Press Enter...")
            
            result = asyncio.run(self.process_natural_language_request(command))
            self.display_result(result)
            
            if not result["success"]:
                print("Demo stopped due to error")
                break
        
        print("Demo completed!")

async def main():
    """Main entry point"""
    try:
        interface = GitHubInterface()
        
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            interface.run_demo_mode()
        else:
            await interface.run_interactive_mode()
            
    except Exception as e:
        print(f"Failed to start: {e}")
        print("Check .env file and dependencies")

if __name__ == "__main__":
    asyncio.run(main())
