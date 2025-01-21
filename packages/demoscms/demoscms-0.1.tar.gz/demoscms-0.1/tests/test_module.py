 import unittest
from demoscms.module import greet

class TestGreetFunction(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World! Welcome to DemoCMS.")

