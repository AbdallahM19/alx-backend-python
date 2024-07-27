#!/usr/bin/env python3
"""unittest is a module for testing"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """
    a TestAccessNestedMap class that
    inherits from unittest.TestCase
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map, path, expected_value
    ):
        """test_access_nested_map function"""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected_value
        )

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self, nested_map, path, exception
    ):
        """test_access_nested_map_exception function"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """TestGetJson class that inherits from unittest.TestCase"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url, test_pay):
        """test_get_json function"""
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = test_pay
            self.assertEqual(get_json(url), test_pay)
            mock_get.assert_called_once_with(url)
