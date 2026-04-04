from main_module import *
from colorama import init, Fore, Back, Style
import random

init(autoreset=True)

player_field = Field()
enemy_field = Field()

player_field.random_placing()
enemy_field.random_placing()

def disp(field) -> None:
        '''
        Печатает поле в консоль
        '''
        print (Fore.CYAN + Style.BRIGHT + '  1 2 3 4 5 6 7 8 9 10')
        letters = 'ABCDEFGHIJ'
        count_letters = 0
        for line in field:
            print (Fore.CYAN + Style.BRIGHT + letters[count_letters], *line)
            count_letters += 1
        

def banner(count):
    print()
    print('==================================================')
    print(f'              МОРСКОЙ БОЙ: ХОД {count}            ')
    print('==================================================')
    disp(player_field.get_grid(False))
    print()
    disp(enemy_field.get_grid(True))

count = 1

while not player_field.is_game_over() or not enemy_field.is_game_over():
    banner(count)
    shot = str(input())
    while enemy_field.validation_coordinate(shot) is False:
         print("Ошибка - неверная координата")
         shot = str(input())
         
    if enemy_field.shot(shot) == SHOT_HIT or enemy_field.shot(shot) == SHOT_KILL:
        banner(count)
        shot = str(input())
        while enemy_field.validation_coordinate(shot) is False:
            print("Ошибка - неверная координата")
            shot = str(input())
         
    coord = random.choice(list(player_field.valid_coordinates))
    player_field.shot(coord)

    count += 1