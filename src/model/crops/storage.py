from model.database import *


class Storage:

    items = None
    acc_items = None
    main = None

    def __init__(self, main_ref: Database):
        self.items = {}
        self.acc_items = {}
        self.main = main_ref

    def add(self, item_ref):
        if item_ref not in self.items:
            self.items[item_ref] = 0
        self.items[item_ref] += 1

        if item_ref not in self.acc_items:
            self.acc_items[item_ref] = 0
        self.acc_items[item_ref] += 1

    def delete(self, item_ref):
        self.items[item_ref] -= 1

    def find(self, item_ref, num=1):
        if item_ref in self.items:
            found = self.items[item_ref]
            if found >= num:
                return True
        return False

    def how_many(self, item_ref):
        if item_ref in self.items:
            return self.items[item_ref]
        return 0

    def how_many_acc(self, item_ref):
        if item_ref in self.acc_items:
            return self.acc_items[item_ref]
        return 0

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

    def list_acc(self):
        print("====== Acc Storage =======")
        for item in self.acc_items:
            print(item, "=>", self.acc_items[item])
        print("==========================")

