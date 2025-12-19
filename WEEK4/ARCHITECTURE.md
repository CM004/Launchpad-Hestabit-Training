```markdown
PROJECT STRUCTURE - WEEK 4
==========================

WEEK4/
├── src/
│   ├── config/
│   │   └── index.js                     # Configuration management
│   │
│   ├── controllers/
│   │   ├── product.controller.js        # Product HTTP request handlers
│   │   └── user.controller.js           # User HTTP request handlers
│   │
│   ├── jobs/
│   │   └── email.job.js                 # Background email queue (BullMQ)
│   │
│   ├── loaders/
│   │   ├── app.js                       # Express app initialization
│   │   └── db.js                        # MongoDB connection
│   │
│   ├── middlewares/
│   │   ├── errors.middleware.js         # Global error handler
│   │   ├── index.js                     # Middleware orchestrator
│   │   ├── security.js                  # Security (Helmet, CORS, Rate Limiting)
│   │   └── validate.js                  # Joi validation middleware
│   │
│   ├── models/
│   │   ├── Product.js                   # Product schema
│   │   └── User.js                      # User schema with password hashing
│   │
│   ├── repositories/
│   │   ├── product.repository.js        # Product data access layer
│   │   └── user.repository.js           # User data access layer
│   │
│   ├── routes/
│   │   ├── index.js                     # Route aggregator
│   │   ├── product.routes.js            # Product endpoints
│   │   └── user.routes.js               # User endpoints
│   │
│   ├── services/
│   │   ├── product.service.js           # Product business logic
│   │   └── user.service.js              # User business logic
│   │
│   ├── utils/
│   │   ├── errors.js                    # Custom error classes
│   │   ├── logger.js                    # Winston structured logging
│   │   └── tracing.js                   # Request ID middleware
│   │
│   ├── validators/
│   │   ├── product.validator.js         # Product validation schemas
│   │   └── user.validator.js            # User validation schemas
│   │
│   └── app.js                           # Application entry point
│
├── prod/
│   └── ecosystem.config.js              # PM2 production configuration
│
├── logs/
│   ├── app.log                          # Combined logs with request IDs
│   ├── error.log                        # Error-only logs
│   ├── pm2-out.log                      # PM2 stdout logs
│   └── pm2-error.log                    # PM2 stderr logs
│
├── .env.example                         # Environment template
├── .env.local                           # Local environment variables
├── .env.prod                            # Production environment variables
├── .gitignore                           # Git ignore rules
├── package.json                         # Dependencies and scripts
├── package-lock.json                    # Locked dependency versions
│
├── ARCHITECTURE.md                      # Project architecture documentation
├── DEPLOYMENT-NOTES.md                  # Deployment guide
├── SECURITY-REPORT.md                   # Security testing report
├── QUERY-ENGINE.md                      # Query engine documentation
└── README.md                            # Project overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIRECTORY PURPOSE
-----------------

src/config/
- Centralized configuration loading
- Environment variable management

src/controllers/
- HTTP request/response handling
- Route handler functions
- Request validation coordination

src/jobs/
- Background job processing
- Email queue with BullMQ
- Async task management

src/loaders/
- Application bootstrap
- Express middleware setup
- Database connection initialization

src/middlewares/
- Request preprocessing
- Security layers (Helmet, CORS, Rate Limiting)
- Validation (Joi)
- Error handling
- Request tracing

src/models/
- Mongoose schemas
- Data structure definitions
- Model hooks and methods

src/repositories/
- Database query abstraction
- CRUD operations
- Data access layer

src/routes/
- API endpoint definitions
- Route grouping
- Middleware application

src/services/
- Business logic
- Data transformation
- Cross-repository orchestration

src/utils/
- Helper functions
- Custom error classes
- Logging utilities
- Request tracing

src/validators/
- Joi validation schemas
- Input validation rules
- Query parameter validation

prod/
- Production-specific configuration
- PM2 ecosystem settings
- Deployment scripts

logs/
- Application logs
- Error logs
- PM2 process logs
- Request tracing logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ARCHITECTURE LAYERS
-------------------

┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT REQUEST                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                  ↓
                         src/middlewares/
                    (Security, Validation, Tracing)
                                  ↓
                          src/routes/
                      (Endpoint Matching)
                                  ↓
                       src/controllers/
                    (Request/Response Handling)
                                  ↓
                        src/services/
                       (Business Logic)
                                  ↓
                      src/repositories/
                       (Data Access)
                                  ↓
                         src/models/
                       (Mongoose Schemas)
                                  ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATABASE (MongoDB)                             │
└─────────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY FILES
---------

src/app.js
- Application entry point
- Server startup
- Graceful shutdown

src/loaders/app.js
- Express configuration
- Middleware loading
- Route mounting

src/loaders/db.js
- MongoDB connection
- Connection pooling
- Error handling

src/middlewares/security.js
- Helmet security headers
- CORS policy
- Rate limiting
- NoSQL injection prevention

src/middlewares/validate.js
- Joi schema validation
- Request validation middleware

src/middlewares/errors.middleware.js
- Global error handler
- Error response formatting

src/utils/logger.js
- Winston logger configuration
- Request ID logging
- File and console transports

src/utils/tracing.js
- Request ID generation
- Request tracking

src/jobs/email.job.js
- BullMQ email queue
- Background email processing
- Job retry logic

prod/ecosystem.config.js
- PM2 configuration
- Cluster mode settings
- Environment variables

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONFIGURATION FILES
-------------------

.env.example
- Template for environment variables
- Committed to git
- Reference for setup

.env.local
- Local development environment
- Not committed to git

.env.prod
- Production environment
- Not committed to git

.gitignore
- Excludes .env files
- Excludes node_modules
- Excludes logs

package.json
- Dependencies
- Scripts (start, dev, test)
- Project metadata

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOCUMENTATION FILES
-------------------

ARCHITECTURE.md
- System design
- Component interactions
- Data flow diagrams

DEPLOYMENT-NOTES.md
- PM2 deployment guide
- Production setup
- Commands reference

SECURITY-REPORT.md
- Security measures
- Vulnerability testing
- Test results

QUERY-ENGINE.md
- Search API documentation
- Query parameters
- MongoDB query patterns

README.md
- Project overview
- Setup instructions
- API documentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL FILE COUNT: ~30 files
TOTAL DIRECTORIES: 13 directories
```