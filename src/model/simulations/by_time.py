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

    data = {}
    data["time"] = []
    data["level"] = []

    print("Fielding")

    time = 0

    simulator.storage.add("Corn")
    simulator.storage.add("Corn")
    simulator.storage.add("Corn")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Soybean")
    simulator.storage.add("Soybean")
    simulator.storage.add("Soybean")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Carrot")
    simulator.storage.add("Carrot")
    simulator.storage.add("Carrot")

    #simulator.storage.add("Chicken Food")
    #simulator.storage.add("Cow Food")

    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")

    #simulator.manager.add("Bakery")

    for counter in range(1, 32):
        simulator.manager.add("Vegetables")

    for counter in range(1, 10):
        simulator.manager.add("Cow", animal=True)
    for counter in range(1, 15):
        simulator.manager.add("Chicken", animal=True)
    for counter in range(1, 10):
        simulator.manager.add("Pig", animal=True)

    for iterations in range(1, 3000):
        time += 1000*10*60
        simulator.update_harvest_show_list(time)

        data["time"].append(time)
        data["level"].append(simulator.level)

    my_data = pd.Series(data["level"], index=data["time"])
    myplot = my_data.plot(figsize=(20, 16), kind="line", grid=True, title="level")

    point = __file__.rfind(".")
    bar = __file__.rfind("/")
    plt.savefig(__file__[bar+1:point] + ".png")

    exit(1)
