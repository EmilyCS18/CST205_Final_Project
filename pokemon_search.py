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


def get_pokemon(pokemon: str):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"
        response = requests.get(url)
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "sprite": data["sprites"]["front_default"],
        }
    except:
        print("Invalid request, try again")


def url_to_image(spirte_url: str) -> str:
    urllib.request.urlretrieve(spirte_url, "poke.png")
    return "poke.png"


"""
this is the main screen, the first one that opens when you run the program
maybe we adjust this to have a tab window, or a dropdown box that you can select a category from
wouldnt be too hard to use a dropdown, because from there you just take the selected option and 
use that in the url
https://pokeapi.co/api/v2/{category}/{pokemon}/

so if we are searching for a specific pokemon, the user selects "Pokemon" in the drowndown, and types 
the pokemon name into the search bar, if they type "Pikachu" the link should look like:
https://pokeapi.co/api/v2/pokemon/pikachu/
and that info will be used to determine which type of window pops up showing details

if the dropdown selection is "berry" then the berryDetailWindow class should be used

"""


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        background_color = QColor("#ffc4ba")
        self.palette = background_color
        title_label = QLabel("<h1>Pokemon Search</h1>")

        self.search_term = QLineEdit("What pokemon are you curious about?")
        self.search_term.minimum_width = 250
        self.search_term.select_all()

        #Emily Edits
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Pokemon", "Berry"])

        search_btn = QPushButton("Search")

        vbox = QVBoxLayout()
        vbox.add_widget(title_label)
        #Emily Edit
        vbox.addWidget(self.category_dropdown)
        vbox.add_widget(self.search_term)
        vbox.add_widget(search_btn)
        self.set_layout(vbox)
        search_btn.clicked.connect(self.show_results)

    @Slot()
    def show_results(self):
        pokemon = self.search_term.text
        result = get_pokemon(pokemon)
        img_name = url_to_image(result["sprite"])
        self.new_win = NewWindow(pokemon, img_name, result)
        self.new_win.show()


"""
This class below opens a new window for pokemon, maybe we make a separate
class for each possible window that we open? so this class below instead can be called 
something like "pokemonDetailWindow"

and another would be "berryDetailWindow", and would display the appropriate info
found from a query about the berry

"""


class NewWindow(QWidget):
    def __init__(self, pokemon: str, img_name: str, result: dict):
        super().__init__()
        pokemon_name = QLabel(f"<h1>{result["name"]}</h1>")
        pokemon_id = QLabel(f"Pokemon id: {result['id']}")
        pokemon_type = QLabel(f"Pokemon types: {result['types']}")
        pokemon_height = QLabel(f"Pokemon height: {result['height']}")
        pokemon_weight = QLabel(f"Pokemon weight: {result['weight']}")
        img_display = QPixmap(img_name)
        label = QLabel()
        label.pixmap = img_display

        background_color = QColor("#ffc4ba")
        self.palette = background_color

        self.layout = QVBoxLayout()
        self.layout.add_widget(pokemon_name)
        self.layout.add_widget(label)
        self.layout.add_widget(pokemon_id)
        self.layout.add_widget(pokemon_type)
        self.layout.add_widget(pokemon_height)
        self.layout.add_widget(pokemon_weight)
        self.set_layout(self.layout)


app = QApplication([])
my_win = MyWindow()
my_win.show()
sys.exit(app.exec())
