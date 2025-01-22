from .github_client import GithubClient
from .github_enterprise_client import GithubEnterpriseClient

GithubClientType = GithubClient | GithubEnterpriseClient
