# V-LLATS Deployment Guide

## Virtual Laboratory Logbook and Tracking System (V-LLATS)

A complete step-by-step deployment and installation manual for a clean-slate Ubuntu environment.

---

# 1. Project Overview

The **Virtual Laboratory Logbook and Tracking System (V-LLATS)** is a web-based laboratory monitoring and tracking platform developed using Flask and MySQL. The system allows students to digitally submit laboratory logbook entries while enabling administrators to monitor, search, filter, and analyze laboratory usage in real time.

The system was designed to replace traditional handwritten laboratory logbooks with a centralized digital solution that improves efficiency, organization, accessibility, and monitoring within educational laboratory environments.

The application supports two main user roles:

1. **Student Users**
   - Submit laboratory attendance and session records
   - Encode laboratory session details
   - Select instructors and laboratories
   - Record laboratory start and end times

2. **Administrator Users**
   - Monitor submitted laboratory logs
   - View analytics and dashboard statistics
   - Search and filter laboratory records
   - Track laboratory activity and usage patterns

---

# 2. System Features

## Student Features

- Student login
- Laboratory logbook submission
- Instructor selection
- Laboratory selection
- Time tracking
- Session recording
- Form validation

## Administrator Features

- Admin login authentication
- Dashboard analytics
- Laboratory monitoring
- Search functionality
- Date filtering
- Student activity tracking
- Most-used laboratory tracking
- Most-selected instructor tracking
- Submitted log visualization

---

# 3. Technologies Used

## Backend Technologies

- Python 3
- Flask
- Flask SQLAlchemy
- PyMySQL

## Frontend Technologies

- HTML5
- CSS3
- JavaScript

## Database

- MySQL

## Server and Deployment Technologies

- Ubuntu Server
- Nginx Reverse Proxy
- Systemd Service
- UFW Firewall

## Optional Deployment Technology

- Docker Containerization (future enhancement)

---

# 4. System Architecture

The system architecture follows a layered web application structure.

```text
Client Browser
       ↓
Nginx Reverse Proxy
       ↓
Flask Web Application
       ↓
SQLAlchemy ORM
       ↓
MySQL Database
```

---

# 5. Project Directory Structure

```text
vllats_group5/
│
├── app.py
├── requirements.txt
├── venv/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── admin_login.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   ├── review_log.html
│   ├── update_log.html
│   └── index.html
│
└── vllats_db.sql
```

---

# 6. HTML Templates Explanation

## index.html

The landing page of the system. This page contains the system introduction and the buttons for Student Login and Admin Login.

## login.html

This page allows students to authenticate before accessing the laboratory logging features.

## admin_login.html

This page allows administrators to securely access the monitoring dashboard.

## dashboard.html

Displays the student interface after login. Students can access the laboratory logging form from this page.

## admin_dashboard.html

Displays all monitoring analytics and submitted laboratory logs.

### Features include:

- Total logs today
- Most used laboratory
- Most active student
- Most selected instructor
- Search filtering
- Date filtering

## review_log.html

Displays submitted log information and allows updating or deleting of logs.

## update_log.html

Allows students to modify previously submitted logs.

---

# 7. Flask Routes Explanation

## Route: `/`

### Function

Displays the landing page.

### HTML Rendered

`index.html`

---

## Route: `/login`

### Function

Authenticates student users.

### Process

1. Student enters login credentials.
2. Flask validates credentials.
3. Session is created.
4. Student dashboard is opened.

### HTML Rendered

`login.html`

---

## Route: `/admin_login`

### Function

Authenticates administrators.

### Process

1. Admin enters username and password.
2. Flask checks database credentials.
3. Session authentication occurs.
4. Admin dashboard becomes accessible.

### HTML Rendered

`admin_login.html`

---

## Route: `/dashboard`

### Function

Displays the student dashboard after successful login.

### HTML Rendered

`dashboard.html`

---

## Route: `/submit_log`

### Function

Handles laboratory log submissions.

### Process

