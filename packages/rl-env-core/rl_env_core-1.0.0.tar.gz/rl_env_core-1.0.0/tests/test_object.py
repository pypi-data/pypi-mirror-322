import math

from core import Vec3, Triangle, BBox, PlainObject, angleAxis, Mat4x4, World


def test_fill():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 0.7), 1)

    assert obj.is_filled(Vec3(0.3, 0.4, 0.5))
    assert not obj.is_filled(Vec3(0.1, 0.1, 0.1))

    obj.carve(BBox(Vec3(0.3, 0.4, 0.5), Vec3(0.1, 0.2, 0.1)))

    assert not obj.is_filled(Vec3(0.35, 0.55, 0.55))


def test_generate_mesh():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0.0, 0.0, 0.0), 0.5), 1)
    assert obj.generate_mesh() == [Triangle(Vec3(0, 0, 0), Vec3(0, 0, 0.5), Vec3(0, 0.5, 0), 1),
                                   Triangle(Vec3(0, 0, 0.5), Vec3(0, 0.5, 0.5), Vec3(0, 0.5, 0), 1),
                                   Triangle(Vec3(0.5, 0, 0), Vec3(0.5, 0.5, 0), Vec3(0.5, 0, 0.5), 1),
                                   Triangle(Vec3(0.5, 0.5, 0), Vec3(0.5, 0.5, 0.5), Vec3(0.5, 0, 0.5), 1),
                                   Triangle(Vec3(0, 0, 0), Vec3(0.5, 0, 0), Vec3(0, 0, 0.5), 1),
                                   Triangle(Vec3(0.5, 0, 0), Vec3(0.5, 0, 0.5), Vec3(0, 0, 0.5), 1),
                                   Triangle(Vec3(0, 0.5, 0), Vec3(0, 0.5, 0.5), Vec3(0.5, 0.5, 0), 1),
                                   Triangle(Vec3(0, 0.5, 0.5), Vec3(0.5, 0.5, 0.5), Vec3(0.5, 0.5, 0), 1),
                                   Triangle(Vec3(0, 0, 0), Vec3(0, 0.5, 0), Vec3(0.5, 0, 0), 1),
                                   Triangle(Vec3(0, 0.5, 0), Vec3(0.5, 0.5, 0), Vec3(0.5, 0, 0), 1),
                                   Triangle(Vec3(0, 0, 0.5), Vec3(0.5, 0, 0.5), Vec3(0, 0.5, 0.5), 1),
                                   Triangle(Vec3(0.5, 0, 0.5), Vec3(0.5, 0.5, 0.5), Vec3(0, 0.5, 0.5), 1)]


def tesh_have_changed():
    world = World()

    obj = world.create()
    assert not obj.changed

    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 0.7), 1)

    assert obj.changed

    obj.clear_changed()
    assert not obj.changed

    obj.carve(BBox(Vec3(0.3, 0.4, 0.5), Vec3(0.1, 0.2, 0.1)))
    assert obj.changed


def test_transform():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0, 0, 0), 1), 1)

    obj.position = Vec3(1, 2, 3)
    obj.rotation = angleAxis(math.pi / 2, Vec3(0, 0, 1))

    assert obj.position == Vec3(1, 2, 3)

    assert obj.rotation.x - angleAxis(math.pi / 2, Vec3(0, 0, 1)).x < 1e-6
    assert obj.rotation.y - angleAxis(math.pi / 2, Vec3(0, 0, 1)).y < 1e-6
    assert obj.rotation.z - angleAxis(math.pi / 2, Vec3(0, 0, 1)).z < 1e-6
    assert obj.rotation.w - angleAxis(math.pi / 2, Vec3(0, 0, 1)).w < 1e-6

    assert obj.transform.nearly_equal(Mat4x4(
        0, 1, 0, 0,
        -1, 0, 0, 0,
        0, 0, 1, 0,
        1, 2, 3, 1,
    ), 1.e-6)


def test_transform_is_filled():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0, 0, 0), 1), 1)

    obj.position = Vec3(1, 2, 3)
    obj.rotation = angleAxis(math.pi / 2, Vec3(0, 0, 1))

    assert obj.is_filled(Vec3(0, 1.5, 2))


def test_fill_transformed():
    world = World()

    obj = world.create()
    obj.position = Vec3(0.5, 0.5, 0.5)

    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 1.2), 1)

    assert obj.is_filled(Vec3(0.3, 0.4, 0.5))
    assert not obj.is_filled(Vec3(0.1, 0.1, 0.1))

    obj.carve(BBox(Vec3(0.3, 0.4, 0.5), Vec3(0.1, 1.1, 0.1)))

    assert not obj.is_filled(Vec3(0.35, 1.2, 0.55))


def test_fill_expand():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0.2, 0.15, 0.15), 10), 1)
    obj.position = Vec3(1, 1, 1)

    assert obj.is_filled(Vec3(7, 7, 7))
    assert not obj.is_filled(Vec3(0.1, 0.1, 0.1))


def test_carve_keeps():
    world = World()

    obj = world.create()

    obj.fill(BBox(Vec3(0, 0, 0), 1), 1)
    obj.carve(BBox(Vec3(0, 0.5, 0), 0.5))
    assert obj.is_filled(Vec3(0, 0.05, 0))


def test_carve():
    world = World()

    obj = world.create()
    obj.fill(BBox(Vec3(0.2, 0.1, 0.15), 1.2), 1)
    obj.carve(BBox(Vec3(0.2, 0.15, 0.15), 10))
    obj.position = Vec3(1, 1, 1)

    assert not obj.is_filled(Vec3(1.35, 1.2, 1.55))
    assert obj.is_filled(Vec3(1.3, 1.12, 1.2))


def test_dict_key():
    world = World()

    obj1 = world.create()
    obj2 = world.create()

    dct = {obj1: 1, obj2: 2}

    assert dct[obj1] == 1
    assert dct[obj2] == 2
