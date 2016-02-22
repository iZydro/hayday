from model.main import *


class Storage:

    items = None
    main = None

    def __init__(self, main_ref: Main):
        self.items = []
        self.main = main_ref

    def add(self, item_ref):
        self.items.append(item_ref)

    def delete(self, item_ref):
        self.items.remove(item_ref)

    def find(self, item_ref, num=1):
        found = 0
        for item in self.items:
            print("Searching:" + item + "(" + str(num) + ")")
            if item == item_ref:
                found = found + 1
                print("Found " + str(found))
                print("comp: " + str(found) + str(num))
                if found == num:
                    print("Found all!")
                    return True
        return None

    def get_one(self, item_ref):
        found = 0
        for item in self.items:
            if item == item_ref:
                return item
        return None

    def list(self):
        print("====== Storage =======")
        for item in self.items:
            print(item)
        print("======================")

