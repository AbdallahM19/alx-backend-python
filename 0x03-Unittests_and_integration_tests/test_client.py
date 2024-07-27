# !/usr/bin/env python3
"""unittest is a module for testing"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class"""
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")
    def test_org(
        self,
        org: str,
        mock_get_json: MagicMock,
    ) -> None:
        """test_org"""
        expected_json = {
            "repos_url": "https://api.github.com/orgs/{}".format(org)
        }
        mock_get_json.return_value = expected_json
        class_test = GithubOrgClient(org)
        self.assertEqual(class_test.org, expected_json)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )
