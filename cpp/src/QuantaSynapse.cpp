#include "QuantaSynapse.h"

#include <iostream>

QuantaSynapse::QuantaSynapse() {
    std::cout << "QuantaSynapse constructor" << std::endl;
}

QuantaSynapse::~QuantaSynapse() {
    std::cout << "QuantaSynapse destructor" << std::endl;
}

void QuantaSynapse::connect() {
    std::cout << "Connecting to Quanta projects..." << std::endl;
}

void QuantaSynapse::disconnect() {
    std::cout << "Disconnecting from Quanta projects..." << std::endl;
}