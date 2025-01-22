import unittest
from topsis.topsis import topsis

class TestTopsis(unittest.TestCase):
    def test_topsis(self):
        topsis('examples/example.csv', [0.3, 0.2, 0.5], ['+', '-', '+'], 'output.csv')
        with open('output.csv', 'r') as f:
            result = f.read()
        self.assertIn('Topsis Score', result)
        self.assertIn('Rank', result)

if __name__ == '__main__':
    unittest.main()
