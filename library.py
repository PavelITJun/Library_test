import json
import os

DATA_FILE = 'data.json'

class Book:
    """
    Класс для представления книги в библиотеке.

    Attributes:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги (в наличии/выдана).
    """

    def __init__(self, id: int, title: str, author: str, year: int, status='в наличии'):
        """
        Инициализирует новую книгу.

        Args:
            id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str, optional): Статус книги. По умолчанию - 'в наличии'.
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """
        Возвращает словарь, представляющий книгу.

        Returns:
            dict: Словарь, представляющий книгу.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

class Services:
    """
    Класс для обслуживания данных библиотеки.

    Attributes:
        data_file (str): Путь к файлу с данными библиотеки.
    """

    def __init__(self, data_file: str):
        """
        Инициализирует новые обслуживающие данные.

        Args:
            data_file (str): Путь к файлу с данными библиотеки.
        """
        self.data_file = data_file

    def load_data(self):
        """
        Загружает данные из файла и преобразует их в объекты Book.

        Returns:
            list: Список объектов Book.
        """
        if not os.path.exists(self.data_file) or os.stat(self.data_file).st_size == 0:
            print("Файл data.json не существует или пуст")
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        except json.JSONDecodeError:
            print("Файл data.json повреждён")
            return []

    def save_data(self, books):
        """
        Преобразует объекты Book обратно в словари и сохраняет их в файл в формате JSON.

        Args:
            books (list): Список объектов Book.
        """
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in books], file, indent=4, ensure_ascii=False)

class Library:
    """
    Класс для представления библиотеки.

    Attributes:
        data_file (str): Путь к файлу с данными библиотеки.
        services (Services): Объект класса Services для обслуживания данных библиотеки.
        books (list): Список объектов Book в библиотеке.
    """

    def __init__(self, data_file: str):
        """
        Инициализирует новую библиотеку.

        Args:
            data_file (str): Путь к файлу с данными библиотеки.
        """
        self.services = Services(data_file)
        self.books = self.services.load_data()

    def generate_id(self):
        """
        Возвращает новый уникальный идентификатор для книги.

        Returns:
            int: Новый уникальный идентификатор для книги.
        """
        return max([book.id for book in self.books], default=0) + 1

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        new_book = Book(self.generate_id(), title, author, year)
        self.books.append(new_book)
        self.services.save_data(self.books)
        print(f"Книга '{title}' добавлена с ID {new_book.id}.")

    def delete_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки.

        Args:
            book_id (int): Уникальный идентификатор книги.
        """
        book_exists = any(book.id == book_id for book in self.books)
        if not book_exists:
            print(f"Книга с ID {book_id} не найдена.")
            return
        self.books = [book for book in self.books if book.id != book_id]
        self.services.save_data(self.books)
        print(f"Книга с ID {book_id} удалена.")

    def search_books(self, query: str, field: str):
        """
        Ищет книги в библиотеке по указанному полю и запросу.

        Args:
            query (str): Запрос для поиска.
            field (str): Поле для поиска. Должно быть одним из 'title', 'author', 'year'.
        """
        results = [book for book in self.books if query.lower() in getattr(book, field).lower()]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print(f"Книги по запросу '{query}' не найдены.")

    def display_books(self):
        """
        Отображает все книги в библиотеке.
        """
        if self.books:
            for book in self.books:
                print(book.to_dict())
        else:
            print("В библиотеке нет книг.")

    def change_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги в библиотеке.

        Args:
            book_id (int): Уникальный идентификатор книги.
            new_status (str): Новый статус книги. Должен быть одним из 'в наличии', 'выдана'.
        """
        if new_status not in ['в наличии', 'выдана']:
            print("Некорректный статус. Доступные статусы: 'в наличии', 'выдана'.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.services.save_data(self.books)
                print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")

def main():
    library = Library(DATA_FILE)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите название книги: ")
            if any(book.title.encode('utf-8').decode('utf-8') == title for book in library.books):
                print(f"Книга с названием '{title}' уже существует.")
                title = input("Введите название книги ещё раз: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            if not year.isdigit():
                year = input("Год должен быть числом!\nВведите год издания ещё раз: ")
            library.add_book(title, author, int(year))
        elif choice == '2':
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == '3':
            field = input("Введите поле для поиска из (title/author/year): ").strip().lower()
            #Так как мы отображем ID при добавлении книги, считаю, что было бы хорошо добавить поиск и по ID
            if field in ['title', 'author', 'year']:
                query = input(f"Введите {field}: ").strip()
                library.search_books(query, field)
            else:
                print("Некорректное поле для поиска.")
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
                #Мне кажется, логичнее не спрашивать какой статус хочет установить пользователь, так как вариант всего 1)
                new_status = input("Введите новый статус (в наличии/выдана): ").strip().lower()
                library.change_status(book_id, new_status)
            except ValueError:
                print("Некорректный ID.")
        elif choice == '6':
            break
        else:
            print("Выберите цифру от 1 до 6")

if __name__ == "__main__":
    main()
