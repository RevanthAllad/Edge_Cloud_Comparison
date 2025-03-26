import json
import time
import boto3
import numpy as np
from datetime import datetime

# Initialize AWS clients
iot_client = boto3.client('iot-data')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    start_time = time.time()
    
    try:
        # Extract signal data from the event
        signal_data = event['signal']
        signal = np.array(signal_data)
        
        # Process the signal
        processed_signal = {
            'timestamp': datetime.now().isoformat(),
            'signal': signal.tolist(),
            'mean': float(np.mean(signal)),
            'std': float(np.std(signal)),
            'max': float(np.max(signal)),
            'min': float(np.min(signal))
        }
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log metrics
        metrics = {
            'timestamp': processed_signal['timestamp'],
            'processing_time': processing_time,
            'signal_length': len(signal),
            'memory_used': context.memory_limit_in_mb,
            'execution_time': context.get_remaining_time_in_millis()
        }
        
        # Store metrics in S3
        bucket_name = 'signal-processing-metrics'
        metrics_key = f"metrics/{datetime.now().strftime('%Y-%m-%d')}/{context.aws_request_id}.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=metrics_key,
            Body=json.dumps(metrics)
        )
        
        # Publish processed signal to IoT topic
        iot_client.publish(
            topic='processed/signal',
            qos=1,
            payload=json.dumps(processed_signal)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Signal processed successfully',
                'processing_time': processing_time,
                'processed_signal': processed_signal
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'processing_time': time.time() - start_time
            })
        } 