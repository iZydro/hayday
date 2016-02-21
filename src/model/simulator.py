from model.main import *
from model.crops.field import *

class Simulator:

    main = None

    def __init__(self):
        self.main = Main()
        self.main.init_data()


if __name__ == "__main__":

    simulator = Simulator()
    main = simulator.main
    base = main.base

    #print("=================================================================================")
    #product = "Caramel Apple"
    #base.recursive_search(main.items.search(product, main.generators), main.generators, main.items)

    manager = FieldManager(main)
    print("Fielding")

    time = 0

    manager.add().plant("carrot", time)
    manager.add().plant("wheat", time)
    manager.add()

    for item in manager.items:
        print(item, item.name, item.ts, item.parent)


    print("Done!")

