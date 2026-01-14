import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from cinema_table import *
from movie_table import *
from schedule_table import *

class Main:
    config = ProjectConfig()
    connection = DbConnection(config)
    
    def __init__(self):
        DbTable.dbconn = self.connection
        self.selected_cinema_id = -1
        self.selected_movie_id = -1
    
    def db_init(self):
        ct = CinemaTable()
        mt = MovieTable()
        st = ScheduleTable()
        ct.create()
        mt.create()
        st.create()
    
    def db_insert_sample(self):
        ct = CinemaTable()
        mt = MovieTable()
        st = ScheduleTable()
        
        # Добавляем кинотеатры
        ct.insert_one(["Кинотеатр Победа", "ул. Ленина, 15, Москва"])
        ct.insert_one(["Синема Парк", "ТРЦ Авиапарк, Ходынский бульвар, 4, Москва"])
        ct.insert_one(["Каро 11 Октябрь", "Новоясеневский проспект, 24, Москва"])
        
        # Добавляем фильмы
        mt.insert_one(["Джентльмены", "криминал/комедия", 113, "Великобритания, США", "Miramax", 18])
        mt.insert_one(["Дюна: Часть вторая", "фантастика", 166, "США", "Legendary Pictures", 12])
        mt.insert_one(["Оппенгеймер", "биография/драма", 180, "США, Великобритания", "Universal Pictures", 16])
        
        # Добавляем расписание
        st.insert_one([1, "Зал 1", "2024-12-05 18:00:00", 1, "standard", 450.00])
        st.insert_one([1, "Зал 2", "2024-12-05 20:30:00", 2, "VIP", 800.00])
        st.insert_one([2, "Красный зал", "2024-12-07 19:15:00", 3, "standard", 500.00])
        st.insert_one([3, "Зал 3", "2024-12-10 21:00:00", 1, "standard", 400.00])
    
    def db_drop(self):
        st = ScheduleTable()
        mt = MovieTable()
        ct = CinemaTable()
        st.drop()
        mt.drop()
        ct.drop()
    
    def show_main_menu(self):
        menu = """Добро пожаловать в систему кинотеатров!
Основное меню:
    1 - просмотр кинотеатров;
    2 - просмотр фильмов;
    3 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
    
    def read_next_step(self):
        return input("=> ").strip()
    
    def after_main_menu(self, next_step):
        if next_step == "3":
            self.db_drop()
            self.db_init()
            self.db_insert_sample()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step not in ["1", "2", "9"]:
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        return next_step
    
    def show_cinemas(self):
        self.selected_cinema_id = -1
        print("Список кинотеатров:")
        print("№\tНазвание\tАдрес")
        cinemas = CinemaTable().all()
        for i, cinema in enumerate(cinemas, 1):
            print(f"{i}\t{cinema[1]}\t{cinema[2]}")
        
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    4 - добавление кинотеатра;
    5 - удаление кинотеатра;
    6 - просмотр расписания кинотеатра;
    9 - выход."""
        print(menu)
    
    def show_movies(self):
        self.selected_movie_id = -1
        print("Список фильмов:")
        print("№\tНазвание\tЖанр\tДлит.\tВозраст")
        movies = MovieTable().all()
        for i, movie in enumerate(movies, 1):
            print(f"{i}\t{movie[1]}\t{movie[2]}\t{movie[3]}\t{movie[6]}+")
        
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    7 - добавление фильма;
    8 - удаление фильма;
    9 - просмотр сеансов фильма;
    9 - выход."""
        print(menu)
    
    def after_show_cinemas(self, next_step):
        if next_step == "4":
            self.add_cinema()
            return "1"
        elif next_step == "5":
            self.delete_cinema()
            return "1"
        elif next_step == "6":
            next_step = self.show_cinema_schedule()
        elif next_step not in ["0", "9"]:
            print("Выбрано неверное число! Повторите ввод!")
            return "1"
        return next_step
    
    def after_show_movies(self, next_step):
        if next_step == "7":
            self.add_movie()
            return "2"
        elif next_step == "8":
            self.delete_movie()
            return "2"
        elif next_step == "9":
            next_step = self.show_movie_sessions()
        elif next_step not in ["0", "9"]:
            print("Выбрано неверное число! Повторите ввод!")
            return "2"
        return next_step
    
    def add_cinema(self):
        name = input("Введите название кинотеатра (1 - отмена): ").strip()
        if name == "1":
            return
        while len(name) == 0 or len(name) > 100:
            print("Название не может быть пустым или длиннее 100 символов!")
            name = input("Введите название заново (1 - отмена): ").strip()
            if name == "1":
                return
        
        address = input("Введите адрес (1 - отмена): ").strip()
        if address == "1":
            return
        while len(address) == 0 or len(address) > 255:
            print("Адрес не может быть пустым или длиннее 255 символов!")
            address = input("Введите адрес заново (1 - отмена): ").strip()
            if address == "1":
                return
        
        CinemaTable().insert_one([name, address])
        print("Кинотеатр добавлен!")
    
    def delete_cinema(self):
        try:
            num = int(input("Укажите номер кинотеатра для удаления (0 - отмена): "))
            if num == 0:
                return
            
            cinema = CinemaTable().find_by_position(num)
            if not cinema:
                print("Кинотеатр не найден!")
                return
            
            # Проверка наличия связанных сеансов
            schedules = ScheduleTable().all_by_cinema_id(cinema[0])
            if schedules:
                print(f"Невозможно удалить кинотеатр! С ним связано {len(schedules)} сеансов.")
                choice = input("Удалить все связанные сеансы и кинотеатр? (да/нет): ").lower()
                if choice != 'да':
                    return
            
            CinemaTable().delete_by_id(cinema[0])
            print("Кинотеатр удален!")
        except ValueError:
            print("Введите корректный номер!")
    
    def add_movie(self):
        title = input("Введите название фильма (1 - отмена): ").strip()
        if title == "1":
            return
        while len(title) == 0 or len(title) > 255:
            print("Название не может быть пустым или длиннее 255 символов!")
            title = input("Введите название заново (1 - отмена): ").strip()
            if title == "1":
                return
        
        genre = input("Введите жанр (Enter - пропустить): ").strip()
        if len(genre) > 100:
            print("Жанр слишком длинный! Обрезано до 100 символов.")
            genre = genre[:100]
        
        while True:
            duration = input("Введите продолжительность (минуты, >0): ").strip()
            if duration == "1":
                return
            try:
                dur = int(duration)
                if dur > 0:
                    break
                print("Продолжительность должна быть >0!")
            except ValueError:
                print("Введите целое число!")
        
        country = input("Введите страну (Enter - пропустить): ").strip()
        if len(country) > 100:
            print("Страна слишком длинная! Обрезано до 100 символов.")
            country = country[:100]
        
        studio = input("Введите киностудию (Enter - пропустить): ").strip()
        if len(studio) > 255:
            print("Название студии слишком длинное! Обрезано до 255 символов.")
            studio = studio[:255]
        
        while True:
            min_age = input("Введите минимальный возраст (≥0): ").strip()
            if min_age == "1":
                return
            try:
                age = int(min_age)
                if age >= 0:
                    break
                print("Возраст должен быть ≥0!")
            except ValueError:
                print("Введите целое число!")
        
        MovieTable().insert_one([title, genre, dur, country, studio, age])
        print("Фильм добавлен!")
    
    def delete_movie(self):
        try:
            num = int(input("Укажите номер фильма для удаления (0 - отмена): "))
            if num == 0:
                return
            
            movie = MovieTable().find_by_position(num)
            if not movie:
                print("Фильм не найден!")
                return
            
            # Проверка наличия связанных сеансов
            schedules = ScheduleTable().all_by_movie_id(movie[0])
            if schedules:
                print(f"Невозможно удалить фильм! С ним связано {len(schedules)} сеансов.")
                choice = input("Удалить все связанные сеансы и фильм? (да/нет): ").lower()
                if choice != 'да':
                    return
            
            MovieTable().delete_by_id(movie[0])
            print("Фильм удален!")
        except ValueError:
            print("Введите корректный номер!")
    
    def show_cinema_schedule(self):
        if self.selected_cinema_id == -1:
            while True:
                try:
                    num = int(input("Укажите номер кинотеатра (0 - отмена): "))
                    if num == 0:
                        return "1"
                    
                    cinema = CinemaTable().find_by_position(num)
                    if not cinema:
                        print("Кинотеатр не найден!")
                        continue
                    
                    self.selected_cinema_id = cinema[0]
                    self.selected_cinema = cinema
                    break
                except ValueError:
                    print("Введите число!")
        
        print(f"Расписание кинотеатра: {self.selected_cinema[1]}")
        print("Дата/время\tЗал\tФильм\tЗона\tЦена")
        schedules = ScheduleTable().all_by_cinema_id(self.selected_cinema_id)
        
        if not schedules:
            print("Сеансов нет.")
        else:
            for schedule in schedules:
                movie = MovieTable().find_by_id(schedule[4])
                movie_title = movie[1] if movie else "Неизвестно"
                print(f"{schedule[3]}\t{schedule[2]}\t{movie_title}\t{schedule[5]}\t{schedule[6]}")
        
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат к списку кинотеатров;
    9 - выход."""
        print(menu)
        return self.read_next_step()
    
    def show_movie_sessions(self):
        if self.selected_movie_id == -1:
            while True:
                try:
                    num = int(input("Укажите номер фильма (0 - отмена): "))
                    if num == 0:
                        return "2"
                    
                    movie = MovieTable().find_by_position(num)
                    if not movie:
                        print("Фильм не найден!")
                        continue
                    
                    self.selected_movie_id = movie[0]
                    self.selected_movie = movie
                    break
                except ValueError:
                    print("Введите число!")
        
        print(f"Сеансы фильма: {self.selected_movie[1]}")
        print("Кинотеатр\tДата/время\tЗал\tЗона\tЦена")
        schedules = ScheduleTable().all_by_movie_id(self.selected_movie_id)
        
        if not schedules:
            print("Сеансов нет.")
        else:
            for schedule in schedules:
                cinema = CinemaTable().find_by_id(schedule[1])
                cinema_name = cinema[1] if cinema else "Неизвестно"
                print(f"{cinema_name}\t{schedule[3]}\t{schedule[2]}\t{schedule[5]}\t{schedule[6]}")
        
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    2 - возврат к списку фильмов;
    9 - выход."""
        print(menu)
        return self.read_next_step()
    
    def main_cycle(self):
        current_menu = "0"
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_cinemas()
                next_step = self.read_next_step()
                current_menu = self.after_show_cinemas(next_step)
            elif current_menu == "2":
                self.show_movies()
                next_step = self.read_next_step()
                current_menu = self.after_show_movies(next_step)
        print("До свидания!")

m = Main()
m.main_cycle()