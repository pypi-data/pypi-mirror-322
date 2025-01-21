#ifndef RAGDOLL_HPP_
#define RAGDOLL_HPP_

#include "PlainObject.hpp"

#include "Triangle.hpp"
#include "conversions.hpp"

#include <Jolt/Jolt.h>
#include <Jolt/Physics/Ragdoll/Ragdoll.h>
#include <Jolt/Physics/Constraints/PointConstraint.h>
#include <Jolt/Physics/PhysicsSystem.h>

#include <glm/glm.hpp>
#include <glm/gtc/quaternion.hpp>

#include <span>
#include <unordered_map>

class Ragdoll {
public:
    struct PartSettings {
        std::string name{};
        std::string parent_name{};

        glm::dvec3 size{};

        glm::dvec3 position{};
        glm::dquat rotation{};

        int material;

        double inertia;
        double gravity;

        JPH::Ref<JPH::PointConstraintSettings> constraint{};
    };

    Ragdoll(std::span<const PartSettings> parts, JPH::PhysicsSystem* system);

    void rotate(std::string_view body_part, glm::dquat rotation);
    void move(glm::dvec3 velocity);

    glm::dvec3 position(std::string_view body_part) const {
        return to_glm_dvec3(body_interface->GetPosition(body_id(body_part)));
    }

    glm::dvec3 velocity(std::string_view body_part) const {
        return to_glm_dvec3(body_interface->GetLinearVelocity(body_id(body_part)));
    }

    glm::dquat rotation(std::string_view body_part) const {
        return to_glm_dquat(body_interface->GetRotation(body_id(body_part)));
    }

    glm::dmat4x4 transform(std::string_view body_part) const {
        return glm::translate(glm::identity<glm::dmat4x4>(), position(body_part))
            * glm::mat4_cast(rotation(body_part));
    }

    void attach(std::string_view body_part, std::shared_ptr<PlainObject> object);

    void accept(InOrderVisitor& visitor, std::string_view body_part) const {
        const auto& shape = static_cast<const JPH::BoxShape&>(*body_interface->GetShape(body_id(body_part)));
        visitor.visit_leaf(materials.at(std::string{body_part}),
            to_glm_dvec3(-shape.GetHalfExtent()), to_glm_dvec3(2 * shape.GetHalfExtent()));
    }

    void remove() {
        ragdoll->RemoveFromPhysicsSystem();
        ragdoll = nullptr;
    }
private:
    JPH::Ref<JPH::Ragdoll> ragdoll;
    JPH::BodyInterface* body_interface = nullptr;
    JPH::PhysicsSystem* physics = nullptr;

    std::unordered_map<std::string, int> materials;

    JPH::BodyID body_id(std::string_view body_part) const {
        const auto& skeleton = ragdoll->GetRagdollSettings()->GetSkeleton();
        if (int joindIndex = skeleton->GetJointIndex(body_part); joindIndex != -1) {
            return ragdoll->GetBodyID(joindIndex);
        } else {
            throw std::logic_error{"invalid body part name"};
        }
    }
};

#endif