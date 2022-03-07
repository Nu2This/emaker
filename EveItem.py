from typing import Dict, List


class ItemDependency:
    def __init__(self, ID: str, quantity: int):
        self.ID = ID
        self.quantity = quantity


class EvEItem:
    def __init__(self, ID: str, name: str, materials: List):
        self.ID = ID
        self.name = name
        self.madeFrom = []
        self.rawMaterials = None

        if len(materials) > 0:
            for item in materials:
                self.madeFrom.append(ItemDependency(item[0], int(item[1])))
