from model.database import *
from model.simulator import Simulator
from model.crops.storage import Storage
from model.crops.itemsprocessor import ItemsProcessorManager

import math

import pandas as pd
import matplotlib.pylab as plt


if __name__ == '__main__':

    simulator = Simulator()
    database = Database()
    database.init_data()

    simulator.storage = Storage(database)
    simulator.manager = ItemsProcessorManager(database, simulator.storage)

    simulator.experience = 0

    data = {}
    data["time"] = []
    data["level"] = []

    print("Fielding")

    time = 0

    for crop in database.fields.items:
        simulator.storage.add(crop)
        simulator.storage.add(crop)
        simulator.storage.add(crop)

    #simulator.storage.add("Chicken Food")
    #simulator.storage.add("Cow Food")

    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")

    #simulator.manager.add("Bakery")

    for counter in range(1, 14*4):
        simulator.manager.add("Vegetables")

    for counter in range(1, 15):
        simulator.manager.add("Cow", animal=True)
    for counter in range(1, 15):
        simulator.manager.add("Chicken", animal=True)
    for counter in range(1, 10):
        simulator.manager.add("Pig", animal=True)
    for counter in range(1, 10):
        simulator.manager.add("Sheep", animal=True)
    for counter in range(1, 10):
        simulator.manager.add("Goat", animal=True)

    print("Trees")
    simulator.database.fruit_trees.show()
    print("Fruits")
    simulator.database.fruits.show()
    print("PB")
    simulator.database.processing_buildings.show()
    print("Fishes")
    simulator.database.fishes.show()

    simulator.manager.add("AppleTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("CherryTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("CacaoTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("OliveTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("LemonTree", tree=True, simulator=simulator, ts=time)

    simulator.manager.add("CoffeeBush", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("RaspberryBush", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("BlueberryBush", tree=True, simulator=simulator, ts=time)

    simulator.manager.add("BeeHive", tree=True, simulator=simulator, ts=time)

    session_minutes = 10
    session_hours = [8, 12, 14, 18, 21]
    session_days = 365*2

    ticks_density = session_days / 30
    ticks_density = int(ticks_density / 5) * 5

    for day in range(1, session_days+1):
        # For each day
        for session in session_hours:
            time_session = time + session * 60*60*1000
            simulator.update_harvest_show_list(time_session, verbose=True)
            #simulator.manager.show(time_session)
            for minute in range(1, session_minutes):
                time_minute = time_session + minute * 60*1000
                simulator.update_harvest_show_list(time_minute, verbose=False)
                #simulator.manager.show(time_minute)
            print("Simulated day: " + str(day) + ", session: " + str(session))
        time += 1000*60*60*24

        data["time"].append(day)
        data["level"].append(simulator.level)

        #simulator.database.processing_buildings.show()
        #simulator.manager.show(time)

    #simulator.storage.list_acc()

    for item in simulator.database.items.items:
        acc = simulator.storage.how_many_acc(item)
        item_data, item = simulator.database.items.search(item, simulator.database.generators)
        unlock = 0
        if "UnlockLevel" in item_data["data"]:
            unlock = int(item_data["data"]["UnlockLevel"])
        prefix = ""
        if acc == 0:
            prefix = "**********"

        if unlock <= simulator.level:
            print(prefix, item, "unlock:", unlock, "acc:", acc)

    my_data = pd.Series(data["level"], index=data["time"])
    myplot = my_data.plot(figsize=(64, 32), kind="line", grid=True, title="level")

    xticks = [n for n in range(1, session_days+1)]
    xticklabels = []
    for n in range(0, len(xticks)):
        tick = xticks[n]
        if (tick-1) % ticks_density == 0:
            xticklabels.append(xticks[n])
        else:
            xticklabels.append("")

    myplot.xaxis.set_ticks(xticks)
    myplot.xaxis.set_ticklabels(xticklabels, rotation=0)

    yticks = [n for n in range(1, simulator.level+1)]
    yticklabels = [ n for n in xticks ]
    myplot.yaxis.set_ticks(yticks)
    myplot.yaxis.set_ticklabels(yticklabels, rotation=0)

    point = __file__.rfind(".")
    bar = __file__.rfind("/")
    plt.savefig(__file__[bar+1:point] + ".png")

    exit(1)
