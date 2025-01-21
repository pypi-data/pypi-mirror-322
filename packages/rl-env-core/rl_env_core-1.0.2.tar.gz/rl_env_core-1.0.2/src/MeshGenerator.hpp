#ifndef MESH_GENERATOR_HPP_
#define MESH_GENERATOR_HPP_

#include "InOrderVisitor.hpp"

#include "Triangle.hpp"

#include <glm/glm.hpp>

#include <vector>

class MeshGenerator : public InOrderVisitor {
public:
    void visit_leaf(int material, glm::dvec3 position, glm::dvec3 extents) override {
        if (material != -1) {
            Triangle::add_box(mesh_, position, extents, material);
        }
    }

    const std::vector<Triangle>& mesh() const {
        return mesh_;
    }

    template <typename T, typename... Args>
    static std::vector<Triangle> visit(const T& t, Args&& ...args) {
        MeshGenerator generator{};
        t.accept(generator, std::forward<Args>(args)...);
        return generator.mesh();
    }
private:
    std::vector<Triangle> mesh_{};
};

#endif