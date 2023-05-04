import tkinter
class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = "R"


class RedBlackTree:
    def __init__(self):
        self.nil = Node(0)
        self.nil.color = "B"
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert_tree_into_list(self, node, tree_list):  # called by passing root node
        if node != self.nil:
            tree_list.append(node)
            self.insert_tree_into_list(node.left)
            self.insert_tree_into_list(node.right)

    def my_pre_order_print(self, node):  # for testing
        if node != self.nil:
            print(str(node.key)+","+(node.color) + "," + " -> ( ", end=" ")
            self.my_pre_order_print(node.left)
            print(" , ", end=" ")
            self.my_pre_order_print(node.right)
            print(" )", end=" ")

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.key = key
        node.left = self.nil
        node.right = self.nil
        node.color = "R"

        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "B"
            return

        if node.parent.parent is None:
            return

        self.rb_insert_fix_up(node)

    def search(self, val):
        x = self.root
        while x != self.nil and val != x.key:
            if val < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def rb_insert_fix_up(self, k):
        while k.parent.color == "R":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "R":
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "R":
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "B"

    def get_tree_height(self):
        return self.get_height(self.root)

    def get_height(self, node):
        if node == self.nil:
            return 0
        else:
            left_height = self.get_height(node.left)
            right_height = self.get_height(node.right)
            return max(left_height, right_height) + 1

    def print_tree_height(self):
        tree_height =self.get_tree_height()
        print("Tree height: ", tree_height)

    def print_tree_size(self, node):
        if node != self.nil:
            return self.print_tree_size(node.left) + 1 + self.print_tree_size(node.right)
        else:
            return 0


class Dictionary:
    def __init__(self):
        file = open("EN-US-Dictionary.txt", "r")
        self.dictionary_list = file.read().split("\n")
        self.tree = RedBlackTree()

        for word in self.dictionary_list:
            self.tree.insert(word)

    def load_from_tree(self):
        self.dictionary_list.clear()
        self.tree.insert_tree_into_list(self.tree.root, self.dictionary_list)

        with open('EN-US-Dictionary.txt', 'w+') as file:
            for items in self.dictionary_list:
                file.write('%s\n' % items)

    def print_dictionary_size(self, status=1):
        size = self.tree.print_tree_size(self.tree.root)
        if status == 1:
            output_text.config(text="")
            dictionary_size_label.config(text=f"Dictionary size: {size} words", font=("Arial", 8, "bold"))
        else:
            dictionary_size_label.config(text=f"Dictionary size: {size} words\n Tree height: {self.tree.get_tree_height()}", font=("Arial", 8, "bold"))

    def insert_word_to_dictionary(self):
        if input_field.get() == "":
            output_text.config(text="Text field is empty...!!!")
            dictionary_size_label.config(text="")
            return

        x = self.tree.search(input_field.get())

        if x != self.tree.nil:
            output_text.config(text="ERROR: Word already in the dictionary!", font=("Arial", 8, "bold"))
        else:
            self.tree.insert(input_field.get())
            output_text.config(text=f"Success...... {input_field.get()} inserted", font=("Arial", 8, "bold"))
            self.print_dictionary_size(0)

    def lookup_word(self):
        dictionary_size_label.config(text="")

        if input_field.get() == "":
            output_text.config(text="Text field is empty...!!!")
            return

        x = self.tree.search(input_field.get())

        output_text.config(text="")

        if x != self.tree.nil:
            output_text.config(text=f"YES...... {input_field.get()} exists", font=("Arial", 8, "bold"))
        else:
            output_text.config(text=f"NO...... {input_field.get()} doesn't exist", font=("Arial", 8, "bold"))


window = tkinter.Tk()
window.title("EN-US-Dictionary.......")
window.minsize(width=480, height=240)

user_input = ""

dictionary = Dictionary()

intro = tkinter.Label(text="Choose one of the following", font=("Arial", 8, "bold"))

print_size_button = tkinter.Button(text="Print Dic. size", font=("Arial", 8, "bold"), command=dictionary.print_dictionary_size)
print_size_button.config(padx=20, pady=20)

insert_word_button = tkinter.Button(text="Insert Word", font=("Arial", 8, "bold"), command=dictionary.insert_word_to_dictionary)
insert_word_button.config(padx=24, pady=20)

look_up_word_button = tkinter.Button(text="Look up Word", font=("Arial", 8, "bold"), command=dictionary.lookup_word)
look_up_word_button.config(padx=18, pady=20)

input_field = tkinter.Entry(width=50)
output_text = tkinter.Label()
dictionary_size_label = tkinter.Label()

intro.grid(column=0, row=0)

print_size_button.grid(column=0, row=1)
insert_word_button.grid(column=0, row=2)
look_up_word_button.grid(column=0, row=3)

input_field.grid(column=1, row=1)
output_text.grid(column=1, row=2)
dictionary_size_label.grid(column=1, row=3)

window.mainloop()


