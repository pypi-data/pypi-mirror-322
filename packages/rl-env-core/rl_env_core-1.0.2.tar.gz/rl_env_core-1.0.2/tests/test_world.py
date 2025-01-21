from core import World, PlainObject, Vec3, BBox
import gc


def test_world():
    world = World()
    assert world.objects == []

    obj = world.create()
    obj.fill(BBox(Vec3(0, 0, 0), 1), 1)
    obj.position = Vec3(1, 2, 3)

    assert [obj.position for obj in world.objects] == [Vec3(1, 2, 3)]

    obj.position = Vec3(2, 3, 4)
    assert [obj.position for obj in world.objects] == [Vec3(2, 3, 4)]


def test_remove():
    world = World()

    obj1 = world.create()
    obj1.position = Vec3(1, 2, 3)

    obj2 = world.create()
    obj2.position = Vec3(2, 3, 4)

    assert len(world.objects) == 2

    world.remove(obj1)

    assert len(world.objects) == 1
    assert world.objects == [obj2]


def test_simulate_physics():
    world = World()
    world.simulate_physics()

    obj1 = world.create()
    obj1.fill(BBox(Vec3(0, 0, 0), 3), 1)
    obj1.position = Vec3(1, 2, 3)

    world.simulate_physics()

    obj2 = world.create()
    obj2.fill(BBox(Vec3(0, 0, 0), 5), 1)
    obj2.position = Vec3(-10, 15, 30)

    world.simulate_physics(1000)


def test_several_worlds():
    world1 = World()
    obj1 = world1.create()
    obj1.fill(BBox(Vec3(0, 0, 0), 3), 1)
    obj1.position = Vec3(1, 2, 3)

    world1.simulate_physics()

    world2 = World()
    obj2 = world2.create()
    obj2.fill(BBox(Vec3(0, 0, 0), 3), 1)
    obj2.position = Vec3(1, 2, 3)

    world2.simulate_physics()
    world1.simulate_physics()

    del world1
    gc.collect()
    world2.simulate_physics()


def test_update_body():
    world = World()
    obj = world.create()
    obj.fill(BBox(Vec3(0, 0, 0), 3), 1)
    obj.position = Vec3(1, 2, 3)

    world.simulate_physics()

    obj.fill(BBox(Vec3(1, 1, 1), 3), 1)
    world.simulate_physics()

    obj.carve(BBox(Vec3(0, 0, 1), 2))
    world.simulate_physics()


def test_update_body_starts_empty():
    world = World()
    obj = world.create()

    world.simulate_physics()

    obj.fill(BBox(Vec3(1, 1, 1), 3), 1)
    world.simulate_physics()

    obj.carve(BBox(Vec3(0, 0, 1), 2), 8)

    world.simulate_physics()
