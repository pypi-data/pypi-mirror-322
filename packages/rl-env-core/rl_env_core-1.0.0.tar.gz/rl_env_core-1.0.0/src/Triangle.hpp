#ifndef TRIANGLE_HPP_
#define TRIANGLE_HPP_

#include "to_string.hpp"

#include <glm/vec3.hpp>

#include <format>
#include <iostream>

struct Triangle {
    glm::dvec3 a;
    glm::dvec3 b;
    glm::dvec3 c;
    int material;

    friend bool operator == (Triangle, Triangle) = default;

    std::string to_string() const {
        return std::format("Triangle({}, {}, {}, {})", 
            vec3_to_string(a), vec3_to_string(b), vec3_to_string(c), material);
    }

    friend std::ostream& operator << (std::ostream& os, Triangle triangle) {
        return os << triangle.to_string();
    }

    static void add_quad(std::vector<Triangle>& mesh, glm::dvec3 pos, double scale,
                         glm::dvec3 a, glm::dvec3 b, glm::dvec3 c, glm::dvec3 d, int material) {
        mesh.emplace_back(pos + scale * a, pos + scale * b, pos + scale * c, material);
        mesh.emplace_back(pos + scale * b, pos + scale * d, pos + scale * c, material);
    }

    static void add_box(std::vector<Triangle>& mesh, glm::dvec3 pos, glm::dvec3 size, int material) {
        add_quad(mesh, pos, 1.0, glm::dvec3{0,      0,      0     }, glm::dvec3{0,      0,      size.z}, 
                                 glm::dvec3{0,      size.y, 0     }, glm::dvec3{0,      size.y, size.z}, material);
        add_quad(mesh, pos, 1.0, glm::dvec3{size.x, 0,      0     }, glm::dvec3{size.x, size.y, 0     },
                                 glm::dvec3{size.x, 0,      size.z}, glm::dvec3{size.x, size.y, size.z}, material);
        add_quad(mesh, pos, 1.0, glm::dvec3{0,      0,      0     }, glm::dvec3{size.x, 0,      0     },
                                 glm::dvec3{0,      0,      size.z}, glm::dvec3{size.x, 0,      size.z}, material);
        add_quad(mesh, pos, 1.0, glm::dvec3{0,      size.y, 0     }, glm::dvec3{0,      size.y, size.z},
                                 glm::dvec3{size.x, size.y, 0     }, glm::dvec3{size.x, size.y, size.z}, material);
        add_quad(mesh, pos, 1.0, glm::dvec3{0,      0,      0     }, glm::dvec3{0,      size.y, 0     },
                                 glm::dvec3{size.x, 0,      0     }, glm::dvec3{size.x, size.y, 0     }, material);
        add_quad(mesh, pos, 1.0, glm::dvec3{0,      0,      size.z}, glm::dvec3{size.x, 0,      size.z},
                                 glm::dvec3{0,      size.y, size.z}, glm::dvec3{size.x, size.y, size.z}, material);
    }

    static std::vector<Triangle> make_box(glm::dvec3 pos, glm::dvec3 size, int material) {
        std::vector<Triangle> mesh;
        add_box(mesh, pos, size, material);
        return mesh;
    }
};

#endif