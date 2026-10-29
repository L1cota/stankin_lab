from dataclasses import dataclass, field
from exceptions import BookNotFoundError

@dataclass
class Author:
    name: str

@dataclass
class Publisher:
    name: str

@dataclass
class Category:
    name: str

@dataclass
class Book:
    id: int
    title: str
    author: Author
    publisher: Publisher
    category: Category
    price: float
    quantity: int

    def __str__(self) -> str:
        return (f'{self.id}: {self.title}, {self.author.name}; '
                f'{self.price:.2f} руб., осталось: {self.quantity}')


@dataclass
class Customer:
    name: str


@dataclass
class CartItem:
    book: Book
    quantity: int

    def total(self) -> float:
        return self.book.price * self.quantity


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)

    def add(self, book: Book, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Количество должно быть больше нуля')
        existing = next((i for i in self.items if i.book.id == book.id), None)
        if quantity + (existing.quantity if existing else 0) > book.quantity:
            raise ValueError('Недостаточно книг на складе')
        if existing:
            existing.quantity += quantity
        else:
            self.items.append(CartItem(book, quantity))

    def total(self) -> float:
        return sum(item.total() for item in self.items)

@dataclass
class OrderItem:
    title: str
    price: float
    quantity: int

@dataclass
class Order:
    customer: Customer
    items: list[OrderItem]
    total: float

class BookStore:
    def __init__(self) -> None:
        self.books: list[Book] = []

    def find(self, book_id: int) -> Book:
        for book in self.books:
            if book.id == book_id:
                return book
        raise BookNotFoundError(f'Книга с номером {book_id} не найдена')

    def add(self, book: Book) -> None:
        if any(item.id == book.id for item in self.books):
            raise ValueError('Книга с таким номером уже существует')
        self.books.append(book)

    def delete(self, book_id: int) -> None:
        self.books.remove(self.find(book_id))

    def update(self, book_id: int, price: float, quantity: int) -> None:
        if price < 0 or quantity < 0:
            raise ValueError('Цена и количество не могут быть отрицательными')
        book = self.find(book_id)
        book.price = price
        book.quantity = quantity

    def checkout(self, customer: Customer, cart: Cart) -> Order:
        if not cart.items:
            raise ValueError('Корзина пуста')
        for item in cart.items:
            if not any(book is item.book for book in self.books) or item.quantity > item.book.quantity:
                raise ValueError('Проверьте наличие книг в корзине')
        order = Order(customer, [OrderItem(i.book.title, i.book.price, i.quantity)
                                 for i in cart.items], cart.total())
        for item in cart.items:
            item.book.quantity -= item.quantity
        cart.items.clear()
        return order
