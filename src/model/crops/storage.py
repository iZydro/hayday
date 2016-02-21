from model.main import *


class Storage:

    items = None
    main = None

    def __init__(self, main_ref: Main):
        self.items = []
        self.main = main_ref

    def add(self, item):
        self.items.append(item)

    def list(self):
        print("====== Storage =======")
        for item in self.items:
            print(item)
        print("======================")
