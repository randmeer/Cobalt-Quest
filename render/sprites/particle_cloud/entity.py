from render.sprites.particle_cloud import ParticleCloud

class Footstep(ParticleCloud):
    def __init__(self, pos, priority):
        ParticleCloud.__init__(self, center=pos, radius=3, particlesize=(2, 2), color=(40, 20, 20), density=1, velocity=20, colorvariation=10, priority=priority)

class Dash(ParticleCloud):
    def __init__(self, center, priority):
        ParticleCloud.__init__(self, center=center, radius=7, particlesize=(1, 1), color=(100, 100, 255), density=10, velocity=20, colorvariation=20, priority=priority)

class Damage(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=6, particlesize=(1, 1), color=(200, 20, 0), density=30, velocity=20, priority=0, distribution=0.5)

class Die1(ParticleCloud):
    def __init__(self, center, region, radius):
        ParticleCloud.__init__(self, center=center, spawnregion=region, radius=radius, particlesize=(1, 1), color=(255, 50, 0), density=40, velocity=50, colorvariation=20, priority=3, distribution=0.5)

class Die2(ParticleCloud):
    def __init__(self, center, radius):
        ParticleCloud.__init__(self, center=center, radius=radius, particlesize=(2, 2), color=(100, 10, 0), density=30, velocity=30, colorvariation=20, priority=3, distribution=0.5)

