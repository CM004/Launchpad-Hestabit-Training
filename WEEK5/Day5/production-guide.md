# Day 5 - Production Deployment Guide

## Overview
Full-stack application with Next.js frontend, Node.js backend, MongoDB Atlas, NGINX reverse proxy, and HTTPS.

---

## Architecture


                    ┌─────────────────────────────────────┐
                    │         Internet (HTTPS/HTTP)       │
                    └──────────────┬──────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────────────┐
                    │   NGINX (Port: 80/443)               │
                    │   - Reverse Proxy                    │
                    │   - SSL Termination                  │
                    └──────────┬───────────────────┬───────┘
                               │                   │
                ┌──────────────▼─────┐    ┌───────▼──────────────┐
                │  Frontend          │    │  Backend             │
                │  Next.js:3000      │    │  Node.js:3000        │
                └────────────────────┘    └──────────┬───────────┘
                                                     │
                                          ┌──────────▼───────────┐
                                          │  MongoDB Atlas       │
                                          │  (Cloud Database)    │
                                          └──────────────────────┘
                    
                    Docker Network: app-network


---

## Project Structure

Day5/
  - backend/
    - Dockerfile
    - index.js
    - package.json
  - frontend/
    - Dockerfile
    - next.config.js
    - package.json
  - certs/
    - localhost.crt
    - localhost.key
  - docker-compose.prod.yml
  - nginx.conf
  - .env
  - .env.example
  - .gitignore
  - deploy.sh
  - production-guide.md

---

## Environment Variables

Create `.env` file (never commit this):

MONGO_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/myapp?retryWrites=true&w=majority
NODE_ENV=production

---

## Deployment

### 1. Setup MongoDB Atlas

1. Create cluster at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create database user with password
3. Whitelist IP: `0.0.0.0/0` (or your server IP)
4. Get connection string and update `.env`

### 2. Generate SSL Certificates

Create certs folder
mkdir certs

Now generate certificates
mkcert -cert-file certs/localhost.crt -key-file certs/localhost.key localhost 127.0.0.1 ::1

Verify
ls -la certs/

### 3. Deploy

chmod +x deploy.sh
./deploy.sh

### 4. Verify

docker ps
curl -k https://localhost/api
curl -k https://localhost/health

---

## Accessing the Application

- **Frontend:** https://localhost
- **Backend API:** https://localhost/api
- **Health Check:** https://localhost/health

---

## Container Management

### View Logs

docker logs day5-backend -f
docker logs day5-frontend -f
docker logs day5-nginx -f

### Stop All
docker compose -f docker-compose.prod.yml down

---

## Health Checks

All containers have health checks:
- Backend: `http://localhost:3000/health`
- Frontend: `http://localhost:3000`
- NGINX: `http://localhost`

Check status:
docker ps

---

## Troubleshooting

### Port 80 Already in Use
sudo lsof -i :80
sudo systemctl stop apache2

### MongoDB Connection Failed
- Verify credentials in `.env`
- Check MongoDB Atlas IP whitelist
- Ensure database name in URI: `/myapp`
- URL encode special characters in password

### Container Won't Start
docker logs day5-<service> -f
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build


---

## Security Checklist

-  `.env` in `.gitignore`
-  HTTPS enabled with SSL certificates
-  MongoDB credentials not hardcoded
-  Health checks enabled
-  Restart policy: `always`
-  Read-only nginx config volumes

---

## Production Best Practices

1. **Never commit `.env`** - Use `.env.example` for templates
2. **Use strong passwords** - Generate secure MongoDB passwords
3. **Update dependencies** - Keep Docker images and npm packages updated
4. **Monitor logs** - Check container logs regularly
5. **Backup database** - Schedule MongoDB Atlas backups

---

## Maintenance

### Update Application
git pull
./deploy.sh
Remove old images
docker image prune -a

Remove unused volumes
docker volume prune

---

## Status

 Docker Compose production file  
 Environment variables in `.env`  
 Health checks configured  
 Container restart policies  
 Deployment script  
 HTTPS with SSL certificates  
 NGINX reverse proxy  
 MongoDB Atlas integration  

**Stack Status:** Production Ready 
