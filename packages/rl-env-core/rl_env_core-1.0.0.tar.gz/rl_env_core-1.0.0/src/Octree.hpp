#ifndef OCTREE_HPP_
#define OCTREE_HPP_

#include "BBox.hpp"
#include "InOrderVisitor.hpp"

#include <glm/glm.hpp>

#include <variant>
#include <string>
#include <array>
#include <memory>

class PlainObject;

class Octree {
    struct Leaf {
        int material = -1;
    };

    using Branch = std::array<Octree, 8>;

    std::variant<Leaf, std::unique_ptr<Branch>> node{Leaf{}};

    inline static const BBox bounding_box{{0, 0, 0}, 1};
    inline static const std::array children_bounding_boxes{
        BBox{{0  , 0  , 0  }, 0.5},
        BBox{{0  , 0  , 0.5}, 0.5},
        BBox{{0  , 0.5, 0  }, 0.5},
        BBox{{0  , 0.5, 0.5}, 0.5},
        BBox{{0.5, 0  , 0  }, 0.5},
        BBox{{0.5, 0  , 0.5}, 0.5},
        BBox{{0.5, 0.5, 0  }, 0.5},
        BBox{{0.5, 0.5, 0.5}, 0.5}
    };

    static glm::dvec3 in_child_coordinates(glm::dvec3 pos, int child_id) {
        return 2.0 * (pos - children_bounding_boxes[child_id].origin());
    }

    static BBox in_child_coordinates(BBox p, int child_id) {
        return {in_child_coordinates(p.origin(), child_id), 2.0 * p.size()};
    }
public:
    Octree() = default;

    Octree(int material) : node{Leaf{material}} {}

    Octree(const Octree& other) {
        std::visit([this]<typename T>(const T& node) {
            if constexpr (std::same_as<T, Leaf>) {
                this->node = node;
            } else {
                this->node = std::make_unique<Branch>(*node);
            }
        }, other.node);
    }

    Octree& operator = (const Octree& other) {
        std::visit([this]<typename T>(const T& node) {
            if constexpr (std::same_as<T, Leaf>) {
                this->node = node;
            } else {
                this->node = std::make_unique<Branch>(*node);
            }
        }, other.node);
        return *this;
    }

    int material_at(glm::dvec3 pos) const;

    void fill(BBox p, int material, int max_depth);

    void cut(BBox p, glm::dvec3 position, double scale, PlainObject& result, int max_depth);

    std::string debug_tree_repr(std::string indent) const;

    std::pair<glm::dvec3, double> expand_to_include(BBox to_include);

    void accept(InOrderVisitor& visitor, glm::dvec3 pos, double scale) const;
};

#endif