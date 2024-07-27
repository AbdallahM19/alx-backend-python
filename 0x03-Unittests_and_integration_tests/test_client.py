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
        ("google", {'repo_name': "google"}),
        ("abc", {'repo_name': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(
        self,
        org: str,
        params: Dict,
        mock_get_json: MagicMock,
    ) -> None:
        """test_org"""
        mock_get_json.return_value = MagicMock(return_value=params)
        class_test = GithubOrgClient(org)
        self.assertEqual(class_test.org(), params)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )
