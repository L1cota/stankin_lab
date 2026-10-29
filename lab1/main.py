from pathlib import Path

from exceptions import StoreError
from models import BookStore, Cart, Customer
from storage import JsonStorage, XmlStorage, book_from_dict

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / 'catalog.json'


def save_catalog(store: BookStore) -> None:
    JsonStorage().save(store, str(CATALOG_PATH))
    print(f'Каталог сохранён: {CATALOG_PATH}')


def file_path(text: str, fmt: str) -> Path:
    path = Path(text.strip().strip('"') or f'books.{fmt}')
    return path if path.is_absolute() else BASE_DIR / path


def read_book() -> dict:
    return {'id': input('Номер: '), 'title': input('Название: '),
            'author': input('Автор: '), 'publisher': input('Издательство: '),
            'category': input('Категория: '), 'price': input('Цена: '),
            'quantity': input('Количество: ')}


def main() -> None:
    store = BookStore()
    cart = Cart()
    if CATALOG_PATH.exists():
        try:
            store = JsonStorage().load(str(CATALOG_PATH))
            print(f'Загружен сохранённый каталог: {len(store.books)} книг.')
        except (StoreError, OSError) as error:
            print(f'Не удалось загрузить каталог: {error}')
            print('Исправьте файл catalog.json или загрузите другой файл через меню.')
            return
    else:
        print('Новый каталог пуст. Добавьте книгу или загрузите пример books.json.')
    while True:
        print('\n1. Показать книги  2. Добавить  3. Изменить цену и остаток')
        print('4. Удалить  5. Добавить в корзину  6. Оформить заказ')
        print('7. Загрузить файл  8. Сохранить файл  0. Выход')
        try:
            choice = input('Выберите действие: ').strip()
            if choice == '0':
                break
            if choice == '1':
                if not store.books:
                    print('Каталог пуст')
                for book in store.books:
                    print(book)
            elif choice == '2':
                store.add(book_from_dict(read_book()))
                print('Книга добавлена')
                save_catalog(store)
            elif choice == '3':
                book_id = int(input('Номер книги: '))
                # Повторно проверяем число так же, как и при загрузке файла.
                old = store.find(book_id)
                data = {'id': old.id, 'title': old.title, 'author': old.author.name,
                        'publisher': old.publisher.name, 'category': old.category.name,
                        'price': input('Новая цена: '), 'quantity': input('Новый остаток: ')}
                updated = book_from_dict(data)
                store.update(book_id, updated.price, updated.quantity)
                print('Данные изменены')
                save_catalog(store)
            elif choice == '4':
                store.delete(int(input('Номер книги: ')))
                print('Книга удалена')
                save_catalog(store)
            elif choice == '5':
                book = store.find(int(input('Номер книги: ')))
                cart.add(book, int(input('Количество: ')))
                print(f'Сумма корзины: {cart.total():.2f} руб.')
            elif choice == '6':
                name = input('Имя покупателя: ').strip()
                if not name:
                    raise ValueError('Имя не может быть пустым')
                order = store.checkout(Customer(name), cart)
                print(f'Заказ для {order.customer.name}: {order.total:.2f} руб.')
                for item in order.items:
                    print(f'{item.title}: {item.quantity} шт. по {item.price:.2f} руб.')
                save_catalog(store)
            elif choice in ('7', '8'):
                fmt = input('Формат (json/xml): ').strip().lower()
                if fmt not in ('json', 'xml'):
                    raise ValueError('Выберите json или xml')
                path = file_path(input(f'Имя или путь (Enter: books.{fmt}): '), fmt)
                storage = JsonStorage() if fmt == 'json' else XmlStorage()
                if choice == '7':
                    store = storage.load(str(path))
                    cart = Cart()  # Корзина относится к прежнему каталогу.
                    print(f'Каталог загружен: {len(store.books)} книг из {path}')
                    save_catalog(store)
                else:
                    storage.save(store, str(path))
                    print(f'Каталог сохранён: {path}')
            else:
                print('Нет такого пункта меню')
        except (StoreError, ValueError, OSError) as error:
            print(f'Ошибка: {error}')
        except EOFError:
            print('\nВвод завершён')
            break


if __name__ == '__main__':
    main()
