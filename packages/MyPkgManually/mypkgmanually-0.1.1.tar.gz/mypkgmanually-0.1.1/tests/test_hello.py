import unittest
from MyPkgManually.hello import say_hello, say_hello2

class TestHello(unittest.TestCase):
    def test_default(self):
        self.assertEqual(say_hello(), "Hello, World!")

    def test_custom_name(self):
        self.assertEqual(say_hello("Python"), "Hello, Python!")

    def test_default2(self):
        self.assertEqual(say_hello2(), "World, Hello!")

    def test_custom_name2(self):
        self.assertEqual(say_hello2("Python"), "Python, Hello!")

if __name__ == "__main__":
    unittest.main()
