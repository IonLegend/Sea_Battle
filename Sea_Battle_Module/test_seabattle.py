import pytest
from main_module_restyling import *

# ============================================
# ТЕСТЫ РАССТАНОВКИ
# ============================================

def test_auto_add_ship_valid():
    """Проверка добавления валидного корабля"""
    field = Field()
    result = field.auto_add_ship('a1-b1-c1', 3)
    assert result == True
    assert len(field.ships) == 1
    assert field.cell_state('a1') == 'ship'

def test_auto_add_ship_invalid_line():
    """Проверка добавления невалидной линии (не прямая)"""
    field = Field()
    result = field.auto_add_ship('a1-b2-c3', 3)
    assert result == False
    assert len(field.ships) == 0

def test_auto_add_ship_occupied():
    """Проверка добавления корабля на занятое место"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    result = field.auto_add_ship('a1-a2-a3', 3)
    assert result == False

def test_can_place_ship():
    """Проверка метода can_place_ship"""
    field = Field()
    assert field.can_place_ship('a1-a2-a3', 3) == True
    field.auto_add_ship('a1-a2-a3', 3)
    assert field.can_place_ship('a1-a2-a3', 3) == False

def test_delete_ship():
    """Проверка удаления корабля"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    assert len(field.ships) == 1
    field.delete_ship('a1-b1-c1')
    assert len(field.ships) == 0
    assert field.cell_state('a1') == 'clear'

def test_replace_ship():
    """Проверка перемещения корабля"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    old_id = field.ships[0].get_id()
    result = field.replace_ship('a1-b1-c1', 'j8-j9-j10')
    assert result == True
    assert len(field.ships) == 1
    assert field.ships[0].get_id() == old_id
    assert field.cell_state('a1') == 'clear'
    assert field.cell_state('j8') == 'ship'

# ============================================
# ТЕСТЫ ВЫСТРЕЛОВ
# ============================================

def test_shot_miss():
    """Проверка промаха"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    result = field.shot('a2')
    assert result == SHOT_MISS
    assert field.cell_state('a2') == 'was beaten'

def test_shot_hit():
    """Проверка попадания"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    result = field.shot('a1')
    assert result == SHOT_HIT
    assert field.cell_state('a1') == 'hitted'

def test_shot_kill():
    """Проверка уничтожения корабля"""
    field = Field()
    field.auto_add_ship('a1', 1)  # однопалубный
    result = field.shot('a1')
    assert result == SHOT_KILL
    assert field.cell_state('a1') == 'destroyed'
    assert len(field.ships) == 0
    assert field.is_game_over() == True

def test_shot_invalid():
    """Проверка выстрела по невалидной координате"""
    field = Field()
    result = field.shot('k1')
    assert result == SHOT_ERROR

# ============================================
# ТЕСТЫ АВТОМАТИЧЕСКОЙ РАССТАНОВКИ
# ============================================

def test_random_placing():
    """Проверка автоматической расстановки"""
    field = Field()
    result = field.random_placing()
    assert result == True
    assert len(field.ships) == 10
    
    # Проверяем, что все клетки кораблей отмечены
    ship_cells = []
    for ship in field.ships:
        ship_cells.extend(ship.parameters['alive coordinates'])
    for cell in ship_cells:
        assert field.cell_state(cell) == 'ship'

# ============================================
# ТЕСТЫ GET-МЕТОДОВ
# ============================================

def test_get_remaining_ships_lengths():
    """Проверка получения длин оставшихся кораблей"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    field.auto_add_ship('e4-e5', 2)
    lengths = field.get_remaining_ships_lengths()
    assert 3 in lengths
    assert 2 in lengths
    assert len(lengths) == 2

def test_get_available_cells():
    field = Field()
    field.auto_add_ship('a1', 1)
    available = field.get_available_cells()
    assert 'a1' not in available  # клетка корабля недоступна
    assert 'a2' not in available  # клетка в буферной зоне тоже недоступна
    assert 'b2' not in available  # диагональ тоже в буфере
    assert 'b1' not in available  # соседняя по стороне

def test_get_grid():
    """Проверка получения сетки"""
    field = Field()
    field.auto_add_ship('a1', 1)
    grid = field.get_grid(hide_ships=False)
    assert grid[0][0] == SHIP
    grid_hidden = field.get_grid(hide_ships=True)
    assert grid_hidden[0][0] == CLEAR

# ============================================
# ЗАПУСК ТЕСТОВ
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])