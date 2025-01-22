from ..configs.config import config
from ..schemas.github import GithubType
from .github_client import GithubClient


class GithubEnterpriseClient(GithubClient):
    """Manages interaction with GitHub Enterprise"""

    type = GithubType.GithubEnterprise
    base_url = config.GITHUB_ENTERPRISE_URL
