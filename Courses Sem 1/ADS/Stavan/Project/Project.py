import heapq
import time

class Book:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None):
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservationHeap = []

    def __lt__(self, other):
        return self.bookID < other.bookID

class ReservationNode:
    def __init__(self, patronID, priorityNumber, timeOfReservation):
        self.patronID = patronID
        self.priorityNumber = priorityNumber
        self.timeOfReservation = timeOfReservation

    def __lt__(self, other):
        if self.priorityNumber == other.priorityNumber:
            return self.timeOfReservation < other.timeOfReservation
        return self.priorityNumber < other.priorityNumber

class GatorLibrary:
    def __init__(self):
        self.bookTree = []
        self.colorFlipCount = 0

    def print_book(self, bookID):
        book = self.find_book(bookID)
        if book:
            print(f"BookID = {book.bookID}\nTitle = \"{book.bookName}\"\nAuthor = \"{book.authorName}\"")
            print(f"Availability = \"{book.availabilityStatus}\"")
            print(f"BorrowedBy = {book.borrowedBy if book.borrowedBy is not None else 'None'}")
            print(f"Reservations = {['patron' + str(res.patronID) for res in book.reservationHeap]}")
        else:
            print(f"Book {bookID} not found in the Library")

    def print_books(self, bookID1, bookID2):
        for book in sorted(self.bookTree):
            if bookID1 <= book.bookID <= bookID2:
                print(f"BookID = {book.bookID}\nTitle = \"{book.bookName}\"\nAuthor = \"{book.authorName}\"")
                print(f"Availability = \"{book.availabilityStatus}\"")
                print(f"BorrowedBy = {book.borrowedBy if book.borrowedBy is not None else 'None'}")
                print(f"Reservations = {['patron' + str(res.patronID) for res in book.reservationHeap]}")

    def insert_book(self, bookID, bookName, authorName, availabilityStatus):
        book = Book(bookID, bookName, authorName, availabilityStatus)
        self.bookTree.append(book)
        self.color_flip_count()

    def borrow_book(self, patronID, bookID, patronPriority):
        book = self.find_book(bookID)
        if book and book.availabilityStatus == "Yes":
            book.availabilityStatus = "No"
            book.borrowedBy = patronID
            print(f"Book {bookID} Borrowed by Patron {patronID}")
        elif book:
            reservation_node = ReservationNode(patronID, patronPriority, time.time())
            heapq.heappush(book.reservationHeap, reservation_node)
            print(f"Book {bookID} Reserved by Patron {patronID}")
        self.color_flip_count()

    def return_book(self, patronID, bookID):
        book = self.find_book(bookID)
        if book:
            print(f"Book {bookID} Returned by Patron {patronID}")
            if book.reservationHeap:
                top_reservation = heapq.heappop(book.reservationHeap)
                book.borrowedBy = top_reservation.patronID
                print(f"Book {bookID} Allotted to Patron {top_reservation.patronID}")
            else:
                book.availabilityStatus = "Yes"
                book.borrowedBy = None
        self.color_flip_count()

    def delete_book(self, bookID):
        book = self.find_book(bookID)
        if book:
            if book.reservationHeap:
                patrons = ', '.join(['patron' + str(res.patronID) for res in book.reservationHeap])
                if len(book.reservationHeap) > 1:
                    print(f"Book {bookID} is no longer available. Reservations made by Patrons {patrons} "
                          f"have been cancelled!")
                else:
                    print(f"Book {bookID} is no longer available. Reservation made by Patron {patrons} "
                          f"has been cancelled!")
            else:
                print(f"Book {bookID} is no longer available")
            self.bookTree.remove(book)
        self.color_flip_count()

    def find_closest_book(self, targetID):
        closest_books = []
        for book in sorted(self.bookTree):
            if book.bookID <= targetID:
                closest_books.append(book)
            else:
                break
        closest_books.sort(key=lambda x: abs(x.bookID - targetID))
        for book in closest_books:
            print(f"BookID = {book.bookID}\nTitle = \"{book.bookName}\"\nAuthor = \"{book.authorName}\"")
            print(f"Availability = \"{book.availabilityStatus}\"")
            print(f"BorrowedBy = {book.borrowedBy if book.borrowedBy is not None else 'None'}")
            print(f"Reservations = {['patron' + str(res.patronID) for res in book.reservationHeap]}")

    def color_flip_count(self):
        # The color flip count logic can be implemented during tree operations (insert, delete, rotation).
        # For simplicity, in this example, we assume color flips are tracked at each operation.
        self.colorFlipCount += 1

    def find_book(self, bookID):
        for book in self.bookTree:
            if book.bookID == bookID:
                return book
        return None

    def execute_operation(self, operation):
        if operation.startswith("InsertBook"):
            _, bookID, bookName, authorName, availabilityStatus = operation.split()
            self.insert_book(int(bookID), bookName.strip('"'), authorName.strip('"'), availabilityStatus.strip('"'))
        elif operation.startswith("PrintBook"):
            _, bookID = operation.split()
            self.print_book(int(bookID))
        elif operation.startswith("PrintBooks"):
            _, bookID1, bookID2 = operation.split()
            self.print_books(int(bookID1), int(bookID2))
        elif operation.startswith("BorrowBook"):
            _, patronID, bookID, patronPriority = operation.split()
            self.borrow_book(int(patronID), int(bookID), int(patronPriority))
        elif operation.startswith("ReturnBook"):
            _, patronID, bookID = operation.split()
            self.return_book(int(patronID), int(bookID))
        elif operation.startswith("DeleteBook"):
            _, bookID = operation.split()
            self.delete_book(int(bookID))
        elif operation.startswith("FindClosestBook"):
            _, targetID = operation.split()
            self.find_closest_book(int(targetID))
        elif operation.startswith("ColorFlipCount"):
            print(f"Colour Flip Count: {self.colorFlipCount}")
        elif operation.startswith("Quit"):
            print("Program Terminated!!")

# Example Usage:
if __name__ == "__main__":
    gator_library = GatorLibrary()

    with open("C:\\Users\\Stavan Shah\\Courses Sem 1\\ADS\\Stavan\\Project\\test_input.txt", "r") as file:
        operations = file.readlines()

    for operation in operations:
        gator_library.execute_operation(operation.strip())
