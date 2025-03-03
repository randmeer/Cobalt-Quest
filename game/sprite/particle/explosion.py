from octagon.environment.object.particle import ParticleCloud, Emitter


class Smoke(ParticleCloud):
    def __init__(self, env, pos):
        ParticleCloud.__init__(self, env=env, center=pos, radius=20, ptsize=7, density=20, velocity=0.5, fadeout=True, dist=0.5, preset="smoke")


class Fire(ParticleCloud):
    def __init__(self, env, pos):
        ParticleCloud.__init__(self, env=env, center=pos, radius=15, ptsize=3, density=20, velocity=0.5, fadeout=True, dist=0.5, damage="single", damage_amount=5, preset="fire")


class Sparks(ParticleCloud):
    def __init__(self, env, pos):
        ParticleCloud.__init__(self, env=env, center=pos, radius=15, ptsize=1, density=20, velocity=0.5, dist=0.7, preset="sparks")


class SparkEmitter(Emitter):
    def __init__(self, env, pos):
        Emitter.__init__(self, env=env, center=pos, radius=5, velocity=0.3, ptsize=1, density=0, dist=0.7, pps=40, preset="sparks")


ExplosionPts = [Smoke, Fire, Sparks, SparkEmitter]
