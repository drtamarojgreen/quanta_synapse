from quanta_synapse import QuantaSynapse
import time

# 1. Define a callback function for a subscriber
def sensor_data_handler(message, ack, nack):
    """
    This function is called when a message is received on the subscribed topic.
    It simulates processing the message and then acknowledges it.
    """
    print(f"\n[CALLBACK] ==> Received sensor data: {message}")
    if message.get("value") is None:
        print("[CALLBACK] ==> Invalid message format. Negatively Acknowledging (nack).")
        nack()
        return

    print("[CALLBACK]     Processing data...")
    time.sleep(1)  # Simulate work
    print("[CALLBACK]     Processing complete. Acknowledging (ack).")
    ack()

def main():
    """
    Main function to demonstrate the QuantaSynapse pub/sub model.
    """
    print("--- QuantaSynapse Pub/Sub Demonstration ---")
    qs = QuantaSynapse()
    qs.connect()

    # === Demonstration 1: Successful ACK ===
    topic_ack = "events.sensors.temperature"
    print(f"\n--- Subscribing to topic: '{topic_ack}' ---")
    qs.subscribe(topic_ack, sensor_data_handler)

    message_payload_ok = {"sensor_id": "temp-001", "value": "25.5", "unit": "C"}
    print(f"\n--- Publishing a valid message to '{topic_ack}': {message_payload_ok} ---")
    qs.publish(topic_ack, message_payload_ok)

    print("\n--- Verifying ACK Mechanism ---")
    if not qs._topics[topic_ack]:
        print("OK: Message queue for topic is empty. ack() worked as expected.")
    else:
        print(f"FAIL: Message queue still contains messages: {qs._topics[topic_ack]}")

    # === Demonstration 2: NACK on Invalid Message ===
    topic_nack = "events.sensors.pressure"
    print(f"\n--- Subscribing to topic: '{topic_nack}' ---")
    qs.subscribe(topic_nack, sensor_data_handler)

    message_payload_bad = {"sensor_id": "press-002", "reading": "98.2"} # Invalid key 'reading'
    print(f"\n--- Publishing an invalid message to '{topic_nack}': {message_payload_bad} ---")
    qs.publish(topic_nack, message_payload_bad)

    print("\n--- Verifying NACK Mechanism ---")
    if qs._topics[topic_nack]:
        print(f"OK: Message queue for NACK topic still contains the message.")
        print(f"   Message: {qs._topics[topic_nack][0]}")
    else:
        print("FAIL: Message was removed from queue despite being NACK'd.")

    print("\n--- Tearing down QuantaSynapse Demo ---")
    qs.disconnect()


if __name__ == "__main__":
    main()
