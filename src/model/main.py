#from model.base import *
from model.fish import *
from model.item import *
from model.fruit_trees import *
from model.animals import *
from model.fruit import *
from model.field import *


class Main:

    items = None
    fishes = None
    animals = None
    fruit_trees = None
    gatherer_habitats = None
    fruits = None
    fields = None
    base = None

    processing_buildings = None

    generators = None

    def autofill(self, filename, string_id, array_to_add):

        csv_data = Base()
        csv_data.read(filename)
        for element in csv_data.items:
            array_to_add.add(element, string_id, csv_data.items[element])
            self.items.add(element, string_id)

    def init_data(self):

        self.items = Item() # List of all items

        self.fishes = Fish()
        self.autofill("fishing_goods", "Fishing", self.fishes)

        self.fruit_trees = FruitTree()
        self.autofill("fruit_trees", "Trees", self.fruit_trees)
        self.autofill("gatherer_nest_goods", "Trees", self.fruit_trees)

        self.animals = Animal()
        self.autofill("animals", "Animals", self.animals)

        self.fruits = Fruit()
        self.autofill("fruits", "Fruits", self.fruits)
        self.autofill("honey_extractor_goods", "Fruits", self.fruits)

        # Create milk, eggs, etc from animals
        for animal in self.animals.items:
            good = self.animals.items[animal]["data"]["Good"]
            print(good)
            self.fruits.add(good, "Fruits", {"ProcessingBuilding": animal})
            self.items.add(good, "Fruits")

#        self.autofill("animal_goods", "Fruits", self.fruits)

        self.fields = Field()
        self.autofill("fields", "Vegetables", self.fields)

        print("caca")
        csv_data = Base()
        csv_data.read("processing_buildings")

        self.processing_buildings = ProcessingBuilding()

        for element in csv_data.items:

            if element == "Cafe_Kiosk":
                element = "cafe"

            if element == "Hammermill":
                element = "animal_feed"

            mill_name = element.lower()
            if mill_name != "animal_feed":
                mill_name += "_goods"

            building_csv = Base()
            building_csv.read(mill_name)

            self.processing_buildings.add(mill_name, building_csv)

            # Now add to items

            for item in building_csv.items:
                self.items.add(item, mill_name)

        self.generators = {}
        self.generators["ProcessingBuildings"] = self.processing_buildings
        self.generators["Fishing"] = self.fishes
        self.generators["Trees"] = self.fruit_trees
        self.generators["Fruits"] = self.fruits
        self.generators["Animals"] = self.animals
        self.generators["Vegetables"] = self.fields

        self.fishes.show()
        print()
        self.fruits.show()
        print()
        self.fruit_trees.show()
        print()
        self.animals.show()
        print()
        self.fields.show()

        #self.base = Base()

        return

if __name__ == "__main__":

    main = Main()
    main.init_data()

    main.base = Base()

    print("=================================================================================")
    product = "Bread"
    main.base.recursive_search(main.items.search(product, main.generators), main.generators, main.items)

    #main.items.show()
