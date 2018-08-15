#!/usr/bin/env python

import unittest
import pytest
import requests

import make_new_instance as mni


class ConstructRepoDownloadURLTestCase(unittest.TestCase):
    """
    Test cases for _construct_repo_download_url.
    """

    # test plan:
    # check if github.com in given URL
    # check that it returns an existing file through HEAD given the main repo

    def test_check_if_returned_value_has_github(self):
        """
        Check if the returned URL has github.com in it.
        """
        assert "github.com" in mni._construct_repo_download_url(
            mni.DEFAULT_REPO, mni.DEFAULT_BRANCH
        )

    def test_check_exists_on_github(self):
        """
        Check that the returned URL exists on github.
        """
        url = mni._construct_repo_download_url(mni.DEFAULT_REPO, mni.DEFAULT_BRANCH)
        r = requests.head(url)
        r.raise_for_status()
