```markdown
SECURITY REPORT - WEEK 4 DAY 4
===============================
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERVIEW
--------

This report documents the security measures implemented in Week 4 Day 4,
including input validation, rate limiting, NoSQL injection prevention, and
HTTP security headers.

SECURITY LAYERS IMPLEMENTED:
✅ Request Validation (Joi)
✅ NoSQL Injection Prevention
✅ Rate Limiting (express-rate-limit)
✅ HTTP Security Headers (Helmet)
✅ CORS Policy
✅ Payload Size Limits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. INPUT VALIDATION WITH JOI
-----------------------------

VALIDATION RULES:

User:
- name: 3-50 characters, required
- email: Valid email format, required
- password: Minimum 8 characters, required
- status: Enum (active/inactive), optional

Product:
- name: 3-100 characters, required
- price: Positive number, required
- description: Max 500 characters, optional
- tags: Array of strings, optional

Search:
- page: 1-1000, default 1
- limit: 1-100, default 10
- minPrice < maxPrice validation

PROTECTION AGAINST:
✅ Invalid data types
✅ Missing required fields
✅ Out-of-range values
✅ Malformed email addresses
✅ Weak passwords

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. NOSQL INJECTION PREVENTION
------------------------------

BLOCKED PATTERNS:
- { "$ne": null }           → $ prefix removed
- { "$gt": 0 }              → $ prefix removed
- { "user.role": "admin" }  → . in key removed
- { "$where": "code" }      → $ prefix removed

PROTECTION AGAINST:
✅ MongoDB operator injection
✅ Authentication bypass attempts
✅ Query manipulation
✅ Unauthorized data access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. RATE LIMITING
----------------

USAGE:
app.use('/api', apiLimiter);
router.post('/users', strictLimiter, userController.createUser);

RATE LIMITS:
┌─────────────────────┬──────────┬─────────────────────────────────────┐
│ Endpoint            │ Window   │ Limit                               │
├─────────────────────┼──────────┼─────────────────────────────────────┤
│ /api/* (General)    │ 1 min    │ 30 requests                         │
│ POST /api/users     │ 15 min   │ 5 requests                          │
└─────────────────────┴──────────┴─────────────────────────────────────┘

RESPONSE WHEN LIMIT EXCEEDED:
HTTP 429 Too Many Requests
{
  "success": false,
  "message": "Too many requests, please try again later"
}

PROTECTION AGAINST:
✅ Brute force attacks
✅ DDoS attacks
✅ Account enumeration
✅ API abuse

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. HTTP SECURITY HEADERS (HELMET)
----------------------------------

FILE: src/middlewares/security.js

const helmet = require('helmet');
app.use(helmet());

HEADERS APPLIED:
┌────────────────────────────────┬─────────────────────┬──────────────────────┐
│ Header                         │ Value               │ Protection           │
├────────────────────────────────┼─────────────────────┼──────────────────────┤
│ X-Frame-Options                │ SAMEORIGIN          │ Clickjacking         │
│ X-Content-Type-Options         │ nosniff             │ MIME sniffing        │
│ X-XSS-Protection               │ 0                   │ Disable buggy filter │
│ Strict-Transport-Security      │ max-age=15552000    │ HTTPS enforcement    │
└────────────────────────────────┴─────────────────────┴──────────────────────┘

PROTECTION AGAINST:
✅ Clickjacking attacks
✅ MIME-type confusion
✅ Man-in-the-middle attacks
✅ Information disclosure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. CORS POLICY
--------------

FILE: src/middlewares/security.js

const cors = require('cors');

// Development
app.use(cors());

// Production
app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE']
}));

CONFIGURATION:
Development: Allow all origins
Production: Whitelist specific origin from env variable

PROTECTION AGAINST:
✅ Unauthorized cross-origin requests
✅ CSRF attacks
✅ Data theft from malicious sites

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. PAYLOAD SIZE LIMITS
-----------------------

FILE: src/loaders/app.js

app.use(express.json({ limit: '10kb' }));

LIMIT: 10KB per request

PROTECTION AGAINST:
✅ Large payload attacks
✅ Memory exhaustion
✅ Denial of Service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. SECURITY TEST RESULTS
-------------------------

TEST 1: NOSQL INJECTION - LOGIN BYPASS
---------------------------------------
Attack Vector: POST /api/users
Payload: { "email": { "$ne": null }, "password": "test" }

Expected: Request blocked, $ne operator removed
Result: ✅ PASSED - Malicious operator removed by sanitization middleware

Evidence:
Before sanitization: { "email": { "$ne": null }, "password": "test" }
After sanitization: { "password": "test" }


TEST 2: NOSQL INJECTION - QUERY MANIPULATION
---------------------------------------------
Attack Vector: GET /api/products/search?price[$gt]=0
Payload: Query parameter with MongoDB operator

Expected: Request blocked, $gt operator removed
Result: ✅ PASSED - Query parameter sanitized

Evidence:
Before: { price: { "$gt": 0 } }
After: { }


TEST 3: VALIDATION BYPASS - MISSING REQUIRED FIELDS
----------------------------------------------------
Attack Vector: POST /api/users
Payload: { "name": "Test" }  // Missing email and password

Expected: 400 Bad Request with validation error
Result: ✅ PASSED - Request rejected

Response:
{
  "success": false,
  "message": "Validation error: email is required",
  "code": "VALIDATION_ERROR"
}


TEST 4: VALIDATION BYPASS - INVALID EMAIL FORMAT
-------------------------------------------------
Attack Vector: POST /api/users
Payload: { "name": "Test", "email": "invalid", "password": "Test@123" }

Expected: 400 Bad Request with validation error
Result: ✅ PASSED - Request rejected

Response:
{
  "success": false,
  "message": "Validation error: email must be a valid email",
  "code": "VALIDATION_ERROR"
}


TEST 5: WEAK PASSWORD
---------------------
Attack Vector: POST /api/users
Payload: { "name": "Test", "email": "test@test.com", "password": "123" }

Expected: 400 Bad Request with validation error
Result: ✅ PASSED - Password too short rejected

Response:
{
  "success": false,
  "message": "Validation error: password length must be at least 8 characters",
  "code": "VALIDATION_ERROR"
}


TEST 6: RATE LIMITING - BRUTE FORCE
------------------------------------
Attack Vector: 100 rapid POST requests to /api/users
Payload: Valid user creation requests

Expected: First 5 requests succeed, rest blocked for 15 minutes
Result: ✅ PASSED - Rate limiter triggered after 5 requests

Response after limit:
HTTP 429 Too Many Requests
{
  "success": false,
  "message": "Too many account creation attempts"
}


TEST 7: RATE LIMITING - API ABUSE
----------------------------------
Attack Vector: 50 rapid GET requests to /api/products
Payload: Valid product search requests

Expected: First 30 requests succeed, rest blocked for 1 minute
Result: ✅ PASSED - Rate limiter triggered after 30 requests

Response after limit:
HTTP 429 Too Many Requests
{
  "success": false,
  "message": "Too many requests, please try again later"
}


TEST 8: XSS ATTACK - SCRIPT INJECTION
--------------------------------------
Attack Vector: POST /api/products
Payload: { "name": "<script>alert('XSS')</script>", "price": 100 }

Expected: Input stored as plain text, not executed
Result: ✅ PASSED - Script stored safely, validated by Joi

Evidence:
Stored in database: "<script>alert('XSS')</script>"
Returned in API: "<script>alert('XSS')</script>" (as string)
Browser: Does not execute (proper Content-Type headers)


TEST 9: PARAMETER POLLUTION
----------------------------
Attack Vector: GET /api/products/search?page=1&page=2&page=3
Payload: Multiple values for same parameter

Expected: Only one value processed
Result: ✅ PASSED - Last value used, validated against schema

Evidence:
Request: page=1&page=2&page=3
Processed: page=3 (last value)


TEST 10: PAYLOAD SIZE LIMIT
----------------------------
Attack Vector: POST /api/products
Payload: 15KB JSON body (exceeds 10KB limit)

Expected: 413 Payload Too Large
Result: ✅ PASSED - Request rejected

Response:
HTTP 413 Payload Too Large


TEST 11: CLICKJACKING
---------------------
Attack Vector: Embed API endpoint in iframe
Test: Check X-Frame-Options header

Expected: X-Frame-Options: SAMEORIGIN
Result: ✅ PASSED - Header present

Evidence:
Response headers include: X-Frame-Options: SAMEORIGIN


TEST 12: CORS POLICY (PRODUCTION)
----------------------------------
Attack Vector: Request from unauthorized origin
Origin: https://malicious-site.com
Environment: Production

Expected: Request blocked by CORS policy
Result: ✅ PASSED - Only whitelisted origin allowed

Evidence:
Allowed origin: https://yourdomain.com (from FRONTEND_URL)
Request from https://malicious-site.com: BLOCKED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
