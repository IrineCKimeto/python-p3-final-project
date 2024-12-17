import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Librarian, Book, Borrower

DATABASE_URL = "sqlite:///lib.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized.")

# Librarian
def create_librarian():
    name = input("Enter Librarian name: ")
    librarian = Librarian(name=name)
    session.add(librarian)
    session.commit()
    print(f"Librarian '{name}' created with ID {librarian.id}.")

def update_librarian():
    librarian_id = int(input("Enter Librarian ID to update: "))
    librarian = session.get(Librarian, librarian_id)
    if not librarian:
        print("Librarian not found.")
        return
    librarian.name = input(f"Enter new name (current: {librarian.name}): ") or librarian.name
    session.commit()
    print(f"Librarian ID {librarian_id} updated successfully.")

def delete_librarian():
    librarian_id = int(input("Enter Librarian ID to delete: "))
    librarian = session.get(Librarian, librarian_id)
    if not librarian:
        print("Librarian not found.")
        return
    session.delete(librarian)
    session.commit()
    print(f"Librarian ID {librarian_id} deleted.")

def list_librarians():
    librarians = session.query(Librarian).all()
    for librarian in librarians:
        print(librarian)

# Book
def create_book():
    title = input("Enter Book title: ")
    librarian_id = int(input("Enter Librarian ID: "))
    librarian = session.get(Librarian, librarian_id)
    if not librarian:
        print("Librarian not found.")
        return
    book = Book(title=title, librarian_id=librarian_id)
    session.add(book)
    session.commit()
    print(f"Book '{title}' created with ID {book.id} under Librarian '{librarian.name}'.")

def list_books_by_librarian():
    librarian_id = int(input("Enter Librarian ID: "))
    librarian = session.get(Librarian, librarian_id)
    if not librarian:
        print("Librarian not found.")
        return
    for book in librarian.books:
        print(book)

# Borrower
def create_borrower():
    name = input("Enter Borrower name: ")
    borrower = Borrower(name=name)
    session.add(borrower)
    session.commit()
    print(f"Borrower '{name}' created with ID {borrower.id}.")

def borrow_book():
    borrower_id = int(input("Enter Borrower ID: "))
    book_id = int(input("Enter Book ID: "))
    borrower = session.get(Borrower, borrower_id)
    book = session.get(Book, book_id)
    if not borrower or not book:
        print("Invalid Borrower or Book ID.")
        return
    borrower.books.append(book)
    session.commit()
    print(f"Borrower '{borrower.name}' borrowed '{book.title}'.")

def view_borrowers_by_book():
    book_id = int(input("Enter Book ID: "))
    book = session.get(Book, book_id)
    if not book:
        print("Book not found.")
        return
    print(f"Borrowers for Book '{book.title}':")
    for borrower in book.borrowers:
        print(borrower)

def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Create Librarian")
        print("2. Update Librarian")
        print("3. Delete Librarian")
        print("4. List Librarians")
        print("5. Create Book")
        print("6. List Books by Librarian")
        print("7. Create Borrower")
        print("8. Borrow Book")
        print("9. View Borrowers by Book")
        print("10. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_librarian()
        elif choice == "2":
            update_librarian()
        elif choice == "3":
            delete_librarian()
        elif choice == "4":
            list_librarians()
        elif choice == "5":
            create_book()
        elif choice == "6":
            list_books_by_librarian()
        elif choice == "7":
            create_borrower()
        elif choice == "8":
            borrow_book()
        elif choice == "9":
            view_borrowers_by_book()
        elif choice == "10":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
