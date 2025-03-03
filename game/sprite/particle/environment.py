from octagon.environment.object.particle import Emitter


class Cinder(Emitter):
    def __init__(self, env):
        Emitter.__init__(self, env=env, center=(env.sidelength / 2, 0), radius=env.sidelength * 2, spawnregion=(2, env.sidelength), velocity=1, priority=0, no_debug=True, dist=0.1, pps=100, preset="cinder")