1. Student selects laboratory.
2. Student selects instructor.
3. Student enters time schedule.
4. Form data is sent to Flask backend.
5. SQLAlchemy stores data inside MySQL database.
6. Confirmation is displayed.

### HTML Rendered

`review_log.html`

---

## Route: `/update_log/<int:log_id>`

### Function

Allows modification of previously submitted logs.

### Process

1. Student edits log details.
2. Flask updates database records.
3. Updated information is saved.
4. Updated review page is displayed.

### HTML Rendered

`update_log.html`

---

## Route: `/admin_dashboard`

### Function

Displays administrative monitoring and analytics.

### Features

- Search logs
- Filter by date
- Monitor laboratory activity
- Display statistics

### HTML Rendered

`admin_dashboard.html`

---

# 8. Database Structure

## Main Tables

### Students Table

Stores:

- Student ID
- SR-Code
- Full Name
- Program
- Section

### Logs Table

Stores:

- Log ID
- Student reference
- Instructor
- Laboratory
- Start time
- End time
- Timestamp

### Admin Table

Stores:

- Admin username
- Admin password

---

# 9. Clean-Slate Ubuntu Installation Guide

This section explains how to deploy the system from zero.

---

# STEP 1 — Update Ubuntu System

```bash
sudo apt update && sudo apt upgrade -y
```

This updates all Ubuntu packages and dependencies.

---

# STEP 2 — Install Python

```bash
sudo apt install python3 python3-pip python3-venv -y
```

---

# STEP 3 — Install MySQL

```bash
sudo apt install mysql-server -y
```

Verify installation:

```bash
sudo systemctl status mysql
```

---

# STEP 4 — Create MySQL Database

Open MySQL:

```bash
sudo mysql
```

Create database:

```sql
CREATE DATABASE vllats_db;
```

Create user:

```sql
CREATE USER 'vllats_user'@'localhost' IDENTIFIED BY 'yourpassword';
```

Grant privileges:

```sql
GRANT ALL PRIVILEGES ON vllats_db.* TO 'vllats_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

# STEP 5 — Clone or Copy the Project

If using GitHub:

```bash
git clone https://github.com/yourusername/vllats.git
```

If manually copying:

```bash
scp -r vllats_group5 user@server:/home/user/
```

---

# STEP 6 — Enter Project Directory

```bash
cd vllats_group5
```

---

# STEP 7 — Create Python Virtual Environment

```bash
python3 -m venv venv
```

Activate environment:

```bash
source venv/bin/activate
```

---

# STEP 8 — Install Project Dependencies

```bash
pip install -r requirements.txt
```

If cryptography error appears:

```bash
pip install cryptography
```

---

# STEP 9 — Configure Flask Database Connection

Inside `app.py`, configure:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://vllats_user:yourpassword@localhost/vllats_db'
```

---

# STEP 10 — Import Database Schema

```bash
mysql -u vllats_user -p vllats_db < vllats_db.sql
```

---

# STEP 11 — Test Flask Application

Run Flask manually:

```bash
python app.py
```

Open browser:

```text
http://SERVER-IP:5000
```

---

# STEP 12 — Install Nginx

```bash
sudo apt install nginx -y
```

---

# STEP 13 — Configure Nginx Reverse Proxy

Open configuration:

```bash
sudo nano /etc/nginx/sites-available/default
```

Replace contents with:

```nginx
server {
    listen 80;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Save and exit.

---

# STEP 14 — Test Nginx Configuration

```bash
sudo nginx -t
```

---

# STEP 15 — Restart Nginx

```bash
sudo systemctl restart nginx
```

Enable automatic startup:

```bash
sudo systemctl enable nginx
```

---

# STEP 16 — Configure Flask Systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/vllats.service
```

Insert:

