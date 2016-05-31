from model.database import *
from model.simulator import Simulator
from model.crops.storage import Storage
from model.crops.itemsprocessor import ItemsProcessorManager

import pandas as pd
import matplotlib.pylab as plt


if __name__ == '__main__':

    simulator = Simulator()
    database = Database()
    database.init_data()

    simulator.storage = Storage(database)
    simulator.manager = ItemsProcessorManager(database, simulator.storage)

    data = ["Level","MaxChickenHabitats", "MaxCowHabitats",
            "MaxSheepHabitats", "MaxPigHabitats", "MaxGoatHabitats", "MaxFields"]
    data1 = ["Crops", "Mills", "Products", "Animals"]
    nums1 = {}
    h = ""
    sep = ""
    for d in data:
        h += sep + d
        sep = ","
    for d in data1:
        h += sep + d
        sep = ","
    print(h)

    for level in range(1, 100):
        l = str(level)
        h = ""
        sep = ""
        for d in data:
            if d in database.levels[l]:
                h += sep + database.levels[l][d]
            else:
                h += sep + "0"
            sep = ","

        num = 0
        for d in database.fields.items:
            if int(database.fields.items[d]["data"]["UnlockLevel"]) <= level:
                num += 1
        nums1["Crops"] = str(num)

        mills, total_recipes = simulator.get_all_products(level)

        nums1["Products"] = str(total_recipes)

        nums1["Mills"] = str(len(mills["CraftedProducts"]))

        total_animals = 0
        for d in data:
            if "Habitats" in d:
                if d in database.levels[l]:
                    habitat = d.replace("Max", "").replace("Habitats", "Habitat")
                    animals = int(database.levels[l][d]) * int(database.animal_habitats.items[habitat]["data"]["Capacity"])
                    total_animals += animals
        nums1["Animals"] = total_animals

        for d in data1:
            if d in nums1:
                h += sep + str(nums1[d])
            else:
                h += sep + "0"
            sep = ","

        # CSV data print!
        print(h)


    from collections import OrderedDict
    import operator

    print(database.items.items)

    ordered_items = sorted(database.items.items, key=lambda t: int(database.items.items[t]["unlock"]))
    for r in ordered_items:
        if database.items.items[r]["Mill"] in globalNames.listable_products:
            time = "?"
            if "TimeMin" in database.items.items[r]["data"]:
                time = database.items.items[r]["data"]["TimeMin"]
            print(database.items.items[r]["unlock"] + "," + database.items.items[r]["Mill"] + "," + r + "," + time)
