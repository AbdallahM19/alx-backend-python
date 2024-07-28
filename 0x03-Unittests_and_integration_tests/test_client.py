#!/usr/bin/env python3
"""unittest is a module for testing"""

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
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

    def test_public_repos_url(self) -> None:
        """test_public_repos_url function"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_test:
            mock_test.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            client = GithubOrgClient("google")._public_repos_url
            self.assertEqual(
                client, "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_test: MagicMock) -> None:
        """test_public_repos function"""
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 460600860,
                    "name": ".allstar",
                    "full_name": "google/.allstar",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        "url": "https://api.github.com/users/google",
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/.allstar",
                    "created_at": "2022-02-17T20:40:32Z",
                    "updated_at": "2024-06-17T11:54:24Z",
                    "has_issues": True,
                    "has_projects": True,
                    "has_downloads": True,
                    "forks": 2,
                    "default_branch": "main"
                },
                {
                    "id": 170908616,
                    "name": ".github",
                    "full_name": "google/.github",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        "url": "https://api.github.com/users/google",
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/.github",
                    "created_at": "2019-02-15T18:14:38Z",
                    "updated_at": "2024-07-17T04:01:57Z",
                    "has_issues": True,
                    "has_projects": False,
                    "has_downloads": True,
                    "forks": 250,
                    "default_branch": "master"
                },
            ]
        }
        mock_test.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos:
            mock_repos.return_value = test_payload["repos_url"]
            client = GithubOrgClient("google").public_repos()
            self.assertEqual(
                client, [".allstar", ".github"]
            )
            mock_repos.assert_called_once()
        mock_test.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        licence_dict: Dict,
        name: str,
        expected: bool
    ) -> None:
        """Test that the client has a license."""
        get_org_client = GithubOrgClient("google")
        get_org_licence = get_org_client.has_license(licence_dict, name)
        self.assertEqual(get_org_licence, expected)
