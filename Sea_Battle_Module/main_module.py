"""Основной модуль библиотеки"""
import random
import json

# ============ КОНСТАНТЫ ==============
# Состояния клеток
CLEAR = ' '
HITTED = 'x'
DESTROYED = 'X'
SHIP = '1'
WAS_BEATEN = '.'
# Результаты выстрелов
SHOT_MISS = 'Blunder'
SHOT_HIT = 'Hit'
SHOT_KILL = 'Target destroyed'
SHOT_WAS_BEATEN = 'Was beaten'
SHOT_ERROR = 'Invalid shot'
# Доступные длины кораблей
FLEET_LENGTHS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

class Field:
    """Класс Игрового поля"""
    # ============================================
    # ИНИЦИАЛИЗАЦИЯ
    # ============================================

    def __init__(self):
        size = 10
        self.grid = [[CLEAR for i in range (size)] for i in range(size)]
        self.columns = {
            '1' : 0,
            '2' : 1,
            '3' : 2,
            '4' : 3,
            '5' : 4,
            '6' : 5,
            '7' : 6,
            '8' : 7,
            '9' : 8,
            '10' : 9,
            }
        self.rows = {
            'a' : 0,
            'b' : 1,
            'c' : 2,
            'd' : 3,
            'e' : 4,
            'f' : 5,
            'g' : 6,
            'h' : 7,
            'i' : 8,
            'j' : 9,
            }
        self.ships_on_field = []
        self.ships = []

        self.valid_coordinates = {f"{rows}{columns}"
                               for rows in 'abcdefghij'
                               for columns in range(1, 11)}

        self.forbidden_squares = set()
        self.available_squares = {f"{rows}{columns}"
                               for rows in 'abcdefghij'
                               for columns in range(1, 11)}
        self.fleet_lengths = FLEET_LENGTHS.copy()
        self.shots_history = []

    # ============================================
    # ОТОБРАЖЕНИЕ
    # ============================================

    def display(self) -> None:
        '''
        Печатает поле в консоль
        '''

        print ('  1 2 3 4 5 6 7 8 9 10')
        letters = 'ABCDEFGHIJ'
        count_letters = 0
        for line in self.grid:
            print (letters[count_letters], *line)
            count_letters += 1

    def display_clear(self) -> None:
        '''
         Печатает доску в консоль (без кораблей)
        '''

        grid_clear = [row[:] for row in self.grid] # Делаем глубокое копирование
        print ('  1 2 3 4 5 6 7 8 9 10')
        letters = 'ABCDEFGHIJ'
        count_letters = 0
        for line in grid_clear:
            for i in range(len(line)):
                if line[i] == SHIP:
                    line[i] = CLEAR
            print (letters[count_letters], *line)
            count_letters += 1

    def field_game_reset(self) -> None:
        '''
        Очищает доску и удаляет все корабли
        '''

        for line in self.grid:
            for i in range(len(line)):
                if line[i] != CLEAR:
                    line[i] = CLEAR
        self.ships.clear()
        self.ships_on_field.clear()
        self.fleet_lengths = FLEET_LENGTHS.copy()
        self.forbidden_squares.clear()
        self.available_squares = self.valid_coordinates.copy()

    # ============================================
    # GET-МЕТОДЫ ДЛЯ ПОЛЯ
    # ============================================

    def get_grid(self, hide_ships: bool) -> list[list[str]]:
        """
        Возвращает копию сетки 10×10.

        Символы в сетке:
            ' ' — пустая клетка
            '1' — живой корабль (если hide_ships=False)
            'x' — попадание (корабль ранен)
            'X' — уничтоженный корабль
            '.' — промах

        Args:
            hide_ships: если True, заменяет '1' на ' '
        """

        if not hide_ships:
            return [row[:] for row in self.grid]

        if hide_ships is True:
            grid_clear = [row[:] for row in self.grid]
            for line in grid_clear:
                for i in range(len(line)):
                    if line[i] == SHIP:
                        line[i] = CLEAR
            return grid_clear

        return []

    def get_ship_information(self) -> list[dict]:
        """ Выводит информацию по всем кораблям """
        information = []
        for ship in self.ships:
            information.append({
                'id': ship.get_id(),
                'alive coordinates': ship.parameters['alive coordinates'],
                'hitted coordinates' : ship.parameters['hitted coordinates'],
                'buffer zone' : ship.parameters['buffer zone']
                })
        return information

    def get_statistics(self) -> dict:
        """ Выводит статистику по всему полю """

        return {
            'surviving ships': len(self.ships),
            'ships length' : self.fleet_lengths,
            'shots made': len(self.shots_history),
            'shots history' : self.get_shots_history(),
            'cells_remaining': len(self.available_squares)
        }

    # ============================================
    #  ВАЛИДАЦИЯ
    # ============================================``

    def _validation_coordinate_log(self, coordinate : str) -> bool:
        """
        Проверяет координату на валидность с подробным выводом ошибок.

        Использует полную проверку: тип, длина, буква, число.
        При ошибке печатает сообщение в консоль.

        Args:
            coordinate (str): Координата в формате 'a1'..'j10'

        Returns:
            bool: True — координата валидна, False — невалидна
        """

        rows_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        columns_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if type(coordinate) is not str:
            print ('Error: Type of coordinate must be string')
            return False

        if len(coordinate) < 2 or len(coordinate) >= 4: # Контроль длины координаты
            print('Error: Invalid coordinate length')
            return False

        if coordinate[0] not in rows_letters:# Проверка правильности ряда
            print('Error: Invalid rows name')
            return False

        try:
            if int(coordinate[1:]) not in columns_numbers: # Проверка правильности столбца
                print('Error: Invalid column number')
                return False
        except ValueError:
            print ('Error: Column must be number')
            return False

        return True

    def validation_coordinate(self, coordinate : str) -> bool:
        """
        Проверяет координату на валидность

        Args:
            coordinate (str): Координата в формате 'a1'..'j10'

        Returns:
            bool: True — координата валидна, False — невалидна
        """
        if type(coordinate) is not str:
            return False

        if coordinate not in self.valid_coordinates:
            return False
        return True

    def _ship_line_validation(self, coordinate_line) -> bool:
        """Валидация поступающей линии из координат

        True - линия валидна

        False - линия невалидна"""
        if type(coordinate_line) is not str:
            return False

        coordinates = coordinate_line.split('-') # Выделили каждую координату

        for cor in coordinates: # Отвалидировали отдельно
            if not self.validation_coordinate(cor):
                return False

        letters = [] # список букв координат
        numbers = [] # списко цифр координат

        for cor in coordinates:
            letters.append(cor[0])
            numbers.append(int(cor[1:]))
        numbers.sort()

        letter_equal = self._letter_equal(letters) # Проверка на равность
        number_equal = self._number_equal(numbers) # Проверка на равность
        letter_in_order = self._letter_in_order(letters) # Проверка на последовательность
        number_in_order = self._number_in_order(numbers) # Проверка на последовательность


        if number_in_order is True and letter_equal is True:
            return True
        if number_equal is True and letter_in_order is True:
            return True
        return False

    # ============================================
    #  ПРОВЕРКА ЛИНИЙ КОРАБЛЯ
    # ============================================

    def _letter_equal(self, letters) -> bool:
        """Проверка, одинаковы ли все буквы"""
        if len(set(letters)) == 1:
            return True
        return False

    def _letter_in_order(self, letters) -> bool:
        """Проверка, стоят ли буквы в последовательности"""
        letters.sort()
        letter_line = 'abcdefghij'
        index = letter_line.find(letters[0])
        list_for_difference = []

        for i in letters:
            try:
                if i == letter_line[index]:
                    list_for_difference.append(1)
                else:
                    list_for_difference.append(0)
                index += 1
            except IndexError:
                break

        if len(set(list_for_difference)) == 1:
            return True
        return False

    def _number_in_order(self, numbers) -> bool:
        """Проверка, одинаковы ли все цифры"""
        number_in_order = True
        for i in range(len(numbers) - 1):
            if numbers[i + 1] != numbers[i] + 1:
                number_in_order = False
                break
            else:
                number_in_order = True
        return number_in_order

    def _number_equal(self, numbers) -> bool:
        """Проверка, стоят ли цифры в последовательности"""
        if len(set(numbers)) == 1:
            return True
        return False

    # ============================================
    #  РАБОТА С КООРДИНАТАМИ
    # ============================================

    def cell_state(self, coordinate: str) -> (str | None):
        """
        Возвращает состояние клетки по её координате.

        Args:
            coordinate (str): Координата в формате 'a1'..'j10'

        Returns:
            Optional[str]: Состояние клетки:
                - 'clear'      — пустая клетка
                - 'ship'       — живой корабль
                - 'hitted'     — попадание (корабль ранен)
                - 'destroyed'  — корабль уничтожен
                - 'was beaten' — промах (клетка обстреляна)
                - None         — координата невалидна

        Examples:
            >>> field = Field()
            >>> field.auto_add_ship('a1-b1-c1', 3)
            >>> field.cell_state('a1')
            'ship'
            >>> field.shot('a1')
            'Hit'
            >>> field.cell_state('a1')
            'hitted'
        """

        if not self.validation_coordinate(coordinate):
            return None

        # Valid Coordinate
        square_data = self.grid[self.rows[coordinate[0]]][self.columns[coordinate[1:]]]

        square_condition = 'clear'

        if square_data == CLEAR:
            return square_condition

        if square_data == HITTED:
            square_condition = 'hitted'
            return square_condition

        if square_data == DESTROYED:
            square_condition = 'destroyed'
            return square_condition

        if square_data == SHIP:
            square_condition = 'ship'
            return square_condition

        if square_data == WAS_BEATEN:
            square_condition = 'was beaten'
            return square_condition

    def coord_to_index(self, coordinate: str) -> tuple[int, int]:
        """
        Преобразует строковую координату в индексы для доступа к grid.

        Args:
            coordinate (str): Координата в формате 'a1'..'j10'

        Returns:

              Tuple[int, int]: (строка, столбец) — оба от 0 до 9
    """

        # coordinate[0] — буква ('a'), ищем её индекс в rows
        x = self.rows[coordinate[0]]  # 'a' → 0
        # coordinate[1:] — число ('1' или '10'), ищем индекс в columns
        y = self.columns[coordinate[1:]]  # '1' → 0
        return x, y

    def index_to_coord(self, x: int, y: int) -> (str | None):
        """
        Преобразует индексы строки и столбца в строковую координату.

        Args:
            x (int): Индекс строки (0..9)
            y (int): Индекс столбца (0..9)

        Returns:
            Optional[str]: Координата в формате 'a1'..'j10',
                      или None если индексы выходят за границы поля"""

        letter = None
        for l, index in self.rows.items():
            if index == x:
                letter = l
                break

        # Ищем число: перебираем columns, где значение равно y
        number = None
        for n, idx in self.columns.items():
            if idx == y:
                number = n
                break

        if letter != None and number != None:
            return letter + number
        return None

    def _write_coordinate(self, coordinate: str, DATA: str) -> bool:
        """Изменение состояния координаты на DATA"""
        if not self.validation_coordinate(coordinate):
            return False
        rows = self.rows[coordinate[0]]
        columns = self.columns[coordinate[1:]]
        self.grid[rows][columns] = DATA
        return True

    def get_neighbours(self, coordinate: str) -> list:
        """Возвращает соседние клетки координаты"""
        return list(self._create_buffer_zone(coordinate))

    def get_available_cells(self) -> list[str]:
        """Возвращает доступные для постановки корабля клетки"""
        return list(self.available_squares)

    def get_valide_cells(self) -> list[str]:
        """Возвращает валидные клетки"""
        return list(self.valid_coordinates)

    def _get_forbidden_squares(self) -> list[str]:
        """Возвращает запрещённые клетки"""
        return list(self.forbidden_squares)

    def _generate_horizontal_coords(self, length: int) -> str:
        """Генерирует случайную горизонтальную линию"""

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        row = random.choice(letters)
        max_start = 11 - length
        start = random.randint(1, max_start)
        coordinate_line = [f"{row}{start + i}" for i in range(length)]

        return '-'.join(coordinate_line)

    def _generate_vertical_coords(self, length: int) -> str:
        """Генерирует случайную вертикальную линию"""

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        max_start = len(letters) - length

        start_letter = random.randint(0, max_start)
        our_number = random.choice(numbers)

        our_letters = letters[start_letter : start_letter + length] # Срез из букв


        coordinate_line = []
        for letter in our_letters:
            coordinate_line.append(letter + str(our_number))

        return '-'.join(coordinate_line)

    # ============================================
    # БУФЕР
    # ============================================

    def _create_buffer_zone(self, coordinate_line: str) -> set:
        """Создает и возвращает координаты буферной зоны для линии"""
        coordinates = coordinate_line.split('-') # Выделили каждую координату
        result_buffer = set()

        for coordinate in coordinates:   
            x = self.coord_to_index(coordinate)[0]
            y = self.coord_to_index(coordinate)[1]

            result_buffer.add(self.index_to_coord(x + 1, y + 1))
            result_buffer.add(self.index_to_coord(x - 1, y - 1))
            result_buffer.add(self.index_to_coord(x + 1, y - 1))
            result_buffer.add(self.index_to_coord(x - 1, y + 1))

            result_buffer.add(self.index_to_coord(x + 1, y))
            result_buffer.add(self.index_to_coord(x - 1, y))
            result_buffer.add(self.index_to_coord(x, y + 1))
            result_buffer.add(self.index_to_coord(x, y - 1))
        
        for result in coordinates: # Удаляем коордианты самого корабля (чтобы потом не было проблем с отображением)
            result_buffer.discard(result) 
        
        result_buffer.discard(None)  # Удалям None из перечня, которые возникли при парсинге
        return result_buffer

    # ============================================
    # РАБОТА С КОРАБЛЯМИ
    # ============================================

    def get_ship_name(self, length: int) -> str:
        """Функция возвращает название корабля"""
        if length == 1:
            ship_name = 'Speedboat'
        elif length == 2:
            ship_name = 'Destroyer'
        elif length == 3:
            ship_name = 'Cruiser'
        elif length == 4:
            ship_name = 'Battleship'
        else:
            ship_name = 'Invalid length'

        return ship_name

    def can_place_ship(self, coordinate_line: str, length: int) -> bool:
        """Проверка, можно ли поставить корабль на указанные координаты"""
        coordinates = coordinate_line.split('-') # Выделили каждую координату

        if length != len(coordinates): # Обработал длину корабля
            return False

        if not self._ship_line_validation(coordinate_line):
            return False

        for coordinate in coordinates:
            if coordinate in self.forbidden_squares: # Проверка на наличие в запрещённом списке
                return False
        return True

    def auto_add_ship(self, coordinate_line: str, length: int) -> bool:
        """
    Добавляет корабль на поле по заданной линии координат.

    Процесс добавления:
        1. Проверяет соответствие длины количеству координат
        2. Проверяет, что такая длина ещё не превысила лимит (через fleet_lengths)
        3. Валидирует линию: прямая, клетки идут подряд, не выходят за границы
        4. Проверяет, что все клетки свободны и не входят в запрещённую зону
        5. Создаёт объект Ship, добавляет координаты
        6. Отмечает клетки корабля на поле (символ SHIP)
        7. Добавляет клетки в forbidden_squares (сам корабль)
        8. Удаляет клетки из available_squares
        9. Создаёт буферную зону вокруг корабля (8 направлений)
        10. Обновляет forbidden_squares и available_squares буферной зоной
        11. Сохраняет корабль в списки ships и ships_on_field
        12. Удаляет длину из fleet_lengths (больше нельзя добавить такой же)

    Args:
        coordinate_line (str): Линия координат через дефис, например 'a1-b1-c1'
        length (int): Длина корабля (должна совпадать с количеством координат)

    Returns:
        bool: True — корабль успешно добавлен, False — ошибка (причина выводится в консоль)

    Examples:
        >>> field = Field()
        >>> field.auto_add_ship('a1-b1-c1', 3)  # трёхпалубный
        True
        >>> field.auto_add_ship('a1-b1-c1', 3)  # повторно нельзя
        False
        >>> field.auto_add_ship('a1-b1', 2)     # двухпалубный в ту же клетку
        False  # клетка a1 уже занята

    Note:
        После успешного добавления длина удаляется из fleet_lengths.
        Это гарантирует, что в игре будет правильное количество кораблей.
        Буферная зона добавляется сразу, чтобы нельзя было ставить корабли вплотную.
    """

        coordinates = coordinate_line.split('-') # Выделили каждую координату

        if length != len(coordinates): # Обработал длину корабля
            # Error: invalid length of coordinate line
            return False

        if length not in self.fleet_lengths:
            return False

        ship = Ship()
        ship_name = self.get_ship_name(length)

        # Привязываем корабль к полю
        ship._set_field(self)
        if not self._ship_line_validation(coordinate_line):
            return False

        added_coordinates = [] # координаты, которые выставлены (чтобы удалить только их, не трогая другое)
        for coordinate in coordinates:

            if coordinate in self.forbidden_squares: # Проверка на наличие в запрещённом списке

                for coord in added_coordinates: # Удаляем все раставленные в этом цикле координаты

                    self._write_coordinate(coord, CLEAR)
                    self.forbidden_squares.remove(coord)
                    self.available_squares.add(coord)
                    ship._delete_coordinate_in_ship(coord)

                return False

            # Добавляем координату в корабль
            result = ship._set_coordinate_in_ship(coordinate)

            if result:
                # Отмечаем корабль на поле (например, ставим '1')
                self._write_coordinate(coordinate, SHIP)

                self.forbidden_squares.add(coordinate) # Добавляем в запрещенные клетки
                self.available_squares.remove(coordinate) # Удаляем из доступных клеток

                added_coordinates.append(coordinate)

        buffer = self._create_buffer_zone(coordinate_line)
        self.forbidden_squares.update(buffer)
        self.available_squares.difference_update(buffer)
        ship.parameters['buffer zone'] = list(buffer)

        # Добавляем в списки корабль с ID
        self.ships_on_field.append((ship.get_id(), ship_name))
        self.ships.append(ship)

        # Удаляем из вакантных длин кораблей во флоте
        self.fleet_lengths.remove(length)

        return True

    def replace_ship(self, coordinate_line_from: str, coordinate_line_to: str) -> bool:
        """Функция перемещает корабль с одной линни координат на другую (если не получилось, не меняет)

        Учитывает длины корбля и сохраняет один ID"""
        coordinate = coordinate_line_from.split('-')
        length = len(coordinate)

        if not self.can_place_ship(coordinate_line_to, length):
            return False

        target_ship = None
        for ship in self.ships:
            if ship.ship_in_coordinate(coordinate[0]):
                target_ship = ship
                break

        if not target_ship:
            return False
        old_id = target_ship.get_id()

        if not self.delete_ship(coordinate_line_from):
            return False

        old_ids = []
        for ship in self.ships:
            old_ids.append(ship.get_id())

        if not self.auto_add_ship(coordinate_line_to, length):
            return False

        for ship in self.ships:
            if ship.get_id() not in old_ids:
                ship.parameters['ID'] = old_id
                # Обновляем ID в ships_on_field
                for i, (sid, name) in enumerate(self.ships_on_field):
                    if sid == ship.get_id():
                        self.ships_on_field[i] = (old_id, name)
                        break
                return True

        return False

    def delete_ship(self, coordinate_line) -> bool:
        """Удаление корабля"""
        coordinate = coordinate_line.split('-')
        length = len(coordinate)
        for ship in self.ships:
            if ship.ship_in_coordinate(coordinate[0]): # Если координата принадлежит кораблю

                ID = ship.get_id()

                for coord in coordinate:
                    self._write_coordinate(coord, CLEAR)
                    self.forbidden_squares.discard(coord)
                    self.available_squares.add(coord)
                for buffer in ship.parameters['buffer zone']:
                    self._write_coordinate(buffer, CLEAR)
                    self.forbidden_squares.discard(buffer)
                    self.available_squares.add(buffer)

                self.ships.remove(ship)
                self._delete_from_ship_list(ID)
                self.fleet_lengths.append(length)
                return True

        return False

    def _delete_from_ship_list(self, ID) -> bool:
        # Удаление корабля из списка ships_on_field
        for i in reversed(range(len(self.ships_on_field))):
            if self.ships_on_field[i][0] == ID:
                self.ships_on_field.pop(i)
                return True
        return False

    def shot(self, coordinate: str) -> str:
        """
        Производит выстрел по указанной координате.

        Args:
            coordinate (str): Координата в формате 'a1'..'j10'

        Returns:
            str: Результат выстрела:
                - SHOT_MISS   — промах
                - SHOT_HIT    — попадание (корабль не уничтожен)
                - SHOT_KILL   — корабль уничтожен
                - SHOT_ERROR  — неверная координата
                - SHOT_WAS_BEATEN - по координате уже стреляли
        """

        if not self.validation_coordinate(coordinate):
            return SHOT_ERROR

        square_condition = self.cell_state(coordinate)

        if square_condition == 'clear':
            self._write_coordinate(coordinate, WAS_BEATEN)
            self.available_squares.discard(coordinate) # Куда стреляли - уже не доступно
            return SHOT_MISS

        elif square_condition == 'ship':

            for ship in self.ships: # Для каждого корабля
                if ship.ship_in_coordinate(coordinate): # Если координата принадлежит кораблю

                    ship._kill_coordinate_in_ship(coordinate)
                    ID = ship.get_id()

                    if ship._is_alive():
                        self._write_coordinate(coordinate, HITTED)
                    else:
                        replace_list = ship.get_died_coordinate()

                        for coord in replace_list:
                            self._write_coordinate(coord, DESTROYED) # Меняем "х" на "Х"

                        for buffer in ship.parameters['buffer zone']: # Отмечаем буфферную зону
                            self._write_coordinate(buffer, WAS_BEATEN)

                        self.ships.remove(ship) # Удаляем из списка кораблей
                        self._delete_from_ship_list(ID) # И из этого тоже
                        self.shots_history.append(coordinate)

                        return SHOT_KILL

            self.shots_history.append(coordinate)

            return SHOT_HIT

        return SHOT_WAS_BEATEN

    def random_placing(self) -> bool:
        """
    Автоматическая расстановка всех кораблей на поле.

    Returns:
        bool: True — все корабли расставлены успешно,
              False — расстановка не удалась (поле очищено)

    Warning:
        Метод может выполняться долго (до 1 секунды) из-за большого числа попыток.
        Если расстановка не удалась, поле очищается — повторный вызов начнёт заново.
    """
        # Сохраняем копию длин
        lengths_to_place = FLEET_LENGTHS.copy()

        # Очищаем поле
        self.field_game_reset()

        for length in lengths_to_place:

            placed = False
            our_strategy = random.choice(['horizontal', 'vertical'])

            for _ in range(500):

                if our_strategy == 'horizontal':

                    coordinate_line = self._generate_horizontal_coords(length)

                    if self.can_place_ship(coordinate_line, length):

                        self.auto_add_ship(coordinate_line, length)
                        placed = True
                        break

                else:
                    coordinate_line = self._generate_vertical_coords(length)

                    if self.can_place_ship(coordinate_line, length):
                        self.auto_add_ship(coordinate_line, length)
                        placed = True
                        break

            if placed is False:
                self.field_game_reset()
                return False
        return True

    def find_from_id(self, id):
        """Возвращает корабль по ID, в случае неудачи - None"""
        for ship in self.ships:
            if id == ship.get_id():
                return ship
        return None

    # ============================================
    # ЛОГИКА ДЛЯ ИГРЫ
    # ============================================

    def is_game_over(self) -> bool:
        """Проверяет конец игры

        False - игра окончена, True - игра продолжается"""
        if len(self.ships) == 0:
            return True
        return False

    def get_shots_history(self) -> list:
        """Возвращает историю выстрелов"""
        return self.shots_history

    def get_remaining_ships_lengths(self) -> list[int]:
        """
        Возвращает длины всех оставшихся (не уничтоженных) кораблей.

        Returns:
            list[int]: Список длин кораблей, например [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        """
        lengths = []
        for ship in self.ships:
            length = len(ship.parameters['alive coordinates']) + len(ship.parameters['hitted coordinates'])
            lengths.append(length)
        return lengths

    # ============================================
    # СОХРАНЕНИЕ В ФАЙЛ
    # ============================================

    def save(self, filename: str) -> bool:
        'Сохраняет доску с кораблями в указанный файл JSON'
        data = {
            'grid' : [row[:] for row in self.grid],
            'ships' : [],
            'ships_on_field' : self.ships_on_field,
            'forbidden_squares' : list(self.forbidden_squares),
            'available_squares' : list(self.available_squares),
            'fleet_lengths' : self.fleet_lengths,
            'shots_history' : self.shots_history
        }

        for ship in self.ships:
            data['ships'].append({
                'id' : ship.get_id(),
                'alive coordinates' : ship.parameters['alive coordinates'],
                'hitted coordinates' : ship.parameters['hitted coordinates'],
                'buffer zone' : ship.parameters['buffer zone']
            })
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            #print(f"✅ Сохранено в {filename}")
            return True
        except Exception:
            return False

    @classmethod

    def load(cls, filename: str):
        'Загружает конфигурацию из файла'
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return None

        field = cls()
        field.grid = [row[:] for row in data['grid']]
        field.forbidden_squares = set(data['forbidden_squares'])
        field.available_squares = set(data['available_squares'])
        field.fleet_lengths = data['fleet_lengths']
        field.shots_history = data['shots_history']

        for ship_data in data['ships']:
            ship = Ship()
            ship.id = ship_data['id']
            ship.parameters['alive coordinates'] = ship_data['alive coordinates']
            ship.parameters['hitted coordinates'] = ship_data['hitted coordinates']
            ship.parameters['buffer zone'] = ship_data['buffer zone']
            ship.parameters['ID'] = ship_data['id']
            ship.parameters['alive'] = len(ship_data['alive coordinates']) > 0
            ship._set_field(field)

            field.ships.append(ship)
        for ship in data['ships_on_field']:
            field.ships_on_field.append(ship)
        return field


