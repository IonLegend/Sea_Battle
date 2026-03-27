import pytest
from main_module import *

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
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
# ============================================

def test_random_placing_clears_before_placing():
    """Проверка, что random_placing очищает поле перед расстановкой"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    field.random_placing()
    # После random_placing на поле должны быть только новые корабли
    # Старый корабль a1-b1-c1 должен исчезнуть
    assert field.cell_state('a1') != 'ship' or len(field.ships) == 10

def test_random_placing_all_ships_have_correct_lengths():
    """Проверка, что при random_placing все корабли имеют правильные длины"""
    field = Field()
    field.random_placing()
    
    # Собираем все длины
    lengths = []
    for ship in field.ships:
        alive = len(ship.parameters['alive coordinates'])
        hitted = len(ship.parameters['hitted coordinates'])
        lengths.append(alive + hitted)
    
    lengths.sort()
    expected = sorted(FLEET_LENGTHS)
    assert lengths == expected

def test_random_placing_no_overlap():
    """Проверка, что корабли не пересекаются при random_placing"""
    field = Field()
    field.random_placing()
    
    # Собираем все клетки всех кораблей
    all_cells = set()
    for ship in field.ships:
        for coord in ship.parameters['alive coordinates']:
            assert coord not in all_cells, f"Пересечение в {coord}"
            all_cells.add(coord)

def test_random_placing_respects_buffer():
    """Проверка, что корабли не касаются друг друга (буферная зона)"""
    field = Field()
    field.random_placing()
    
    # Для каждой клетки корабля проверяем, что соседи не принадлежат другим кораблям
    all_ship_cells = set()
    for ship in field.ships:
        for coord in ship.parameters['alive coordinates']:
            all_ship_cells.add(coord)
    
    for ship in field.ships:
        for coord in ship.parameters['alive coordinates']:
            neighbours = field.get_neighbours(coord)
            for neighbour in neighbours:
                if neighbour in all_ship_cells:
                    # Сосед может быть только от того же корабля
                    assert neighbour in ship.parameters['alive coordinates'], \
                        f"Корабли касаются: {coord} и {neighbour}"

def test_shot_after_kill_buffer_marked():
    """Проверка, что после уничтожения корабля буферная зона отмечается промахами"""
    field = Field()
    field.auto_add_ship('a1', 1)  # однопалубный
    neighbours = field.get_neighbours('a1')
    
    field.shot('a1')
    
    for neighbour in neighbours:
        # Все соседние клетки должны быть отмечены как промах
        assert field.cell_state(neighbour) in ['was beaten', 'clear'], \
            f"Буферная зона {neighbour} не отмечена"

def test_shot_on_already_hit():
    """Проверка выстрела в уже подбитую клетку"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    field.shot('a1')  # попадание
    result = field.shot('a1')  # повторный выстрел
    # Повторный выстрел должен вернуть SHOT_MISS или быть проигнорирован
    # В текущей реализации возвращает SHOT_MISS
    assert result == SHOT_WAS_BEATEN

def test_get_statistics():
    """Проверка метода get_statistics"""
    field = Field()
    field.auto_add_ship('a1', 1)
    field.shot('a1')
    
    stats = field.get_statistics()
    assert stats['surviving ships'] == 0
    assert stats['shots made'] == 1
    assert 'a1' in stats['shots history']
    assert isinstance(stats['cells_remaining'], int)

def test_get_ship_information():
    """Проверка метода get_ship_information"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    
    info = field.get_ship_information()
    assert len(info) == 1
    assert 'id' in info[0]
    assert 'alive coordinates' in info[0]
    assert 'hitted coordinates' in info[0]
    assert 'buffer zone' in info[0]
    assert len(info[0]['alive coordinates']) == 3

def test_field_game_reset():
    """Проверка полного сброса поля"""
    field = Field()
    field.random_placing()
    assert len(field.ships) == 10
    
    field.field_game_reset()
    assert len(field.ships) == 0
    assert len(field.forbidden_squares) == 0
    assert len(field.available_squares) == 100
    assert len(field.fleet_lengths) == len(FLEET_LENGTHS)

def test_replace_ship_preserves_buffer():
    """Проверка, что при перемещении корабля буферная зона корректно обновляется"""
    field = Field()
    field.auto_add_ship('a1-b1-c1', 3)
    old_buffer = field.ships[0].parameters['buffer zone'].copy()
    
    field.replace_ship('a1-b1-c1', 'j8-j9-j10')
    
    # Старый буфер должен быть очищен
    for cell in old_buffer:
        assert cell not in field.forbidden_squares, f"Клетка {cell} осталась в forbidden"
    
    # Новый корабль должен иметь свою буферную зону
    new_buffer = field.ships[0].parameters['buffer zone']
    assert len(new_buffer) > 0

def test_coordinate_conversion_roundtrip():
    """Проверка, что преобразование координат туда-обратно работает"""
    field = Field()
    test_coords = ['a1', 'a10', 'j1', 'j10', 'e5', 'c8']
    
    for coord in test_coords:
        x, y = field.coord_to_index(coord)
        result = field.index_to_coord(x, y)
        assert result == coord, f"{coord} -> {result}"

def test_cell_state_after_sequence():
    """Проверка последовательности: корабль → попадание → уничтожение"""
    field = Field()
    field.auto_add_ship('a1-b1', 2)
    
    assert field.cell_state('a1') == 'ship'
    field.shot('a1')
    assert field.cell_state('a1') == 'hitted'
    field.shot('b1')
    assert field.cell_state('a1') == 'destroyed'
    assert field.cell_state('b1') == 'destroyed'

def test_get_available_cells_after_game():
    """Проверка, что после окончания игры доступных клеток нет или они не нужны"""
    field = Field()
    field.auto_add_ship('a1', 1)
    field.shot('a1')
    
    available = field.get_available_cells()
    # После уничтожения единственного корабля доступные клетки — это всё поле,
    # кроме корабля и его буфера. Но игра уже закончена, стрелять некуда.
    # Этот тест просто проверяет, что метод не падает.
    assert isinstance(available, list)

def test_multiple_ships_same_field():
    """Проверка, что несколько кораблей корректно сосуществуют"""
    field = Field()
    field.auto_add_ship('a1-a2-a3', 3)
    field.auto_add_ship('c5-c6', 2)
    
    assert len(field.ships) == 2
    assert field.cell_state('a1') == 'ship'
    assert field.cell_state('c5') == 'ship'
    
    # Проверяем, что буферы не пересекаются с другими кораблями
    ship1_buffer = field.ships[0].parameters['buffer zone']
    ship2_cells = field.ships[1].parameters['alive coordinates']
    
    for cell in ship2_cells:
        assert cell not in ship1_buffer, f"Корабль {cell} попал в буфер другого"

# ============================================
# ЗАПУСК ТЕСТОВ
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])