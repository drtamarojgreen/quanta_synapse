#pragma once

#include "Signal.h"
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <thread>
#include <atomic>
#include <mutex>
#include <chrono>

// Enum for connection status
enum class ConnectionStatus {
    DISCONNECTED,
    CONNECTING,
    CONNECTED,
    DISCONNECTING,
    ERROR
};

// Struct for configuration
struct Config {
    std::string host;
    int port = 0;
    std::string api_key;
    int timeout_ms = 10000; // Default timeout 10 seconds
};

class QuantaSynapse {
public:
    using SignalCallback = std::function<void(const Signal&)>;
    using StatusCallback = std::function<void()>;
    using ErrorCallback = std::function<void(const std::string&)>;

    QuantaSynapse();
    ~QuantaSynapse();

    // Connection lifecycle
    void connect();
    void disconnect();
    ConnectionStatus getStatus() const;

    // Configuration management
    void setConfig(const Config& config);
    const Config& getConfig() const;

    // Publish-Subscribe
    void subscribe(const std::string& topic, SignalCallback callback);
    void publish(const std::string& topic, const Signal& signal);

    // Event Callbacks
    void setOnConnected(StatusCallback callback);
    void setOnDisconnected(StatusCallback callback);
    void setOnError(ErrorCallback callback);

    // Metrics
    long getMessagesSent() const;
    long getMessagesReceived() const;

private:
    void heartbeatLoop();

    std::atomic<ConnectionStatus> m_status;
    Config m_config;

    std::map<std::string, std::vector<SignalCallback>> m_subscriptions;
    std::mutex m_mutex;

    std::thread m_heartbeatThread;
    std::atomic<bool> m_runHeartbeat;

    std::atomic<long> m_messagesSent;
    std::atomic<long> m_messagesReceived;

    StatusCallback m_onConnected;
    StatusCallback m_onDisconnected;
    ErrorCallback m_onError;
};