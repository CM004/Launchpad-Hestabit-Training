# NGINX Reverse Proxy + Load Balancing - Day 3

A practical guide demonstrating load balancing between two Node.js backend instances using NGINX as a reverse proxy in Docker.

---

## 1. Objective

- Deploy two identical backend instances
- Configure NGINX to distribute traffic using round-robin load balancing
- Route all `/api` requests through NGINX reverse proxy

---

## 2. Folder Structure

Day3/
├── backend/
│ ├── server.js
│ ├── package.json
│ └── Dockerfile
├── nginx.conf
├── docker-compose.yml
├── reverse-proxy-readme.md
└── screenshots-day3/

---

## 3. Docker Compose Architecture (Summary)

### backend-alpha
- Built from `./backend`
- Internal port `3000`
- Not exposed to host (only accessible via NGINX)

### backend-beta
- Built from `./backend`
- Internal port `3000`
- Not exposed to host (only accessible via NGINX)

### nginx-proxy
- Image: `nginx:alpine`
- Host port `8080` maps to container port `80`
- Proxies `/api` requests to both backends (round-robin)
- Single entry point for all traffic

---

## 4. Steps Followed

1. Created two backend services (`backend-alpha` and `backend-beta`) in `docker-compose.yml`, both building from `./backend`

2. Configured NGINX `upstream` block to define both backends for load balancing

3. Set up NGINX `location /api` block to proxy requests to the upstream backends

4. Mounted NGINX configuration file as volume

5. Started the complete stack:
   docker compose up -d --build

6. This builds and starts: `backend-alpha`, `backend-beta`, and `nginx-proxy`

---

## 5. Key Learnings

- **Upstream Block:** Defines backend servers for load balancing
- **Round-Robin:** Default NGINX algorithm, distributes requests evenly
- **Reverse Proxy:** Single entry point (NGINX) routes to multiple backends
- **Container Networking:** Backends communicate using container names as hostnames
- **No Port Exposure:** Backend ports only accessible internally, not from host
