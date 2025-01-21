#ifndef OBJECT_HPP_
#define OBJECT_HPP_

#include "Octree.hpp"
#include "Triangle.hpp"
#include "conversions.hpp"
#include "Layers.hpp"
#include "InOrderVisitor.hpp"

#include <Jolt/Jolt.h>
#include <Jolt/Physics/PhysicsSystem.h>
#include <Jolt/Physics/Body/BodyCreationSettings.h>
#include <Jolt/Physics/Collision/Shape/CompoundShape.h>
#include <Jolt/Physics/Collision/Shape/BoxShape.h>
#include <Jolt/Physics/Collision/Shape/StaticCompoundShape.h>

#include <glm/vec3.hpp>
#include <glm/gtc/quaternion.hpp>
#include <glm/mat4x4.hpp>

#include <memory>
#include <concepts>

class World;

class PlainObject {
    Octree octree{};

    bool changed = false;

    double scale_ = 1.0;

    bool movable = true;

    JPH::BodyID body_id_{};
    JPH::BodyInterface* bodies = nullptr;
    const JPH::BodyLockInterface* lock_interface = nullptr;

    BBox to_local_cords(BBox bbox) const {
        return bbox.translated(-position()).scaled(1 / scale_);
    }
public:
    PlainObject(JPH::BodyInterface* bodies_, const JPH::BodyLockInterface* lock_interface_, bool movable_ = true) :
        bodies{bodies_}, lock_interface{lock_interface_}, movable{movable_} {}
    PlainObject(Octree&& octree_, JPH::BodyInterface* bodies_, const JPH::BodyLockInterface* lock_interface_, bool movable_ = true) :
        octree{std::move(octree_)}, bodies{bodies_}, lock_interface{lock_interface_}, movable{movable_} {}

    bool have_changed() const {
        return changed;
    }

    void clear_changed() {
        changed = false;
    }

    int material_at(glm::dvec3 pos) const {
        glm::dvec4 in_tree = glm::inverse(transform()) * glm::dvec4{pos, 1.0};
        return octree.material_at(glm::vec3{in_tree.x, in_tree.y, in_tree.z});
    }

    bool is_filled(glm::dvec3 pos) const {
        return material_at(pos) != -1;
    }

    void fill(BBox bbox, int material, int max_depth = 5) {
        if (material == -1) {
            carve(bbox, max_depth);
        } else {
            auto [offset, scale] = octree.expand_to_include(to_local_cords(bbox));

            scale_ *= 1 / scale;

            octree.fill(to_local_cords(bbox).translated(offset), material, max_depth);
            changed = true;
            update_body();

            move(-offset / scale);
        }
    }

    void carve(BBox bbox, int max_depth = 5) {
        octree.fill(to_local_cords(bbox), -1, max_depth);
        changed = true;
        update_body();
    }

    void cut(BBox bbox, std::shared_ptr<PlainObject> to, int max_depth = 5);

    std::string debug_tree_repr() const {
        return octree.debug_tree_repr("|");
    }

    glm::dvec3 position() const {
        if (!body_id_.IsInvalid()) {
            return to_glm_dvec3(bodies->GetPosition(body_id_));
        } else {
            return glm::dvec3{0, 0, 0};
        }
    }

    void set_position(glm::dvec3 position) {
        if (!body_id_.IsInvalid()) {
            bodies->SetPosition(body_id_, to_jolt_vec3(position), JPH::EActivation::Activate);
        }
    }

    void move(glm::dvec3 offset) {
        set_position(position() + offset);
    }

    glm::dquat rotation() const {
        if (!body_id_.IsInvalid()) {
            return to_glm_dquat(bodies->GetRotation(body_id_));
        } else {
            return glm::dquat{0, 0, 0, 0};
        }
    }

    void set_rotation(glm::dquat rotation) {
        if (!body_id_.IsInvalid()) {
            bodies->SetRotation(body_id_, to_jolt_quat(rotation), JPH::EActivation::Activate);
        }
    }

    void rotate(glm::dquat newRotation) {
         set_rotation(rotation() * newRotation);
    }

    glm::dmat4x4 transform() const {
        if (body_id_.IsInvalid()) {
            return glm::identity<glm::dmat4x4>();
        }

        return glm::translate(glm::identity<glm::dmat4x4>(), position())
            * glm::mat4_cast(rotation())
            * glm::scale(glm::identity<glm::dmat4x4>(), glm::dvec3{scale_, scale_, scale_});
    }

    void update_body();

    void remove() {
        if (!body_id_.IsInvalid()) {
            bodies->RemoveBody(body_id_);
            bodies->DestroyBody(body_id_);
        }

        bodies = nullptr;
        body_id_ = {};
    }

    JPH::BodyID body_id() const {
        return body_id_;
    }

    void accept(InOrderVisitor& visitor) const {
        octree.accept(visitor, {0, 0, 0}, 1);
    }
};

#endif