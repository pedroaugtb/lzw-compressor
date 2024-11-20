class TrieNode:
    """
    Represents a single node in a Trie (prefix tree).

    Attributes:
        children (dict): A dictionary mapping characters to TrieNode objects.
        value (int or None): The code associated with the string ending at this node.
        is_end_of_word (bool): Indicates whether this node marks the end of a valid word.
    """

    def __init__(self):
        """
        Initializes a TrieNode instance with no children, no value, 
        and not marked as the end of a word.
        """
        self.children = {}  # Dictionary mapping characters to TrieNode
        self.value = None  # Code associated with the string
        self.is_end_of_word = False  # Indicates if the node represents the end of a word


class Trie:
    """
    Implements a Trie (prefix tree) structure for efficient string storage and retrieval.

    Attributes:
        root (TrieNode): The root node of the Trie.
        next_code (int): The next available code for encoding strings.
    """

    def __init__(self):
        """
        Initializes a Trie instance with an empty root node and a next_code starting at 256.
        """
        self.root = TrieNode()
        self.next_code = 256  # Next available code (0-255 are reserved)

    def insert(self, string):
        """
        Inserts a string into the Trie, associating it with a unique code.

        Args:
            string (str): The string to insert into the Trie.
        """
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
        """
        Searches for a string in the Trie and retrieves its associated code.

        Args:
            string (str): The string to search for.

        Returns:
            int or None: The code associated with the string, or None if the string is not found.
        """
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
        """
        Deletes a string from the Trie.

        Args:
            string (str): The string to delete from the Trie.
        """
        if not string:
            return  # Do not delete empty strings
        self._delete(self.root, string, 0)

    def _delete(self, node, string, depth):
        """
        Recursively deletes a string from the Trie.

        Args:
            node (TrieNode): The current node being examined.
            string (str): The string to delete.
            depth (int): The current depth in the string.

        Returns:
            bool: True if the current node can be deleted, False otherwise.
        """
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
        """
        Initializes the Trie with all ASCII characters (0-255).

        Each character is stored as a single entry in the Trie with its ASCII value as the code.
        """
        for i in range(256):
            char = chr(i)
            node = self.root
            node.children[char] = TrieNode()
            node = node.children[char]
            node.is_end_of_word = True
            node.value = i