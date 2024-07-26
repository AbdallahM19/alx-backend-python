#!/usr/bin/env python3
"""unittest is a module for testing"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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
