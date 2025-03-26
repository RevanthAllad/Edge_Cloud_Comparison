# Cloud vs Edge Computing Comparison Project

This project demonstrates a comparison between cloud and edge computing approaches using AWS and Docker, with a focus on real-time signal transmission from a remote location to a fire station.

## Project Overview

The project implements two different architectures:
1. Cloud-based approach using AWS services
2. Edge-based approach using Docker containers

### Use Case: Real-time Signal Transmission
- Remote location monitoring system
- Real-time signal processing
- Transmission to fire station
- Performance comparison between cloud and edge approaches

## Project Structure
```
.
├── README.md
├── requirements.txt
├── docker-compose.yml
├── src/
│   ├── cloud/
│   │   ├── aws_lambda/
│   │   └── aws_iot/
│   └── edge/
│       ├── signal_processor/
│       └── transmitter/
└── tests/
    ├── cloud_tests/
    └── edge_tests/
```

## Prerequisites
- Python 3.8+
- Docker
- AWS CLI configured with appropriate credentials
- AWS IoT Core setup

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Start the edge computing environment:
```bash
docker-compose up
```

## Running the Project

1. Cloud-based approach:
```bash
python src/cloud/aws_lambda/process_signal.py
```

2. Edge-based approach:
```bash
python src/edge/signal_processor/process.py
```

## Performance Metrics
The project measures and compares:
- Latency
- Bandwidth usage
- Processing time
- Cost implications
- Resource utilization

## License
MIT License 