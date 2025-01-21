#ifndef SHAPE_GENERATOR_HPP_
#define SHAPE_GENERATOR_HPP_ 

#include "InOrderVisitor.hpp"

#include "conversions.hpp"

#include <Jolt/Physics/Collision/Shape/CompoundShape.h>
#include <Jolt/Physics/Collision/Shape/BoxShape.h>

#include <glm/glm.hpp>

class ShapeGenerator : public InOrderVisitor {
public:
    ShapeGenerator(JPH::CompoundShapeSettings* settings_) : settings{settings_} {}

    void visit_leaf(int material, glm::dvec3 position, glm::dvec3 extents) override {
        if (material != -1) {
            settings->AddShape(to_jolt_rvec3(position + extents / 2.0), JPH::Quat::sIdentity(),
                new JPH::BoxShapeSettings{to_jolt_vec3(extents / 2.0), 0.0});
            added_any_ = true;
        }
    }

    bool added_any() const {
        return added_any_;
    }

    template <typename T, typename... Args>
    static bool visit(JPH::CompoundShapeSettings* settings, const T& t, Args&& ...args) {
        ShapeGenerator generator{settings};
        t.accept(generator, std::forward<Args>(args)...);
        return generator.added_any();
    }
private:
    JPH::CompoundShapeSettings* settings = nullptr;
    bool added_any_ = false;
};

#endif