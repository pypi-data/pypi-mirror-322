#ifndef WORLD_HPP_
#define WORLD_HPP_

#include "PlainObject.hpp"
#include "Ragdoll.hpp"
#include "Layers.hpp"

#include <Jolt/Jolt.h>

#include <Jolt/RegisterTypes.h>
#include <Jolt/Core/Factory.h>
#include <Jolt/Core/TempAllocator.h>
#include <Jolt/Core/JobSystemThreadPool.h>
#include <Jolt/Physics/PhysicsSettings.h>
#include <Jolt/Physics/PhysicsSystem.h>
#include <Jolt/Physics/Collision/Shape/BoxShape.h>
#include <Jolt/Physics/Collision/Shape/SphereShape.h>
#include <Jolt/Physics/Body/BodyCreationSettings.h>
#include <Jolt/Physics/Body/BodyActivationListener.h>
#include <Jolt/Physics/Constraints/PointConstraint.h>

#include <span>
#include <unordered_map>
#include <exception>
#include <numbers>

class World {
    std::vector<std::shared_ptr<PlainObject>> objects_;
    std::vector<std::shared_ptr<Ragdoll>> ragdolls_;

    class ObjectLayerPairFilterImpl : public JPH::ObjectLayerPairFilter {
    public:
        bool ShouldCollide(JPH::ObjectLayer inObject1, JPH::ObjectLayer inObject2) const override {
            switch (inObject1) {
            case Layers::NON_MOVING:
                return inObject2 == Layers::MOVING;
            case Layers::MOVING:
                return true;
            default:
                JPH_ASSERT(false);
                return false;
            }
        }
    };

    struct BroadPhaseLayers {
        inline static constexpr JPH::BroadPhaseLayer NON_MOVING{0};
        inline static constexpr JPH::BroadPhaseLayer MOVING{1};
        inline static constexpr JPH::uint NUM_LAYERS{2};
    };

    class BPLayerInterfaceImpl final : public JPH::BroadPhaseLayerInterface {
    public:
        BPLayerInterfaceImpl() {
            objectToBroadPhase[Layers::NON_MOVING] = BroadPhaseLayers::NON_MOVING;
            objectToBroadPhase[Layers::MOVING] = BroadPhaseLayers::MOVING;
        }

        JPH::uint GetNumBroadPhaseLayers() const override {
            return BroadPhaseLayers::NUM_LAYERS;
        }

        JPH::BroadPhaseLayer GetBroadPhaseLayer(JPH::ObjectLayer inLayer) const override {
            JPH_ASSERT(inLayer < Layers::NUM_LAYERS);
            return objectToBroadPhase[inLayer];
        }

    #if defined(JPH_EXTERNAL_PROFILE) || defined(JPH_PROFILE_ENABLED)
        const char* GetBroadPhaseLayerName(JPH::BroadPhaseLayer inLayer) const override {
            switch ((JPH::BroadPhaseLayer::Type) inLayer) {
                case (JPH::BroadPhaseLayer::Type) BroadPhaseLayers::NON_MOVING:
                    return "NON_MOVING";
                case (JPH::BroadPhaseLayer::Type) BroadPhaseLayers::MOVING:
                    return "MOVING";
                default:
                    JPH_ASSERT(false);
                    return "INVALID";
            }
        }
    #endif // JPH_EXTERNAL_PROFILE || JPH_PROFILE_ENABLED

    private:
        JPH::BroadPhaseLayer objectToBroadPhase[Layers::NUM_LAYERS];
    };

    class ObjectVsBroadPhaseLayerFilterImpl : public JPH::ObjectVsBroadPhaseLayerFilter {
    public:
        bool ShouldCollide(JPH::ObjectLayer inLayer1, JPH::BroadPhaseLayer inLayer2) const override {
            switch (inLayer1) {
            case Layers::NON_MOVING:
                return inLayer2 == BroadPhaseLayers::MOVING;
            case Layers::MOVING:
                return true;
            default:
                JPH_ASSERT(false);
                return false;
            }
        }
    };

    JPH::TempAllocatorImpl* temp_allocator = nullptr;
    JPH::JobSystemThreadPool* job_system;

    BPLayerInterfaceImpl broad_phase_layer_interface;
    ObjectVsBroadPhaseLayerFilterImpl object_vs_broadphase_layer_filter;
    ObjectLayerPairFilterImpl object_vs_object_layer_filter;

    JPH::PhysicsSystem physics_system;
    JPH::BodyInterface* body_interface;
public:
    World(glm::dvec3 gravity = {0, -9.81, 0});

    ~World();

    const std::vector<std::shared_ptr<PlainObject>>& objects() const {
        return objects_;
    }

    std::shared_ptr<PlainObject> create(bool movable = true);
    std::shared_ptr<PlainObject> create_from_octree(Octree&& octree, bool movable = true);

    void remove(std::shared_ptr<PlainObject> object) {
        auto iter = std::ranges::find(objects_, object);
        if (iter == objects_.end()) {
            throw std::logic_error("Unknown object");
        }
        
        object->remove();
        objects_.erase(iter);
    }

    void simulate_physics(int steps = 1, double step_length = 1.0 / 60.0);

    const std::vector<std::shared_ptr<Ragdoll>>& ragdolls() const {
        return ragdolls_;
    }

    std::shared_ptr<Ragdoll> create_ragdoll(std::span<const Ragdoll::PartSettings> parts) {
        ragdolls_.push_back(std::make_shared<Ragdoll>(parts, &physics_system));
        return ragdolls_.back();
    }

    void remove_ragdoll(std::shared_ptr<Ragdoll> ragdoll) {
        auto iter = std::ranges::find(ragdolls_, ragdoll);
        if (iter == ragdolls_.end()) {
            throw std::logic_error("Unknown ragdoll");
        }

        ragdoll->remove();
        ragdolls_.erase(iter);
    }

    std::shared_ptr<Ragdoll> create_test_ragdoll() {
        JPH::Ref<JPH::PointConstraintSettings> settings = new JPH::PointConstraintSettings{};
        settings->mPoint1 = {0, 0, 0};
        settings->mPoint2 = {0, 0, 0};

        // settings->mNormalHalfConeAngle = std::numbers::pi / 2;
        // settings->mPlaneHalfConeAngle = std::numbers::pi / 2;
        // settings->mTwistMinAngle = std::numbers::pi / 2;
        // settings->mTwistMaxAngle = std::numbers::pi / 2;

        return create_ragdoll(std::vector{
            Ragdoll::PartSettings{
                "body", "", {2, 2, 2},
                {0, 0, 0}, glm::identity<glm::dquat>(), 0, 100.0, 1.0, nullptr
            },
            Ragdoll::PartSettings{
                "hand", "body", {2, 0.0625, 0.0625},
                {2.25, 0, 0}, glm::identity<glm::dquat>(), 1, 1, 0.0, settings

            }
        });
    }

    std::vector<std::shared_ptr<PlainObject>> changed_objects() const {
        std::vector<std::shared_ptr<PlainObject>> res{};
        for (auto obj : objects_) {
            if (obj->have_changed()) {
                res.push_back(obj);
            }
        }
        return res;
    }
};

#endif