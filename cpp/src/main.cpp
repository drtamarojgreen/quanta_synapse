#include "QuantaSynapse.h"
#include <iostream>
#include <chrono>
#include <thread>

// Helper function to print a signal
void printSignal(const Signal& s) {
    auto time_point = std::chrono::system_clock::to_time_t(s.timestamp);
    // Use std::put_time for thread-safe time printing
    std::cout << "  -> Received Signal:" << std::endl;
    std::cout << "     Sender: " << s.sender << std::endl;
    std::cout << "     Type: " << s.type << std::endl;
    std::cout << "     Content: '" << s.content << "'" << std::endl;
    // std::ctime is not thread-safe, but for this demo it's ok.
    // In a real multi-threaded app, a safer alternative should be used.
    std::cout << "     Timestamp: " << std::ctime(&time_point);
}

int main() {
    std::cout << "[Main] Creating QuantaSynapse instance." << std::endl;
    QuantaSynapse qs;

    // Set up callbacks
    qs.setOnConnected([]() {
        std::cout << "[Callback] Connection established!" << std::endl;
    });

    qs.setOnDisconnected([]() {
        std::cout << "[Callback] Connection lost!" << std::endl;
    });

    // Subscribe to topics
    std::cout << "[Main] Subscribing to 'test.topic' and 'system.heartbeat'." << std::endl;
    qs.subscribe("test.topic", [](const Signal& s) {
        std::cout << "[Callback] Received message on 'test.topic':" << std::endl;
        printSignal(s);
    });

    qs.subscribe("system.heartbeat", [](const Signal& s) {
        std::cout << "[Callback] Received heartbeat:" << std::endl;
        printSignal(s);
    });

    // Connect
    qs.connect();

    // Give some time for the connection to establish
    std::this_thread::sleep_for(std::chrono::seconds(2));

    // Publish a test signal
    std::cout << "[Main] Publishing a test signal." << std::endl;
    Signal testSignal;
    testSignal.sender = "main_app";
    testSignal.type = "greeting";
    testSignal.content = "Hello, QuantaSynapse!";
    testSignal.timestamp = std::chrono::system_clock::now();
    qs.publish("test.topic", testSignal);

    // Let the application run for a bit to receive heartbeats
    std::cout << "[Main] Running for 12 seconds to observe heartbeats..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(12));

    // Disconnect
    std::cout << "[Main] Disconnecting..." << std::endl;
    qs.disconnect();

    // Print final metrics
    std::cout << "[Main] Final Metrics:" << std::endl;
    std::cout << "  -> Messages Sent: " << qs.getMessagesSent() << std::endl;
    std::cout << "  -> Messages Received: " << qs.getMessagesReceived() << std::endl;

    std::cout << "[Main] Application finished." << std::endl;

    return 0;
}