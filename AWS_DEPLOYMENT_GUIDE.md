# 🚀 AWS Deployment Guide — AI Diet Balance

This guide provides clear options to publish and deploy your **AI Diet Balance** application to AWS.

---

## 💡 Option 1: AWS EC2 or AWS Lightsail (Recommended & Easiest)

Using **Docker Compose** on an AWS EC2 instance or Lightsail server provides a complete production environment (PostgreSQL + Django Backend + Nginx/React Frontend) in a single virtual server for **~$5–$10/month**.

### Step 1: Launch an AWS EC2 Instance / Lightsail
1. Log into your **AWS Management Console**.
2. Go to **EC2** -> **Launch Instance** (or **Lightsail** -> **Create Instance**).
3. Select **Ubuntu 22.04 LTS** or **Ubuntu 24.04 LTS**.
4. Choose Instance Type: `t3.small` or `t3.micro` (or 2 GB RAM minimum on Lightsail).
5. In **Security Group Settings**, allow inbound traffic on:
   - **Port 80** (HTTP)
   - **Port 443** (HTTPS)
   - **Port 22** (SSH)

### Step 2: SSH into your EC2 Instance
```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Install Docker & Docker Compose
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
sudo usermod -aG docker ubuntu
newgrp docker
```

### Step 4: Clone your Repository & Set Up `.env`
```bash
git clone https://github.com/Nithyanaidu23/AI-DIET-BALANCE.git
cd AI-DIET-BALANCE

# Create your backend .env file
nano backend/.env
```

Ensure your `backend/.env` has:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_PUBLIC_IP,yourdomain.com
GEMINI_API_KEY=your_google_gemini_api_key
CORS_ALLOWED_ORIGINS=http://YOUR_EC2_PUBLIC_IP,https://yourdomain.com
```

### Step 5: Build and Run with Docker Compose
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### Step 6: Verify Deployment
Open your browser and navigate to:
`http://YOUR_EC2_PUBLIC_IP`

---

## 🌐 Option 2: AWS Amplify (Frontend) + AWS App Runner / Elastic Beanstalk (Backend)

For serverless auto-scaling deployment:

### Frontend (AWS Amplify):
1. Go to **AWS Amplify Console**.
2. Click **Host web app** -> connect to GitHub repository (`frontend` folder).
3. Environment variables: `VITE_API_BASE_URL=https://your-backend-app-runner.awsapprunner.com`.
4. Deploy!

### Backend (AWS App Runner):
1. Go to **AWS App Runner Console**.
2. Select **Source code repository** or **Container registry (ECR)**.
3. Configure runtime: Python 3.12 or Docker.
4. Build command: `pip install -r backend/requirements.txt`
5. Start command: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`
6. Set Environment Variables (`SECRET_KEY`, `GEMINI_API_KEY`, `DATABASE_URL`, etc.).

---

## 🔒 Optional: Add Free SSL (HTTPS) with Certbot (For Option 1)

If you point a domain name to your EC2 IP address:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Summary of Production Files Created:
- [docker-compose.prod.yml](file:///c:/Users/polai/OneDrive/Desktop/AI-DITE-BALANCE/docker-compose.prod.yml): Production Docker stack.
- [frontend/Dockerfile.prod](file:///c:/Users/polai/OneDrive/Desktop/AI-DITE-BALANCE/frontend/Dockerfile.prod): Multi-stage build for React with Nginx.
- [frontend/nginx.conf](file:///c:/Users/polai/OneDrive/Desktop/AI-DITE-BALANCE/frontend/nginx.conf): Nginx configuration for single-page routing & API proxying.
