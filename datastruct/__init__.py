class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.index = None
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, value, index):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        node.value = value
        node.index = index

    def start_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def get_start_with(self, prefix):
        '''
        给出一个前辍，获取所有匹配的字符串
        :param prefix:
        :return:
        '''
        res = []
        if not self.start_with(prefix):
            return res
        node = self.root
        for p in prefix:
            node = node.children[p]
        self.__preorder(node, res)
        return res

    def __preorder(self, node: TrieNode, res: list):
        if node is None:
            return res
        if node.is_word:
            res.append((node.value, node.index))
        for child in node.children.values():
            self.__preorder(child, res)
