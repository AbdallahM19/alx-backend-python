#!/usr/bin/env python3
"""unittest is a module for testing"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
    Tuple,
    Union
)


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
        self,
        nested_map: Dict,
        path: Tuple[str],
        expected_value: Union[Dict, int],
    ) -> None:
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
        self,
        nested_map: Dict,
        path: Tuple[str],
        exception: Exception,
    ) -> None:
        """test_access_nested_map_exception function"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """TestGetJson class that inherits from unittest.TestCase"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        url: str,
        test_pay: Dict,
    ) -> None:
        """test_get_json function"""
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = test_pay
            self.assertEqual(get_json(url), test_pay)
            mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """TestMemoize class that inherits from unittest.TestCase"""
    def test_memoize(self) -> None:
        """test_memoize function"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42,
        ) as test_memoized:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property, 42)
            self.assertEqual(test_obj.a_property, 42)
            test_memoized.assert_called_once()
