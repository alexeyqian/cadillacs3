class Character:
    def __init__(self, name, hp, speed, attack_power):
        self.name = name
        self.hp = hp
        self.speed = speed
        self.attack_power = attack_power

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        if isinstance(target, Character):
            target.take_damage(self.attack_power)