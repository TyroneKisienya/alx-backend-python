#!/usr/bin/env python3
"""
Unittests for the client.GithubOrgClient class.

Covers:
- org()
- _public_repos_url
- public_repos()
"""

from client import GithubOrgClient
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from fixtures import TEST_PAYLOAD

org_payload, repos_payload, expected_repos, apache2_repos = TEST_PAYLOAD[0]


class TestGithubOrgClient(unittest.TestCase):
    '''Test cases for TestGithubOrgClient'''
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        '''Test that method returns the correct url'''
        test_payload = {"repos_url":
                        "https://api.github.com/orgs.google/repos"}
        with patch.object(GithubOrgClient,
                          'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        '''Test method for public repos is returned correct'''
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as Mock_public_repos_url:
            Mock_public_repos_url.return_value = "https:" \
                             "//api.github.com/orgs/google/repos"

            client = GithubOrgClient("goole")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_get_json.assert_called_once_with
            ("https://api.github.com/orgs/google/repos")
            Mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        '''Test the has_license staticmethod'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": repos_payload,
        "apache2_repos": apache2_repos,
    }
])

class TestintegrationGithubOrgClient(unittest.TestCase):
    '''Integration test for the org_client'''
    
    @classmethod
    def setUpClass(cls):
        """Set up requests.get patcher"""
        def mock_get(url, *args, **kwargs):
            mock_resp = Mock()
            if url == f"https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.get_patcher = patch("requests.get", side_effect=mock_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        '''stop patcher'''
        cls.get_patcher.stop()
    
    def test_public_repos(self):
        '''test for expected repository'''
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)
    
    def test_public_repos_with_license(self):
        '''test for values with only Apache license'''
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
