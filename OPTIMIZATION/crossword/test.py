import sys

from crossword import *
def enforce_node_consistency(self):
    """
    Update `self.domains` such that each variable is node-consistent.
    (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)
    """
    print(self.crossword.variables)
    for x in self.crossword.variables:
        for w in self.crossword.words:
            if x.length != len(w):
                self.domains[x].remove(w)
self.enforce_node_consistency()

