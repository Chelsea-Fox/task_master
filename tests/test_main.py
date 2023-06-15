"""
Main test file for TaskMaster
"""
from unittest import TestCase
from main import get_task


# pylint: disable=missing-class-docstring
class Test(TestCase):
    def test_input_is_passed_and_returned(self):
        """Simple input and output"""
        expected_value = "Clean"
        actual_value = get_task("Clean")

        self.assertEqual(expected_value, actual_value, "Values are not matching")
