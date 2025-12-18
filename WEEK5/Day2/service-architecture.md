Overview
Multi-container application with React frontend, Node.js backend, and MongoDB database.

Services
1. MongoDB (Database)
Image: mongo:latest

Container: week5-db

Port: 27017

Volume: db-data (persists data)

Network: app-network

2. Server (Node.js Backend)
Build: From root Dockerfile

Container: week5-server

Port: 9000

Environment:

NODE_ENV=production

MONGO_URI=mongodb://week5db:27017/week5-db

Network: app-network

Dependencies: week5db

3. Client (React Frontend)
Build: From client/Dockerfile
Container: testapp-client

Port: 3000

Network: app-network

Dependencies: server

Networking
All services on shared bridge network: app-network

Server connects to MongoDB using hostname: db

Client connects to server at: http://localhost:9000

Volumes
db-data: Persistent storage for MongoDB at /data/db

Commands
bash
# Start all services
docker compose up -d 

# View logs
docker compose logs -f (-f for real time filter)

# Stop services
docker compose down

# Remove volumes
docker compose down -v