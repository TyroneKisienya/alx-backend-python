#!/usr/bin/env python3

from client import GithubOrgClient
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch, PropertyMock


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
            with patch.object(GithubOrgClient, 'org',
                              new_callable=PropertyMock) as mock_org:
                mock_org.return_value = test_payload

                client = GithubOrgClient("google")
                result = client._public_repos_url

                self.assertEqual(result, test_payload["repos_url"])
                mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
