#!/usr/bin/env python
# Steps:
# Clone the studio repo and branch given (use learningequality/studio, develop branch by default).
# Run gcloud builds submit on the freshly fetched repo.
# Record the person who triggered the new studio repo, and remind them to clean it up when they're done!

import sh

DEFAULT_REPO = "learningequality/studio"
DEFAULT_BRANCH = "develop"

REPO_DOWNLOAD_URL_TEMPLATE = "https://github.com/{repo}/archive/{branch}.zip"


def _construct_repo_download_url(repo, branch):
    return REPO_DOWNLOAD_URL_TEMPLATE.format(repo=repo, branch=branch)


# Download a shallow clone of the studio repo by using the zip file provided by Github
def download_studio_repo(repo=DEFAULT_REPO, branch=DEFAULT_BRANCH):
    pass


if __name__ == "__main__":
    download_studio_repo()