class Ship:
    """Класс Корабля"""
    def __init__(self):
        self.id = random.randint(1, 1000)
        self.parameters = {
            'alive coordinates': [],
            'hitted coordinates' : [],
            'alive' : True,
            'ID': self.id,
            'buffer zone' : []
        }
        self.field = None # Ссылка будет дальше в коде

    def _set_field(self, field):
        self.field = field

    def display_parameters(self):
        """ Вывод параметров корабля в консоль"""
        print()
        print(f"КОРАБЛЬ {self.parameters['ID']}")
        squares = self.parameters['alive coordinates']
        print (f"✅ Целые клетки: {', '.join(squares)}")

        hitted_squares = self.parameters['hitted coordinates']
        print (f"💥 Раненые клетки: {', '.join(hitted_squares)}")

        alive = self.parameters['alive']
        print (f"❓ Живой?: {alive}")

        ID = self.parameters['ID']
        print (f"🆔 Уникальный номер: {ID}")

        buffer = self.parameters['buffer zone']
        print (f"📋 Буферная зона: {', '.join(buffer)}")
        print()

        return self.parameters

    def _set_coordinate_in_ship(self, coordinate: str) -> bool:
        """Добавляет координату в корабль"""
        coordinate_validated = self.field.validation_coordinate(coordinate)

        if not coordinate_validated:
            return False

        self.parameters['alive coordinates'].append(coordinate)
        return True

    def _delete_coordinate_in_ship(self, coordinate: str) -> bool:
        """Удаляет координату у корабля"""
        coordinate_validated = self.field.validation_coordinate(coordinate)

        if not coordinate_validated:
            return False
        self.parameters['alive coordinates'].remove(coordinate)
        return True

    def _kill_coordinate_in_ship(self, coordinate:str) -> bool:
        """Перемещает координату в параметрах корабля из живых в мертвые"""
        coordinate_validated = self.field.validation_coordinate(coordinate)

        if not coordinate_validated:
            return False
        self.parameters['hitted coordinates'].append(coordinate)
        self.parameters['alive coordinates'].remove(coordinate)
        return True

    def ship_in_coordinate(self, coordinate: str) -> bool:
        """Проверяет, стоит ли корабль на данной клетке"""
        coordinate_validated = self.field.validation_coordinate(coordinate)
        if not coordinate_validated:
            return False

        if coordinate in self.parameters['alive coordinates']:
            return True
        return False

    # ============================================
    # ЛОГИКА ДЛЯ ИГРЫ
    # ============================================

    def _is_alive(self):
        """Проверка, жив ли корабль"""
        if len(self.parameters['alive coordinates']) == 0:
            return False
        return True

    def get_died_coordinate(self):
        """Возвращает список мёртвых координат корабля"""
        return self.parameters['hitted coordinates']

    def get_id(self):
        """Возвращает ID"""
        return self.parameters['ID']

