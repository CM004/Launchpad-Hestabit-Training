```markdown
QUERY ENGINE DOCUMENTATION
==========================

Purpose: Dynamic search/filter/sort/pagination engine for Product API

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUPPORTED QUERY PARAMETERS
---------------------------

┌─────────────────┬─────────────┬─────────┬───────────────────────────────────┐
│ Parameter       │ Type        │ Default │ Description                       │
├─────────────────┼─────────────┼─────────┼───────────────────────────────────┤
│ name            │ String      │ null    │ Text search (case-insensitive)    │
│ minPrice        │ Number      │ null    │ Minimum price range               │
│ maxPrice        │ Number      │ null    │ Maximum price range               │
│ tags            │ String/Arr  │ null    │ Comma-separated tags (OR logic)   │
│ page            │ Number      │ 1       │ Page number (1-based)             │
│ limit           │ Number      │ 10      │ Items per page (max: 100)         │
│ includeDeleted  │ Boolean     │ false   │ Include soft-deleted products     │
└─────────────────┴─────────────┴─────────┴───────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUERY BEHAVIOR & SEMANTICS
---------------------------

1. TEXT SEARCH (name)
   Query: name=phone
   Filter: { name: { $regex: "phone", $options: "i" } }
   Behavior: Case-insensitive partial match

2. PRICE RANGE (minPrice, maxPrice)
   Query: minPrice=100&maxPrice=500
   Filter: { price: { $gte: 100, $lte: 500 } }
   Behavior: Inclusive range, omit absent bounds

3. TAG MATCHING (tags)
   Query: tags=apple,samsung
   Filter: { tags: { $in: ["apple", "samsung"] } }
   Behavior: OR semantics (matches ANY tag)

4. PAGINATION (page, limit)
   Query: page=2&limit=10
   Options: { skip: 10, limit: 10 }
   Calculation: skip = (page - 1) × limit

5. SOFT DELETE (includeDeleted)
   Default: { isDeleted: false }
   includeDeleted=true: Remove isDeleted filter
   Behavior: Exclude deleted products by default

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE REQUESTS → MONGODB QUERIES
-----------------------------------

EXAMPLE 1: SIMPLE TEXT SEARCH
------------------------------
Request:
GET /api/products/search?name=phone

MongoDB Filter:
{
  name: { $regex: "phone", $options: "i" },
  isDeleted: false
}

MongoDB Options:
{ sort: { createdAt: -1 }, skip: 0, limit: 10 }

Response:
{
  "success": true,
  "data": {
    "products": [...],
    "pagination": { "total": 12, "page": 1, "pages": 2, "limit": 10 }
  }
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 2: PRICE RANGE FILTER
------------------------------
Request:
GET /api/products/search?minPrice=100&maxPrice=500

MongoDB Filter:
{
  price: { $gte: 100, $lte: 500 },
  isDeleted: false
}

MongoDB Options:
{ sort: { createdAt: -1 }, skip: 0, limit: 10 }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 3: TAG FILTER
----------------------
Request:
GET /api/products/search?tags=apple,samsung

MongoDB Filter:
{
  tags: { $in: ["apple", "samsung"] },
  isDeleted: false
}

MongoDB Options:
{ sort: { createdAt: -1 }, skip: 0, limit: 10 }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 4: COMBINED FILTERS WITH PAGINATION
--------------------------------------------
Request:
GET /api/products/search?name=phone&minPrice=100&maxPrice=500&tags=apple,samsung&page=2&limit=10

MongoDB Filter:
{
  $and: [
    { name: { $regex: "phone", $options: "i" } },
    { price: { $gte: 100, $lte: 500 } },
    { tags: { $in: ["apple", "samsung"] } },
    { isDeleted: false }
  ]
}

MongoDB Options:
{ sort: { createdAt: -1 }, skip: 10, limit: 10 }

Response:
{
  "success": true,
  "data": {
    "products": [...],
    "pagination": { "total": 45, "page": 2, "pages": 5, "limit": 10 }
  }
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE 5: INCLUDE DELETED PRODUCTS
------------------------------------
Request:
GET /api/products/search?tags=accessory&includeDeleted=true

MongoDB Filter:
{
  tags: { $in: ["accessory"] }
  // No isDeleted filter
}

MongoDB Options:
{ sort: { createdAt: -1 }, skip: 0, limit: 10 }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUERY OPERATORS REFERENCE
--------------------------

TEXT SEARCH:
{ name: { $regex: "searchterm", $options: "i" } }
- $regex: Regular expression pattern match
- $options: "i" = case-insensitive

RANGE QUERIES:
{ price: { $gte: min, $lte: max } }
- $gte: Greater than or equal
- $lte: Less than or equal

ARRAY MATCHING:
{ tags: { $in: ["tag1", "tag2"] } }
- $in: Matches if ANY value in array

BOOLEAN FILTERS:
{ isDeleted: false }
- Direct equality match

SORTING:
.sort({ createdAt: -1 })
- 1: Ascending (oldest first)
- -1: Descending (newest first)

PAGINATION:
.skip((page - 1) * limit).limit(limit)
- skip: Number of documents to skip
- limit: Maximum documents to return

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILTER BUILDING LOGIC
----------------------

const buildFilter = (queryParams) => {
  const filter = { isDeleted: false };
  
  // Text search
  if (queryParams.name) {
    filter.name = new RegExp(queryParams.name, 'i');
  }
  
  // Price range
  if (queryParams.minPrice || queryParams.maxPrice) {
    filter.price = {};
    if (queryParams.minPrice) filter.price.$gte = Number(queryParams.minPrice);
    if (queryParams.maxPrice) filter.price.$lte = Number(queryParams.maxPrice);
  }
  
  // Tags
  if (queryParams.tags) {
    const tagsArray = Array.isArray(queryParams.tags) 
      ? queryParams.tags 
      : queryParams.tags.split(',');
    filter.tags = { $in: tagsArray };
  }
  
  // Include deleted
  if (queryParams.includeDeleted === 'true') {
    delete filter.isDeleted;
  }
  
  return filter;
};

const buildOptions = (queryParams) => {
  const page = Number(queryParams.page) || 1;
  const limit = Math.min(Number(queryParams.limit) || 10, 100);
  
  return {
    sort: { createdAt: -1 },
    skip: (page - 1) * limit,
    limit: limit
  };
};

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERROR RESPONSES
---------------

VALIDATION ERROR:
{
  "success": false,
  "message": "Validation error: minPrice must be less than maxPrice",
  "code": "VALIDATION_ERROR",
  "timestamp": "2025-12-20T03:39:00.000Z",
  "path": "/api/products/search",
  "requestId": "a1b2c3d4..."
}

INVALID PARAMETER:
{
  "success": false,
  "message": "Validation error: limit must be between 1 and 100",
  "code": "VALIDATION_ERROR",
  "timestamp": "2025-12-20T03:39:00.000Z",
  "path": "/api/products/search",
  "requestId": "a1b2c3d4..."
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFORMANCE OPTIMIZATION
------------------------

INDEXES REQUIRED:
productSchema.index({ name: 1 });
productSchema.index({ price: 1 });
productSchema.index({ tags: 1 });
productSchema.index({ isDeleted: 1, createdAt: -1 });

BEST PRACTICES:
✅ Use .lean() for read-only queries (5x faster)
✅ Execute count and find in parallel with Promise.all()
✅ Cap limit at 100 to prevent overwhelming responses
✅ Use indexes on frequently queried fields
✅ Validate and sanitize user input before querying

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUERY ENGINE COMPLETE ✅
```