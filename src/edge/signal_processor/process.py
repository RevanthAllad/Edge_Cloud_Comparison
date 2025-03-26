import os
import time
import json
import paho.mqtt.client as mqtt
import numpy as np
from datetime import datetime

class SignalProcessor:
    def __init__(self):
        self.mqtt_broker = os.getenv('MQTT_BROKER', 'localhost')
        self.mqtt_port = int(os.getenv('MQTT_PORT', 1883))
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.processed_signals = []

    def connect(self):
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()
        self.client.subscribe("sensors/raw_data")

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            processed_data = self.process_signal(data)
            self.processed_signals.append(processed_data)
            
            # Publish processed data
            self.client.publish("processed/signal", json.dumps(processed_data))
            
            # Log performance metrics
            self.log_metrics(processed_data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def process_signal(self, data):
        # Simulate signal processing
        signal = np.array(data['signal'])
        
        # Apply signal processing operations
        processed_signal = {
            'timestamp': datetime.now().isoformat(),
            'signal': signal.tolist(),
            'mean': float(np.mean(signal)),
            'std': float(np.std(signal)),
            'max': float(np.max(signal)),
            'min': float(np.min(signal))
        }
        
        return processed_signal

    def log_metrics(self, processed_data):
        metrics = {
            'timestamp': processed_data['timestamp'],
            'processing_time': time.time() - float(processed_data['timestamp']),
            'signal_length': len(processed_data['signal'])
        }
        
        with open('metrics.log', 'a') as f:
            f.write(json.dumps(metrics) + '\n')

if __name__ == "__main__":
    processor = SignalProcessor()
    processor.connect()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping signal processor...")
        processor.client.loop_stop()
        processor.client.disconnect() 