import json
import math
import xml.etree.ElementTree as ET
from exceptions import DataError
from models import Author, Book, BookStore, Category, Publisher

def book_to_dict(book: Book) -> dict:
    return {'id': book.id, 'title': book.title, 'author': book.author.name,
            'publisher': book.publisher.name, 'category': book.category.name,
            'price': book.price, 'quantity': book.quantity}

def book_from_dict(data: dict) -> Book:
    try:
        book_id = int(data['id'])
        title = str(data['title']).strip()
        author = str(data['author']).strip()
        publisher = str(data['publisher']).strip()
        category = str(data['category']).strip()
        price = float(data['price'])
        quantity = int(data['quantity'])
        if (book_id <= 0 or not all((title, author, publisher, category))
                or not math.isfinite(price) or price < 0 or quantity < 0):
            raise ValueError
        return Book(book_id, title, Author(author), Publisher(publisher),
                    Category(category), price, quantity)
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        raise DataError('Некорректные данные книги') from error

class JsonStorage:
    def save(self, store: BookStore, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump({'books': [book_to_dict(book) for book in store.books]},
                      file, ensure_ascii=False, indent=4)

    def load(self, path: str) -> BookStore:
        try:
            with open(path, encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get('books'), list):
                raise DataError('Ожидался список книг')
            store = BookStore()
            for item in data['books']:
                if not isinstance(item, dict):
                    raise DataError('Некорректные данные книги')
                store.add(book_from_dict(item))
            return store
        except (json.JSONDecodeError, UnicodeError, ValueError) as error:
            raise DataError('Ошибка в JSON-файле') from error

class XmlStorage:
    def save(self, store: BookStore, path: str) -> None:
        root = ET.Element('bookstore')
        for book in store.books:
            element = ET.SubElement(root, 'book')
            for key, value in book_to_dict(book).items():
                ET.SubElement(element, key).text = str(value)
        tree = ET.ElementTree(root)
        ET.indent(tree, space='    ')
        tree.write(path, encoding='utf-8', xml_declaration=True)

    def load(self, path: str) -> BookStore:
        try:
            root = ET.parse(path).getroot()
            if root.tag != 'bookstore' or any(child.tag != 'book' for child in root):
                raise DataError('Неверная структура XML')
            store = BookStore()
            for element in root:
                store.add(book_from_dict({child.tag: child.text or '' for child in element}))
            return store
        except (ET.ParseError, UnicodeError, ValueError) as error:
            raise DataError('Ошибка в XML-файле') from error
