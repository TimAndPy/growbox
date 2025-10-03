# Docker Deployment Guide for Nvidia Jetson Nano

This guide explains how to run GrowBox in a Docker container on your Nvidia Jetson Nano 2GB Developer Kit.

## Why Docker?

Docker solves version conflicts and dependency issues by packaging your entire application with all its libraries into a single container. This ensures:
- Consistent environment across devices
- No conflicts with system Python or libraries
- Easy deployment and updates
- Isolated from system packages

## Prerequisites

1. **Install Docker on Jetson Nano**

```bash
# Update package list
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# Reboot to apply group changes
sudo reboot
```

2. **Install Docker Compose**

```bash
# Install docker-compose
sudo apt-get install -y docker-compose
```

3. **Verify Installation**

```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Clone or Navigate to Project

```bash
cd /path/to/growbox
```

### 2. Configure Your Settings

Make sure your configuration files are set up:

```bash
# Copy example configs if needed
cp config/devices.json.example config/devices.json
cp config/sensors.json.example config/sensors.json
cp config/mqtt.json.example config/mqtt.json
cp config/targets.json.example config/targets.json

# Edit configs for your setup
nano config/devices.json
nano config/sensors.json
```

### 3. Build and Run

**Using Docker Compose (Recommended):**

```bash
# Build and start container in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

**Using Docker directly:**

```bash
# Build the image (takes 5-10 minutes on Jetson Nano)
docker build -t growbox .

# Run the container
docker run -d \
  --name growbox \
  --privileged \
  --network host \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config:ro \
  --restart unless-stopped \
  growbox
```

## Accessing the Web Interface

Once running, access the web interface at:

```
http://<jetson-nano-ip>:5000
```

Or if running locally on the Jetson:

```
http://localhost:5000
```

## Managing the Container

### View Running Containers
```bash
docker ps
```

### View Logs
```bash
# Using docker-compose
docker-compose logs -f

# Using docker
docker logs -f growbox
```

### Stop Container
```bash
# Using docker-compose
docker-compose stop

# Using docker
docker stop growbox
```

### Start Container
```bash
# Using docker-compose
docker-compose start

# Using docker
docker start growbox
```

### Restart Container
```bash
# Using docker-compose
docker-compose restart

# Using docker
docker restart growbox
```

### Remove Container
```bash
# Using docker-compose (stops and removes)
docker-compose down

# Using docker
docker stop growbox
docker rm growbox
```

## Updating the Application

When you make code changes:

```bash
# Rebuild and restart
docker-compose up -d --build

# Or with docker
docker build -t growbox .
docker stop growbox
docker rm growbox
docker run -d --name growbox --privileged --network host \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config:ro \
  --restart unless-stopped \
  growbox
```

## Troubleshooting

### Check Container Status
```bash
docker ps -a
docker-compose ps
```

### View Full Logs
```bash
docker logs growbox --tail 100
```

### Enter Container Shell (for debugging)
```bash
docker exec -it growbox /bin/bash
```

### Check GPIO Permissions
```bash
# Verify GPIO devices are accessible
docker exec -it growbox ls -la /dev/gpiochip*
docker exec -it growbox ls -la /sys/class/gpio
```

### Memory Issues (2GB RAM)
If the container crashes due to memory:

1. Check memory usage:
```bash
docker stats growbox
```

2. Reduce memory limit in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 768M  # Reduce from 1G
```

### GPIO Not Working

If GPIO access fails:

1. Verify privileged mode is enabled
2. Check device mappings in docker-compose.yml
3. Ensure Jetson.GPIO is compatible with your Jetson Nano OS version

### Network Issues

If you can't access the web interface:

1. Verify container is running: `docker ps`
2. Check port mapping: Container uses `network_mode: host` so port 5000 should be directly accessible
3. Check firewall: `sudo ufw status`

## Resource Limits

The docker-compose.yml file sets memory limits appropriate for the 2GB Jetson Nano:
- Memory limit: 1GB
- Memory reservation: 512MB

This leaves ~1GB for the system and other processes.

## Data Persistence

The following directories are persisted outside the container:
- `./data` - SQLite database
- `./logs` - Application logs
- `./config` - Configuration files (read-only in container)

## Auto-Start on Boot

To automatically start GrowBox when the Jetson Nano boots:

```bash
# Enable Docker service
sudo systemctl enable docker

# The container has restart: unless-stopped policy
# It will auto-start when Docker starts
```

Or create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/growbox.service
```

Add:
```ini
[Unit]
Description=GrowBox Docker Container
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/growbox
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable growbox
sudo systemctl start growbox
```

## Security Notes

1. **Change the secret key** in production:
   - Set `GROWBOX_SECRET_KEY` environment variable in docker-compose.yml

2. **Network security**:
   - The container uses `network_mode: host` for GPIO access
   - Consider using a firewall to restrict access to port 5000

3. **Privileged mode**:
   - Required for GPIO access on Jetson Nano
   - For better security, you can try using `devices:` mapping instead (commented in docker-compose.yml)

## Support

For issues specific to:
- **Docker**: Check Docker documentation
- **Jetson Nano**: Check NVIDIA Jetson forums
- **GrowBox application**: Check project README.md
