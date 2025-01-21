#include "Octree.hpp"

#include "PlainObject.hpp"

int Octree::material_at(glm::dvec3 pos) const {
    return std::visit([pos]<typename T>(const T& node) {
        if constexpr (std::same_as<T, Leaf>) {
            return node.material;
        } else {
            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                if (children_bounding_boxes[i].contains(pos)) {
                    return (*node)[i].material_at(in_child_coordinates(pos, i));
                }
            }
            return -1;
        }
    }, node);
}

void Octree::fill(BBox p, int material, int max_depth) {
    if (bounding_box.is_disjoint(p)) {
        return;
    }

    if (max_depth <= 0 || bounding_box.is_subset(p)) {
        node = Leaf{material};
        return;
    }

    auto branch = std::visit([]<typename T>(T& node) {
        if constexpr (std::same_as<T, Leaf>) {
            auto res = std::make_unique<Branch>();
            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                (*res)[i] = Octree{node.material};
            }
            return res;
        } else {
            return std::move(node);
        }
    }, node);

    for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
        (*branch)[i].fill(in_child_coordinates(p, i), material, max_depth - 1);
    }
    node = std::move(branch);
}

void Octree::cut(BBox to_cut, glm::dvec3 position, double scale, PlainObject& result, int max_depth) {
    if (bounding_box.is_disjoint(to_cut)) {
        return;
    }

    std::visit([&]<typename T>(T& actual_node) {
        if constexpr (std::same_as<T, Leaf>) {
            if (max_depth <= 0 || bounding_box.is_subset(to_cut)) {
                if (actual_node.material != -1) {
                    result.fill(bounding_box.scaled(scale).translated(position), actual_node.material);
                }
                node = Leaf{-1};
            } else {
                auto res = std::make_unique<Branch>();
                for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                    (*res)[i] = Octree{actual_node.material};
                    (*res)[i].cut(in_child_coordinates(to_cut, i),
                        position + children_bounding_boxes[i].origin() * scale, scale / 2, result, max_depth - 1);
                }
                node = std::move(res);
            }
        } else {
            if (max_depth <= 0) {
                node = Leaf{-1};
                return;
            }

            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                (*actual_node)[i].cut(in_child_coordinates(to_cut, i),
                    position + children_bounding_boxes[i].origin() * scale, scale / 2, result, max_depth - 1);
            }

            if (bounding_box.is_subset(to_cut)) {
                node = Leaf{-1};
            }
        }
    }, node);
}

std::string Octree::debug_tree_repr(std::string indent) const {
    return std::visit([indent]<typename T>(const T& node) -> std::string {
        if constexpr (std::same_as<T, Leaf>) {
            return indent + std::to_string(node.material) + "\n";
        } else {
            std::string res = indent + "branch\n";
            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                res += (*node)[i].debug_tree_repr(indent + "    ");
            }
            return res;
        }
    }, node);
}

std::pair<glm::dvec3, double> Octree::expand_to_include(BBox to_include) {
    glm::dvec3 offset{};
    double scale = 1;

    while (true) {
        auto current = to_include.scaled(scale).translated(offset);
        if (bounding_box.is_superset(current)) {
            break;
        }

        Branch branch{};

        scale /= 2;
        offset /= 2;

        if (current.right()  > bounding_box.right()
            && current.bottom() > bounding_box.bottom()
            && current.front()  < bounding_box.front()) {
            branch[1] = std::move(*this);
            offset += glm::dvec3{0, 0, 1};
        } else if (current.right()  > bounding_box.right()
            && current.top()    < bounding_box.top()
            && current.back()   > bounding_box.back()) {
            branch[2] = std::move(*this);
            offset += glm::dvec3{0, 1, 0};
        } else if (current.right()  > bounding_box.right()
            && current.top()    < bounding_box.top()
            && current.front()  < bounding_box.front()) {
            branch[3] = std::move(*this);
            offset += glm::dvec3{0, 1, 1};
        } else if (current.left()   < bounding_box.left()
            && current.bottom() > bounding_box.bottom()
            && current.back()   > bounding_box.back()) {
            branch[4] = std::move(*this);
            offset += glm::dvec3{1, 0, 0};
        } else if (current.left()   < bounding_box.left()
            && current.bottom() > bounding_box.bottom()
            && current.front()  < bounding_box.front()) {
            branch[5] = std::move(*this);
            offset += glm::dvec3{1, 0, 1};
        } else if (current.left()   < bounding_box.left()
            && current.top()    < bounding_box.top()
            && current.back()   > bounding_box.back()) {
            branch[6] = std::move(*this);
            offset += glm::dvec3{1, 1, 0};
        } else if (current.right()  > bounding_box.right()
            || current.bottom() > bounding_box.bottom()
            || current.back()   > bounding_box.back()) {
            branch[0] = std::move(*this);
            offset += glm::dvec3{0, 0, 0};
        } else if (current.left()   < bounding_box.left()
            || current.top()    < bounding_box.top()
            || current.front()  < bounding_box.front()) {
            branch[7] = std::move(*this);
            offset += glm::dvec3{1, 1, 1};
        }

        node = std::make_unique<Branch>(branch);
    }
    return {offset, scale};
}

void Octree::accept(InOrderVisitor& visitor, glm::dvec3 pos, double scale) const {
    std::visit([&]<typename T>(const T& node) {
        if constexpr (std::same_as<T, Leaf>) {
            visitor.visit_leaf(node.material, pos, {scale, scale, scale});
        } else {
            for (int i = 0; i < std::ssize(children_bounding_boxes); ++i) {
                (*node)[i].accept(visitor, pos + scale * children_bounding_boxes[i].origin(), scale / 2);
            }
        }
    }, node);
}
