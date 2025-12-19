```markdown
PRODUCTION DEPLOYMENT GUIDE
===========================

Overview
--------
The application is deployed in production using PM2, a robust process manager 
for Node.js. PM2 ensures reliability through process monitoring, automatic 
restarts, clustering, and zero-downtime reloads.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PM2 FOR PRODUCTION
------------------

Key advantages:
✓ Background process management
✓ Automatic restart on crashes
✓ Cluster mode for load balancing
✓ Centralized log handling
✓ Zero-downtime reloads

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIRECTORY STRUCTURE
-------------------

WEEK4/
├── prod/
│   └── ecosystem.config.js    # PM2 production configuration
├── src/                       # Application source code
├── logs/                      # Production logs
│   ├── app.log
│   ├── error.log
│   ├── pm2-out.log
│   └── pm2-error.log
├── .env.prod                  # Production environment variables
└── package.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ECOSYSTEM CONFIGURATION
-----------------------

File: prod/ecosystem.config.js

module.exports = {
  apps: [{
    name: 'week4-api',
    script: './src/app.js',
    instances: 2,
    exec_mode: 'cluster',
    watch: false,
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true,
    autorestart: true,
    max_memory_restart: '1G'
  }]
};

Application Settings:
- Entry script: src/app.js
- Watch mode: Disabled
- Execution mode: cluster
- Instances: 2 worker processes

Environment Variables:
- NODE_ENV: production
- PORT: 3000
- MONGODB_URI: <production MongoDB connection string>
- GMAIL_USER: <your-email@gmail.com>
- GMAIL_APP_PASSWORD: <16-char-app-password>
- FRONTEND_URL: <https://yourdomain.com>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEPLOYMENT COMMANDS
-------------------

Install PM2:
npm install -g pm2

Start Application:
pm2 start prod/ecosystem.config.js

Check Status:
pm2 status

View Logs:
pm2 logs

Monitor Resources:
pm2 monit

Reload (Zero-Downtime):
pm2 reload prod/ecosystem.config.js

Stop Application:
pm2 stop prod/ecosystem.config.js

Delete from PM2:
pm2 delete prod/ecosystem.config.js

Save Configuration:
pm2 save

Auto-Start on Reboot:
pm2 startup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEPLOYMENT WORKFLOW
-------------------

Initial Deployment:
1. Clone repository: git clone <repo-url>
2. Navigate: cd week4-api
3. Install: npm install
4. Create .env.prod with production values
5. Start: pm2 start prod/ecosystem.config.js
6. Save: pm2 save
7. Setup auto-restart: pm2 startup
8. Verify: curl http://localhost:3000/health

Update Deployment:
1. Pull latest: git pull origin main
2. Install: npm install
3. Reload: pm2 reload prod/ecosystem.config.js
4. Verify: pm2 status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HEALTH CHECKS
-------------

After deployment, verify:

1. PM2 Status:
   pm2 status
   Expected: week4-api online, 2 instances

2. API Health:
   curl http://localhost:3000/health
   Expected: HTTP 200 OK

3. Endpoints:
   curl http://localhost:3000/api/products
   curl http://localhost:3000/api/users

4. Logs:
   pm2 logs week4-api
   Expected: No errors, request IDs present

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TROUBLESHOOTING
---------------

Application not starting:
- Check logs: pm2 logs week4-api --err
- Verify .env.prod exists
- Check MongoDB connection

High memory usage:
- Monitor: pm2 monit
- Restart: pm2 restart week4-api

Application keeps restarting:
- Check error logs: pm2 logs week4-api --err
- Verify environment variables
- Check database connectivity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USEFUL COMMANDS REFERENCE
--------------------------

pm2 start prod/ecosystem.config.js     # Start application
pm2 stop all                            # Stop all processes
pm2 restart all                         # Restart all processes
pm2 reload all                          # Zero-downtime reload
pm2 delete all                          # Remove all processes
pm2 logs                                # View all logs
pm2 monit                               # Monitor resources
pm2 list                                # List all processes
pm2 save                                # Save current process list
pm2 startup                             # Setup auto-start

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEPLOYMENT STATUS: PRODUCTION-READY ✅
```