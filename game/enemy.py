class Enemy:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.position = (0, 0)
        self.inventory = []