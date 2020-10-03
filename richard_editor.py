from collections import defaultdict


class TrieNode():

    def __init__(self):
        self.children = {}
        self.terminating = False

    def auto_complete(self, prefix):

        if self.terminating:
        	#print("HI")
        	yield prefix
        for letter, child in self.children.items():
        	#print("HI")
        	yield from child.auto_complete(prefix + letter)


class Trie():

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def get_index(self, ch):
        return ord(ch) - ord('a')

    def insert(self, word):

        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = word[i]

            if index not in root.children:
                root.children[index] = self.get_node()
            root = root.children.get(index)

        root.terminating = True

    def search(self, word):
        root = self.root
        len1 = len(word)

        for i in range(len1):
            index = word[i]
            if not root:
                return False
            root = root.children.get(index)

        return True if root and root.terminating else False


    def begins_with_prefix(self,prefix):
    	#print("he")
    	root = self.root
    	print(root.children)
    	for char in prefix:
    		root = root.children.get(char)
    		if not root:
    			#print("here")
    			return
    	yield from root.auto_complete(prefix)

        

if __name__ == "__main__":

    strings = ["foobar", "fooofoo", "likeyou", "likeme", "lcik"]

    t = Trie()
    for word in strings:
        t.insert(word)



    print(list(t.begins_with_prefix("foo")))

   	# print(t.auto_complete("pq"))