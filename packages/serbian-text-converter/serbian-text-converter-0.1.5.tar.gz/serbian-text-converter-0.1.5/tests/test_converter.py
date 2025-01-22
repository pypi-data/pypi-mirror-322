import unittest
from serbian_text_converter import SerbianTextConverter

class TestSerbianTextConverter(unittest.TestCase):
    def test_to_latin(self):
        self.assertEqual(SerbianTextConverter.to_latin("Љубав"), "Ljubav")

    def test_to_cyrillic(self):
        self.assertEqual(SerbianTextConverter.to_cyrillic("Ljubav"), "Љубав")

    def test_normalize(self):
        self.assertEqual(SerbianTextConverter.normalize("Љубав и Живот"), "ljubav-i-zivot")
        
if __name__ == "__main__":
    unittest.main()