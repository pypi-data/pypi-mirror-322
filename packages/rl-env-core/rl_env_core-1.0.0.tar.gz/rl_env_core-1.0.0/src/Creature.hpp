#ifndef CREATURE_HPP
#define CREATURE_HPP

#include "Skeleton.hpp"
#include "Ragdoll.hpp"
#include "World.hpp"

#include <memory>
/*
class Creature {
public:
    Creature(){};
    // virtual void perform_step_actions() = 0;
    virtual ~Creature() = 0;
};*/


class OneHandOneEyeCreature /*: Creature*/ {

    class Hand {
        // Bone b1;
        // Bone b2;
        std::vector<Ragdoll::PartSettings> parts_settings;

    public:
        using State = std::vector<glm::dvec3>;
        using MovingParameters = std::vector<glm::dvec3>;

        Hand() : parts_settings() {
        // -[x] make physical hand (TODO)
        // -[x] make logical hand
        // -[] attach physical hand to logical (TODO)
            parts_settings.push_back(Ragdoll::PartSettings{
                "root", "", {0.5, 0.5, 0.5},
                {0, 0, 0}, glm::identity<glm::dquat>(), 0, 1000000.0, 0.0, nullptr
            });

            JPH::Ref<JPH::PointConstraintSettings> j1 = new JPH::PointConstraintSettings{};

            parts_settings.push_back(Ragdoll::PartSettings{
                "bone1", "root", {0.0625, 2, 0.0625},
                {0, 1, 0}, glm::identity<glm::dquat>(), 1, 1.0, 0.0, j1
            });

            JPH::Ref<JPH::PointConstraintSettings> j2 = new JPH::PointConstraintSettings{};
            j2->mPoint1 = {0,2,0};
            j2->mPoint2 = {0,2,0};

            parts_settings.push_back(Ragdoll::PartSettings{
                "bone2", "bone1", {0.0625, 0.0625, 2},
                {0, 2, 1}, glm::identity<glm::dquat>(), 1, 1.0, 0.0, j2
            });
        }

        const std::vector<Ragdoll::PartSettings>& get_parts_settings(){
            return parts_settings;
        }

        State get_state(){
            //TODO
            return State();
        }

        void move(MovingParameters params){
            //TODO
        }
    };
    std::shared_ptr<Ragdoll> ragdoll;
    Eye eye;
    Hand hand; // This I called "implicit skeleton" because there are no Skeleton class.
    //class Time lifespan maybe?
public:
    OneHandOneEyeCreature(World* world/*, HandSettings hand_settings*/)
    : eye(glm::dvec3(1.l,0.l,0.l)), hand(/*hand_settings*/) {
        ragdoll = world->create_ragdoll(hand.get_parts_settings());
    }

    void spawn(/*SpawnParameters summon_params*/) {

    }

    std::shared_ptr<Ragdoll> get_ragdoll(){
        return ragdoll;
    }

    Hand::State get_hand_state() {
        return hand.get_state();
    }

    void move_hand(Hand::MovingParameters params){
        return hand.move(params);
    }

    Eye::State get_eye_state(){
        return eye.get_state();
    }

    void move_eye(Eye::MovingParameters params){
        eye.rotate(params);
    }
};

#endif