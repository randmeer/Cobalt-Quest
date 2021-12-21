from render.sprites.particle import ParticleCloud, Emitter

class Cinder(Emitter):
    def __init__(self, sidelength):
        Emitter.__init__(self, center=(sidelength / 2, 0), radius=sidelength * 2, color=(255, 0, 0), colorvar=100, spawnregion=(2, sidelength), velocity=1, priority=0, no_debug=True, dist=0.1, pps=100)
