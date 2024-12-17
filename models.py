from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

#Table for Books and Borrowers
book_borrower = Table(
    'book_borrower',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('borrower_id', ForeignKey('borrowers.id'), primary_key=True)
)

class Librarian(Base):
    __tablename__ = 'librarians'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='librarian', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Librarian(id={self.id}, name='{self.name}')"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    librarian_id = Column(Integer, ForeignKey('librarians.id'))
    librarian = relationship('Librarian', back_populates='books')
    borrowers = relationship('Borrower', secondary=book_borrower, back_populates='books')
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', librarian_id={self.librarian_id})"

class Borrower(Base):
    __tablename__ = 'borrowers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', secondary=book_borrower, back_populates='borrowers')
    
    def __repr__(self):
        return f"Borrower(id={self.id}, name='{self.name}')"
