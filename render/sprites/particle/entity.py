from render.sprites.particle import ParticleCloud, Emitter

class Footstep(Emitter):
    def __init__(self, pos, priority):
        Emitter.__init__(self, center=pos, radius=5, ptsize=3, color=(40, 20, 20), velocity=0.1, fadeout=True, colorvar=10, priority=priority, pps=10)

class Dash(Emitter):
    def __init__(self, pos, priority):
        Emitter.__init__(self, center=pos, radius=5, ptsize=3, color=(100, 100, 255), velocity=0.2, fadeout=True, colorvar=10, priority=priority, pps=100)

class Damage(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=6, ptsize=1, color=(200, 20, 0), density=30, velocity=0.3, priority=0, dist=0.5)

class Die1(ParticleCloud):
    def __init__(self, center, region, radius):
        ParticleCloud.__init__(self, center=center, spawnregion=region, radius=radius, ptsize=1, color=(255, 50, 0), density=40, velocity=0.2, colorvar=20, priority=3, dist=0.5)

class Die2(ParticleCloud):
    def __init__(self, center, radius):
        ParticleCloud.__init__(self, center=center, radius=radius, ptsize=2, color=(100, 10, 0), density=30, velocity=0.1, fadeout=True, colorvar=20, priority=3, dist=0.5)
