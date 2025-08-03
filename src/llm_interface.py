import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
# ✅ Load .env and configure Gemini
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")
genai.configure(api_key=GOOGLE_API_KEY)
# ✅ Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")  
class LLMInterface:
    def __init__(self):
        print("🤖 Gemini LLM Interface initialized")
    def parse_natural_language(self, user_input):
        """Convert user input to structured GitHub operation (JSON)"""
        system_prompt = """
You are a GitHub operations assistant that converts natural language requests into structured JSON commands.
Available GitHub operations:
- create_repository
- list_repositories
- get_repository_info
- create_issue
- list_issues
- create_pull_request
- create_branch
- get_repository_stats
Parameters:
- create_repository: {"name": "repo-name", "description": "optional", "private": false}
- list_repositories: {}
- get_repository_info: {"repo_name": "repository-name"}
- create_issue: {"repo_name": "repo-name", "title": "issue title", "body": "optional"}
- list_issues: {"repo_name": "repository-name"}
- create_pull_request: {"repo_name": "repo", "title": "PR title", "head": "feature-branch", "base": "main", "body": "description"}
- create_branch: {"repo_name": "repo", "branch_name": "new-branch", "source_branch": "main"}
- get_repository_stats: {"repo_name": "repository-name"}
Examples:
User: "Create a repository called my-project"
Response: {"action": "create_repository", "parameters": {"name": "my-project", "description": "", "private": false}}
User: "Show me my repositories"
Response: {"action": "list_repositories", "parameters": {}}
Respond with **only valid JSON**.
        """
        try:
            prompt = f"{system_prompt}\nUser: {user_input}"
            response = model.generate_content(prompt)
            result = response.text.strip()
            # ✅ Remove code block markdown if present
            if result.startswith("```json"):
                result = result[7:].strip()
            if result.endswith("```"):
                result = result[:-3].strip()
            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError as e:
            print(f"🚨 JSON parsing error: {e}")
            return {"action": "unknown", "parameters": {}, "error": "Failed to parse LLM response"}
        except Exception as e:
            print(f"🚨 Gemini LLM error: {e}")
            return {"action": "unknown", "parameters": {}, "error": str(e)}
    def generate_response(self, operation_result, user_input):
        """Generate a user-friendly message from the result"""
        system_prompt = """
You are a friendly GitHub assistant.
The user made a GitHub request. Generate a helpful and encouraging reply:
- Acknowledge the request
- Explain what was done
- Mention success or failure
- Include links or tips if helpful
- Be cheerful and use emojis when appropriate
        """
        try:
            prompt = f"""
User input: {user_input}
Operation result: {json.dumps(operation_result, indent=2)}
"""
            response = model.generate_content(system_prompt + prompt)
            return response.text.strip()
        except Exception as e:
            if operation_result.get("success"):
                return f"✅ Operation completed successfully! {operation_result.get('message', '')}"
            else:
                return f"❌ Operation failed: {operation_result.get('error', 'Unknown error')}"


