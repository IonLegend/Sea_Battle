"""Класс конфигурации цветов доски"""
import json
import random

class ColorConfig:
    """Класс создания конфигурации для цветного вывода доски"""
    # ============================================
    # ИНИЦИАЛИЗАЦИЯ
    # ============================================

    def __init__ (self):
        self.color_configuration = {
            "letters": 'RESET',
            "numbers": 'RESET',
            "CLEAR": 'RESET',
            "WAS_BEATEN": 'RESET',
            "HITTED": 'RESET',
            "DESTROYED": 'RESET',
            "SHIP": 'RESET',
        }
        self.colors = ['LIGHTBLACK_EX', 'LIGHTRED_EX', 'LIGHTGREEN_EX', 'LIGHTYELLOW_EX',
                       'LIGHTBLUE_EX', 'LIGHTMAGENTA_EX', 'LIGHTCYAN_EX', 'LIGHTWHITE_EX',
                       'RED', 'GREEN', 'BLUE', 'BLACK', 'WHITE', 'CYAN', 'MAGENTA', 'YELLOW'
                      ]

        self.back_configuration = {
            "letters": 'RESET',
            "numbers": 'RESET',
            "CLEAR": 'RESET',
            "WAS_BEATEN": 'RESET',
            "HITTED": 'RESET',
            "DESTROYED": 'RESET',
            "SHIP": 'RESET',
        }
        self.back_colors = ['LIGHTBLACK_EX', 'LIGHTRED_EX', 'LIGHTGREEN_EX', 'LIGHTYELLOW_EX',
                            'LIGHTBLUE_EX', 'LIGHTMAGENTA_EX', 'LIGHTCYAN_EX', 'LIGHTWHITE_EX',
                            'RED', 'GREEN', 'BLUE', 'BLACK', 'WHITE', 'CYAN', 'MAGENTA', 'YELLOW'
                           ]

        self.style_configuration = {
            "letters": 'NORMAL',
            "numbers": 'NORMAL',
            "CLEAR": 'NORMAL',
            "WAS_BEATEN": 'NORMAL',
            "HITTED": 'NORMAL',
            "DESTROYED": 'NORMAL',
            "SHIP": 'NORMAL',
        }
        self.styles = ['DIM', 'NORMAL', 'BRIGHT']

    # ============================================
    # ВАЛИДАЦИЯ
    # ============================================

    def _valid_data(self, data):
        """Определение, существует ли переменная для цвета"""
        if data in self.color_configuration:
            return True
        return False

    def _valid_style_data(self, data):
        """Определение, существует ли переменная для стиля"""
        if data in self.style_configuration:
            return True
        return False

    # ============================================
    # ЗАПИСЬ В КОНФИГУРАЦИЮ
    # ===========================================

    def write_color(self, data: str, color: str) -> bool:
        """Записывает цвет в параметры:

        "letters"
        "numbers"
        "CLEAR"
        "WAS_BEATEN"
        "HITTED"
        "DESTROYED"
        "SHIP"
        """

        if type(color) is not str:
            return False

        color = color.strip().upper()

        if color in self.colors and self._valid_data(data):
            self.color_configuration[data] = color
            return True
        return False

    def write_back_color(self, data: str, color: str) -> bool:
        """Записывает цвет фона в параметры"""

        if type(color) is not str:
            return False

        color = color.strip().upper()

        if color in self.back_colors and self._valid_data(data):
            self.back_configuration[data] = color
            return True
        return False

    def write_style(self, data: str, style: str) -> bool:
        """Записывает стиль в параметры"""

        if type(style) is not str:
            return False

        style = style.upper()

        if style in self.styles and self._valid_style_data(data):
            self.style_configuration[data] = style
            return True
        return False

    # ============================================
    # ПОЛУЧЕНИЕ ЦВЕТА
    # ============================================

    def get_color(self, data: str) -> str:
        """Возвращает цвет как строку"""
        if self._valid_data(data):
            return self.color_configuration[data]

    def get_back_color(self, data: str) -> str:
        """Возвращает цвет как строку"""
        if self._valid_data(data):
            return self.back_configuration[data]

    def get_style(self, data: str) -> str:
        """Возвращает стиль как строку"""
        if self._valid_style_data(data):
            return self.style_configuration[data]

    # ============================================
    # СОЗДАНИЕ ФАЙЛА
    # ============================================

    def save(self, filename = str(random.randint(1, 10000)) + '_theme'):
        """Сохранение конфигурации цветов в JSON-файл"""
        data = {
            "color_configuration": self.color_configuration,
            "back_configuration": self.back_configuration,
            "style_configuration": self.style_configuration
        }
        json.dump(data, open(filename, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
