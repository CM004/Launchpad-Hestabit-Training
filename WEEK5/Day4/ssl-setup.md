# SSL/TLS Setup with mkcert - Day 4

## Overview
HTTPS enabled using self-signed certificates generated with mkcert.

## Steps Taken

### 1. Install mkcert
   mkcert -install

### 2. Generate Certificates
   mkcert -cert-file certs/localhost.crt -key-file certs/localhost.key localhost 127.0.0.1

### 3. NGINX Configuration
- Port 8080: Redirects all HTTP to HTTPS
- Port 8443: Serves HTTPS with SSL certificates
- Certificates mounted as volume: `./certs:/etc/nginx/certs:ro`

### 4. SSL Termination
NGINX handles SSL/TLS:
- Browser → HTTPS → NGINX (decrypts)
- NGINX → HTTP → Backend (internal, secure network)

## Files Generated
- `certs/localhost.crt` - SSL certificate
- `certs/localhost.key` - Private key

## Testing

### HTTP Redirect
   curl -I http://localhost

### HTTPS Works
curl -k https://localhost/api

{"message":"Secure API Response","protocol":"https", "container":"<container_id>"}

### Browser
- URL: https://localhost
- Lock icon visible ✅
- Certificate valid for localhost

## Key Concepts

| Concept              | Explanation                                          |
|----------------------|------------------------------------------------------|
| **mkcert**           | Tool to generate locally-trusted SSL certificates    |
| **SSL Termination**  | NGINX decrypts HTTPS, forwards plain HTTP to backend |
| **HTTP → HTTPS**     | 301 redirect forces all traffic to secure connection |
| **Volume Mount**     | Certificates injected into container at runtime      |

## Security Notes
- Self-signed certs only for development
- Production requires certificates from trusted CA (Let's Encrypt)
- Private key must never be committed to git

## Commands
Start
docker compose up -d --build

Test
curl -k https://localhost/api

Logs
docker compose logs

---

                    ┌─────────────────────────────────────┐
                    │         Internet (HTTPS/HTTP)       │
                    └──────────────┬──────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────────────┐
                    │   NGINX (Port: 8080/8443)            │
                    │   - Reverse Proxy                    │
                    │   - SSL Termination                  │
                    │   - HTTP → HTTPS Redirect            │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼─────┐
                    │  Backend           │
                    │  Node.js:3000      │
                    └────────────────────┘
                    
                    Docker Network: app-network
