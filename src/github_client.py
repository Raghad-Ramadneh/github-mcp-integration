from github import Github
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

class GitHubClient:
    def __init__(self):
        """Initialize GitHub client with token from environment"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        
        self.github = Github(token)
        self.user = self.github.get_user()
        print(f"Connected to GitHub as: {self.user.login}")
    
    def create_repository(self, name, description="", private=False):
        """Create a new repository"""
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private
            )
            return {
                "success": True,
                "message": f"Repository '{name}' created successfully",
                "url": repo.html_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_repositories(self):
        """List all user repositories"""
        try:
            repos = list(self.user.get_repos())
            repo_list = [{"name": repo.name, "url": repo.html_url} for repo in repos[:10]]  # Limit to 10
            return {
                "success": True,
                "repositories": repo_list,
                "count": len(repos)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_issue(self, repo_name, title, body=""):
        """Create an issue in a repository"""
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            issue = repo.create_issue(title=title, body=body)
            return {
                "success": True,
                "message": f"Issue '{title}' created successfully",
                "url": issue.html_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_issues(self, repo_name):
        """List issues in a repository"""
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            issues = list(repo.get_issues(state='open'))
            issue_list = [{"title": issue.title, "url": issue.html_url} for issue in issues]
            return {
                "success": True,
                "issues": issue_list,
                "count": len(issue_list)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_repo_info(self, repo_name):
        """Get repository information"""
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            return {
                "success": True,
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "url": repo.html_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_repo_object(self, repo_name):
        """Return the repo object by name (user/repo_name)"""
        try:
            return self.github.get_repo(f"{self.user.login}/{repo_name}")
        except Exception:
            return None
    
    def create_branch(self, repo_name, branch_name, source_branch="main"):
        """Create a new branch in a repository"""
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            source_branch_obj = repo.get_branch(source_branch)
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_branch_obj.commit.sha
            )
            return {
                "success": True,
                "message": f"Branch '{branch_name}' created successfully",
                "branch": branch_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_pull_request(self, repo, title, head, base, body=""):
        """Create a pull request on the given repo object"""
        try:
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head,
                base=base
            )
            return {
                "success": True,
                "url": pr.html_url,
                "message": f"Pull request created successfully: {pr.title}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_repo_stats(self, repo_name):
        """Get repository statistics"""
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            return {
                "success": True,
                "name": repo.name,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "issues": repo.open_issues_count,
                "language": repo.language,
                "size": repo.size,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
