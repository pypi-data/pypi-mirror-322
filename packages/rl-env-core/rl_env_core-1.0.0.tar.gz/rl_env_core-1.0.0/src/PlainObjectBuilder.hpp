#ifndef PLAIN_OBJECT_BUILDER_HPP_
#define PLAIN_OBJECT_BUILDER_HPP_

#include "BBox.hpp"

#include <glm/glm.hpp>

#include <vector>

class PlainObjectBuilder {
private:
    Octree octree{};

    glm::dvec3 offset{};
    double scale = 1.0;

    glm::dvec3 position_{};
    glm::dquat rotation_ = glm::identity<glm::dquat>();

    bool movable = true;

    int maximal_depth_ = 5;

    BBox to_local_cords(BBox bbox) const {
        return bbox.translated(-offset).scaled(1 / scale);
    }
public:
    PlainObjectBuilder() = default;

    PlainObjectBuilder& fill(BBox bbox, int material) {
        if (material == -1) {
            return carve(bbox);
        } else {
            auto [offset_, scale_] = octree.expand_to_include(to_local_cords(bbox));

            scale *= 1 / scale_;

            octree.fill(to_local_cords(bbox).translated(offset_), material, maximal_depth_);

            offset -= offset_ / scale_;
            return *this;
        }
    }

    PlainObjectBuilder& carve(BBox bbox) {
        octree.fill(to_local_cords(bbox), -1, maximal_depth_);
        return *this;
    }

    PlainObjectBuilder& position(glm::dvec3 newPosition) {
        position_ = newPosition;
        return *this;
    }

    PlainObjectBuilder& rotation(glm::dquat newRotation) {
        rotation_ = newRotation;
        return *this;
    }

    PlainObjectBuilder& maximal_depth(int depth) {
        maximal_depth_ = depth;
        return *this;
    }

    PlainObjectBuilder& immovable() {
        movable = false;
        return *this;
    }

    std::shared_ptr<PlainObject> create(World& world) const {
        auto res = world.create_from_octree(Octree{octree}, movable);

        res->set_position(position_);
        res->set_rotation(rotation_);

        return res;
    }
};

#endif