#ifndef IN_ORDER_VISITOR_HPP_
#define IN_ORDER_VISITOR_HPP_

#include <glm/glm.hpp>

class InOrderVisitor {
public:
    virtual void visit_leaf(int materail, glm::dvec3 position, glm::dvec3 extents) = 0;
};

#endif