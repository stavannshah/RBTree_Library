from redblacktree import RedBlackTree, Node, Book
from binaryminheap import MinHeap
import sys


class GatorLibrary:
    def __init__(self):
        self.books_rb_tree = RedBlackTree()
        self.reservation_heap = MinHeap()

    #Function to read the input
    def readfile(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                return lines

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    #Function to print book details
    def PrintBook(self, book_id):
        # Search for the book in the Red-Black tree
        node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if node != self.books_rb_tree.TNULL:
            print(f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \n"
                  f"Availability: '{'Yes' if node.book.availability_status else 'No'}'")
            if node.book.borrowed_by:
                print(f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}")
            else:
                print("Borrowed by : None")
            print(f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n")
        else:
            print(f"Book {book_id} not found in the Library \n")

    #Function to print books in a range
    def PrintBooks(self, book_id1, book_id2):
        # Iterate through the Red-Black tree and print books within the specified range
        self._print_books_range_helper(self.books_rb_tree.root, book_id1, book_id2)

    #Function to help print books in a range
    def _print_books_range_helper(self, node, book_id1, book_id2):
        if node != self.books_rb_tree.TNULL:
            if book_id1 < node.book.book_id:
                self._print_books_range_helper(node.left, book_id1, book_id2)

            if book_id1 <= node.book.book_id <= book_id2:
                print(f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \n"
                    f"Availability: '{'Yes' if node.book.availability_status else 'No'}'")
                if node.book.borrowed_by:
                    print(f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}")
                else:
                    print("Borrowed by : None")
                print(f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n")
            if book_id2 > node.book.book_id:
                self._print_books_range_helper(node.right, book_id1, book_id2)

    #Function to insert a book
    def InsertBook(self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        # Check if the book with the given ID already exists
        existing_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)
        if existing_node != self.books_rb_tree.TNULL:
            return

        # If not, create a new book and insert it into the Red-Black tree
        new_book = Book(book_id, book_name, author_name, availability_status, borrowed_by, reservation_heap)
        self.books_rb_tree.insert(book_id, new_book)

    #Function to borrow a book
    def BorrowBook(self, patron_id, book_id, patron_priority):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Check if the book is available
        if book_node.book.availability_status:
            # Check if the patron already has the book in possession
            if patron_id in book_node.book.borrowed_by:
                return

            # Update book status and borrower information
            book_node.book.availability_status = False
            book_node.book.borrowed_by.append(patron_id)
            print(f"Book {book_id} Borrowed by Patron {patron_id}\n")
        else:
            # Book is not available, create a reservation node in the heap
            reservation_heap = book_node.book.reservation_heap
            reservation_heap.insert(patron_priority, patron_id)
            print(f"Book {book_id} Reserved by Patron {patron_id}\n")

    #Function to return a book
    def ReturnBook(self, patron_id, book_id):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Check if the patron has borrowed the book
        if patron_id not in book_node.book.borrowed_by:
            return

        # Update book status and borrower information
        book_node.book.availability_status = True
        book_node.book.borrowed_by.remove(patron_id)

        # Assign the book to the patron with the highest priority in the reservation heap (if available)
        reservation_heap = book_node.book.reservation_heap
        if not reservation_heap.is_empty():
            reservation_node = reservation_heap.extract_min()
            next_patron_id = reservation_node.value
            book_node.book.availability_status = False
            book_node.book.borrowed_by.append(next_patron_id)
            print(f"Book {book_id} Returned by Patron {patron_id}\n")
            print(f"Book {book_id} Allotted to Patron {next_patron_id}\n")

        else:
            print(f"Book {book_id} Returned by Patron {patron_id}\n")

    #Function to delete a book
    def DeleteBook(self, book_id):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Notify patrons in the reservation list that the book is no longer available
        reservation_heap = book_node.book.reservation_heap
        if reservation_heap.is_empty():
            print(f"Book {book_id} is no longer available\n")
            
        else:
            print(f"Book {book_id} is no longer available. Reservations made by Patrons ", end="")
    
            while not reservation_heap.is_empty():
                reservation_node = reservation_heap.extract_min()
                patron_id = reservation_node.value
                print(patron_id, ", ", end="")
            print("have been cancelled! \n")
        # Delete the book from the Red-Black tree
        self.books_rb_tree.delete_node(book_id)

    #Function to find the closest book
    def FindClosestBook(self, target_id):
        # Call the corresponding method in the Red-Black tree class
        closest_books = self.books_rb_tree.find_closest_books(target_id)
        book_count = []
        actual_close=[]
        if closest_books:
            for book_id, book_whatever in closest_books.items():
                book_count.append(book_id)
            if len(book_count)>1:
                small = abs(target_id-book_count[0])
                large = abs(book_count[1]-target_id)
                if small!=large:
                    if small<large:
                        actual_close = [book_count[0]]
                    else:
                        actual_close = [book_count[1]]
                else:
                    actual_close = [book_count[0], book_count[1]]
            for book_id in actual_close:
                self.PrintBook(book_id)
        else:
            print(f"No books found in the Library.")

    #Function to Quit the program
    def Quit(self):
        print("Program Terminated!!")
        exit()

    #Function to count the number of flips in color
    def ColorFlipCount(self):
        count = self.books_rb_tree.color_flip_count
        print("Colour Flip Count: ",count, "\n")
        return count

# Example usage:
if __name__ == "__main__":
    library = GatorLibrary()

    filepath = sys.argv[1]
    name = filepath.split('.')[0]
    lines = library.readfile(filepath)
    with open(f'{name}_output_file.txt', 'w') as file:

        import sys
        sys.stdout = file
        for line in lines:
            line = 'library.'+line
            
            exec(line)