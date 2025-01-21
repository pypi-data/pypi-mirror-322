cmake_minimum_required(VERSION 3.4...3.18)
project(core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

set(CORE_DIR ${CMAKE_CURRENT_LIST_DIR})

include(cmake/tweak_target.cmake)

add_library(core_src STATIC)
target_sources(core_src PRIVATE src/World.cpp src/PlainObject.cpp src/Ragdoll.cpp src/Octree.cpp)

tweak_target(core_src)

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(pybind11)
pybind11_add_module(core src/module.cpp)
target_link_libraries(core PRIVATE core_src)

tweak_target(core)

set(ENABLE_ALL_WARNINGS OFF)
add_subdirectory(JoltPhysics/Build)

if(NOT MSVC)
    target_compile_options(Jolt PRIVATE -fPIC)
endif()

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
add_subdirectory(googletest)
add_subdirectory(tests)
