from core import World, Ragdoll, Vec3


def test_ragdoll():
    world = World(Vec3(0, 0, 0))

    ragdoll = world.create_test_ragdoll()
    ragdoll.move(Vec3(1, 0, 0))

    world.simulate_physics()
