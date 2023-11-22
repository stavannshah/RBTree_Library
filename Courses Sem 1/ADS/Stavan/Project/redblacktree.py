
from binaryminheap import MinHeap, MinHeapNode
class Node:
    def __init__(var_self, book):
        var_self.book = book
        var_self.parent = None
        var_self.left = None
        var_self.right = None
        var_self.color = 1  # 1 for red, 0 for black

class Book:
    def __init__(var_self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        var_self.book_id = book_id
        var_self.book_name = book_name
        var_self.author_name = author_name
        var_self.availability_status = availability_status
        var_self.borrowed_by = borrowed_by or []
        var_self.reservation_heap = MinHeap() if reservation_heap is None else reservation_heap

    def __str__(var_self):
        return f"Book ID: {var_self.book_id}, Title: {var_self.book_name}, Author: {var_self.author_name}, Available: {var_self.availability_status}"
    
class RedBlackTree:
    def __init__(var_self):
        var_self.TNULL = Node(None)
        var_self.TNULL.color = 0  # Set color of TNULL to black
        var_self.TNULL.left = None
        var_self.TNULL.right = None
        var_self.root = var_self.TNULL
        var_self.color_flip_count = 0

    # Search the tree
    def search_tree_helper(var_self, node, key):
        if node == var_self.TNULL or key == node.book.book_id:
            return node

        if key < node.book.book_id:
            return var_self.search_tree_helper(node.left, key)
        return var_self.search_tree_helper(node.right, key)

    def color_flip_count_reset(var_self):
        var_self.color_flip_count = 0

    def color_flip_count_increment(var_self):
        var_self.color_flip_count += 1

    def flip_count_update(var_self, previous, updated):
        if(previous != updated):
            var_self.color_flip_count += 1

    # Balance the tree after deletion
    def fix_delete(var_self, x):
        original_color = x.color
        while x != var_self.root and x.color == original_color:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    var_self.flip_count_update(1,s.color)
                    previous_value= x.parent.color
                    x.parent.color = 1
                    var_self.flip_count_update(previous_value,x.parent.color)
                    var_self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    previous_value=s.color
                    s.color = 1
                    var_self.flip_count_update(previous_value,s.color)
                    x = x.parent
                else:
                    if s.right.color == 0:
                        previous_value=s.left.color
                        s.left.color = 0
                        var_self.flip_count_update(previous_value,s.left.color)
                        previous_value=s.color
                        s.color = 1
                        var_self.flip_count_update(previous_value,s.color)
                        var_self.right_rotate(s)
                        s = x.parent.right

                    previous_value=s.color
                    s.color = x.parent.color
                    var_self.flip_count_update(previous_value,s.color)
                    previous_value = x.parent.color
                    x.parent.color = 0
                    var_self.flip_count_update(previous_value,x.parent.color)
                    previous_value= s.right.color
                    s.right.color = 0
                    var_self.flip_count_update(previous_value,s.right.color)
                    var_self.left_rotate(x.parent)
                    x = var_self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    var_self.flip_count_update(1,s.color)
                    previous_value = x.parent.color
                    x.parent.color = 1
                    var_self.flip_count_update(previous_value,x.parent.color)
                    var_self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    previous_value = s.color
                    s.color = 1
                    var_self.flip_count_update(previous_value,s.color)
                    x = x.parent
                else:
                    if s.left.color == 0:
                        previous_value = s.right.color
                        s.right.color = 0
                        var_self.flip_count_update(previous_value,s.right.color)
                        previous_value = s.color
                        s.color = 1
                        var_self.flip_count_update(previous_value,s.color)
                        var_self.left_rotate(s)
                        s = x.parent.left

                    previous_value = s.color
                    s.color = x.parent.color
                    var_self.flip_count_update(previous_value,s.color)

                    previous_value=x.parent.color
                    x.parent.color = 0
                    var_self.flip_count_update(previous_value,x.parent.color)

                    previous_value = s.left.color
                    s.left.color = 0
                    var_self.flip_count_update(previous_value,s.left.color)
                    var_self.right_rotate(x.parent)
                    x = var_self.root

            if x == var_self.root:
                break
            if x.color != original_color:  # Only increment count if color has changed
                var_self.color_flip_count_increment()
        x.color = 0

    # Balance the tree after insertion of a node
    def fix_insert(var_self, k):
        original_color = k.parent.color
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == 1:
                    previous_value=u.color
                    u.color = 0
                    var_self.flip_count_update(previous_value,u.color)

                    previous_value = k.parent.color
                    k.parent.color = 0
                    var_self.flip_count_update(previous_value,k.parent.color)

                    previous_value= k.parent.parent.color
                    k.parent.parent.color = 1
                    var_self.flip_count_update(previous_value,k.parent.parent.color)
                    
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        var_self.right_rotate(k)
                    
                    previous_value = k.parent.color
                    k.parent.color = 0
                    var_self.flip_count_update(previous_value,k.parent.color)

                    previous_value= k.parent.parent.color
                    k.parent.parent.color = 1
                    var_self.flip_count_update(previous_value,k.parent.parent.color)
                    var_self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == 1:
                    previous_value = u.color
                    u.color = 0
                    var_self.flip_count_update(previous_value,u.color)
                    
                    previous_value = k.parent.color
                    k.parent.color = 0
                    var_self.flip_count_update(previous_value,k.parent.color)

                    previous_value = k.parent.parent.color
                    k.parent.parent.color = 1
                    var_self.flip_count_update(previous_value,k.parent.parent.color)
                    k = k.parent.parent  # move x up
                else:
                    if k == k.parent.right:
                        k = k.parent
                        var_self.left_rotate(k)

                    previous_value = k.parent.color
                    k.parent.color = 0
                    var_self.flip_count_update(previous_value,k.parent.color)

                    previous_value= k.parent.parent.color
                    k.parent.parent.color = 1
                    var_self.flip_count_update(previous_value,k.parent.parent.color)
                    var_self.right_rotate(k.parent.parent)

            if k == var_self.root:
                break
            if k.parent.color != original_color:  # Only increment count if color has changed
                var_self.color_flip_count_increment()
        var_self.root.color = 0

    def left_rotate(var_self, x):
        y = x.right
        x.right = y.left
        if y.left != var_self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            var_self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(var_self, x):
        y = x.left
        x.left = y.right
        if y.right != var_self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            var_self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(var_self, key, book):
        node = Node(book)
        node.parent = None
        node.book = book
        node.left = var_self.TNULL
        node.right = var_self.TNULL
        node.color = 1  # new node must be red

        y = None
        x = var_self.root

        while x != var_self.TNULL:
            y = x
            if node.book.book_id < x.book.book_id:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            var_self.root = node
        elif node.book.book_id < y.book.book_id:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return
        
        var_self.fix_insert(node)

    def get_min_value_node(var_self, node):
        while node.left != var_self.TNULL:
            node = node.left
        return node

    def get_max_value_node(var_self, node):
        while node.right != var_self.TNULL:
            node = node.right
        return node

    def delete_node(var_self, key):
        var_self.delete_node_helper(var_self.root, key)

    def delete_node_helper(var_self, root, key):
        z = var_self.TNULL
        while root != var_self.TNULL:
            if root.book.book_id == key:
                z = root

            if root.book.book_id <= key:
                root = root.right
            else:
                root = root.left

        if z == var_self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == var_self.TNULL:
            x = z.right
            var_self.transplant(z, z.right)
        elif z.right == var_self.TNULL:
            x = z.left
            var_self.transplant(z, z.left)
        else:
            y = var_self.get_min_value_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                var_self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            var_self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 0:
            var_self.fix_delete(x)

    def transplant(var_self, u, v):
        if u.parent == None:
            var_self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def find_closest_books(var_self, target_id):
        closest_books = {}
        closest_lower = var_self.find_closest_lower(var_self.root, target_id)
        closest_higher = var_self.find_closest_higher(var_self.root, target_id)
        if closest_lower is not None:
            closest_books[closest_lower.book.book_id] = {
                'book_name': closest_lower.book.book_name,
                'author_name': closest_lower.book.author_name,
                'availability_status': closest_lower.book.availability_status
            }

        if closest_higher is not None:
            closest_books[closest_higher.book.book_id] = {
                'book_name': closest_higher.book.book_name,
                'author_name': closest_higher.book.author_name,
                'availability_status': closest_higher.book.availability_status
            }

        return closest_books


    def find_closest_lower(var_self, node, target_id):
        current_closest = None

        while node != var_self.TNULL:
            if node.book.book_id == target_id:
                return node
            elif node.book.book_id < target_id:
                current_closest = node
                node = node.right
            else:
                node = node.left

        return current_closest

    def find_closest_higher(var_self, node, target_id):
        current_closest = None

        while node != var_self.TNULL:
            if node.book.book_id == target_id:
                return node
            elif node.book.book_id > target_id:
                current_closest = node
                node = node.left
            else:
                node = node.right

        return current_closest



