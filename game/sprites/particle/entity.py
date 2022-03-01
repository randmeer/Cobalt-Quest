from octagon.sprites.particle import ParticleCloud, Emitter


class Footstep(Emitter):
    def __init__(self, pos, priority):
        Emitter.__init__(self, center=pos, radius=5, ptsize=3, velocity=0.1, fadeout=True, priority=priority, pps=10, preset="footstep")


class Dash(Emitter):
    def __init__(self, pos, priority):
        Emitter.__init__(self, center=pos, radius=5, ptsize=3, velocity=0.2, fadeout=True, priority=priority, pps=100, preset="dash")


class Damage(ParticleCloud):
    def __init__(self, pos):
        ParticleCloud.__init__(self, center=pos, radius=6, ptsize=1, density=30, velocity=0.3, priority=0, dist=0.5, preset="damage")


class Die1(ParticleCloud):
    def __init__(self, center, region, radius):
        ParticleCloud.__init__(self, center=center, spawnregion=region, radius=radius, ptsize=1, density=40, velocity=0.2, priority=3, dist=0.5, preset="death1")


class Die2(ParticleCloud):
    def __init__(self, center, radius):
        ParticleCloud.__init__(self, center=center, radius=radius, ptsize=2, density=30, velocity=0.1, fadeout=True, priority=3, dist=0.5, preset="death2")
