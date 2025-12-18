# Linux in a Docker Container — Day 1

## Setup
```
docker init
docker build -t week5 .
docker run -it week5
docker exec -it week5-container /bin/sh
```

## Filesystem Exploration
```
ls -la                    # List files with permissions
ls /usr/src/app          # App directory
```
- Container has typical Linux structure: `/bin`, `/etc`, `/usr`, `/var`
- App files located in `/usr/src/app`

## Users & Permissions
```
whoami                   # Returns: node
id                       # Shows user/group IDs
ls -l                    # View file permissions
```
- Container runs as `node` user (non-root) for security

## Processes
```
ps                       # List all processes
top                      # Real-time process monitor
```
- Node.js app runs as PID 1
- Container runs one main process

## Disk Usage
```
df                       # Filesystem usage
du -                     # App directory size
```

## Logs
```
docker logs week5-container

```

## Key Concepts
- **Image**: Blueprint built from Dockerfile
- **Container**: Running instance of image
- **Volumes**: Persist data outside container
- **Networks**: Port mapping (9000:9000)

## Summary
- Built and ran Node.js app in Docker container
- Explored Linux commands inside container environment
- Verified non-root user execution and process isolation
```