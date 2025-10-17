#!/usr/bin/env python3

from client import GithubOrgClient
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch


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


if __name__ == "__main__":
    unittest.main()
