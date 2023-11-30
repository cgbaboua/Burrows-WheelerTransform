#!/bin/python3

class TrieNode:
    """
    A class representing a node in a trie.

    Attributes:
        children (dict): A dictionary of child TrieNodes.
        isLeaf (bool): Indicates if the node is a leaf node.
        index (int): Stores the starting index of the suffix represented by this node.
    """
    def __init__(self):
        self.children = {}   # Dictionary for child nodes.
        self.isLeaf = False  # Boolean to check if it's a leaf node.
        self.index = -1      # Stores the starting index of the suffix represented by this node.


def build_trie(T):
    """
    Build a trie from a given string.

    Args:
        T (str): The string from which the trie is to be built.

    Returns:
        TrieNode: The root node of the constructed trie.
    """
    root = TrieNode()     # Create the root node.
    # For each suffix of the string T.
    for i in range(len(T)):
        current = root   # Start from the root.
        # For each character in the suffix.
        for c in T[i:]:
            # If the character is not already a child of the current node, add it.
            if c not in current.children:
                current.children[c] = TrieNode()
            # Move to the corresponding child node.
            current = current.children[c]
        # Mark the last visited node as a leaf node and store its index.
        current.isLeaf = True
        current.index = i
    return root  # Return the constructed trie.


def bwt_trie_dfs(node, T, result):
    """
    Perform a depth-first search on a trie to build the Burrows-Wheeler Transform (BWT).

    Args:
        node (TrieNode): The current node in the trie.
        T (str): The original string used to build the trie.
        result (list): A list to accumulate the BWT result.

    Returns:
        None: The function modifies the 'result' list in place.
    """
    # If the node is a leaf node, add the appropriate character to the BWT.
    if node.isLeaf:
        # Add '$' if it's the root, otherwise add the character preceding the suffix.
        if node.index == 0:
            result.append("$")
        else:
            result.append(T[node.index - 1])
    # Traverse the children of the current node in lexicographical order.
    for c in sorted(node.children.keys()):
        bwt_trie_dfs(node.children[c], T, result)


def get_BWT_simplified(T):
    """
    Compute the Burrows-Wheeler Transform (BWT) of a string in a simplified manner.

    Args:
        T (str): The string for which BWT is to be computed.

    Returns:
        str: The BWT of the string T.
    """
    # Add '$' to the end of T if not already present.
    if not T.endswith("$"):
        T = T.upper() + '$'
    # Build the trie from T.
    root = build_trie(T)
    result = []
    # Traverse the trie to construct the BWT.
    bwt_trie_dfs(root, T, result)
    return "".join(result)  # Return the BWT as a string.
