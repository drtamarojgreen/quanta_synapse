#pragma once

#include <string>
#include <chrono>

// Signal structure
struct Signal {
    std::string sender;
    std::string receiver;
    std::string type;
    std::string content;
    float priorityScore;
    float ethicsScore;
    std::chrono::system_clock::time_point timestamp;
};
