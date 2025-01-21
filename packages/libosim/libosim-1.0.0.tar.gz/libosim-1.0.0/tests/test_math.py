from core import Vec3, BBox


def test_vec3():
    vec1 = Vec3(1, 2, 3)

    assert vec1.x == 1
    assert vec1.y == 2
    assert vec1.z == 3

    vec2 = Vec3(4, 5, 6)

    assert vec1 + vec2 == Vec3(5, 7, 9)
    assert vec2 - vec1 == Vec3(3, 3, 3)
    assert vec1 * 2 == Vec3(2, 4, 6)


def test_bbox():
    p = BBox(Vec3(1, 2, 3), Vec3(3, 3, 2))

    assert p.size == Vec3(3, 3, 2)
    assert p.width == 3
    assert p.height == 3
    assert p.length == 2

    assert p.origin == Vec3(1, 2, 3)
    assert p.left == 1
    assert p.top == 2
    assert p.front == 3

    assert p.right == 4
    assert p.bottom == 5
    assert p.back == 5

    assert (BBox(Vec3(1, 2, 3), 3)
            == BBox(Vec3(1, 2, 3), Vec3(3, 3, 3)))

    assert p
    assert not BBox(Vec3(1, 2, 3), 0)

    assert Vec3(3, 3, 3) in p
    assert Vec3(3, 3, 2) not in p

    assert p & BBox(Vec3(1, 2, 3), Vec3(3, 2, 3)) == BBox(
        Vec3(1, 2, 3), Vec3(3, 2, 2))

    assert p.intersects(BBox(Vec3(1, 2, 3), Vec3(3, 2, 3)))
    assert p.isdisjoint(BBox(Vec3(1, 2, 7), Vec3(3, 2, 3)))

    assert p == p
    assert p <= BBox(Vec3(1, 2, 3), 3)
    assert p <= p
    assert BBox(Vec3(1, 2, 3), 3) >= p
    assert not p < p
    assert p < BBox(Vec3(1, 2, 3), 3)


def test_transform_bbox():
    p = BBox(Vec3(1, 2, 3), Vec3(3, 3, 2))

    assert p.translated(Vec3(-2, 1, 4)) == BBox(Vec3(-1, 3, 7), Vec3(3, 3, 2))
    assert p.scaled(5) == BBox(Vec3(5, 10, 15), Vec3(15, 15, 10))
