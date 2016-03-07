from model.database import *


class Storage:

    items = None
    main = None

    def __init__(self, main_ref: Database):
        self.items = {}
        self.main = main_ref

    def add(self, item_ref):
        if item_ref not in self.items:
            self.items[item_ref] = 0
        self.items[item_ref] += 1

    def delete(self, item_ref):
        #print("Deleting: " + item_ref )
        self.items[item_ref] -= 1

    def find(self, item_ref, num=1):
        if item_ref in self.items:
            found = self.items[item_ref]
            if found >= num:
                #print("Found all!")
                return True
        return False

    def get_one(self, item_ref):
        if item_ref in self.items:
            if self.items[item_ref] > 0:
                return item_ref
        return None

    def list(self):
        print("====== Storage =======")
        for item in self.items:
            print(item, "=>", self.items[item])
        print("======================")

