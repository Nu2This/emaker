from EveItem import *


class EvEItemList:
    def __init__(self, materialList: Dict[str, str], materialMapping: Dict[str, List]):
        self.items: Dict[str, EvEItem]
        self.items = {}
        self.mapping = materialMapping

        for key in materialList.keys():
            if key in materialMapping.keys():
                self.items[key] = EvEItem(key, materialList[key], materialMapping[key])
            else:
                self.items[key] = EvEItem(key, materialList[key], [])

    def CalculateAllRawMaterials(self):
        for item in self.items.keys():
            self.CalculateRawMaterials(item)

    def CalculateRawMaterials(self, itemID=None, itemName=None):
        if itemID:
            desiredItem = itemID
        elif itemName:
            for key in self.items.keys():
                if self.items[key].name == itemName:
                    desiredItem = key
                    break

        thisItem = self.items[desiredItem]
        # did we already calculate the materials?
        if thisItem.rawMaterials is not None:
            return thisItem.rawMaterials
        # if not, depth-first search for required materials
        else:
            thisItem.rawMaterials = self.__CalculateRawMaterialsRecursive__(thisItem.ID)
            return thisItem.rawMaterials

    def __CalculateRawMaterialsRecursive__(self, itemID):
        requiredMaterials = {}

        # this is an item with no dependencies
        thisItem = self.items[itemID]
        if len(thisItem.madeFrom) == 0:
            return requiredMaterials
        elif thisItem.rawMaterials is not None:
            return thisItem.rawMaterials
        else:
            for item in self.items[itemID].madeFrom:
                mats = self.__CalculateRawMaterialsRecursive__(item.ID)
                if len(mats) == 0:
                    requiredMaterials[item.ID] = item.quantity
                for mat in mats.keys():
                    if mat in requiredMaterials.keys():
                        requiredMaterials[mat] += mats[mat] * item.quantity
                    else:
                        requiredMaterials[mat] = mats[mat] * item.quantity

        return requiredMaterials
