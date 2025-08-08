#include "QuantaSynapse.h"
#include <iostream>

QuantaSynapse::QuantaSynapse() : m_status(ConnectionStatus::DISCONNECTED) {
    std::cout << "QuantaSynapse constructor" << std::endl;
}

QuantaSynapse::~QuantaSynapse() {
    std::cout << "QuantaSynapse destructor" << std::endl;
}

void QuantaSynapse::connect() {
    std::cout << "Connecting to Quanta projects..." << std::endl;
    m_status = ConnectionStatus::CONNECTED;
}

void QuantaSynapse::disconnect() {
    std::cout << "Disconnecting from Quanta projects..." << std::endl;
    m_status = ConnectionStatus::DISCONNECTED;
}

ConnectionStatus QuantaSynapse::getStatus() const {
    return m_status;
}

void QuantaSynapse::setConfig(const Config& config) {
    m_config = config;
}

const Config& QuantaSynapse::getConfig() const {
    return m_config;
}