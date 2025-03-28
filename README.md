# Kafka Data Pipeline on GCP VM
Before creating a topic run Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties


then kafka producer

bin/kafka-server-start.sh config/server.properties


and for the code you need to install certain dependency

## Overview
This project demonstrates a simple Kafka-based data pipeline on a Google Cloud Platform (GCP) Virtual Machine (VM). It includes:
- A Kafka producer to generate and send messages.
- A Kafka consumer to receive and process messages.
- Data transformation using Python (with Pandas if needed).

## Prerequisites
Ensure you have the following installed on your GCP VM:
- Python 3
- Kafka
- Zookeeper
- Required Python libraries (`kafka-python`, `pandas`)

## Installation
### 1. Update and Install Dependencies
```bash
sudo apt update && sudo apt install -y python3-pip openjdk-11-jdk
```

### 2. Install Kafka
Download and extract Apache Kafka:
```bash
wget https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz // **i downloaded and uplaoded**
mkdir kafka && tar -xvzf kafka_2.13-3.5.0.tgz -C kafka --strip-components=1
```

### 3. Start Kafka and Zookeeper
```bash
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
```

### 4. Install Python Dependencies
```bash
pip install kafka-python pandas
```

## Usage

### 1. Start Kafka Producer
Create a file `kafka_producer.py`:
```python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

data = {'sensor_id': 1, 'temperature': 22.5, 'humidity': 60}

while True:
    producer.send('sensor_data', data)
    print(f"Sent: {data}")
    time.sleep(2)
```
Run the producer:
```bash
python3 kafka_producer.py
```

### 2. Start Kafka Consumer
Create a file `kafka_subscriber.py`:
```python
from kafka import KafkaConsumer
import json
import pandas as pd

consumer = KafkaConsumer('sensor_data',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

data_list = []

for message in consumer:
    data = message.value
    data_list.append(data)
    df = pd.DataFrame(data_list)
    print(df.tail(1))
```
Run the consumer:
```bash
python3 kafka_subscriber.py
```

## Stopping Kafka Services
To stop Kafka and Zookeeper:
```bash
cd kafka
bin/kafka-server-stop.sh
bin/zookeeper-server-stop.sh
```

## License
This project is open-source under the MIT License.

