import logging

from ..schemas.github import GithubType
from ..schemas.repo_config import RepoConfig
from .config import config

logger = logging.getLogger(__name__)


def get_token_for_repo_config(repo_config: RepoConfig, github_type: GithubType = GithubType.GithubEnterprise) -> str:
    # TODO: setup secrets manager for tokens for different repos
    logger.info("Sandbox mode, using token from envvar")
    if github_type == GithubType.GithubEnterprise:
        return config.LOWSIDE_TOKEN
    elif github_type == GithubType.Github:
        return config.HIGHSIDE_TOKEN
