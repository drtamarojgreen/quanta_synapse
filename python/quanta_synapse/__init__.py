import xml.etree.ElementTree as ET
from collections import defaultdict

class QuantaSynapse:
    def __init__(self):
        print("QuantaSynapse constructor")
        # In-memory message broker for simulation
        # self._topics stores messages per topic
        self._topics = defaultdict(list)
        # self._subscriptions stores callbacks per topic
        self._subscriptions = defaultdict(list)

    def __del__(self):
        print("QuantaSynapse destructor")

    def connect(self):
        print("Connecting to Quanta projects...")

    def disconnect(self):
        print("Disconnecting from Quanta projects...")

    def publish(self, topic: str, message: dict):
        """
        Publishes a message to a topic, which is then delivered to all subscribers.
        Includes Ack/Nack logic for message processing confirmation.
        """
        if not isinstance(message, dict):
            print("Error: Message must be a dictionary.")
            return

        # Serialize dictionary to XML for the "message on the wire"
        root = ET.Element("message")
        for key, val in message.items():
            child = ET.SubElement(root, key)
            child.text = str(val)
        xml_message = ET.tostring(root, encoding="unicode")

        # Add raw XML message to the topic queue, simulating persistence
        self._topics[topic].append(xml_message)
        print(f"Message published to topic '{topic}'. Delivering to subscribers...")

        # Deliver the message to all subscribed callbacks
        if topic in self._subscriptions:
            for callback in self._subscriptions[topic]:
                # Define ack/nack handlers for this specific message delivery
                def ack():
                    print(f"ACK received for message on topic '{topic}'. Removing from queue.")
                    try:
                        self._topics[topic].remove(xml_message)
                    except ValueError:
                        print("Warning: Message was already acknowledged and removed.")

                def nack():
                    print(f"NACK received for message on topic '{topic}'. Message will remain in queue.")

                # Pass the deserialized message (the original dict) and handlers to the callback
                callback(message, ack, nack)

    def subscribe(self, topic: str, callback):
        """
        Subscribes to a topic with a callback function.
        """
        self._subscriptions[topic].append(callback)
        print(f"Successfully subscribed to topic '{topic}'.")
