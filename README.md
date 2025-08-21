# GitHub MCP Integration

A command-line interface (CLI) tool that connects a GitHub client with a language model (LLM) to enable natural language GitHub operations.

---

## 🔧 Features

- Connects securely to GitHub using a personal access token  
- Parses natural language requests using an LLM (e.g., Gemini)  
- Modular components for GitHub, LLM, and MCP Server integration  
- Supports operations such as:
  - Creating repositories  
  - Listing repositories  
  - Creating issues  
  - Listing issues in a repository  
  - Getting repository information  
  - Returning the repository object by name  
  - Creating a new branch in a repository  
  - Creating pull requests  
  - Getting repository statistics  

---

## 📁 Project Structure

```text
github-mcp-integration/
├── venv/                   # Python virtual environment
├── src/
│   ├── __init__.py
│   ├── github_client.py    # GitHub API interactions
│   ├── llm_interface.py    # Natural language to structured command parser
│   ├── main.py             # CLI interface
│   ├── mcp_server.py       # Orchestrator for LLM and GitHub client
│   └── __pycache__/        # Compiled files (ignored)
├── .env                    # Environment variables (e.g., tokens)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation



# 🚀 Getting Started

# 1. Clone the repository

git clone https://github.com/raghad-ramadneh/github-mcp-integration.git
cd github-mcp-integration

# 2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies

pip install -r requirements.txt

# 4. Set up environment variables for GitHub and LLM APIs

Create a `.env` file in the root directory of the project and add your API credentials:

```env
# GitHub credentials
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username_here

# Language Model API credentials
GEMINI_API_KEY=your_gemini_api_key_here
    
Note: Replace the placeholder values with your actual tokens and URLs.
Keep this file private and add .env to your .gitignore file to prevent accidental commits.

# 5. Run the project

Start the CLI interface by running:
python -m src.main

#💬 Example Usage
Create a new repository called test-repo
List my repositories
Create an issue in test-repo with title "Bug" and body "Fix needed"



