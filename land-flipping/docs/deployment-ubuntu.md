# Deployment on Ubuntu

1. Install Docker and Docker Compose

```
sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

2. Clone repo and cd

```
# Assuming files staged on server under ~/land-flipping
cd land-flipping
```

3. Configure environment

```
cp landflip-backend/.env.example landflip-backend/.env
# Edit landflip-backend/.env with strong JWT_SECRET and SMTP/DocuSeal credentials
cp landflip-frontend/.env.example landflip-frontend/.env
```

4. Bring up the stack

```
docker compose -f infra/docker-compose.yml up -d --build
```

5. Access services
- Web UI: http://<server-ip>:5173
- API: http://<server-ip>:8000/docs
- DocuSeal: http://<server-ip>:3000
- Postgres (optional): port 5432

6. TLS / Reverse Proxy (recommended)
- Put Caddy or Nginx in front; proxy / to web:5173 and /api to api:8000 with HTTPS
- Or deploy behind Cloudflare Tunnel

7. Optional hardening
- Create a non-default database password and user
- Rotate JWT secret and SMTP credentials regularly
- Configure backups for Postgres volume
- Use firewall rules to limit access to ports 5173/8000/3000; only expose via reverse proxy
