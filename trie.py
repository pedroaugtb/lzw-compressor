# trie.py

class TrieNode:
    def __init__(self):
        self.children = {}          # Dictionary mapping characters to TrieNode
        self.value = None           # Code associated with the string
        self.is_end_of_word = False # Indicates if the node represents the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.next_code = 256  # Next available code (0-255 are reserved)

    def insert(self, string):
        if not string:
            return  # Do not insert empty strings
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end_of_word:
            node.is_end_of_word = True
            node.value = self.next_code
            self.next_code += 1

    def search(self, string):
        if not string:
            return None  # Do not search for empty strings
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return None  # String not found
        if node.is_end_of_word:
            return node.value  # Return the associated code
        else:
            return None  # String not found as a complete entry

    def delete(self, string):
        if not string:
            return  # Do not delete empty strings
        self._delete(self.root, string, 0)

    def _delete(self, node, string, depth):
        if depth == len(string):
            if not node.is_end_of_word:
                return False  # String not found
            node.is_end_of_word = False
            node.value = None
            # If node has no children, it can be deleted
            return len(node.children) == 0
        char = string[depth]
        if char not in node.children:
            return False  # String not found
        should_delete_child = self._delete(node.children[char], string, depth + 1)
        if should_delete_child:
            del node.children[char]
            # Return True if current node can be deleted
            return len(node.children) == 0 and not node.is_end_of_word
        return False

    def initialize_with_ascii(self):
        for i in range(256):    
            char = chr(i)
            node = self.root
            node.children[char] = TrieNode()
            node = node.children[char]
            node.is_end_of_word = True
            node.value = i