```ini
[Unit]
Description=V-LLATS Flask Application
After=network.target

[Service]
User=YOUR-USERNAME
WorkingDirectory=/home/YOUR-USERNAME/vllats_group5
ExecStart=/home/YOUR-USERNAME/vllats_group5/venv/bin/python /home/YOUR-USERNAME/vllats_group5/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

# STEP 17 — Enable Systemd Service

Reload services:

```bash
sudo systemctl daemon-reload
```

Enable startup persistence:

```bash
sudo systemctl enable vllats
```

Start service:

```bash
sudo systemctl start vllats
```

Check status:

```bash
sudo systemctl status vllats
```

---

# STEP 18 — Configure Firewall (UFW)

Allow SSH:

```bash
sudo ufw allow OpenSSH
```

Allow web traffic:

```bash
sudo ufw allow 'Nginx Full'
```

Enable firewall:

```bash
sudo ufw enable
```

Check status:

```bash
sudo ufw status
```

---

# STEP 19 — Access the System

Open browser:

```text
http://SERVER-IP
```

Example:

```text
http://192.168.8.41
```

---

# 10. Systemd Persistence Explanation

The system uses `systemd` to ensure automatic service persistence.

This means:

- Flask automatically starts after reboot
- Flask automatically restarts after crashes
- The application runs continuously in the background
- No manual execution through terminal is needed after deployment

The `vllats.service` file was configured inside:

```text
/etc/systemd/system/vllats.service
```

The service was enabled using:

```bash
sudo systemctl enable vllats
```

This command ensures that the V-LLATS system automatically launches whenever the Ubuntu virtual machine starts.

The service can be managed using the following commands:

Start service:

```bash
sudo systemctl start vllats
```

Stop service:

```bash
sudo systemctl stop vllats
```

Restart service:

```bash
sudo systemctl restart vllats
```

Check service status:

```bash
sudo systemctl status vllats
```

Reload service configuration:

```bash
sudo systemctl daemon-reload
```

---

# 11. Nginx Reverse Proxy Explanation

Nginx acts as the public-facing web server of the system.

Instead of exposing the Flask development server directly to users, Nginx handles all incoming browser requests and forwards them internally to the Flask application running on port 5000.

The reverse proxy setup improves:

- Professional deployment structure
- Security
- Request handling efficiency
- Scalability
- Stability

The Nginx configuration file used was:

```text
/etc/nginx/sites-available/default
```

The configured reverse proxy structure was:

```nginx
server {
    listen 80;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Nginx was restarted using:

```bash
sudo systemctl restart nginx
```

Nginx status can be checked using:

```bash
sudo systemctl status nginx
```

Configuration validation can be tested using:

```bash
sudo nginx -t
```

---

# 12. UFW Firewall Explanation

The system uses UFW (Uncomplicated Firewall) to protect the Ubuntu virtual machine from unauthorized network access.

The firewall only allows trusted and necessary services such as:

- SSH access
- HTTP access
- HTTPS access

All unnecessary incoming traffic is blocked automatically.

The firewall was configured using:

Allow SSH:

```bash
sudo ufw allow OpenSSH
```

Allow web traffic:

```bash
sudo ufw allow 'Nginx Full'
```

Enable firewall:

```bash
sudo ufw enable
```

Check firewall status:

```bash
sudo ufw status
```

The firewall helps secure the deployed Flask system by reducing exposed attack surfaces on the server.

---

# 13. IAM (Identity and Access Management)

The system implements basic IAM (Identity and Access Management) principles through authentication and authorization logic.

The application separates access between:

1. Students
2. Administrators

## Student Authentication

Students must log in using their SR-Code and password before accessing the laboratory logging features.

After successful login:

- Flask creates a session
- Session stores the authenticated student ID
- Student gains access to protected routes

Example protected route:

```python
if 'student_id' not in session:
    return redirect('/login')
```

This prevents unauthorized users from accessing logging functions.

## Administrator Authentication

Administrators use separate credentials and a dedicated admin login page.

Only authenticated administrators can access:

- `/admin_dashboard`
- Monitoring analytics
- Search and filtering tools
- Laboratory records

This separation ensures role-based access control inside the system.

---

# 14. Docker Containerization (Future Enhancement)

Docker containerization was identified as a possible future enhancement for the system.

Containerization would modularize the system into separate isolated services such as:

- Flask Application Container
- MySQL Database Container
- Nginx Reverse Proxy Container

Possible future files include:

```text
Dockerfile
docker-compose.yml
```

Benefits of Docker containerization include:

- Easier deployment
- Faster portability
- Consistent runtime environments
- Simplified dependency management
- Better scalability
- Easier cloud deployment

Although Docker was not fully implemented in the final version of the system, the architecture of V-LLATS is compatible with future containerized deployment.

---

# 15. Common Errors and Fixes

## Flask Module Not Found

Error encountered:

```text
ModuleNotFoundError: No module named 'flask'
```

Cause:

The Flask package was not installed inside the Python virtual environment.

Fix:

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install Flask:

```bash
pip install flask
```

---

## Cryptography Package Missing

Error encountered:

```text
RuntimeError: 'cryptography' package is required
```

Cause:

PyMySQL authentication required the cryptography package.

Fix:

```bash
pip install cryptography
```

---

## Apache Occupying Port 80

Problem encountered:

Apache2 occupied port 80, preventing Nginx from starting correctly.

Fix:

Stop Apache:

```bash
sudo systemctl stop apache2
```

Disable Apache:

```bash
sudo systemctl disable apache2
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

---

## Nginx Configuration Test Failed

Fix:

Validate configuration syntax:

```bash
sudo nginx -t
```

Correct configuration errors inside:

```text
/etc/nginx/sites-available/default
```

Then restart Nginx:

```bash
sudo systemctl restart nginx
```

---

# 16. GitHub Repository Setup

The project can be uploaded to GitHub for version control, backup, collaboration, and deployment documentation purposes.

## Install Git

```bash
sudo apt install git -y
```

---

## Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Initialize Repository

Inside project folder:

```bash
git init
```

---

## Add Project Files

```bash
git add .
```

---

## Create Initial Commit

```bash
git commit -m "Initial commit"
```

---

## Create GitHub Repository

1. Open GitHub
2. Click "New Repository"
3. Enter repository name:
   `vllats`
4. Click "Create Repository"

---

## Connect Local Project to GitHub

```bash
git remote add origin https://github.com/YOUR-USERNAME/vllats.git
```

---

## Push Project to GitHub

```bash
git push -u origin main
```

The project source code, README documentation, and deployment guide will now be accessible online through GitHub.

---

# 17. Final Deployment Verification Checklist

After deployment, the following verification steps should be completed.

## Verify Flask Service

```bash
sudo systemctl status vllats
```

Expected output:

```text
active (running)
```

---

## Verify Nginx Service

```bash
sudo systemctl status nginx
```

Expected output:

```text
active (running)
```

---

## Verify Firewall Status

```bash
sudo ufw status
```

Expected allowed services:

- OpenSSH
- Nginx Full

---

## Verify Browser Access

Open browser and enter:

```text
http://SERVER-IP
```

Example:

```text
http://192.168.8.40
```

The V-LLATS homepage should load successfully.

---

## Verify Persistence

Restart the Ubuntu virtual machine:

```bash
sudo reboot
```

After reboot:

- Nginx should automatically start
- Flask should automatically start
- Browser access should still work
- No manual terminal execution should be needed

---

# 18. Developers

## Developers

- Atienza, Rhaianne Margarette C.
- Buhay, Mark Tristan B.
- Fermalan, Jurby Kevin C.
- Lastimozo, Jericho C.
- Manalo, Ma. Jane Lariz P.
- Matira, Dranreb B.

---

# 19. License

This project was developed for academic and educational purposes only.

The system was created as part of the course requirement for CpEE 401 - Cognate 1 involving:

- Linux System Administration
- Virtualization
- Flask Web Development
- Database Management
- Network Security
- Service Deployment
- Web Infrastructure Configuration
- Identity and Access Management

The project may be modified, improved, and extended for future educational and research purposes.
