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
    def test_org(self, org: str, params: Dict, mock_get_json: MagicMock) -> None:
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
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
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
                client,
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_repos.assert_called_once()
        mock_test.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, licence_dict: Dict, name: str, expected: bool) -> None:
        """Test that the client has a license."""
        get_org_client = GithubOrgClient("google")
        get_org_licence = get_org_client.has_license(licence_dict, name)
        self.assertEqual(get_org_licence, expected)


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
        client = GithubOrgClient("google").public_repos()
        self.assertEqual(
            client,
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """public_repos_with_license test method"""
        client = GithubOrgClient("google").public_repos(
                license="apache-2.0"
            )
        self.assertEqual(
            client,
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test class."""
        cls.get_patcher.stop()
