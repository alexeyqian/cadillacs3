from game.entities.character import Character

class Enemy(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, speed=2, attack_power=10)
        self.position = (0, 0)
        self.inventory = []