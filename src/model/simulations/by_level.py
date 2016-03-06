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
    data["levels"] = []
    data["recipes"] = []
    data["mills"] = []
    data["av_time"] = []

    for level in range(1,100):
        mills, total_recipes = simulator.get_all_products(level)
        #print(mills["CraftedProducts"])
        data["levels"].append(level)
        data["recipes"].append(total_recipes)
        data["mills"].append(len(mills["CraftedProducts"]))
        total_time = 0
        total_recipes = 0
        for mill in mills["CraftedProducts"]:
            for recipe in mills["CraftedProducts"][mill]:
                for element in recipe:
                    time = recipe[element]
                    total_time += int(time)
                    total_recipes += 1
        average_time = total_time / total_recipes
        data["av_time"].append(average_time)

    charts = ["recipes", "mills", "av_time"]
    xticks = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 98]
    xticklabels = [ n+1 for n in xticks ]
    fig, axes = plt.subplots(nrows=3, ncols=1)
    for i, name in enumerate(charts):
        my_data = pd.Series(data[name], index=data["levels"])
        myplot = my_data.plot(ax=axes[i], figsize=(20, 16), kind="bar", grid=True, title=name)
        axes[i].xaxis.set_ticks(xticks)
        axes[i].xaxis.set_ticklabels(xticklabels, rotation=0)

    point = __file__.rfind(".")
    bar = __file__.rfind("/")
    plt.savefig(__file__[bar+1:point] + ".png")

