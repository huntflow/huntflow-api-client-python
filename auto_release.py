import logging
import re
import argparse
import toml
from github import Github, Auth


def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    return logger


def get_project_version() -> str:
    with open("pyproject.toml") as f:
        data = toml.loads(f.read())
    return data["project"]["version"]


def main(github_token: str, current_branch: str):
    logger = get_logger()
    branch_patter = r"^v(?P<major_release>\d+)$"
    branch_matching = re.match(branch_patter, current_branch, re.I)
    if not branch_matching:
        logger.info("Branch %s is not a valid release branch", current_branch)
        return

    major_release = branch_matching.group("major_release")
    project_version = get_project_version()
    logger.info("Project version %s", project_version)

    if not project_version.startswith(major_release):
        logger.info(
            "Release tag %s is invalid, major releases in the %s branch must start with %s",
            project_version,
            current_branch,
            major_release,
        )
        return

    token = Auth.Token(github_token)
    git = Github(auth=token)
    repo = git.get_repo(full_name_or_id="huntflow/huntflow-api-client-python", lazy=False)
    existing_releases = {release.tag_name for release in repo.get_releases()}
    if project_version in existing_releases:
        logger.info("Release %s already exists", project_version)
        return

    repo.create_git_release(
        tag=project_version,
        name=f"Release {project_version}",
        target_commitish=current_branch,
        message=""
    )
    logger.info("Release %s successfully created", project_version)
    git.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--github_token", required=True, type=str)
    parser.add_argument("--current_branch", required=True, type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.github_token, args.current_branch)
