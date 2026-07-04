import random


class ParticleManager:
    def __init__(self):
        self.particles = [] # List of dicts: {x, y, z, vx, vy, life}
        
    def spawn_burst(self, x, y, z, color, count=10):
        for _ in range(count):
            self.particles.append({
                'x': x, 'y': y, 'z': z,
                'vx': random.uniform(-100, 100),
                'vy': random.uniform(100, 300),
                'vz': random.uniform(-50, 50),
                'life': 0.5, 'color': color
            })
            
    def update(self, dt):
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['z'] += p['vz'] * dt
            p['vy'] -= 500 * dt # Gravity
            p['life'] -= dt
        self.particles = [p for p in self.particles if p['life'] > 0]