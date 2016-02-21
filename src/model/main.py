from model.base import *
from model.base_item import *
from model.item import *


class Main:

    items = None
    fishes = None
    animals = None
    animal_products = None
    fruit_trees = None
    gatherer_habitats = None
    fruits = None
    fields = None
    base = None

    processing_buildings = None

    generators = None

    def auto_fill(self, filename, string_id, array_to_add):

        csv_data = Base()
        csv_data.read(filename)
        for element in csv_data.items:
            array_to_add.add(element, string_id, csv_data.items[element])
            self.items.add(element, string_id, csv_data.items[element])

    def init_data(self):

        self.items = Item() # List of all items

        self.fishes = BaseItem()
        self.auto_fill("fishing_goods", "Fishing", self.fishes)

        self.fruit_trees = BaseItem()
        self.auto_fill("fruit_trees", "Trees", self.fruit_trees)
        self.auto_fill("gatherer_nest_goods", "Trees", self.fruit_trees)

        self.animals = BaseItem()
        self.auto_fill("animals", "Animals", self.animals)

        self.fruits = BaseItem()
        self.auto_fill("fruits", "Fruits", self.fruits)
        self.auto_fill("honey_extractor_goods", "Fruits", self.fruits)

        # Create milk, eggs, etc from animals
        self.animal_products = BaseItem()
        for animal in self.animals.items:
            good = self.animals.items[animal]["data"]["Good"]
            print(good)
            self.animal_products.add(good, "AnimalProducts", {"ProcessingBuilding": animal})
            self.items.add(good, "AnimalProducts")

        self.fields = BaseItem()
        self.auto_fill("fields", "Vegetables", self.fields)

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

            self.auto_fill(mill_name, "Mills", self.processing_buildings)

        self.generators = {
            "Mills": self.processing_buildings,
            "Fishing": self.fishes,
            "Trees": self.fruit_trees,
            "Fruits": self.fruits,
            "Animals": self.animals,
            "AnimalProducts": self.animal_products,
            "Vegetables": self.fields,
        }

        self.fishes.show()
        print()
        self.fruits.show()
        print()
        self.fruit_trees.show()
        print()
        self.animals.show()
        print()
        self.animal_products.show()
        print()
        self.fields.show()
        print()
        self.processing_buildings.show()

        return


if __name__ == "__main__":

    main = Main()
    main.init_data()

    main.base = Base()

    print("=================================================================================")
    product = "Shepherds Pie"
    main.base.recursive_search(main.items.search(product, main.generators), main.generators, main.items)

    main.items.show()
