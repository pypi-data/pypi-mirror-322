#ifndef LAYERS_HPP_
#define LAYERS_HPP_

#include <Jolt/Jolt.h>
#include <Jolt/Physics/PhysicsSystem.h>

namespace Layers {
    inline static constexpr JPH::ObjectLayer NON_MOVING = 0;
    inline static constexpr JPH::ObjectLayer MOVING = 1;
    inline static constexpr JPH::ObjectLayer NUM_LAYERS = 2;
};

#endif