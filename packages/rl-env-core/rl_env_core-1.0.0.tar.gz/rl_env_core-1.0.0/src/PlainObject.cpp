#include "PlainObject.hpp"

#include "ShapeGenerator.hpp"

#include "World.hpp"

#define JPH_ENABLE_ASSERTS

void PlainObject::update_body() {
    using namespace JPH::literals;

    JPH::Ref<JPH::StaticCompoundShapeSettings> shape_settings = new JPH::StaticCompoundShapeSettings{};
    if (ShapeGenerator::visit(shape_settings, octree, glm::dvec3{0, 0, 0}, scale_)) {
        JPH::ShapeSettings::ShapeResult shape_result = shape_settings->Create();
        if (shape_result.HasError()) {
            throw std::runtime_error{ shape_result.GetError().c_str() };
        }

        auto shape = shape_result.Get();

        if (body_id_.IsInvalid()) {
            JPH::BodyCreationSettings body_settings(shape,
                JPH::RVec3{ 0, 0, 0 }, JPH::Quat::sIdentity(), 
                movable ? JPH::EMotionType::Dynamic : JPH::EMotionType::Static, 
                movable ? Layers::MOVING : Layers::NON_MOVING);
            body_id_ = bodies->CreateAndAddBody(body_settings, JPH::EActivation::Activate);
        } else {
            bodies->SetShape(body_id_, shape, true, JPH::EActivation::Activate);
        }
    } else {
        if (!body_id_.IsInvalid()) {
            bodies->RemoveBody(body_id_);
            bodies->DestroyBody(body_id_);

            body_id_ = {};
        }
    }
}

void PlainObject::cut(BBox bbox, std::shared_ptr<PlainObject> to, int max_depth) {
    octree.cut(to_local_cords(bbox), position(), scale_, *to, max_depth);
    changed = true;
    update_body();
}
