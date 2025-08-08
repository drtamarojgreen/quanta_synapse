#include "QuantaSynapse.h"
#include <iostream>
#include <chrono>

QuantaSynapse::QuantaSynapse() :
    m_status(ConnectionStatus::DISCONNECTED),
    m_runHeartbeat(false),
    m_messagesSent(0),
    m_messagesReceived(0)
{
    std::cout << "QuantaSynapse constructor" << std::endl;
}

QuantaSynapse::~QuantaSynapse() {
    if (m_status.load() == ConnectionStatus::CONNECTED) {
        disconnect();
    }
    std::cout << "QuantaSynapse destructor" << std::endl;
}

void QuantaSynapse::connect() {
    std::cout << "Connecting to Quanta projects..." << std::endl;
    m_status.store(ConnectionStatus::CONNECTING);

    // Simulate connection delay
    std::this_thread::sleep_for(std::chrono::seconds(1));

    m_status.store(ConnectionStatus::CONNECTED);
    std::cout << "Connection established." << std::endl;

    if (m_onConnected) {
        m_onConnected();
    }

    m_runHeartbeat.store(true);
    m_heartbeatThread = std::thread(&QuantaSynapse::heartbeatLoop, this);
}

void QuantaSynapse::disconnect() {
    std::cout << "Disconnecting from Quanta projects..." << std::endl;
    m_status.store(ConnectionStatus::DISCONNECTING);

    if (m_runHeartbeat.load()) {
        m_runHeartbeat.store(false);
        if (m_heartbeatThread.joinable()) {
            m_heartbeatThread.join();
        }
    }

    m_status.store(ConnectionStatus::DISCONNECTED);
    std::cout << "Disconnected." << std::endl;

    if (m_onDisconnected) {
        m_onDisconnected();
    }
}

ConnectionStatus QuantaSynapse::getStatus() const {
    return m_status.load();
}

void QuantaSynapse::setConfig(const Config& config) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_config = config;
}

const Config& QuantaSynapse::getConfig() const {
    return m_config;
}

void QuantaSynapse::subscribe(const std::string& topic, SignalCallback callback) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_subscriptions[topic].push_back(callback);
}

void QuantaSynapse::publish(const std::string& topic, const Signal& signal) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_messagesSent++;
    if (m_subscriptions.find(topic) != m_subscriptions.end()) {
        for (const auto& callback : m_subscriptions[topic]) {
            callback(signal);
            m_messagesReceived++; // Simulating receipt by a subscriber
        }
    }
}

void QuantaSynapse::setOnConnected(StatusCallback callback) {
    m_onConnected = callback;
}

void QuantaSynapse::setOnDisconnected(StatusCallback callback) {
    m_onDisconnected = callback;
}

void QuantaSynapse::setOnError(ErrorCallback callback) {
    m_onError = callback;
}

long QuantaSynapse::getMessagesSent() const {
    return m_messagesSent.load();
}

long QuantaSynapse::getMessagesReceived() const {
    return m_messagesReceived.load();
}

void QuantaSynapse::heartbeatLoop() {
    while (m_runHeartbeat.load()) {
        std::this_thread::sleep_for(std::chrono::seconds(5));
        if (m_runHeartbeat.load()) {
            Signal heartbeatSignal;
            heartbeatSignal.sender = "QuantaSynapse";
            heartbeatSignal.type = "system.heartbeat";
            heartbeatSignal.content = "ping";
            heartbeatSignal.timestamp = std::chrono::system_clock::now();
            publish("system.heartbeat", heartbeatSignal);
        }
    }
}