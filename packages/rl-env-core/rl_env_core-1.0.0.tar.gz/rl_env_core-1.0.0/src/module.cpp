#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

#include "World.hpp"
#include "Triangle.hpp"
#include "BBox.hpp"
#include "PlainObject.hpp"
#include "Ragdoll.hpp"
#include "Creature.hpp"
#include "MeshGenerator.hpp"
#include "to_string.hpp"

#include <glm/vec3.hpp>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace py::literals;

#define JPH_ENABLE_ASSERTS

PYBIND11_MODULE(core, m) {
    m.doc() = "Environment module";

    py::class_<World>(m, "World")
        .def(py::init<>())
        .def(py::init<glm::dvec3>())
        .def_property_readonly("objects", &World::objects)
        .def("create", &World::create, "movable"_a = true)
        .def("remove", &World::remove)
        .def("simulate_physics", &World::simulate_physics, "steps"_a = 1, "step_length"_a = 1.0 / 60.0)
        .def("create_test_ragdoll", &World::create_test_ragdoll);

    py::class_<glm::dvec3>(m, "Vec3")
        .def(py::init<double, double, double>())
        .def_readwrite("x", &glm::dvec3::x)
        .def_readwrite("y", &glm::dvec3::y)
        .def_readwrite("z", &glm::dvec3::z)
        .def(py::self == py::self)
        .def(py::self + py::self)
        .def(py::self += py::self)
        .def(-py::self)
        .def(py::self - py::self)
        .def(py::self -= py::self)
        .def(py::self * double())
        .def(double() * py::self)
        .def(py::self *= double())
        .def(py::self / double())
        .def(py::self /= double())
        .def("__repr__", &vec3_to_string);

    py::class_<glm::dvec4>(m, "Vec4")
        .def(py::init<double, double, double, double>())
        .def_readwrite("x", &glm::dvec4::x)
        .def_readwrite("y", &glm::dvec4::y)
        .def_readwrite("z", &glm::dvec4::z)
        .def_readwrite("w", &glm::dvec4::w)
        .def(py::self == py::self)
        .def(py::self + py::self)
        .def(py::self += py::self)
        .def(-py::self)
        .def(py::self - py::self)
        .def(py::self -= py::self)
        .def(py::self * double())
        .def(double() * py::self)
        .def(py::self *= double())
        .def(py::self / double())
        .def(py::self /= double())
        .def("__repr__", &vec4_to_string);

    py::class_<glm::dmat4x4>(m, "Mat4x4")
        .def(py::init<double, double, double, double,
                      double, double, double, double,
                      double, double, double, double,
                      double, double, double, double>())
        .def(py::init<glm::dvec4, glm::dvec4, glm::dvec4, glm::dvec4>())
        .def(py::self * py::self)
        .def("__getitem__", [](glm::dmat4x4 mat, int i) {
            return mat[i];
        })
        .def("__setitem__", [](glm::dmat4x4 mat, int i, glm::dvec4 vec) {
            mat[i] = vec;
        })
        .def("__getitem__", [](glm::dmat4x4 mat, py::tuple indices) {
            return mat[indices[0].cast<int>()][indices[1].cast<int>()];
        })
        .def("__setitem__", [](glm::dmat4x4 mat, py::tuple indices, double value) {
            mat[indices[0].cast<int>()][indices[1].cast<int>()] = value;
        })
        .def(py::self * glm::dvec4{})
        .def(glm::dvec4{} * py::self)
        .def("__mul__", [](glm::dmat4x4 mat, glm::dvec3 vec) {
            auto res = mat * glm::dvec4{vec, 1.0};
            return glm::dvec3{res.x, res.y, res.z};
        })
        .def("__repr__", &mat4x4_to_string)
        .def("nearly_equal", [](glm::dmat4x4 lhs, glm::dmat4x4 rhs, double precision) {
            for (int i = 0; i < 4; ++i) {
                for (int j = 0; j < 4; ++j) {
                    if (std::abs(lhs[i][j] - rhs[i][j]) > precision) {
                        return false;
                    }
                }
            }
            return true;
        });

    m.def("angleAxis", &glm::angleAxis<double, glm::defaultp>);

    py::class_<glm::dquat>(m, "Quat")
        .def_property_readonly("angle", &glm::angle<double, glm::defaultp>)
        .def_property_readonly("axis", &glm::axis<double, glm::defaultp>)
        .def(py::self == py::self)
        .def("__mul__", [](glm::dquat lhs, glm::dquat rhs) {
            return lhs * rhs;
        })
        .def("__repr__", &quat_to_string)
        .def_readwrite("x", &glm::dquat::x)
        .def_readwrite("y", &glm::dquat::y)
        .def_readwrite("z", &glm::dquat::z)
        .def_readwrite("w", &glm::dquat::w);

    py::class_<Triangle>(m, "Triangle")
        .def(py::init<glm::dvec3, glm::dvec3, glm::dvec3, int>())
        .def_readwrite("a", &Triangle::a)
        .def_readwrite("b", &Triangle::b)
        .def_readwrite("c", &Triangle::c)
        .def_readwrite("material", &Triangle::material)
        .def(py::self == py::self)
        .def("__repr__", &Triangle::to_string);

    py::class_<BBox>(m, "BBox")
        .def(py::init<glm::dvec3, glm::dvec3>())
        .def(py::init<glm::dvec3, double>())
        .def(py::self == py::self)
        .def("__bool__", &BBox::operator bool)
        .def_property_readonly("size" , &BBox::size)
        .def_property_readonly("width" , &BBox::width)
        .def_property_readonly("height", &BBox::height)
        .def_property_readonly("length", &BBox::length)
        .def_property_readonly("origin" , &BBox::origin)
        .def_property_readonly("left"  , &BBox::left)
        .def_property_readonly("top"   , &BBox::top)
        .def_property_readonly("front" , &BBox::front)
        .def_property_readonly("right" , &BBox::right)
        .def_property_readonly("bottom", &BBox::bottom)
        .def_property_readonly("back"  , &BBox::back)
        .def("__contains__", &BBox::contains)
        .def("contains", &BBox::contains)
        .def("__and__", &BBox::intersection)
        .def("intersection", &BBox::intersection)
        .def("intersects", &BBox::intersects)
        .def("isdisjoint", &BBox::is_disjoint)
        .def("issuperset", &BBox::is_superset)
        .def("issubset", &BBox::is_subset)
        .def("__le__", &BBox::is_subset)
        .def("__lt__", &BBox::is_strict_subset)
        .def("translated", &BBox::translated)
        .def("scaled", &BBox::scaled);

    py::class_<PlainObject, std::shared_ptr<PlainObject>>(m, "PlainObject")
        .def("is_filled", &PlainObject::is_filled)
        .def("fill" , &PlainObject::fill , "p"_a, "material"_a, "max_depth"_a=5)
        .def("carve", &PlainObject::carve, "p"_a, "max_depth"_a=5)
        .def("debug_tree_repr", &PlainObject::debug_tree_repr)
        .def("generate_mesh", [](std::shared_ptr<PlainObject> object) {
            return MeshGenerator::visit(*object);
        })
        .def_property_readonly("changed", &PlainObject::have_changed)
        .def("clear_changed", &PlainObject::clear_changed)
        .def_property("position", &PlainObject::position, &PlainObject::set_position)
        .def("move", &PlainObject::move)
        .def_property("rotation", &PlainObject::rotation, &PlainObject::set_rotation)
        .def("rotate", &PlainObject::rotate)
        .def_property_readonly("transform", &PlainObject::transform);

    py::class_<Ragdoll, std::shared_ptr<Ragdoll>>(m, "Ragdoll")
        .def("generate_mesh", [](std::shared_ptr<Ragdoll> ragdoll, std::string_view body_part) {
            return MeshGenerator::visit(*ragdoll, body_part);
        })
        .def("transform", &Ragdoll::transform)
        .def("move", &Ragdoll::move)
        .def("rotate", &Ragdoll::rotate)
        .def("attach", &Ragdoll::attach);

    py::class_<OneHandOneEyeCreature>(m, "OneHandOneEyeCreature")
        .def(py::init<World*>())
        .def("get_ragdoll", &OneHandOneEyeCreature::get_ragdoll);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
