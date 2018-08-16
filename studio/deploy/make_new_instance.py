#!/usr/bin/env python
# Steps:
# Clone the studio repo and branch given (use learningequality/studio, develop branch by default).
# Run gcloud builds submit on the freshly fetched repo.
# Record the person who triggered the new studio repo, and remind them to clean it up when they're done!

import uuid
import os
import pathlib
import requests
import zipfile
import tempfile
import shutil
import sh

DEFAULT_REPO = "learningequality/studio"
DEFAULT_BRANCH = "develop"

REPO_DOWNLOAD_URL_TEMPLATE = "https://github.com/{repo}/archive/{branch}.zip"


def _construct_repo_download_url(repo, branch):
    return REPO_DOWNLOAD_URL_TEMPLATE.format(repo=repo, branch=branch)


# Download a shallow clone of the studio repo by using the zip file provided by Github
def download_studio_repo(download_directory, repo=DEFAULT_REPO, branch=DEFAULT_BRANCH):
    msg = "Fetching a copy of studio from {repo} with the {branch} branch.".format(
        repo=repo, branch=branch
    )
    print(msg)

    # generate our URL based on the parameters, and start the request.
    url = _construct_repo_download_url(repo, branch)
    r = requests.get(url, stream=True)

    # raise that status in case anything went wrong with our download.
    r.raise_for_status()

    # download and extract the repo on to a temporary directory
    with tempfile.NamedTemporaryFile() as tf:
        # copy the requests zipfile into the local temporary file
        shutil.copyfileobj(r.raw, tf)
        # flush it first to make sure all the bytes are written to disk
        tf.flush()

        # open the local temp file as a zip file
        with zipfile.ZipFile(tf.name) as zf:
            zf.extractall(path=download_directory)

        # Github bundles the real repo root inside a folder formatted as
        # {reponame}-{branch}, e.g. studio-develop/Pipfile, etc. Get the one
        # folder inside our download directory, and return that as the main folder.
        dirs = os.listdir(path=download_directory)

        # we assume that we only have one folder inside there, the one
        # containing the repo root.
        repo_root = pathlib.Path(download_directory) / dirs[0]

        # Confirm that we have a Pipfile inside that repo root.
        # Now we're in the REAL studio repo.
        err_msg = (
            "Oh no! The studio repo zip we got from Github did not conform"
            " to our expectations! Please download {url} and check that the "
            "studio repo root is inside one folder."
        )
        assert (repo_root / "Pipfile").exists(), err_msg
        return str(repo_root)


def submit_build(studio_directory):
    # run gcloud builds submit on the studio directory given
    # command should similar to this in bash/fish:
    # gcloud builds submit . --config=cloudbuild-production.yaml --substitutions=COMMIT_SHA=1e709163b86215e58312fefc7c6e359ee18c3c18,BRANCH_NAME=testing,_DATABASE_INSTANCE_NAME=develop

    print("Submitting the studio directory to gcloud for building.")

    # derive the image tag, instance name (given by the user) and the database name to connect to
    # we pass all this information to gcloud, who will then actually build and deploy this for us.
    id = uuid.uuid4().hex[:7]
    image_name = "custom-studio-instance-{hash}".format(hash=id)
    instance = "arontesting"
    db_name = "develop"

    # let the user know the stats of the studio instance we're about to create
    msg = """
    Metadata:
    image tag: {hash}
    instance name: {instance}
    database: {db}
    """.format(
        hash=id, instance=instance, db=db_name
    )
    print(msg)

    build_substitutions = (
        "COMMIT_SHA={image_name},BRANCH_NAME={instance_name}"
    ).format(image_name="automatedtest", instance_name="automatedtest")

    sh.gcloud.builds.submit(
        ".",
        "--config=cloudbuild.yaml",
        "--project=ops-central",
        "--substitutions={subs}".format(subs=build_substitutions),
        _cwd=studio_directory,
    )


if __name__ == "__main__":
    # Store all of our work on to a temporary directory
    with tempfile.TemporaryDirectory(prefix="studio-") as d:
        repo_root = download_studio_repo(d)
        submit_build(repo_root)
