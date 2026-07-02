from game.entities.character import Character


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, speed=5, attack_power=20)
        self.position = (0, 0)
        self.inventory = []