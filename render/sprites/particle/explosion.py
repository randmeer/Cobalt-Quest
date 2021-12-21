from render.sprites.particle import ParticleCloud, Emitter

class Smoke(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=20, ptsize=7, color=(70, 70, 70), density=20, velocity=0.5, fadeout=True, dist=0.5, colorvar=5)

class Fire(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=15, ptsize=3, color=(200, 70, 0), density=20, velocity=0.5, fadeout=True, dist=0.5, colorvar=5, damage=5)

class Sparks(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=15, ptsize=1, color=(200, 100, 0), density=20, velocity=0.5, dist=0.7, colorvar=5)

class SparkEmitter(Emitter):
    def __init__(self, pos):
        Emitter.__init__(self, center=pos, radius=5, velocity=0.3, ptsize=1, color=(200, 100, 0), density=0, dist=0.7, colorvar=5, pps=40)
