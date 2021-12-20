from render.sprites.particle_cloud import ParticleCloud

class Smoke(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=20, particlesize=7, color=(70, 70, 70), density=20, velocity=0.5, fadeout=True, distribution=0.5, colorvariation=5)

class Fire(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=15, particlesize=3, color=(200, 70, 0), density=20, velocity=0.5, fadeout=True, distribution=0.5, colorvariation=5, damage=5)

class Sparks(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=15, particlesize=1, color=(200, 100, 0), density=20, velocity=0.5, distribution=0.7, colorvariation=5)
