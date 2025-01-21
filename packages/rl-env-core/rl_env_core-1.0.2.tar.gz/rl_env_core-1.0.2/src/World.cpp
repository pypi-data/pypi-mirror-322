#include "World.hpp"

#define JPH_ENABLE_ASSERTS

World::World(glm::dvec3 gravity) {
    JPH::RegisterDefaultAllocator();

    JPH::Factory::sInstance = new JPH::Factory();

    JPH::RegisterTypes();

    temp_allocator = new JPH::TempAllocatorImpl{10 * 1024 * 1024};

    job_system = new JPH::JobSystemThreadPool{
        JPH::cMaxPhysicsJobs, JPH::cMaxPhysicsBarriers, static_cast<int>(std::thread::hardware_concurrency() - 1)
    };

    const JPH::uint max_bodies = 65536 * 4;
    const JPH::uint num_body_mutexes = 1;
    const JPH::uint max_body_pairs = 1024 * 4;
    const JPH::uint max_contact_constraints = 1024 * 4;

    physics_system.Init(max_bodies, num_body_mutexes, max_body_pairs, max_contact_constraints,
        broad_phase_layer_interface, object_vs_broadphase_layer_filter, object_vs_object_layer_filter);
    physics_system.SetGravity(to_jolt_vec3(gravity));

    body_interface = &physics_system.GetBodyInterface();

    physics_system.OptimizeBroadPhase();
}

World::~World() {
    for (auto& object : objects_) {
        object->remove();
    }

    for (auto& ragdoll : ragdolls_) {
        ragdoll->remove();
    }

    JPH::UnregisterTypes();

    delete JPH::Factory::sInstance;
    JPH::Factory::sInstance = nullptr;
}

std::shared_ptr<PlainObject> World::create(bool movable) {
    objects_.push_back(std::make_shared<PlainObject>(
        body_interface, &physics_system.GetBodyLockInterface(), movable));
    objects_.back()->update_body();
    return objects_.back();
}

std::shared_ptr<PlainObject> World::create_from_octree(Octree&& octree, bool movable) {
    objects_.push_back(std::make_shared<PlainObject>(std::move(octree),
        body_interface, &physics_system.GetBodyLockInterface(), movable));
    objects_.back()->update_body();
    return objects_.back();
}

void World::simulate_physics(int steps, double step_length) {
    for (int i = 0; i < steps; ++i) {
        const int collision_steps = 1;
        physics_system.Update(step_length, collision_steps, temp_allocator, job_system);
    }
}
