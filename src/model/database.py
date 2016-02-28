from model.base import *
from model.base_item import *
from model.item import *


class Database:

    items = None
    fishes = None
    animals = None
    animal_products = None
    fruit_trees = None
    gatherer_habitats = None
    fruits = None
    fields = None
    base = None

    level = None

    levels = None

    processing_buildings = None

    generators = None

    def auto_fill(self, filename, string_id, array_to_add):

        csv_data = Base()
        csv_data.read(filename)
        for element in csv_data.items:
            if element != "EmptyField":
                array_to_add.add(element, string_id, csv_data.items[element])
                self.items.add(element, string_id, csv_data.items[element])
                print(element, string_id, csv_data.items[element])

    def init_data(self):

        self.base = Base()

        self.items = Item() # List of all items

        self.fishes = BaseItem()
        self.auto_fill("fishing_goods", globalNames.fishing, self.fishes)

        self.fruit_trees = BaseItem()
        self.auto_fill("fruit_trees", globalNames.trees, self.fruit_trees)
        self.auto_fill("gatherer_nest_goods", globalNames.trees, self.fruit_trees)

        self.animals = BaseItem()
        self.auto_fill("animals", globalNames.animals, self.animals)

        self.fruits = BaseItem()
        self.auto_fill("fruits", globalNames.fruits, self.fruits)
        self.auto_fill("honey_extractor_goods", globalNames.fruits, self.fruits)

        csv_data = Base()
        csv_data.read("animal_goods")

        # Create milk, eggs, etc from animals
        self.animal_products = BaseItem()
        for animal in self.animals.items:
            good = self.animals.items[animal]["data"]["Good"]
            data = csv_data.items[good]
            #print(good, data)
            data["ProcessingBuilding"] = animal
            self.animal_products.add(good, globalNames.animal_products, data)
            self.items.add(good, globalNames.animal_products, data)

        self.fields = BaseItem()
        self.auto_fill("fields", globalNames.vegetables, self.fields)

        # csv_data is a placeholder here, we will use to sequentially read all mills
        csv_data = Base()
        csv_data.read("processing_buildings")

        self.processing_buildings = BaseItem()
        for element in csv_data.items:

            mill_name = element.lower()
            if mill_name == "cafe_kiosk":
                mill_name = "cafe"

            if mill_name == "hammermill":
                mill_name = "animal_feed"

            if mill_name != "animal_feed":
                mill_name += "_goods"

            building_csv = Base()
            building_csv.read(mill_name)

            self.auto_fill(mill_name, globalNames.crafted_products, self.processing_buildings)

        for item_name, item_data in self.items.iterate():
#            print(item_name, item_data["Mill"], item_data["data"])
            if "Food" in item_data["data"]["Name"]:
                animal = item_data["data"]["Name"].split(" ")[0]
                animal_item, animal_name = self.animals.search(animal)
                item_data["unlock"] = animal_item["data"]["UnlockLevel"]
            if "Bush" in item_data["data"]["Name"]:
                animal = item_data["data"]["Name"].split("Bush")[0]
                if animal == "Blueberry":
                    animal = "Raspberry"
                animal_item, animal_name = self.fruits.search(animal)
                item_data["unlock"] = animal_item["data"]["UnlockLevel"]
            if "Tree" in item_data["data"]["Name"]:
                animal = item_data["data"]["Name"].split("Tree")[0]
                animal_item, animal_name = self.fruits.search(animal)
                item_data["unlock"] = animal_item["data"]["UnlockLevel"]
        #exit(1)

        self.generators = {
            globalNames.crafted_products: self.processing_buildings,
            globalNames.fishing: self.fishes,
            globalNames.trees: self.fruit_trees,
            globalNames.fruits: self.fruits,
            globalNames.animals: self.animals,
            globalNames.animal_products: self.animal_products,
            globalNames.vegetables: self.fields,
        }

        #for generator in self.generators:
        #    self.generators[generator].show()

        csv_data = Base()
        csv_data.read("exp_levels", csv_data.level_items)
        # print(levels_csv_data.items)

        from collections import OrderedDict
        self.levels = OrderedDict(sorted(csv_data.items.items(), key=lambda t: int(t[0])))

        return

    def get_level(self, experience):

        for level in self.levels:
            if experience < int(self.levels[level]["ExpToNextLevel"]):
                return level


if __name__ == "__main__":

    database = Database()
    database.init_data()

    database.base = Base()

    print("=================================================================================")
    product = "Lemon Pie"
    req, item = database.items.search(product, database.generators)
    database.base.recursive_search(req, database.generators, database.items)

    #main.processing_buildings.show()
