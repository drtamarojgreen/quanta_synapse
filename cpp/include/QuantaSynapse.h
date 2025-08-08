#pragma once

#include <string>

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
    QuantaSynapse();
    ~QuantaSynapse();

    // Connection lifecycle
    void connect();
    void disconnect();
    ConnectionStatus getStatus() const;

    // Configuration management
    void setConfig(const Config& config);
    const Config& getConfig() const;

private:
    ConnectionStatus m_status;
    Config m_config;
};