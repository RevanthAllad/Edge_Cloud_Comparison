import time
import json
import numpy as np
import boto3
import paho.mqtt.client as mqtt
from datetime import datetime

class PerformanceTester:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('localhost', 1883, 60)
        self.results = []

    def generate_test_signal(self, size=1000):
        return np.random.normal(0, 1, size).tolist()

    def test_cloud_processing(self, signal):
        start_time = time.time()
        
        # Invoke Lambda function
        response = self.lambda_client.invoke(
            FunctionName='process_signal',
            InvocationType='RequestResponse',
            Payload=json.dumps({'signal': signal})
        )
        
        end_time = time.time()
        result = json.loads(response['Payload'].read().decode())
        
        return {
            'approach': 'cloud',
            'processing_time': end_time - start_time,
            'result': result
        }

    def test_edge_processing(self, signal):
        start_time = time.time()
        
        # Publish to MQTT topic
        self.mqtt_client.publish('sensors/raw_data', json.dumps({'signal': signal}))
        
        # Wait for response
        response = None
        def on_message(client, userdata, message):
            nonlocal response
            response = json.loads(message.payload.decode())
        
        self.mqtt_client.on_message = on_message
        self.mqtt_client.subscribe('processed/signal')
        
        # Wait for response with timeout
        timeout = 5
        while response is None and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        
        end_time = time.time()
        
        return {
            'approach': 'edge',
            'processing_time': end_time - start_time,
            'result': response
        }

    def run_comparison(self, num_tests=10):
        for i in range(num_tests):
            print(f"Running test {i+1}/{num_tests}")
            
            # Generate test signal
            signal = self.generate_test_signal()
            
            # Test cloud processing
            cloud_result = self.test_cloud_processing(signal)
            
            # Test edge processing
            edge_result = self.test_edge_processing(signal)
            
            # Store results
            self.results.append({
                'test_number': i + 1,
                'timestamp': datetime.now().isoformat(),
                'cloud': cloud_result,
                'edge': edge_result
            })
            
            # Print comparison
            print(f"\nTest {i+1} Results:")
            print(f"Cloud Processing Time: {cloud_result['processing_time']:.4f}s")
            print(f"Edge Processing Time: {edge_result['processing_time']:.4f}s")
            print("-" * 50)
        
        # Save results to file
        with open('performance_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Calculate and print summary statistics
        cloud_times = [r['cloud']['processing_time'] for r in self.results]
        edge_times = [r['edge']['processing_time'] for r in self.results]
        
        print("\nSummary Statistics:")
        print(f"Cloud Processing - Mean: {np.mean(cloud_times):.4f}s, Std: {np.std(cloud_times):.4f}s")
        print(f"Edge Processing - Mean: {np.mean(edge_times):.4f}s, Std: {np.std(edge_times):.4f}s")

if __name__ == "__main__":
    tester = PerformanceTester()
    tester.run_comparison() 