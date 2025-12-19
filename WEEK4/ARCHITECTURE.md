WEEK4/
├── src/
│   ├── config/
│   │   └── index.js                 # Configuration management
│   ├── controllers/
│   │   ├── product.controller.js    # Product route handlers
│   │   └── user.controller.js       # User route handlers
│   ├── jobs/
│   │   └── email.job.js             # Background email queue (BullMQ)
│   ├── loaders/
│   │   ├── app.js                   # Express app initialization
│   │   └── db.js                    # MongoDB connection
│   ├── middlewares/
│   │   ├── errors.middleware.js     # Global error handler
│   │   ├── index.js                 # Middleware orchestrator
│   │   ├── security.js              # Security middlewares (Helmet, CORS, Rate Limiting)
│   │   └── validate.js              # Joi validation middleware
│   ├── models/
│   │   ├── Product.js               # Product schema
│   │   └── User.js                  # User schema with password hashing
│   ├── repositories/
│   │   ├── product.repository.js    # Product data access layer
│   │   └── user.repository.js       # User data access layer
│   ├── routes/
│   │   ├── index.js                 # Route aggregator
│   │   ├── product.routes.js        # Product endpoints
│   │   └── user.routes.js           # User endpoints
│   ├── services/
│   │   ├── product.service.js       # Product business logic
│   │   └── user.service.js          # User business logic
│   ├── utils/
│   │   ├── errors.js                # Custom error classes
│   │   ├── logger.js                # Winston structured logging
│   │   └── tracing.js               # Request ID middleware
│   ├── validators/
│   │   ├── product.validator.js     # Product validation schemas
│   │   └── user.validator.js        # User validation schemas
│   └── app.js                       # Application entry point
├── prod/
│   └── ecosystem.config.js          # PM2 production configuration
├── logs/
│   ├── app.log                      # Combined logs with request IDs
│   └── error.log                    # Error-only logs
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── package.json                     # Dependencies
└── DEPLOYMENT-NOTES.md              # Deployment guide

