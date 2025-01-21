#include "Ragdoll.hpp"

#include "conversions.hpp"

#include <Jolt/Physics/Constraints/PointConstraint.h>
#include <Jolt/Physics/Constraints/FixedConstraint.h>
#include <Jolt/Physics/Collision/Shape/BoxShape.h>

Ragdoll::Ragdoll(std::span<const PartSettings> parts, JPH::PhysicsSystem* system) {
    physics = system;
    body_interface = &physics->GetBodyInterface();

    JPH::Ref<JPH::RagdollSettings> settings = new JPH::RagdollSettings{};
    settings->mSkeleton = new JPH::Skeleton{};
    for (const PartSettings& part : parts) {
        settings->mSkeleton->AddJoint(part.name, part.parent_name);
    }
    settings->mSkeleton->CalculateParentJointIndices();

    for (const PartSettings& part : parts) {
        JPH::RagdollSettings::Part jolt_part;

        auto halfExtent = to_jolt_vec3(part.size / 2.0);
        JPH::Ref<JPH::ShapeSettings> shape_settings = new JPH::BoxShapeSettings{halfExtent, 0.0};
        auto shape = shape_settings->Create();
        if (shape.HasError()) {
            throw std::runtime_error{shape.GetError().c_str()};
        }
        jolt_part.SetShape(shape.Get());

        jolt_part.mPosition = to_jolt_vec3(part.position);
        jolt_part.mRotation = to_jolt_quat(part.rotation);
        jolt_part.mMotionType = JPH::EMotionType::Dynamic;
        jolt_part.mObjectLayer = Layers::MOVING;

        if (!part.parent_name.empty()) {
            jolt_part.mToParent = part.constraint;
        }

        jolt_part.mInertiaMultiplier = part.inertia;
        jolt_part.mGravityFactor = part.gravity;

        settings->mParts.push_back(std::move(jolt_part));

        materials.try_emplace(part.name, part.material);
    }

    settings->CalculateBodyIndexToConstraintIndex();
    settings->DisableParentChildCollisions();
    ragdoll = settings->CreateRagdoll(JPH::CollisionGroup::GroupID{1}, 0, physics);

    ragdoll->AddToPhysicsSystem(JPH::EActivation::Activate);
}

void Ragdoll::rotate(std::string_view body_part, glm::dquat rotation) {
    const auto* settings = ragdoll->GetRagdollSettings();
    int body_part_index = settings->GetSkeleton()->GetJointIndex(body_part);
    JPH::BodyID body_id = ragdoll->GetBodyID(body_part_index);
    body_interface->SetAngularVelocity(body_id,
        to_jolt_vec3(glm::eulerAngles(rotation)) * to_jolt_vec3(glm::eulerAngles(rotation)));

    auto& constraint = static_cast<JPH::PointConstraintSettings&>(*settings->mParts[body_part_index].mToParent);
    auto constraint_position = constraint.mPoint2;

    auto body_part_position = body_interface->GetPosition(body_id);
    auto velocity = constraint_position + to_jolt_quat(rotation) * (body_part_position - constraint_position) - body_part_position;
    // body_interface->SetLinearVelocity(body_id, -velocity);
}

void Ragdoll::move(glm::dvec3 body_velocity) {
    const auto* settings = ragdoll->GetRagdollSettings();

    JPH::SkeletonPose pose;
    pose.SetSkeleton(ragdoll->GetRagdollSettings()->GetSkeleton());
    ragdoll->GetPose(pose);

    for (int i = 1; i < ragdoll->GetBodyCount(); ++i) {
        auto velocity = body_interface->GetLinearVelocity(ragdoll->GetBodyID(i));
        auto angular_velocity = body_interface->GetAngularVelocity(ragdoll->GetBodyID(i));

        pose.GetJoint(i).mTranslation += velocity + to_jolt_vec3(body_velocity);
        pose.GetJoint(i).mRotation = pose.GetJoint(i).mRotation * JPH::Quat::sEulerAngles(angular_velocity);
    }

    pose.GetJoint(0).mTranslation += to_jolt_vec3(body_velocity);
    if (body_velocity.y == 0) {
        pose.GetJoint(0).mTranslation.SetY(pose.GetJoint(0).mTranslation.GetY()
            + body_interface->GetLinearVelocity(ragdoll->GetBodyID(0)).GetY());
    }

    pose.CalculateJointMatrices();
    ragdoll->DriveToPoseUsingKinematics(pose, 1.0);
}

void Ragdoll::attach(std::string_view body_part, std::shared_ptr<PlainObject> object) {
    int body_part_index = ragdoll->GetRagdollSettings()->GetSkeleton()->GetJointIndex(body_part);
    JPH::BodyID body_id = ragdoll->GetBodyID(body_part_index);

    JPH::Ref<JPH::FixedConstraintSettings> constraint = new JPH::FixedConstraintSettings{};
    constraint->mAutoDetectPoint = true;
    physics->AddConstraint(body_interface->CreateConstraint(constraint, body_id, object->body_id()));
}
