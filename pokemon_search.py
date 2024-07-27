import requests
import urllib.request
import sys
import random
from evolutions import get_tree, sort_evo, find_tree
from moves import get_moves
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
)
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Slot, Qt

"""
Title: Pokemon Info Search
Description: A python program that utilizes PokeAPI to allow a user to search for different
things and see relevant information based on what they searched for
Authors: Emily Contreras, Parker Mcanelly, Miguel Gonzalez, Claire Longsworth
Date: 07/26/2024
Class: CST205 Multimedia and Design

"""


"""
This function is what is searching for the pokemon using the API, and selecting
which information is relevant to our program that we want to display. 
Parameter: The name of the pokemon the user is searching for

Done by: Claire Longsworth
"""


def get_pokemon(pokemon: str):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"
        response = requests.get(url)
        data = response.json()
        moves = [get_moves(move["move"]["name"]) for move in data["moves"][:2]]
        return {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "sprite": data["sprites"]["front_default"],
            "moves": moves,
        }
    except:
        print("Invalid request, try again")


"""
Functions the same as the get_pokemon function, uses API calls to 
receive desired information about a pokemon, however this uses pokemon ID rather than name
Parameter: The name of the pokemon the user is searching for

Done by: Claire Longsworth
"""


def get_pokemon_by_id(pokemon_id: int):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
        response = requests.get(url)
        data = response.json()
        moves = [get_moves(move["move"]["name"]) for move in data["moves"][:2]]
        return {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "sprite": data["sprites"]["front_default"],
            "moves": moves,
        }
    except:
        print("Invalid request, try again")


"""
Random Pokemon generating function that is shown in the home page 
Done by: Emily Contreras
"""


def get_random_pokemon():
    max_pokemon_id = 898  # Total number of Pokémon in the PokeAPI
    random_id = random.randint(1, max_pokemon_id)
    return get_pokemon_by_id(random_id)


"""
This function allows us to take a link of an image and create
and image with that link
Param: url to image
Returns: name of image created

Done by: Claire Longsworth
"""


def url_to_image(sprite_url: str) -> str:
    urllib.request.urlretrieve(sprite_url, "poke.png")
    return "poke.png"


"""
Creates a list of all berries in pokemon using pokeAPI
Returns: a list of all berries

Done by: Emily Contreras
"""


def get_all_berries():
    url = "https://pokeapi.co/api/v2/berry/"
    response = requests.get(url)
    data = response.json()
    return [berry["name"] for berry in data["results"]]


"""
A function that searches for a berry given its name
param: the name of the berry to search for
returns: dictionary of berry info

Done by: Emily Contreras
"""


def get_berry(berry_name):
    url = f"https://pokeapi.co/api/v2/berry/{berry_name}/"
    response = requests.get(url)
    data = response.json()
    berry_info = {
        "name": data["name"],
        "growth_time": data["growth_time"],
        "max_harvest": data["max_harvest"],
        "natural_gift_type": data["natural_gift_type"]["name"],
        "size": data["size"],
        "smoothness": data["smoothness"],
        "soil_dryness": data["soil_dryness"],
    }
    return berry_info


"""
Main QtWindow of application, generates a random pokemon sprite to display the user,
and gives a textbox prompt for them to enter the pokemon they are searching for.
Also allows the user to search for information on berries by giving them a dropdown 
menu option of what berry they want info on, once selected, a new window opens and shows 
the info about chosen berry.

- random pokemon made by Emily Contreras
- textbox prompt made by Claire Longsworth 
- berry dropdown & berry stuff made by Emily Contreras
- evolution button made by Parker Mcanelly 
"""


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        background_color = QColor("#ffc4ba")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        title_label = QLabel("<h1>Pokemon Search</h1>")
        title_label.setStyleSheet("color: black;")

        self.search_term = QLineEdit("What pokemon are you curious about?")
        self.search_term.setMinimumWidth(250)
        self.search_term.selectAll()

        search_btn = QPushButton("Search")

        # Add a dropdown for berries
        self.berry_dropdown = QComboBox()
        self.berry_dropdown.addItem("Select a Berry")
        berries = get_all_berries()
        self.berry_dropdown.addItems(berries)

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(self.search_term)
        vbox.addWidget(search_btn)
        vbox.addWidget(self.berry_dropdown)  # Add the dropdown to the layout

        self.setLayout(vbox)

        search_btn.clicked.connect(self.show_results)
        self.berry_dropdown.currentIndexChanged.connect(self.show_berry_details)

        self.show_random_pokemon()

    @Slot()
    def show_results(self):
        pokemon = self.search_term.text()
        result = get_pokemon(pokemon)
        img_name = url_to_image(result["sprite"])
        self.new_win = NewWindow(pokemon, img_name, result)
        self.new_win.show()

    @Slot()
    def show_berry_details(self):
        selected_berry = self.berry_dropdown.currentText()
        if selected_berry != "Select a Berry":
            berry_info = get_berry(selected_berry)
            self.berry_win = BerryDetailWindow(berry_info)
            self.berry_win.show()

    def show_random_pokemon(self):
        result = get_random_pokemon()
        img_name = url_to_image(result["sprite"])
        pixmap = QPixmap(img_name)
        pixmap = pixmap.scaled(
            200, 200, Qt.KeepAspectRatio
        )  # Scale the image to make it larger
        label = QLabel()
        label.setPixmap(pixmap)
        self.layout().insertWidget(1, label)  # Insert the image below the title label


