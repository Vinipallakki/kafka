from kafka import KafkaConsumer
import pandas as pd

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'sensor_data',  # Kafka topic name
    bootstrap_servers='localhost:9092',  # Kafka broker
    auto_offset_reset='latest',  # Read latest messages
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')  # Decode messages to strings
)

# Initialize an empty list to store received messages
data = []

print("Listening for messages on Kafka topic 'sensor_data'...")

try:
    for message in consumer:
        print(f"Received message: {message.value}")
        values = message.value.split(",")

        if len(values) == 3:
            sensor_id, sensor_type, sensor_value = values
            sensor_id = int(sensor_id)
            sensor_value = float(sensor_value)

            # Example Transformation: Convert Celsius to Fahrenheit
            if sensor_type == "Temperature":
                sensor_value = sensor_value * 1.8 + 32
            
            # Append processed data
            data.append([sensor_id, sensor_type, sensor_value])

            # Save to CSV after every 5 messages
            if len(data) % 5 == 0:
                df = pd.DataFrame(data, columns=["sensor_id", "sensor_type", "sensor_value"])
                df.to_csv("sensor_data_processed.csv", index=False)
                print("Saved processed data to sensor_data_processed.csv")

except KeyboardInterrupt:
    print("\nStopping Kafka Subscriber...")

