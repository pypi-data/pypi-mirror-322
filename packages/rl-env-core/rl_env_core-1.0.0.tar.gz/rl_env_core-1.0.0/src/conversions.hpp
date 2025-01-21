#ifndef CONVERSIONS_HPP_
#define CONVERSIONS_HPP_

#include <Jolt/Jolt.h>

#include <glm/vec3.hpp>
#include <glm/gtc/quaternion.hpp>

template <typename T>
JPH::RVec3 to_jolt_rvec3(T vec) {
    return {static_cast<JPH::Real>(vec.x), static_cast<JPH::Real>(vec.y), static_cast<JPH::Real>(vec.z)};
}

template <typename T>
JPH::Vec3 to_jolt_vec3(T vec) {
    return {static_cast<float>(vec.x), static_cast<float>(vec.y), static_cast<float>(vec.z)};
}

template <typename T>
JPH::Quat to_jolt_quat(T quat) {
    return {static_cast<float>(quat.x), static_cast<float>(quat.y), static_cast<float>(quat.z),
            static_cast<float>(quat.w)};
}

template <typename T>
glm::dvec3 to_glm_dvec3(T vec) {
    return {static_cast<double>(vec.GetX()), static_cast<double>(vec.GetY()), static_cast<double>(vec.GetZ())};
}

template <typename T>
glm::dquat to_glm_dquat(T quat) {
    return { static_cast<double>(quat.GetW()),
             static_cast<double>(quat.GetX()), static_cast<double>(quat.GetY()), static_cast<double>(quat.GetZ())};
}

#endif