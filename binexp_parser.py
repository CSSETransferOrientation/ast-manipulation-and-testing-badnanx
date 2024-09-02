#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        # IMPLEMENT ME! Done
        # ;;> This doesn't recur
        if self.type == NodeType.operator and self.val == '+':
            if self.left and self.left.type == NodeType.number and self.left.val == '0':
                self.val = self.right.val
                self.type = self.right.type
                self.left = self.right.left
                self.right = self.right.right
            elif self.right and self.right.type == NodeType.number and self.right.val == '0':
                self.val = self.left.val
                self.type = self.left.type
                self.right = self.left.right  # This should be self.right = self.left.right after reassigning val
                self.left = self.left.left  # This should be self.left = self.left.left after reassigning val
                        
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        # IMPLEMENT ME! Done
        # ;;> This doesn't recur
        if self.type == NodeType.operator and self.val == '*':
            if self.left and self.left.type == NodeType.number and self.left.val == '1':
                self.val = self.right.val
                self.type = self.right.type
                self.left = self.right.left
                self.right = self.right.right
            elif self.right and self.right.type == NodeType.number and self.right.val == '1':
                self.val = self.left.val
                self.type = self.left.type
                self.left = self.left.left
                self.right = self.left.right if self.left else False  # Ensure left isn't False before accessing .right
    
    
    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        # Optionally, IMPLEMENT ME! (I'm pretty easy)
        pass
    
    def constant_fold(self):
        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """
        # Optionally, IMPLEMENT ME! This is a bit more challenging. 
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass            

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()
        self.constant_fold()
        return self #Return self after simplification

# Test cases
class TestBinOpAst(unittest.TestCase):
    # ;;> This is a good start, but really sparse on tests and doesn't use the file based tested required in the spec
    def test_additive_identity(self):
        ast = BinOpAst(['+', '1', '0'])
        simplified_ast = ast.simplify_binops()
        self.assertEqual(simplified_ast.prefix_str(), '1')

    def test_additive_identity(self):
        ast = BinOpAst(['+', '1', '+', '0', '10'])
        simplified_ast = ast.simplify_binops()
        self.assertEqual(simplified_ast.prefix_str(), '+ 1 10')


    def test_multiplicative_identity(self):
        ast = BinOpAst(['*', '2', '1'])
        simplified_ast = ast.simplify_binops()
        self.assertEqual(simplified_ast.prefix_str(), '2')

if __name__ == "__main__":
    unittest.main()
