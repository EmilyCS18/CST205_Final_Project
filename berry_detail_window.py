import requests
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Slot


def get_berry(berry: str):
    try:
        url = f"https://pokeapi.co/api/v2/berry/{berry}/"
        response = requests.get(url)
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "growth_time": data["growth_time"],
            "max_harvest": data["max_harvest"],
            "natural_gift_power": data["natural_gift_power"],
            "size": data["size"],
            "smoothness": data["smoothness"],
            "soil_dryness": data["soil_dryness"],
        }
    except:
        print("Invalid request, try again")


class BerryDetailWindow(QWidget):
    def __init__(self, berry: str):
        super().__init__()
        berry_info = get_berry(berry)
        berry_name = QLabel(f"<h1>{berry_info['name']}</h1>")
        berry_id = QLabel(f"Berry id: {berry_info['id']}")
        growth_time = QLabel(f"Growth time: {berry_info['growth_time']}")
        max_harvest = QLabel(f"Max harvest: {berry_info['max_harvest']}")
        gift_power = QLabel(f"Natural gift power: {berry_info['natural_gift_power']}")
        size = QLabel(f"Size: {berry_info['size']}")
        smoothness = QLabel(f"Smoothness: {berry_info['smoothness']}")
        soil_dryness = QLabel(f"Soil dryness: {berry_info['soil_dryness']}")

        description = QLabel(
            "Berries are small fruits that can provide HP and status condition restoration, "
            "stat enhancement, and even damage negation when eaten by Pokémon. "
            "Check out Bulbapedia for greater detail."
        )

        background_color = QColor("#ffc4ba")
        self.setPalette(background_color)

        self.layout = QVBoxLayout()
        self.layout.addWidget(berry_name)
        self.layout.addWidget(berry_id)
        self.layout.addWidget(growth_time)
        self.layout.addWidget(max_harvest)
        self.layout.addWidget(gift_power)
        self.layout.addWidget(size)
        self.layout.addWidget(smoothness)
        self.layout.addWidget(soil_dryness)
        self.layout.addWidget(description)
        self.setLayout(self.layout)
