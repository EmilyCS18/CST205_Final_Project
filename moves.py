import requests
import urllib.request
import sys
from evolutions import get_tree, sort_evo, find_tree
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


def get_moves(moves: str):
    try:
        url = f"https://pokeapi.co/api/v2/move/{moves}/"
        response = requests.get(url)
        data = response.json()
        return {
            "name": data["name"],
            "type": data["type"]["name"],
            "power": data.get("power"),
            "pp": data.get("pp"),
            "accuracy": data.get("accuracy"),
        }
    except:
        print("Invalid request, try again")

