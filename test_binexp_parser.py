import unittest
from binexp_parser import BinOpAst

class TestBinOpAst(unittest.TestCase):
    def test_additive_identity(self):
        ast = BinOpAst(['+', '1', '0'])
        simplified_ast = ast.simplify_binops()
        self.assertEqual(simplified_ast.prefix_str(), '1')

    def test_multiplicative_identity(self):
        ast = BinOpAst(['*', '2', '1'])
        simplified_ast = ast.simplify_binops()
        self.assertEqual(simplified_ast.prefix_str(), '2')

if __name__ == "__main__":
    unittest.main()
