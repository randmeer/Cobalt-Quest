from render.sprites.particle_cloud import ParticleCloud

class Smoke(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, rotation=True, center=pos, radius=20, particlesize=(7, 7), color=(70, 70, 70), density=15, velocity=30, distribution=0.8, colorvariation=5)

class Fire(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, rotation=True, center=pos, radius=15, particlesize=(3, 3), color=(200, 70, 0), density=10, velocity=40, distribution=0.8, colorvariation=30, damage=5)

class Sparks(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=25, particlesize=(1, 1), color=(200, 100, 0), density=20, velocity=50, distribution=0.7, colorvariation=5)
