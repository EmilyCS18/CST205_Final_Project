import requests
import urllib.request
import sys
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
            "moves": moves
        }
    except:
        print("Invalid request, try again")

def url_to_image(sprite_url: str) -> str:
    urllib.request.urlretrieve(sprite_url, "poke.png")
    return "poke.png"

def get_all_berries():
    url = "https://pokeapi.co/api/v2/berry/"
    response = requests.get(url)
    data = response.json()
    return [berry["name"] for berry in data["results"]]

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

class BerryDetailWindow(QWidget):
    def __init__(self, berry_info):
        super().__init__()

        berry_name = QLabel(f"<h1>{berry_info['name']}</h1>")
        berry_name.setStyleSheet("color: black;")
        berry_description = QLabel("Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by Pokémon.")
        berry_description.setStyleSheet("color: black;")
        berry_growth_time = QLabel(f"Growth Time: {berry_info['growth_time']}")
        berry_growth_time.setStyleSheet("color: black;")
        berry_max_harvest = QLabel(f"Max Harvest: {berry_info['max_harvest']}")
        berry_max_harvest.setStyleSheet("color: black;")
        berry_natural_gift_type = QLabel(f"Natural Gift Type: {berry_info['natural_gift_type']}")
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
        for move in result['moves']:
            move_label = QLabel(
                f"Move: {move['name']}\n"
                f"Type: {move['type']}\n"
                f"Power: {move['power']}\n"
                f"PP: {move['pp']}\n"
                f"Accuracy: {move['accuracy']}\n"
            )
            move_label.setStyleSheet("color: black;")
            moves_layout.addWidget(move_label)

        evo_btn = QPushButton('-- Evolutions --')

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
        self.layout.addWidget(evo_btn)

        self.setLayout(self.layout)
        self.show()

        evo_btn.clicked.connect(lambda: self.show_tree(result["name"]))

    @Slot()
    def show_tree(self, name):
        self.evo_win = EvoWindow(name)
        self.evo_win.show()

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
