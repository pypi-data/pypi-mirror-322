#ifndef SKELETON_HPP
#define SKELETON_HPP

#include <memory>
#include <vector>
#include <string_view>
#include <glm/vec3.hpp>

using pPhysicalRepr = void*;

// struct BodyPart {
//     pPhysicalRepr physicalRepr;
//     virtual ~BodyPart() = 0;
// };

template <class T>
using pBodyPart = std::unique_ptr<T>;

// Wrapper, makes body part with one or zero next body part
template <class NextBodyPartT>
class WithNext {
protected:
    pBodyPart<NextBodyPartT> next;
public:
    WithNext() = default;
    WithNext(pBodyPart<NextBodyPartT>&& next){
        this->next = std::move(next);
    }

    NextBodyPartT* get_next(){
        return next.get();
    }

// ! Warning: destroys previous 'next object' !
    void reset_next(NextBodyPartT* p){
        next.reset(p);
    }

    pBodyPart<NextBodyPartT> swap_next(pBodyPart<NextBodyPartT> p){
        next.swap(p);
    }
};

template <class NextBodyPartT>
struct WithNextRequired : WithNext<NextBodyPartT> {
    WithNextRequired(pBodyPart<NextBodyPartT>&& next){
        if constexpr (next) {
            this->next = std::move(next);
        } else {
            static_assert(false, "Not-nullptr is required, nullptr is passed");
        }
    }
};

template <class NextBodyPartT>
struct Joint : WithNext<NextBodyPartT>{
    //TODO physics-related methods like 'move'
};

// struct Bone {
//     int get_length(){
//         //TODO
//         return 0;
//     }
//     int thickness = 1000;
//     Bone(std::string_view part_name){

//     }
// };

struct Offset {
    glm::dvec3 offset;
};


struct Eye {
    using MovingParameters = std::array<long double, 3>;
    struct State {
        std::array<long double, 3> dir;
        State(glm::dvec3 dir): dir{dir.x, dir.y, dir.z}{}
    };

    glm::dvec3 direction;
    Eye(glm::dvec3 direction) : direction(direction){}
    State get_state() {
        return State(direction);
    }
    void rotate(MovingParameters params) {
        //TODO
    }
};

/*// Maybe implement skeleton like this? 
// Describes body parts hierarchy
struct Skeleton {
    std::vector<pBodyPart<BodyPart>> origins;
    
    void add_body_part(pBodyPart&& p){
        origins.push_back(std::move(p));
    }
};*/// Is it useful?

#endif