class BerryDetailWindow(QWidget):
    def __init__(self, berry_info):
        super().__init__()

        berry_name = QLabel(f"<h1>{berry_info['name']}</h1>")
        berry_name.setStyleSheet("color: black;")
        berry_description = QLabel(
            "Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by Pokémon."
        )
        berry_description.setStyleSheet("color: black;")
        berry_growth_time = QLabel(f"Growth Time: {berry_info['growth_time']}")
        berry_growth_time.setStyleSheet("color: black;")
        berry_max_harvest = QLabel(f"Max Harvest: {berry_info['max_harvest']}")
        berry_max_harvest.setStyleSheet("color: black;")
        berry_natural_gift_type = QLabel(
            f"Natural Gift Type: {berry_info['natural_gift_type']}"
        )
        berry_natural_gift_type.setStyleSheet("color: black;")
        berry_size = QLabel(f"Size: {berry_info['size']}")
        berry_size.setStyleSheet("color: black;")
        berry_smoothness = QLabel(f"Smoothness: {berry_info['smoothness']}")
        berry_smoothness.setStyleSheet("color: black;")
        berry_soil_dryness = QLabel(f"Soil Dryness: {berry_info['soil_dryness']}")
        berry_soil_dryness.setStyleSheet("color: black;")

        background_color = QColor("#ffc4ba")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.addWidget(berry_name)
        self.layout.addWidget(berry_description)
        self.layout.addWidget(berry_growth_time)
        self.layout.addWidget(berry_max_harvest)
        self.layout.addWidget(berry_natural_gift_type)
        self.layout.addWidget(berry_size)
        self.layout.addWidget(berry_smoothness)
        self.layout.addWidget(berry_soil_dryness)
        self.setLayout(self.layout)


class NewWindow(QWidget):
    def __init__(self, pokemon: str, img_name: str, result: dict):
        super().__init__()
        pokemon_name = QLabel(f"<h1>{result['name']}</h1>")
        pokemon_name.setStyleSheet("color: black;")
        pokemon_id = QLabel(f"Pokemon id: {result['id']}")
        pokemon_id.setStyleSheet("color: black;")
        pokemon_type = QLabel(f"Pokemon types: {', '.join(result['types'])}")
        pokemon_type.setStyleSheet("color: black;")
        pokemon_height = QLabel(f"Pokemon height: {result['height']}")
        pokemon_height.setStyleSheet("color: black;")
        pokemon_weight = QLabel(f"Pokemon weight: {result['weight']}")
        pokemon_weight.setStyleSheet("color: black;")
        img_display = QPixmap(img_name)
        label = QLabel()
        label.setPixmap(img_display)

        # Moves added
        moves_layout = QVBoxLayout()
        for move in result["moves"]:
            move_label = QLabel(
                f"Move: {move['name']}\n"
                f"Type: {move['type']}\n"
                f"Power: {move['power']}\n"
                f"PP: {move['pp']}\n"
                f"Accuracy: {move['accuracy']}\n"
            )
            move_label.setStyleSheet("color: black;")
            moves_layout.addWidget(move_label)

        # added
        evo_btn = QPushButton("-- Evolutions --")

        background_color = QColor("#ffc4ba")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.addWidget(pokemon_name)
        self.layout.addWidget(label)
        self.layout.addWidget(pokemon_id)
        self.layout.addWidget(pokemon_type)
        self.layout.addWidget(pokemon_height)
        self.layout.addWidget(pokemon_weight)
        # Moves
        self.layout.addLayout(moves_layout)
        # added
        self.layout.addWidget(evo_btn)

        self.setLayout(self.layout)
        self.show()

        # added
        evo_btn.clicked.connect(lambda: self.show_tree(result["name"]))

    # added
    @Slot()
    def show_tree(self, name):
        self.evo_win = EvoWindow(name)
        self.evo_win.show()


# added
class EvoWindow(QWidget):
    def __init__(self, pokemon: str):
        super().__init__()
        treeID = find_tree(pokemon)
        evo_names = get_tree(treeID)
        evoLabel = QLabel(sort_evo(evo_names))
        evoLabel.setStyleSheet("color: black;")

        background_color = QColor("#ffc4ba")
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.addWidget(evoLabel)
        self.setLayout(self.layout)


app = QApplication([])
my_win = MyWindow()
my_win.show()
sys.exit(app.exec())
