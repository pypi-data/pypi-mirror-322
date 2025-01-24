import unittest
from MyPkgAuto1.hello import auto1_say_hello

class TestHello(unittest.TestCase):
    def test_default(self):
        self.assertEqual(auto1_say_hello(), "Hello, World!")

    def test_custom_name(self):
        self.assertEqual(auto1_say_hello("Python"), "Hello, Python!")

if __name__ == "__main__":
    unittest.main()
