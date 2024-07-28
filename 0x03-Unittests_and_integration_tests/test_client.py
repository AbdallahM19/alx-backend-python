#!/usr/bin/env python3
"""unittest is a module for testing"""

from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError
from typing import Dict
import unittest


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class"""
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
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
                    "name": "allstar",
                    "full_name": "google/allstar",
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
                    "name": "github",
                    "full_name": "google/github",
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
                client, ["allstar", "github"]
            )
            mock_repos.assert_called_once()
        mock_test.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(
        self, licence_dict: Dict, name: str, expected: bool
    ) -> None:
        """Test that the client has a license."""
        get_org_client = GithubOrgClient("google")
        get_org_licence = get_org_client.has_license(
            licence_dict, name
        )
        self.assertEqual(get_org_licence, expected)
        # print(get_org_licence == expected)


@parameterized_class([{
    "org_payload": TEST_PAYLOAD[0][0],
    "repos_payload": TEST_PAYLOAD[0][1],
    "expected_repos": TEST_PAYLOAD[0][2],
    "apache2_repos": TEST_PAYLOAD[0][3],
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test the integration of the GithubOrgClient class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(
                    **{'json.return_value': route_payload[url]}
                )
            return HTTPError

        cls.get_patcher = patch(
            "requests.get", side_effect=get_payload
        )
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """public_repos test method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """public_repos_with_license test method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test class."""
        cls.get_patcher.stop()
