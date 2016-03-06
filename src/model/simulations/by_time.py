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
    simulator.manager.add("AppleTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("CherryTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("CacaoTree", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("CoffeeBush", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("RaspberryBush", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("BlueberryBush", tree=True, simulator=simulator, ts=time)
    simulator.manager.add("BeeHive", tree=True, simulator=simulator, ts=time)

    time += 1000 * 1000 * 60

    simulator.manager.update(time, verbose=True)
    simulator.manager.show(time)

    simulator.update_harvest_show_list(time, verbose=False)

    #tree = simulator.manager.find("AppleTree")
    #tree.plant("Apple", simulator, 0)

    #print("Tree:", tree)
    #print("Tree:", tree.name)
    #print("Tree:", tree.data)
    #simulator.manager.plant("AppleTree", simulator, 0)

    session_minutes = 10
    session_hours = [8, 12, 14, 18, 21]

    for day in range(1, 20):
        # For each day
        for session in session_hours:
            time_session = time + session * 60*60*1000
            simulator.update_harvest_show_list(time_session, verbose=True)
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

    my_data = pd.Series(data["level"], index=data["time"])
    myplot = my_data.plot(figsize=(20, 16), kind="line", grid=True, title="level")

    point = __file__.rfind(".")
    bar = __file__.rfind("/")
    plt.savefig(__file__[bar+1:point] + ".png")

    exit(1)
