import sys


class OG_SimpleEditor:
    def __init__(self, document):
        self.document = document
        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        with open("C:/Users/Richard Le/AppData/Roaming/Microsoft/Spelling/en-US/default.dic","r",encoding ="utf-16") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = ""


    def cut(self, i, j):
        self.paste_text = self.document[i:j]
        self.document = self.document[:i] + self.document[j:]

    def copy(self, i, j):
        self.paste_text = self.document[i:j]

    def paste(self, i):
        self.document = self.document[:i] + self.paste_text + self.document[i:]

    def get_text(self):
        #print(self.document)
        return self.document

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result


######################################## my code ###############################

from collections import defaultdict
class TrieNode():
    def __init__(self):
        self.children = dict()
        self.terminating = False
    def auto_complete(self, prefix):
        if self.terminating:
            #print("HI")
            yield prefix
        for char, child in self.children.items():
            #print("HI")
            yield from child.auto_complete(prefix + char)

class Trie():
    def __init__(self):
        self.root = self.get_node()
    def get_node(self):
        return TrieNode()
    def get_index(self, ch):
        return ch
    def insert(self, word):
        root = self.root
        for i in range(len(word)):
            index = word[i]
            if index not in root.children:
                root.children[index] = self.get_node()
            root = root.children.get(index)
        root.terminating = True
    def search(self, word): # By the return numbers, I get information on the key.
        root = self.root
        for i in range(len(word)):
            index = word[i]
            if not root:
             #   print("just straight wrong")
                return -2
            root = root.children.get(index)
        if root and root.terminating:
            #print(it's a match)
            return 1 
        if not root:
           # print("went too far")
            return -1
       # print("on the way there")
        return 0
    def begins_with_prefix(self,prefix):
        #print("he")
        root = self.root
        for char in prefix:
            root = root.children.get(char)
            if not root:
                #print("here")
                return
        yield from root.auto_complete(prefix)

class Richard_SimpleEditor:
    def __init__(self, document):
        self.trie = Trie()
        self.document = document
        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        ###please replace this with your own dictionary path### 

        #my_path = "C:/Users/Richard Le/AppData/Roaming/Microsoft/Spelling/en-US/default.dic","r",encoding ="utf-16"
        #original_path =  "/usr/share/dict/words"
        with open("C:/Users/Richard Le/AppData/Roaming/Microsoft/Spelling/en-US/default.dic","r",encoding ="utf-16") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                   # print(word)
                    self.trie.insert(word)
        self.paste_text = ""


    def cut(self, i, j):
        self.paste_text = self.document[i:j]
        self.document = self.document[:i] + self.document[j:]

    def copy(self, i, j):
        self.paste_text = self.document[i:j]

    def paste(self, i):
        self.document = self.document[:i] + self.paste_text + self.document[i:]

    def get_text(self):
        return self.document

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if self.trie.search(word) < 1:
                result += 1
        return result

    def suggestions(self,prefix):
        return list(self.trie.begins_with_prefix(prefix))



import timeit

class EditorBenchmarker:
    new_editor_case = """
from __main__ import OG_SimpleEditor
s = OG_SimpleEditor("{}")"""

    richard_new_editor_case = """
from __main__ import Richard_SimpleEditor
s = Richard_SimpleEditor("{}")"""
    
    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, 3)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 3)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""
    def __init__(self, cases, N,version):
        self.version = version
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)
    def benchmark(self):
        for case in self.cases:
            # command line version
            if self.version == 1: #use original editor
                print("##################################################################")    
                print("                 You are using the original Editor.")
                print("##################################################################")    
                new_editor = self.new_editor_case.format(case)
            elif self.version == 2: #use richards editor
                print("##################################################################")
                print("                 You are using the Richard's Editor.")
                print("##################################################################")    
                new_editor = self.richard_new_editor_case.format(case)
            elif self.version == 3:
                new_editor = self.new_editor_case.format(case)

            print("Evaluating case: {}".format(case))
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)

            if self.version == 1 or self.version == 2: # just one
                print("{} (cut paste):     {} s".format(self.N, cut_paste_time))
                print("{} (copy paste):    {} s".format(self.N, copy_paste_time))
                print("{} (text retrieval):{} s".format(self.N, get_text_time))
                print("{} (mispelling):    {} s".format(self.N, mispellings_time))
            if self.version == 3: #print and compare both
                new_editor2 = self.richard_new_editor_case.format(case)
                richard_cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor2,number=1)
                richard_copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor2,number=1)
                richard_get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor2,number=1)
                richard_mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor2,number=1)

                print("OG(cut paste) | Richard (cut paste)  (#trials {}) = {} s    ||| ".format(self.N, cut_paste_time),  "{} s".format(richard_cut_paste_time))
                print("OG(copy paste)| Richard (copy paste) (#trials {}) = {} s    ||| ".format(self.N, copy_paste_time), "{} s".format(richard_copy_paste_time))
                print("OG(text ret.) | Richard (text ret.)  (#trials {}) = {} s    |||".format(self.N, get_text_time),"{} s".format(richard_get_text_time))
                print("OG(mispelling)| Richard (mispelling) (#trials {}) = {} s    ||| ".format(self.N, mispellings_time),"{} s".format(richard_mispellings_time))


if __name__ == "__main__":
    args = (sys.argv) #command line
    if len(args) > 1:
        if args[1] == "original":
            version = 1
        elif args[1] == "richard":
            version = 2

        elif args[1] == "both":
            version = 3
        else:
            version = 2 
    else:
        version = 2 #OG IS 1

        
    b = EditorBenchmarker(["hello world I really like the weather today deaaa"], 2,version)
    b.benchmark()


    ##########################editor autocorrect implementation showcase #####################################
    s = Richard_SimpleEditor("hello world")
    # this will use words in the dictionary to try to suggest autocompletes.
    prefix = "i"
    suggestions = list(s.suggestions(prefix))
    print("auto complete suggestions for '"+ prefix+ "': " + str(suggestions))