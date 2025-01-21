#ifndef PARALLELEPIPED_HPP
#define PARALLELEPIPED_HPP

#include <glm/vec3.hpp>

class BBox {
    glm::dvec3 origin_;
    glm::dvec3 size_;
public:
    BBox(glm::dvec3 origin, glm::dvec3 size) : origin_{origin}, size_{size} {}
    BBox(glm::dvec3 origin, double size) : origin_{origin}, size_{size, size, size} {}

    friend bool operator == (BBox, BBox) = default;

    explicit operator bool() const {
        return width() > 0 && height() > 0 && length() > 0;
    }

    glm::dvec3 size() const {
        return size_;
    }

    double width() const {
        return size_.x;
    }

    double height() const {
        return size_.y;
    }

    double length() const {
        return size_.z;
    }

    glm::dvec3 origin() const {
        return origin_;
    }

    double left() const {
        return origin_.x;
    }

    double top() const {
        return origin_.y;
    }

    double front() const {
        return origin_.z;
    }

    double right() const {
        return left() + width();
    }

    double bottom() const {
        return top() + height();
    }

    double back() const {
        return front() + length();
    }

    bool contains(glm::dvec3 point) const {
        return left()  <= point.x && point.x < right()
            && top()   <= point.y && point.y < bottom()
            && front() <= point.z && point.z < back();
    }

    BBox intersection(BBox other) const {
        glm::dvec3 left_top_front   {std::max(left() , other.left()),
                                    std::max(top()  , other.top()),
                                    std::max(front(), other.front())};
        glm::dvec3 right_bottom_back{std::min(right() , other.right()),
                                    std::min(bottom(), other.bottom()),
                                    std::min(back()  , other.back())};

        return {left_top_front, right_bottom_back - left_top_front};
    }

    bool intersects(BBox other) const {
        return static_cast<bool>(intersection(other));
    }

    bool is_disjoint(BBox other) const {
        return !intersects(other);
    }

    bool is_superset(BBox other) const {
        return left()  <= other.left()  && other.right()  <= right()
            && top()   <= other.top()   && other.bottom() <= bottom()
            && front() <= other.front() && other.back()   <= back();
    }

    bool is_strict_superset(BBox other) const {
        return *this != other && is_superset(other);
    }

    bool is_subset(BBox other) const {
        return other.is_superset(*this);
    }

    bool is_strict_subset(BBox other) const {
        return *this != other && is_subset(other);
    }

    BBox translated(glm::dvec3 offset) const {
        return {origin() + offset, size()};
    }

    BBox scaled(double scale) const {
        return {scale * origin(), scale * size()};
    }
};

#endif