import requests
import urllib.request
import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
)
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Slot
from PySide6.QtCore import Qt
from __feature__ import snake_case, true_property

# file made by Parker Mcanelly

def get_tree(tree: int):
    try:
        url = f"https://pokeapi.co/api/v2/evolution-chain/{tree}/"
        response = requests.get(url)
        data = response.json()
        
        evolutions = []
        
        if not data:
            return evolutions
        
        # baby / base evolution
        evolutions.append(data["chain"]["species"]["name"])
        
        # prints middle evolution(s)
        if not data["chain"]["evolves_to"]:
            return evolutions
        elif 'species' in data["chain"]["evolves_to"][0]:
            for x in data["chain"]["evolves_to"]: 
                evolutions.append(x["species"]["name"])
                
        # prints final evolution(s) 
        if not data["chain"]["evolves_to"][0]["evolves_to"]:
                return evolutions
        else:
            for x in data["chain"]["evolves_to"][0]["evolves_to"]:
                evolutions.append(x["species"]["name"])
        
        # checks for branching evolution(s)
        if len(data["chain"]["evolves_to"]) > 1:
            if not data["chain"]["evolves_to"][1]["evolves_to"]:
                return evolutions
            else:
                for x in data["chain"]["evolves_to"][1]["evolves_to"]:
                    evolutions.append(x["species"]["name"])

        return evolutions

    except:
        print("Invalid request, try again")
        
def sort_evo(list):
    # print(list)
    if not list:
        print('Record is Empty')
        return 'Record is Empty'
    if len(list) == 1:
        print(f'{list[0]} doesnt have any evolutions')
        str = (f'{list[0]} doesnt have any evolutions')
        return str
    if len(list) == 2:
        print(f'{list[0]} has one evolution, it evolves into {list[1]}')
        str = (f'{list[0]} has one evolution, it evolves into {list[1]}')
        return str
    if len(list) == 3:
        print(f'{list[0]} evolves into {list[1]}, and then {list[1]} evolves into {list[2]}')
        str = (f'{list[0]} evolves into {list[1]}, and then {list[1]} evolves into {list[2]}')
        return str
    if len(list) == 4:
        print(f'{list[0]} evolves into {list[1]}, and {list[1]} can evolve intpytho {list[2]} or {list[3]}')
        str = (f'{list[0]} evolves into {list[1]}, and {list[1]} can evolve into {list[2]} or {list[3]}')
        return str
    if len(list) == 5:
        print(f'{list[0]} evolves into {list[1]} or {list[2]}, and {list[1]} evolves into {list[3]} while {list[2]} evolves into {list[4]}')
        str = (f'{list[0]} evolves into {list[1]} or {list[2]}, and {list[1]} evolves into {list[3]} while {list[2]} evolves into {list[4]}')
        return str   
    if len(list) > 5:
        print('Eevee-lutions:')
        print(f'{list[0]} has {len(list)-1} possible evolutions')
        str = (f'{list[0]} has {len(list)-1} possible evolutions')
        return 
    return


def find_tree(pokemon: str):
    max = 550 # total 549 tree IDs
    for x in range(1, max):
        tmp = get_tree(x)
        if not tmp: # error check
            continue
        for el in tmp:
            if el == pokemon:
                return x
        if x%20 == 0:
            print(x)
        tmp.clear()
        
    return

def grab_sprite(pokemon: str):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"
        response = requests.get(url)
        data = response.json()
        return data["sprites"]["front_default"]

    except:
        return
    

