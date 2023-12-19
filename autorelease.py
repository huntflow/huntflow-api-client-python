import argparse
import logging
import re
from typing import List, Optional

import httpx
import toml  # type: ignore

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def get_project_version() -> str:
    with open("pyproject.toml") as f:
        data = toml.loads(f.read())
    return data["project"]["version"]


def make_request(
    method: str,
    path: str,
    token: str,
    data: Optional[dict] = None,
    params: Optional[dict] = None,
) -> httpx.Response:
    base_url = "https://api.github.com/repos/huntflow/huntflow-api-client-python"
    url = base_url + path
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.request(method=method, url=url, json=data, headers=headers, params=params)
    response.raise_for_status()
    return response


def get_release_tags(github_token: str) -> List[str]:
    result: List[str] = []
    params = {"page": 1}
    while True:
        response = make_request(method="GET", path="/releases", token=github_token, params=params)
        data = response.json()
        if not data:
            return result
        existing_tags = [item["tag_name"] for item in data]
        result.extend(existing_tags)
        params["page"] += 1


def main(github_token: str, current_branch: str) -> None:
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
    existing_releases = get_release_tags(github_token=github_token)

    if project_version in existing_releases:
        logger.info("Release %s already exists", project_version)
        return

    is_latest = all(project_version > item for item in existing_releases)
    logger.info("Latest release: %s", is_latest)
    release_data = {
        "tag_name": project_version,
        "name": f"Release {project_version}",
        "target_commitish": current_branch,
        "make_latest": str(is_latest).lower(),
    }
    make_request(method="POST", path="/releases", token=github_token, data=release_data)

    logger.info("Release %s successfully created", project_version)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--github_token", required=True, type=str)
    parser.add_argument("--current_branch", required=True, type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.github_token, args.current_branch)
