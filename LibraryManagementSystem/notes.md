# Functional Requirements

1. Add a Book to the catalog (multiple copies allowed)
2. Search for books by title, author, subject
3. Borrow a book (if available)
4. eturn a book
5. Reserve a book if all copies are checked out
6. Calculate overdue fines
7. Track multiple copies of the same book
8. Librarian-specific tasks: add/remove books, unblock users
9. Member/User-specific tasks: borrow, return, reserve

# Core Actors

- Librarian (Add/remove books, unblock users)
- User / Member (Search, borrow, return, reserve books)
- System (Handle catalog, inventory, and fines)

# Entities

Book (bookname, author) , BookItem (physical copy), Library, Catalog (search by title/author/topic),
Account (base class for member/librarian), Member, Librarian, Transaction, Reservation
