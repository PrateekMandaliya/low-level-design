from enum import Enum
from typing import List, Dict

"""
BOOK CLASSES - States, Book, and BookItem
"""

class BookStatus(Enum):
    AVAILABLE = "AVAILABLE"
    LOANED = "LOANED"
    LOST = "LOST"


class Book:
    def __init__(self, title: str, author: str, subject: str, publisher: str):
        self.title = title
        self.author = author
        self.subject = subject
        self.publisher = publisher
        self.book_items: List["BookItem"] = []

    def add_book_item(self, item: "BookItem"):
        self.book_items.append(item)


class BookItem:
    def __init__(self, barcode: str, book: Book, location: str):
        self.barcode = barcode
        self.book = book
        self.location = location
        self.status = BookStatus.AVAILABLE
        self.borrowed_by = None

    def borrow(self, member: "Member"):
        if self.status == BookStatus.AVAILABLE:
            self.status = BookStatus.LOANED
            self.borrowed_by = member
            print(f"✅ BookItem {self.barcode} borrowed by {member.name}")
        else:
            print(f"❌ BookItem {self.barcode} is not available.")

    def return_book(self):
        if self.status == BookStatus.LOANED:
            print(f"📚 BookItem {self.barcode} returned.")
            self.status = BookStatus.AVAILABLE
            self.borrowed_by = None
        else:
            print(f"⚠️ BookItem {self.barcode} was not loaned out.")


"""
ACCOUNT CLASSES - LIBRARIAN AND MEMBER
"""


class Account:
    def __init__(self, username: str, password: str, name: str, email: str):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


class Member(Account):
    def __init__(self, username: str, password: str, name: str, email: str):
        super().__init__(username, password, name, email)
        self.borrowed_books: List[BookItem] = []

    def borrow_book(self, item: BookItem):
        if item.status == BookStatus.AVAILABLE:
            item.borrow(self)
            self.borrowed_books.append(item)
        else:
            print(f"❌ BookItem {item.barcode} is not available for borrowing.")

    def return_book(self, item: BookItem):
        if item in self.borrowed_books:
            item.return_book()
            self.borrowed_books.remove(item)
        else:
            print(f"⚠️ BookItem {item.barcode} not borrowed by {self.name}.")


class Librarian(Account):
    def __init__(self, username: str, password: str, name: str, email: str):
        super().__init__(username, password, name, email)

    def add_book(self, book: Book, library: "Library"):
        library.catalog.add_book(book)



"""
LIBRARY and CATALOG 
"""


class Catalog:
    def __init__(self):
        self.books_by_title: Dict[str, List[Book]] = {}

    def add_book(self, book: Book):
        self.books_by_title.setdefault(book.title.lower(), []).append(book)

    def search_by_title(self, title: str) -> List[Book]:
        return self.books_by_title.get(title.lower(), [])


class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.members: Dict[str, Member] = {}

    def add_member(self, member: Member):
        self.members[member.username] = member

    def find_member(self, username: str) -> Member:
        return self.members.get(username)



if __name__ == "__main__":
    # Create a book and add a copy
    book = Book("Sapiens", "Yuval Harari", "History", "Penguin")
    copy1 = BookItem("B001", book, "Rack-1")
    book.add_book_item(copy1)

    # Create library and add catalog entry
    library = Library()
    library.catalog.add_book(book)

    # Create members
    alice = Member("alice123", "pass", "Alice", "alice@example.com")
    bob = Member("bob456", "pass", "Bob", "bob@example.com")

    library.add_member(alice)
    library.add_member(bob)

    # Borrow and return operations
    print("\n--- Alice borrows the book ---")
    alice.borrow_book(copy1)

    print("\n--- Bob tries to borrow the same book ---")
    bob.borrow_book(copy1)

    print("\n--- Alice returns the book ---")
    alice.return_book(copy1)

    print("\n--- Bob borrows it now ---")
    bob.borrow_book(copy1)
