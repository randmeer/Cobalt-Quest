from octagon.sprites.particle import ParticleCloud, Emitter


class Footstep(Emitter):
    def __init__(self, env, pos, priority):
        Emitter.__init__(self, env, center=pos, radius=5, ptsize=3, velocity=0.1, fadeout=True, priority=priority, pps=10, preset="footstep")


class Dash(Emitter):
    def __init__(self, env, pos, priority):
        Emitter.__init__(self, env, center=pos, radius=5, ptsize=3, velocity=0.2, fadeout=True, priority=priority, pps=100, preset="dash")


class Damage(ParticleCloud):
    def __init__(self, env, pos):
        ParticleCloud.__init__(self, env, center=pos, radius=6, ptsize=1, density=30, velocity=0.3, priority=0, dist=0.5, preset="damage")


class Die1(ParticleCloud):
    def __init__(self, env, center):
        ParticleCloud.__init__(self, env, center=center, radius=10, ptsize=1, density=40, velocity=0.1, priority=3, dist=0.5, preset="death1")


class Die2(ParticleCloud):
    def __init__(self, env, center):
        ParticleCloud.__init__(self, env, center=center, radius=5, ptsize=2, density=30, velocity=0.05, fadeout=True, priority=3, dist=0.5, preset="death2")


class ManaDrop(ParticleCloud):
    def __init__(self, env, center):
        ParticleCloud.__init__(self, env=env, center=center, radius=50, ptsize=1, density=30, velocity=0.5, priority=3, dist=0.5, target=env.player, on_target_reach=env.player.add1mana, preset="entity_mana_drop")
