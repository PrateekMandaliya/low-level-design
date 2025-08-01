from enum import Enum
from datetime import datetime, timedelta
from typing import List, Optional, Dict


"""
BOOK CLASSES - States, Book, and BookItem
"""

class BookStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    LOANED = "LOANED"
    LOST = "LOST"


class Book:
    def __init__(self, title: str, author: str, subject: str, publisher: str):
        self.title = title
        self.author = author
        self.subject = subject
        self.publisher = publisher
        self.book_items : List["BookItem"] = []

    def add_book_item(self, book_item: "BookItem"):
        self.book_items.append(book_item)

    

class BookItem:
    def __init__(self, barcode: str, book: Book, rack_location: str):
        self.barcode = barcode
        self.book = book
        self.rack_location = rack_location
        self.status = BookStatus.AVAILABLE
        self.due_date: Optional[datetime] = None
        self.borrowed_by: Optional["Member"] = None

    def borrow(self, member: "Member", loan_period_days: int = 14):
        self.borrowed_by = member
        self.status = BookStatus.LOANED
        self.due_date = datetime.now() + timedelta(days = loan_period_days)

    def return_book(self):
        self.borrowed_by = None
        self.due_date = None
        self.status = BookStatus.AVAILABLE



"""
ACCOUNT CLASSES - LIBRARIAN AND MEMBER
"""

class Account:
    def __init__(self, username: str, password: str, name: str, email: str):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.is_active = True


class Librarian(Account):
    def __init__(self, username: str, password: str, name: str, email: str):
        super().__init__(username, password, name, email)

    def add_book_item(self, book: Book, barcode: str, rack_location: str):
        book_item = BookItem(barcode, book, rack_location)
        book.add_book_item(book_item)
        return book_item
    

MAX_BORROW_LIMIT = 5

class Member(Account):    
    def __init__(self, username: str, password: str, name: str, email: str):
        super().__init__(username, password, name, email)
        self.borrowed_books : List[BookItem] = []
        self.reserved_books: List[Book] = []

    def can_borrow(self):
        return len(self.borrowed_books) < MAX_BORROW_LIMIT

    def reserve_book(self, book: Book, library: "Library"):
        all_loaned = all(item.status == BookStatus.LOANED for item in book.book_items)
        if not all_loaned:
            print(f"⚠️ Book '{book.title}' has available copies. Try borrowing instead.")
            return
        
        library.reservation_manager.add_reservation(self, book)
        self.reserved_books.append(book)

    def borrow_book(self, book_item: BookItem):
        if book_item.status != BookStatus.AVAILABLE:
            print(f"❌ Book {book_item.barcode} is not available")
            return False
        if not self.can_borrow():
            print(f"❌ Borrow limit reached for {self.name}")
            return False
        
        book_item.borrow(self)
        self.borrowed_books.append(book_item)
        print(f"✅ {self.name} borrowed '{book_item.book.title}' [{book_item.barcode}]")
        return True

    def return_book(self, book_item: BookItem, library: "Library"):
        if book_item not in self.borrowed_books:
            print(f"❌ {self.name} has not borrowed this book.")
            return
        
        book_item.return_book()
        self.borrowed_books.remove(book_item)
        library.process_return(book_item)
        print(f"🔁 {self.name} returned '{book_item.book.title}' [{book_item.barcode}]")


"""
RESERVATION and RESERVATIONMANAGER 
"""


class Reservation:
    def __init__(self, member: Member, book: Book, timestamp: datetime = None):
        self.member = member
        self.book = book
        self.timestamp = timestamp or datetime.now()


from collections import deque

class ReservationManager:
    def __init__(self):
        # Maps book title -> queue of Reservation objects
        self.reservation_queues: Dict[str, deque[Reservation]] = {}
    
    def add_reservation(self, member: Member, book: Book):
        queue = self.reservation_queues.setdefault(book.title, deque())
        queue.append(Reservation(member, book))
        print(f"📌 {member.name} reserved '{book.title}'")

    def get_next_reserver(self, book: Book) -> Member | None:
        queue = self.reservation_queues.get(book.title)
        if queue and len(queue) > 0:
            reservation = queue.popleft()
            return reservation.member
        return None
    
    def has_reservation(self, book: Book) -> bool:
        return bool(self.reservation_queues.get(book.title))
    

"""
LIBRARY and CATALOG 
"""

class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.members: List[Member] = []
        self.librarians: List[Librarian] = []
        self.reservation_manager = ReservationManager()

    def add_member(self, member: Member):
        self.members.append(member)

    def add_librarian(self, librarian: Librarian):
        self.librarians.append(librarian)

    # added after reservation class addition
    def process_return(self, book_item: BookItem):
        book = book_item.book
        next_member = self.reservation_manager.get_next_reserver(book)
        if next_member:
            book_item.status = BookStatus.RESERVED
            book_item.borrowed_by = next_member
            print(f"📌 Book '{book.title}' is reserved for {next_member.name}")
        else:
            book_item.return_book() 



class Catalog:
    def __init__(self):
        self.books_by_title = {}
        self.books_by_author = {}
        self.books_by_subject = {}

    def add_book(self, book: Book):
        # dict_name.setdefault(key, value)
        self.books_by_title.setdefault(book.title.lower(), []).append(book)
        self.books_by_author.setdefault(book.author.lower(), []).append(book)
        self.books_by_subject.setdefault(book.subject.lower(), []).append(book)

    def search_by_title(self, title: str):
        return self.search_by_title.get(title.lower(), [])
    
    def search_by_author(self, author: str):
        return self.search_by_author.get(author.lower(), [])
    
    def search_by_subject(self, subject: str):
        return self.search_by_subject.get(subject.lower(), [])
        
        


book = Book("Sapiens", "Yuval Harari", "History", "Penguin")
copy1 = BookItem("B001", book, "Rack-1")
book.add_book_item(copy1)

alice = Member("alice123", "pass", "Alice", "alice@example.com")
bob = Member("bob456", "pass", "Bob", "bob@example.com")

library = Library()
library.catalog.add_book(book)
library.add_member(alice)
library.add_member(bob)

alice.borrow_book(copy1)              # Alice borrows
bob.reserve_book(book, library)      # Bob reserves
alice.return_book(copy1, library)    # Bob gets it reserved



        

