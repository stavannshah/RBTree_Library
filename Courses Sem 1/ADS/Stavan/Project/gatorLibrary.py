from redblacktree import RedBlackTree, Node, Book
from binaryminheap import MinHeap
import sys


class GatorLibrary:
    def __init__(var_self):
        var_self.books_rb_tree = RedBlackTree()
        var_self.reservation_heap = MinHeap()

    ##Function to read the input
    def readfile(var_self, file_path):
        lines = []
        
        try:
            file = open(file_path, 'r')
            lines = file.readlines()
            file.close()
        
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return lines
    ###Function to print book detai
    def PrintBook(var_self, book_id):
        # Search for the book in the Red-Black tree
        node = var_self.books_rb_tree.search_tree_helper(var_self.books_rb_tree.root, book_id)

        if node != var_self.books_rb_tree.TNULL:
            book_info = f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \n"
            book_info += f"Availability: '{'Yes' if node.book.availability_status else 'No'}'\n"
            
            if node.book.borrowed_by:
                book_info += f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}\n"
            else:
                book_info += "Borrowed by: None\n"
            
            book_info += f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n"
            print(book_info)
        else:
            print(f"Book {book_id} not found in the Library\n")

    ##Function to help print books in a range
    def book_range(var_self, node, book_id1, book_id2):
        if node != var_self.books_rb_tree.TNULL:
            if book_id1 < node.book.book_id:
                var_self.book_range(node.left, book_id1, book_id2)

            if book_id1 <= node.book.book_id <= book_id2:
                book_info = f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \nAvailability: '{'Yes' if node.book.availability_status else 'No'}'"
                borrowed_by = f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}" if node.book.borrowed_by else "Borrowed by: None"
                reservations = f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n"
                print(book_info)
                print(borrowed_by)
                print(reservations)

            if book_id2 > node.book.book_id:
                var_self.book_range(node.right, book_id1, book_id2)
    
    ##Function to print books in a range
    def PrintBooks(var_self, book_id_1, book_id_2):
        # Iterate through the Red-Black tree and print books within the specified range
        var_self.book_range(var_self.books_rb_tree.root, book_id_1, book_id_2)
    ##Function to insert a book
    def InsertBook(var_self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        # Check if the book with the given ID already exists
        if var_self.books_rb_tree.search_tree_helper(var_self.books_rb_tree.root, book_id) != var_self.books_rb_tree.TNULL:
            return
        # If not, create a new book and insert it into the Red-Black tree
        new_book = Book(book_id, book_name, author_name, availability_status, borrowed_by, reservation_heap)
        var_self.books_rb_tree.insert(book_id, new_book)

    ##Function to borrow a book
    def BorrowBook(library, patron_id, book_id, patron_priority):
        # Search for the book in the Red-Black tree
        book_node = library.books_rb_tree.search_tree_helper(library.books_rb_tree.root, book_id)
        
        if book_node == library.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return
        # Check if the book is available
        if book_node.book.availability_status:
            # Check if the patron already has the book in possession
            if patron_id not in book_node.book.borrowed_by:
                 # Update book status and borrower information
                book_node.book.availability_status = False
                book_node.book.borrowed_by.append(patron_id)
                print(f"Book {book_id} Borrowed by Patron {patron_id}\n")
        else:
            # Book is not available, create a reservation node in the heap
            reservation_heap = book_node.book.reservation_heap
            reservation_heap.insert(patron_priority, patron_id)
            print(f"Book {book_id} Reserved by Patron {patron_id}\n")

    ## Function to return to book
    def ReturnBook(var_self, patron_id, book_id):
    # Find the book in the Red-Black tree
        book_node = var_self.books_rb_tree.search_tree_helper(var_self.books_rb_tree.root, book_id)
        if book_node == var_self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Verify if the patron has borrowed the book
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
    
    ##Function to delete a book
    def DeleteBook(var_self, book_id):
        # Search for the book in the Red-Black tree
        book_node = var_self.books_rb_tree.search_tree_helper(var_self.books_rb_tree.root, book_id)

        if book_node == var_self.books_rb_tree.TNULL:
            return f"Book {book_id} not found in the Library"
        # Notify patrons in the reservation list that the book is no longer available
        reservation_heap = book_node.book.reservation_heap
        if reservation_heap.is_empty():
            print(f"Book {book_id} is no longer available")

        reservations = []
        while not reservation_heap.is_empty():
            reservation_node = reservation_heap.extract_min()
            patron_id = reservation_node.value
            reservations.append(patron_id)

        cancellation_message = f"Book {book_id} is no longer available. Reservations made by Patrons {', '.join(reservations)} have been cancelled!"
        # Delete the book from the Red-Black tree
        var_self.books_rb_tree.delete_node(book_id)
        return cancellation_message
    ##
    

    #Function to find the closest book
    def FindClosestBook(var_self, target_id):
        # Call the corresponding method in the Red-Black tree class
        closest_books = var_self.books_rb_tree.find_closest_books(target_id)
        book_count = []
        actual_close=[]
        if closest_books:
            for book_id, book_whatever in closest_books.items():
                book_count.append(book_id)
            if len(book_count)>1:
                closest_lower = abs(target_id-book_count[0])
                closest_higher = abs(book_count[1]-target_id)
                if closest_lower!=closest_higher:
                    if closest_lower<closest_higher:
                        actual_close = [book_count[0]]
                    else:
                        actual_close = [book_count[1]]
                else:
                    actual_close = [book_count[0], book_count[1]]
            for book_id in actual_close:
                var_self.PrintBook(book_id)
            else:
                for book_id in book_count:
                    if book_id == target_id:
                        var_self.PrintBook(book_id)
                        return
        else:
            print(f"No books found in the Library.")

    #Function to Quit the program
    def Quit(var_self):
        print("Program Terminated!!")
        exit()

    #Function to count the number of flips in color
    def ColorFlipCount(var_self):
        count = var_self.books_rb_tree.color_flip_count
        print("Colour Flip Count: ",count, "\n")
        return count

# Example usage:
if __name__ == "__main__":
    library = GatorLibrary()
    main_file = sys.argv[1]
    name_file = main_file.split('.')[0]
    run_commands = library.readfile(main_file)
    output_file = f'{name_file}_output_file.txt'

    with open(output_file, 'w') as file:
        sys.stdout = file
        
        for r_command in run_commands:
            r_command = 'library.' + r_command
            exec(r_command)