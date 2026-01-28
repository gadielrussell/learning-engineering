# Geospatial Indexing for System Design

A comprehensive guide to understanding spatial data indexing, covering when and why to use it, how the major approaches work, and practical implementation patterns for systems like UberEats, Uber, and Yelp.

---

## Table of Contents

1. [The Core Problem](#the-core-problem)
2. [Why Standard Indexes Fail](#why-standard-indexes-fail)
3. [Geospatial Indexing Approaches](#geospatial-indexing-approaches)
   - [Geohashes](#geohashes)
   - [QuadTrees](#quadtrees)
   - [R-Trees](#r-trees)
4. [Production Implementations](#production-implementations)
   - [PostgreSQL with PostGIS](#postgresql-with-postgis)
   - [Redis Geo Commands](#redis-geo-commands)
   - [Elasticsearch](#elasticsearch)
5. [System Design Patterns](#system-design-patterns)
6. [Interview Talking Points](#interview-talking-points)
7. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
8. [Quick Reference](#quick-reference)

---

## The Core Problem

When building location-based services, you constantly need to answer queries like:

- "What restaurants are within 5 miles of this user?"
- "Find the 10 closest drivers to this pickup location"
- "Show all stores in this map viewport"

These are **range queries in two-dimensional space**. The challenge is that traditional database indexes weren't designed for this.

### Why This Matters for Scale

Consider UberEats in a major city:

- 50,000+ restaurants in the database
- Millions of users opening the app daily
- Each app open triggers a "find nearby" query
- Users expect results in < 100ms

Scanning the entire restaurant table for each query is not viable. You need an index that understands geography.

---

## Why Standard Indexes Fail

### B-Trees Are One-Dimensional

A B-tree index organizes data along a **single axis of comparison**. At each node, the question is: "Is this value less than or greater than the pivot?" This positions data on a number line — inherently one-dimensional.

```
B-tree on latitude:

           37.5
          /    \
       37.2    37.8
       /  \    /  \
    37.0 37.3 37.6 37.9
```

This efficiently answers: "Find all latitudes between 37.2 and 37.5."

But location has **two independent axes** (latitude and longitude). A B-tree on latitude knows nothing about longitude.

### The Two-Index Problem

With separate indexes on latitude and longitude:

```sql
SELECT * FROM restaurants 
WHERE latitude BETWEEN 37.7 AND 37.8 
  AND longitude BETWEEN -122.5 AND -122.4
```

The query optimizer must choose:

1. Use the latitude index → find all rows in that latitude band (potentially 100,000 rows spanning the entire vertical strip)
2. Scan those results checking longitude one by one

Or vice versa. Either way, you're doing a linear scan on half the query.

**Analogy**: Imagine a filing cabinet sorted by last name. Finding "last names M-P" is fast. Finding "last names M-P AND first names A-C" requires pulling the M-P drawer and checking each file manually.

### Composite Indexes Don't Help

A composite index on `(latitude, longitude)` doesn't solve this either. B-tree composite indexes work left-to-right — they're efficient for:

- Exact match on latitude + range on longitude
- Range on latitude only

But NOT for independent ranges on both dimensions simultaneously.

---

## Geospatial Indexing Approaches

### Geohashes

Geohashes convert 2D coordinates into a 1D string where **common prefixes indicate geographic proximity**.

#### How It Works

1. Start with the entire world as a grid
2. Divide into 32 cells, each gets a character (0-9, b-z excluding a, i, l, o)
3. Recursively subdivide each cell
4. The resulting string encodes nested subdivisions

```
World:
9 = Southwest US region
9q = San Francisco Bay Area  
9q8 = San Francisco city
9q8y = Specific neighborhood
9q8yy = ~5km x 5km cell
9q8yyk = ~1km x 1km cell
```

**Key insight**: Locations with the same prefix are in the same cell.

```
San Francisco downtown: 9q8yyz
San Francisco Marina:   9q8yyc   (same 5-char prefix = within ~5km)
Oakland:                9q9p1    (different prefix = farther)
```

#### Querying with Geohashes

This transforms 2D spatial queries into 1D string prefix queries:

```sql
-- Add geohash column (computed from lat/long)
ALTER TABLE restaurants ADD COLUMN geohash VARCHAR(12);
CREATE INDEX idx_geohash ON restaurants(geohash);

-- Find nearby restaurants
SELECT * FROM restaurants 
WHERE geohash LIKE '9q8yy%'
```

Standard B-tree indexes handle prefix queries efficiently!

#### Precision Levels

| Characters | Cell Size (approx) | Use Case |
|------------|-------------------|----------|
| 4 | ~40km x 20km | Country/region level |
| 5 | ~5km x 5km | City district |
| 6 | ~1.2km x 600m | Neighborhood |
| 7 | ~150m x 150m | City block |
| 8 | ~40m x 20m | Building level |

#### The Edge Problem

Geohash cells have hard boundaries. Two restaurants 10 meters apart might have completely different geohashes if they're on opposite sides of a cell boundary.

**Solution**: Query the target cell plus its 8 neighbors.

```python
def get_nearby_geohashes(geohash: str) -> list[str]:
    """Returns the geohash and its 8 neighbors"""
    # Libraries like python-geohash provide this
    return geohash_neighbors(geohash)  # Returns 9 hashes

# Query all 9 cells
cells = get_nearby_geohashes('9q8yy')
query = "SELECT * FROM restaurants WHERE geohash IN (%s)" % cells
```

#### Geohash Trade-offs

| Pros | Cons |
|------|------|
| Simple to implement | Rectangular cells don't match circular radius queries |
| Works with any database (just string indexing) | Edge effects require querying neighbors |
| Easy to understand and debug | Precision is discrete (can't query exactly 2.3 miles) |
| Efficient storage | Cells are not equal area (distortion near poles) |

---

### QuadTrees

QuadTrees recursively divide 2D space into four quadrants, creating a tree structure optimized for spatial queries.

#### How It Works

```
           World
         /   |   \   \
       NW   NE   SW   SE
      /|\   ...
    NW NE SW SE
    ...
```

Each node either:
- Contains points directly (leaf node)
- Subdivides into 4 children (internal node)

Subdivision typically occurs when a node exceeds a threshold (e.g., 100 points).

#### Visual Example

```
+-------------------+
|    NW    |   NE   |
|  +--+--+ |        |
|  |••|  | |   •    |
|  +--+--+ |        |
|  |  |••| |        |
+---------+---------+
|         |         |
|    •    |  •   •  |
|   SW    |   SE    |
|         |         |
+-------------------+

• = restaurant location
Dense areas subdivide more (NW quadrant)
Sparse areas remain as single cells
```

#### Querying QuadTrees

To find points within a radius:

1. Start at root
2. Check if query circle intersects each quadrant
3. Recurse into intersecting quadrants only
4. At leaf nodes, check actual point distances

```python
def query_radius(node, center, radius, results):
    if not intersects(node.bounds, center, radius):
        return  # Prune this entire subtree
    
    if node.is_leaf():
        for point in node.points:
            if distance(point, center) <= radius:
                results.append(point)
    else:
        for child in node.children:
            query_radius(child, center, radius, results)
```

This is efficient because you skip entire subtrees that can't contain results.

#### QuadTree Trade-offs

| Pros | Cons |
|------|------|
| Adapts to data density (subdivides more in cities) | More complex to implement |
| Natural fit for "zoom" operations (map viewports) | Requires rebalancing as data changes |
| Efficient for highly non-uniform distributions | In-memory structure (not trivial to persist) |
| Good for nearest-neighbor queries | Point-only (not great for shapes/polygons) |

---

### R-Trees

R-Trees (Rectangle Trees) are the most sophisticated approach, used by production databases like PostGIS. They generalize B-trees to multiple dimensions.

#### How It Works

- Each node contains **bounding boxes** (rectangles in 2D)
- Child nodes' bounding boxes are contained within parent's
- Leaf nodes contain actual data points/shapes

```
Root: [entire dataset bounding box]
├── Node A: [bounding box covering downtown]
│   ├── Leaf: restaurants 1, 2, 3
│   └── Leaf: restaurants 4, 5
├── Node B: [bounding box covering suburbs]
│   └── ...
```

#### Why R-Trees Are Powerful

1. **Handle both points and shapes** — restaurants (points), delivery zones (polygons)
2. **Efficient for range queries** — "find all within this rectangle"
3. **Support nearest-neighbor** — "find K closest"
4. **Disk-optimized** — designed for database storage, not just memory

#### R-Tree Variants

- **R-Tree**: Original, can have overlapping nodes
- **R*-Tree**: Optimized insert/split algorithms, less overlap
- **R+-Tree**: No overlap allowed, may duplicate entries

PostgreSQL's GIST indexes use R-tree principles.

---

## Production Implementations

### PostgreSQL with PostGIS

PostGIS is the industry standard for geospatial data in relational databases.

#### Setup

```sql
-- Enable PostGIS extension
CREATE EXTENSION postgis;

-- Create table with geometry column
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location GEOGRAPHY(POINT, 4326)  -- 4326 = WGS84 coordinate system
);

-- Create spatial index (uses R-tree via GIST)
CREATE INDEX idx_restaurants_location 
ON restaurants USING GIST(location);
```

#### Common Queries

**Find within radius:**
```sql
SELECT id, name, 
       ST_Distance(location, ST_MakePoint(-122.4194, 37.7749)::geography) as distance_meters
FROM restaurants
WHERE ST_DWithin(
    location, 
    ST_MakePoint(-122.4194, 37.7749)::geography,
    8047  -- radius in meters (5 miles)
)
ORDER BY distance_meters;
```

**Find K nearest:**
```sql
SELECT id, name
FROM restaurants
ORDER BY location <-> ST_MakePoint(-122.4194, 37.7749)::geography
LIMIT 10;
```
The `<->` operator uses the index for efficient nearest-neighbor search.

**Find within bounding box (map viewport):**
```sql
SELECT id, name
FROM restaurants
WHERE location && ST_MakeEnvelope(-122.5, 37.7, -122.3, 37.9, 4326);
```

#### PostGIS Trade-offs

| Pros | Cons |
|------|------|
| Full SQL support, joins, transactions | Heavier than simple key-value stores |
| Rich function library (distance, intersection, containment) | Requires PostGIS extension setup |
| Battle-tested at scale | Can be overkill for simple point queries |
| Handles complex shapes (polygons, routes) | |

---

### Redis Geo Commands

Redis provides built-in geospatial commands (since v3.2) — no modules required. Under the hood, it uses geohashes stored in sorted sets.

#### Basic Operations

```python
import redis
r = redis.Redis()

# Add locations
# GEOADD key longitude latitude member [longitude latitude member ...]
r.geoadd('restaurants', [
    (-122.4194, 37.7749, 'restaurant:123'),
    (-122.4089, 37.7837, 'restaurant:456'),
    (-122.4000, 37.7900, 'restaurant:789'),
])

# Find within radius (GEOSEARCH - preferred in Redis 6.2+)
nearby = r.geosearch(
    'restaurants',
    longitude=-122.4100,
    latitude=37.7800,
    radius=5,
    unit='mi',
    withdist=True,
    sort='ASC'
)
# Returns: [('restaurant:456', 0.42), ('restaurant:123', 0.67), ...]

# Get distance between two members
distance = r.geodist('restaurants', 'restaurant:123', 'restaurant:456', unit='mi')

# Get coordinates of members
positions = r.geopos('restaurants', 'restaurant:123', 'restaurant:456')
```

#### Redis Geo Commands Reference

| Command | Purpose |
|---------|---------|
| `GEOADD` | Add members with coordinates |
| `GEOSEARCH` | Find within radius or box |
| `GEOSEARCHSTORE` | Store search results in new key |
| `GEODIST` | Distance between two members |
| `GEOPOS` | Get coordinates of members |
| `GEOHASH` | Get geohash strings |

#### Redis Geo Trade-offs

| Pros | Cons |
|------|------|
| Extremely fast (in-memory) | Only stores points, not shapes |
| Simple API | No complex spatial operations |
| Built into Redis core | Limited query expressiveness |
| Perfect for caching hot paths | Data must fit in memory |

---

### Elasticsearch

Elasticsearch supports geo_point and geo_shape types with various query options.

```json
// Index mapping
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "location": { "type": "geo_point" }
    }
  }
}

// Geo distance query
{
  "query": {
    "bool": {
      "filter": {
        "geo_distance": {
          "distance": "5mi",
          "location": {
            "lat": 37.7749,
            "lon": -122.4194
          }
        }
      }
    }
  },
  "sort": [
    {
      "_geo_distance": {
        "location": { "lat": 37.7749, "lon": -122.4194 },
        "order": "asc"
      }
    }
  ]
}
```

Elasticsearch is a good choice when you need full-text search combined with geo queries (e.g., "pizza restaurants within 5 miles").

---

## System Design Patterns

### Pattern 1: PostGIS + Redis Cache (UberEats)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   App/API    │────▶│    Redis     │────▶│  PostgreSQL  │
│              │     │  (geo cache) │     │   (PostGIS)  │
└──────────────┘     └──────────────┘     └──────────────┘
                           │
                      Cache miss?
                           │
                           ▼
                    Query PostGIS,
                    populate Redis
```

**Flow:**
1. User opens app at location X
2. Compute geohash for location (e.g., "9q8yy")
3. Check Redis: `GEOSEARCH restaurants:9q8yy ...`
4. Cache hit → return results
5. Cache miss → query PostGIS, populate Redis cache for that geohash cell

**Cache key strategy:** Use geohash prefix as cache key to enable geographic cache hits.

### Pattern 2: Sharded by Geography (Uber)

For global scale, shard data by geographic region:

```
┌─────────────┐
│   Router    │
└─────────────┘
       │
   ┌───┴───┬───────┬───────┐
   ▼       ▼       ▼       ▼
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│ US  │ │ EU  │ │APAC │ │ ...│
│West │ │     │ │     │ │    │
└─────┘ └─────┘ └─────┘ └─────┘
```

Each shard handles a geographic region. Routing uses coarse geohash prefix or bounding box check.

### Pattern 3: Real-Time Location Updates (Driver Tracking)

Drivers update location every few seconds. Need fast writes + fast reads.

```
Driver App                    
     │                        
     ▼                        
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Kafka  │───▶│ Worker  │───▶│  Redis  │
│ (buffer)│    │         │    │  Geo    │
└─────────┘    └─────────┘    └─────────┘
                    │
                    ▼
              ┌─────────┐
              │ PostGIS │ (periodic snapshots)
              └─────────┘
```

**Key insight:** Don't write every location update to PostgreSQL. Buffer in Kafka, aggregate in workers, update Redis in real-time, snapshot to PostgreSQL periodically (for analytics/history).

---

## Interview Talking Points

### The Core Explanation

> "For 'find nearby' queries, I'd use geospatial indexing rather than standard B-tree indexes on latitude and longitude. The fundamental issue is that B-trees are one-dimensional — they efficiently answer 'find values in this range' for a single column. But location is inherently two-dimensional. If you have separate indexes on lat and long, the database can use one index efficiently but then must scan all matching rows to check the second dimension.
>
> Geospatial indexes solve this by organizing data in 2D space from the start. The main approaches are geohashes, which cleverly encode 2D coordinates as 1D strings where proximity means similar prefixes, and R-trees, which are like B-trees generalized to multiple dimensions using bounding boxes."

### When Asked About Specific Technologies

> "In practice, I'd use PostgreSQL with PostGIS for the source of truth — it gives you ACID transactions, rich spatial operations, and battle-tested R-tree indexes via GIST. For the hot read path, I'd put a Redis cache in front using its built-in geo commands, which store points as geohashed values in sorted sets. This gives sub-millisecond reads for the common case."

### If They Push on Scale

> "For global scale, I'd shard geographically — each shard owns a region. The router uses a coarse geohash or bounding box to direct queries. Within each shard, the PostGIS + Redis pattern still applies. For real-time location data like driver tracking, I'd buffer writes through Kafka, update Redis in real-time for queries, and batch-write to PostgreSQL for durability and analytics."

### The Trade-off Analysis They Want to Hear

> "The key trade-offs are:
> - **Geohashes** are simple and work with any database but create rectangular cells that don't perfectly match radius queries, so you query a superset and filter.
> - **R-trees** (PostGIS) are more powerful and handle complex shapes but require specialized extensions.
> - **Redis geo** is extremely fast but memory-bound and limited to points only.
> 
> For most location-based services, the pattern is: PostGIS for truth, Redis for speed, geohash-based cache keys for geographic locality."

---

## Common Mistakes to Avoid

### ❌ "I'd just add indexes on lat and long"

This shows you don't understand the fundamental 2D problem.

### ❌ "I'd use a Vector Database"

Vector DBs are optimized for high-dimensional similarity search (100s-1000s of dimensions). For 2D geography, they're overkill and actually less efficient than purpose-built spatial indexes. It's like using a sledgehammer to hang a picture frame.

### ❌ "I'd query all restaurants and filter in application code"

This doesn't scale. Scanning 50,000 restaurants for every app open is O(n) and gets worse as you grow.

### ❌ Forgetting the edge problem with geohashes

Always mention querying neighboring cells to handle points near cell boundaries.

### ❌ Not discussing the caching strategy

The interviewer wants to see you think about read patterns. "Show nearby restaurants" is called on every app open — that's a caching opportunity.

---

## Quick Reference

### Geohash Precision Table

| Length | Cell Size | Use Case |
|--------|-----------|----------|
| 4 | ~40km | Regional |
| 5 | ~5km | City district |
| 6 | ~1.2km | Neighborhood |
| 7 | ~150m | Block level |
| 8 | ~40m | Building |

### PostGIS Cheat Sheet

```sql
-- Distance query (meters)
ST_DWithin(geom1, geom2, distance_meters)

-- K nearest neighbor
ORDER BY geom1 <-> geom2 LIMIT k

-- Bounding box intersection
geom && ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326)

-- Create point from coordinates
ST_MakePoint(longitude, latitude)::geography
```

### Redis Geo Cheat Sheet

```
GEOADD key longitude latitude member
GEOSEARCH key FROMMEMBER member BYRADIUS 5 mi
GEOSEARCH key FROMLONLAT lon lat BYRADIUS 5 km WITHDIST
GEODIST key member1 member2 mi
```

### Technology Selection Guide

| Requirement | Recommendation |
|-------------|----------------|
| Simple point queries, high read volume | Redis Geo |
| Complex shapes, spatial joins, transactions | PostGIS |
| Full-text + geo search combined | Elasticsearch |
| Global scale | Shard by region + above |
| Real-time tracking (high write volume) | Kafka → Redis → periodic PostGIS |

---

## Further Reading

- [PostGIS Documentation](https://postgis.net/documentation/)
- [Redis Geospatial Commands](https://redis.io/commands/?group=geo)
- [Uber's H3 Hexagonal Hierarchical Spatial Index](https://www.uber.com/blog/h3/)
- [Geohash Wikipedia](https://en.wikipedia.org/wiki/Geohash)
