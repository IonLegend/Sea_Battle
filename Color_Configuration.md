# 🎨 Полный список API библиотеки ColorConfig

⚠️ **Важно!** Не рекомендуется использовать методы, начинающиеся с `_`. Это может нарушить логику библиотеки.

---

## 🎭 Класс `ColorConfig`

### 🎮 Инициализация

| Метод | Описание |
|-------|----------|
| `ColorConfig()` | Создает новую конфигурацию цветов со значениями по умолчанию (все `RESET`/`NORMAL`) |

### ✅ Валидация

| Метод | Возврат | Описание |
|-------|---------|----------|
| `_valid_data(data)` | `bool` | Проверяет, существует ли указанный параметр для цвета |
| `_valid_style_data(data)` | `bool` | Проверяет, существует ли указанный параметр для стиля |

### ✍️ Запись в конфигурацию

| Метод | Возврат | Описание |
|-------|---------|----------|
| `write_color(data: str, color: str)` | `bool` | Записывает цвет текста для параметра. Доступные параметры: `'letters'`, `'numbers'`, `'CLEAR'`, `'WAS_BEATEN'`, `'HITTED'`, `'DESTROYED'`, `'SHIP'` |
| `write_back_color(data: str, color: str)` | `bool` | Записывает цвет фона для параметра 🖌️ |
| `write_style(data: str, style: str)` | `bool` | Записывает стиль текста для параметра (DIM, NORMAL, BRIGHT) ✨ |

### 📖 Получение цвета

| Метод | Возврат | Описание |
|-------|---------|----------|
| `get_color(data: str)` | `str` | Возвращает цвет текста для указанного параметра 🎨 |
| `get_back_color(data: str)` | `str` | Возвращает цвет фона для указанного параметра 🖍️ |
| `get_style(data: str)` | `str` | Возвращает стиль для указанного параметра 💫 |

### 💾 Создание файла

| Метод | Возврат | Описание |
|-------|---------|----------|
| `save(filename = str(random.randint(1, 10000)) + '_theme')` | `None` | Сохраняет конфигурацию цветов в JSON-файл. Если имя не указано, генерируется случайное (например `1234_theme.json`) 💾 |

---

## 📌 Доступные значения

### 🎨 Цвета (для `write_color` и `write_back_color`)

| Цвет | Описание |
|------|----------|
| `LIGHTBLACK_EX` | Светло-черный (серый) ⚫ |
| `LIGHTRED_EX` | Светло-красный 🔴 |
| `LIGHTGREEN_EX` | Светло-зеленый 🟢 |
| `LIGHTYELLOW_EX` | Светло-желтый 🟡 |
| `LIGHTBLUE_EX` | Светло-синий 🔵 |
| `LIGHTMAGENTA_EX` | Светло-пурпурный 🟣 |
| `LIGHTCYAN_EX` | Светло-голубой 🔷 |
| `LIGHTWHITE_EX` | Светло-белый ⚪ |
| `RED` | Красный 🔴 |
| `GREEN` | Зеленый 🟢 |
| `BLUE` | Синий 🔵 |
| `BLACK` | Черный ⬛ |
| `WHITE` | Белый ⬜ |
| `CYAN` | Голубой 🔷 |
| `MAGENTA` | Пурпурный 🟣 |
| `YELLOW` | Желтый 🟡 |
| `RESET` | Сброс (цвет по умолчанию) ↩️ |

### ✨ Стили (для `write_style`)

| Стиль | Описание |
|-------|----------|
| `DIM` | Тусклый (полупрозрачный) 🌫️ |
| `NORMAL` | Обычный (стандартный) 📄 |
| `BRIGHT` | Яркий ✨ |

### 📋 Доступные параметры (`data`)

| Параметр | Описание |
|----------|----------|
| `'letters'` | Буквы (A-J) 🔤 |
| `'numbers'` | Цифры (1-10) 🔢 |
| `'CLEAR'` | Пустая клетка (вода) 🌊 |
| `'WAS_BEATEN'` | Промах (точка) ⭕ |
| `'HITTED'` | Попадание (x) 💥 |
| `'DESTROYED'` | Уничтоженный корабль (X) 💀 |
| `'SHIP'` | Живой корабль (1) 🚢 |

---

## 📝 Пример использования

```python
# Создание конфигурации
config = ColorConfig() 🎨

# Настройка цветов
config.write_color('letters', 'LIGHTBLUE_EX')     # Буквы — светло-синие 🔵
config.write_color('numbers', 'LIGHTGREEN_EX')    # Цифры — светло-зеленые 🟢
config.write_color('CLEAR', 'CYAN')               # Вода — голубая 💧
config.write_color('SHIP', 'LIGHTWHITE_EX')       # Корабль — белый ⚪
config.write_color('HITTED', 'RED')               # Попадание — красный 💥
config.write_color('DESTROYED', 'LIGHTRED_EX')    # Уничтожен — светло-красный 💀
config.write_color('WAS_BEATEN', 'LIGHTBLACK_EX') # Промах — серый ⭕

# Настройка фона
config.write_back_color('CLEAR', 'BLUE')          # Фон воды — синий 🌊
config.write_back_color('SHIP', 'BLACK')          # Фон корабля — черный 🚢

# Настройка стилей
config.write_style('SHIP', 'BRIGHT')              # Корабль — яркий ✨
config.write_style('HITTED', 'BRIGHT')            # Попадание — яркое 💥
config.write_style('numbers', 'DIM')              # Цифры — тусклые 🌫️

# Получение настроек
ship_color = config.get_color('SHIP')             # Возвращает 'LIGHTWHITE_EX'
ship_style = config.get_style('SHIP')             # Возвращает 'BRIGHT'
water_back = config.get_back_color('CLEAR')       # Возвращает 'BLUE'

# Сохранение в файл
config.save()                                     # Сохранит в случайный файл (например '1234_theme.json')
config.save('ocean_theme.json')                   # Сохранит в 'ocean_theme.json' 💾
```

---

## 🎮 Интеграция с Field

```python
from main_module import Field
from color_config import ColorConfig

# Создаем и настраиваем тему
theme = ColorConfig()
theme.write_color('SHIP', 'LIGHTGREEN_EX')
theme.write_color('HITTED', 'LIGHTRED_EX')
theme.write_color('WAS_BEATEN', 'LIGHTBLACK_EX')
theme.save('battle_theme.json')

# Применяем тему к полю
field = Field()
field.random_placing()

# Отображаем поле с темой
field.custom_display('battle_theme.json', hide_ships=False) 🎯
```

---

## 💡 Советы

- Используйте `RESET` для сброса к стандартным цветам
- Комбинируйте `BRIGHT` с яркими цветами для акцентов
- Для уничтоженных кораблей (`DESTROYED`) используйте красные/темные цвета
- Сохраняйте разные темы в отдельные файлы для переключения между ними
