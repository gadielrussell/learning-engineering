# Database Scaling: A System Design Study Guide

## Overview

As applications grow, so does the data volume and user load. Without proper scaling, you'll encounter slow response times, timeouts, and system crashes. This guide provides deep dives into four essential database scaling strategies—**Partitioning**, **Sharding**, **Indexing**, and **Replication**—plus critical decision-making frameworks and a real-world case study of how Notion scaled their database infrastructure.

---

## Before You Scale: The Critical Question

**Are you positive you need a different database or scaling solution?**

Before implementing any scaling strategy, exhaust your current options:

1. **Read the manual front-to-back.** There may be configuration knobs you haven't discovered—memory tuning, compaction strategies, garbage collection behavior, connection pooling settings.

2. **Understand your database's architecture and limitations.** Reach out to community experts. People in the know can help in surprising ways.

3. **Quick wins to buy time:**
   - Add a cache in front of the database
   - Add read replicas to offload read traffic
   - Partition or shard if data is naturally siloed
   - Optimize queries and add appropriate indexes

> **Key insight:** Migrating a live production database is risky and costly—often taking much longer than anticipated. Make sure there's no way to keep using your current system before migrating.

---

## The Four Core Scaling Strategies

### 1. Indexing

**Concept:** Indexes are data structures that improve the speed of data retrieval operations on a database table at the cost of additional writes and storage space. Think of them like the index at the back of a book—they help locate specific data quickly without scanning every row.

#### How Indexes Work

When you create an index on a column, the database creates a separate data structure that maintains a sorted reference to the actual table rows. Instead of scanning millions of rows (a "full table scan"), the database can use the index to jump directly to relevant data.

**Most common index types:**

| Index Type | Structure | Best For | Example Use Case |
|------------|-----------|----------|------------------|
| **B-tree** | Balanced tree | Range queries, equality, sorting | `WHERE date BETWEEN '2024-01-01' AND '2024-12-31'` |
| **Hash** | Hash table | Exact equality lookups only | `WHERE user_id = 12345` |
| **GiST** | Generalized search tree | Geometric/spatial data, full-text | `WHERE location && bounding_box` |
| **GIN** | Generalized inverted | Arrays, JSONB, full-text search | `WHERE tags @> ARRAY['postgres']` |
| **BRIN** | Block range | Very large tables with natural ordering | Time-series data sorted by timestamp |

#### B-tree Indexes Deep Dive

B-trees are the default index type in most relational databases because they're versatile:

- Keep data sorted, enabling fast insertion, deletion, and lookup
- Support range queries efficiently (e.g., `BETWEEN`, `<`, `>`, `<=`, `>=`)
- Work well with `ORDER BY` clauses
- Handle equality checks (`=`) efficiently
- Typical lookup time: O(log n)

**How B-tree lookups work:**
1. Start at the root node
2. Compare search key with node values
3. Follow the appropriate child pointer
4. Repeat until reaching a leaf node containing the actual data pointer
5. Use the pointer to fetch the row from the table

#### Composite (Multi-Column) Indexes

Composite indexes index multiple columns together and are crucial for queries that filter on multiple fields:

```sql
-- Single column indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Composite index (often more effective for combined queries)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

**The "leftmost prefix" rule:** A composite index on `(A, B, C)` can be used for queries filtering on:
- `A` alone
- `A` and `B` together
- `A`, `B`, and `C` together

But **not** for queries filtering only on `B` or `C` alone.

#### Covering Indexes

A covering index includes all columns needed by a query, allowing the database to satisfy the query entirely from the index without touching the table ("index-only scan"):

```sql
-- If your query is: SELECT customer_id, order_date, total FROM orders WHERE customer_id = 123
-- A covering index would be:
CREATE INDEX idx_orders_covering ON orders(customer_id, order_date, total);
```

This eliminates the random I/O of fetching rows from the heap, dramatically improving performance.

#### Trade-offs

| Benefit | Cost |
|---------|------|
| Dramatically reduces query execution time | Slows down write operations (index must be updated on every write) |
| Prevents full table scans | Additional storage overhead (indexes can be 10-30% of table size) |
| Enables efficient range queries | More indexes = more work for the query planner |
| Supports efficient sorting | Index maintenance during bulk loads |

#### Index Anti-patterns

**Over-indexing:** Each index adds overhead to every INSERT, UPDATE, and DELETE. A table with 10 indexes means every write must update 10 separate data structures.

**Indexing low-cardinality columns:** An index on a boolean column (only 2 values) rarely helps—the database might as well scan the table.

**Ignoring index maintenance:** Indexes can become bloated or fragmented over time. Regular `REINDEX` or `VACUUM` operations may be necessary.

**Not analyzing query patterns:** Index what you query, not what seems logical. Use `EXPLAIN ANALYZE` to verify indexes are being used.

#### Best Practices

1. Index columns used frequently in `WHERE`, `JOIN`, and `ORDER BY` clauses
2. Consider composite indexes for multi-column filters
3. Monitor index usage—drop unused indexes
4. Use covering indexes for frequently-run queries
5. Be cautious with indexes on frequently-updated columns
6. Consider partial indexes for queries that filter on a subset of rows

---

### 2. Partitioning

**Concept:** Partitioning divides a single logical table into multiple physical pieces (partitions) that are stored and managed separately. Unlike sharding, all partitions typically reside on the same database server.

#### Why Partition?

- **Improved query performance:** Queries that filter on the partition key can skip irrelevant partitions ("partition pruning")
- **Easier maintenance:** Operations like archiving old data become as simple as dropping a partition
- **Better resource utilization:** Frequently accessed "hot" data can be stored on faster storage, while "cold" historical data lives on cheaper storage
- **Parallel processing:** Some operations can process partitions concurrently

#### Partitioning Strategies

| Strategy | How It Works | Best For | Example |
|----------|--------------|----------|---------|
| **Range** | Data divided by ranges of values | Time-series data, sequential IDs | Orders partitioned by month |
| **List** | Data divided by discrete values | Regional data, categories | Users partitioned by country |
| **Hash** | Data distributed via hash function | Even distribution when no natural range | Users partitioned by `hash(user_id) % N` |
| **Composite** | Combines multiple strategies | Complex access patterns | Range by date, then hash by user_id |

#### Range Partitioning Example

```sql
-- PostgreSQL range partitioning by date
CREATE TABLE orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    total DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create partitions for each quarter
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
    
CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');
```

When you query with a date filter, PostgreSQL automatically prunes partitions:

```sql
-- This query only scans orders_2024_q2
SELECT * FROM orders WHERE order_date = '2024-05-15';
```

#### Hash Partitioning Example

```sql
-- PostgreSQL hash partitioning
CREATE TABLE users (
    user_id BIGINT,
    username VARCHAR(100),
    email VARCHAR(255)
) PARTITION BY HASH (user_id);

-- Create 4 hash partitions
CREATE TABLE users_p0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_p1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_p2 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_p3 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

#### Partitioning vs. Sharding

| Aspect | Partitioning | Sharding |
|--------|--------------|----------|
| **Location** | Same database server | Multiple database servers |
| **Scalability** | Limited by single server | Near-infinite horizontal scaling |
| **Complexity** | Lower—database handles routing | Higher—application must route queries |
| **Cross-partition queries** | Handled transparently | Expensive, often requires scatter-gather |
| **Transactions** | Full ACID within database | Distributed transactions are complex |
| **Use case** | Managing large tables on single server | Scaling beyond single server limits |

#### Trade-offs

| Benefit | Cost |
|---------|------|
| Partition pruning improves query performance | Queries without partition key scan all partitions |
| Simplified data lifecycle management | Additional complexity in table design |
| Can improve concurrent access | Partition key changes require data movement |
| Better maintenance operations (VACUUM per partition) | Must create new partitions proactively |

#### Best Practices

1. **Choose partition key carefully**—it should align with your most common query patterns
2. **Create partitions proactively**—automate creation of future partitions
3. **Monitor partition sizes**—aim for relatively uniform partition sizes
4. **Include partition key in queries**—ensure partition pruning can occur
5. **Consider sub-partitioning** for very large datasets with multiple access patterns

---

### 3. Sharding (Horizontal Scaling)

**Concept:** Sharding splits a large database into smaller, more manageable pieces called shards distributed across multiple database servers. Each shard is a fully independent database containing a subset of the total data.

#### Why Shard?

Sharding is typically the solution when:
- A single database server cannot handle the write load
- Dataset size exceeds what a single server can store efficiently
- You need to distribute data geographically for latency
- You've exhausted vertical scaling options

#### Sharding Architectures

**1. Application-Level Sharding**
The application determines which shard to query based on a shard key:

```python
def get_shard_connection(user_id):
    shard_number = hash(user_id) % NUM_SHARDS
    return shard_connections[shard_number]

# Query the appropriate shard
conn = get_shard_connection(user_id)
conn.execute("SELECT * FROM users WHERE user_id = ?", [user_id])
```

**2. Proxy-Based Sharding**
A proxy layer (like Vitess, ProxySQL, or PgBouncer with routing) handles shard routing transparently:

```
Application → Proxy → Shard 1
                   → Shard 2
                   → Shard 3
```

**3. Database-Native Sharding**
Some databases (Citus for PostgreSQL, MySQL Cluster) provide built-in sharding capabilities.

#### Choosing a Shard Key

The shard key determines how data is distributed. This is one of the most critical decisions in a sharded system.

| Criteria | Good Shard Key | Bad Shard Key |
|----------|----------------|---------------|
| **Distribution** | Even distribution of data and load | Creates hot spots (uneven distribution) |
| **Query patterns** | Aligns with common query patterns | Requires cross-shard queries frequently |
| **Stability** | Stable—doesn't change often | Changes frequently, requiring data movement |
| **Cardinality** | High cardinality (many unique values) | Low cardinality (few unique values) |

**Example shard key decisions:**

| Application | Good Shard Key | Why |
|-------------|----------------|-----|
| Social network | user_id | Users typically access their own data |
| Multi-tenant SaaS | tenant_id | Tenants rarely need cross-tenant queries |
| E-commerce | customer_id | Order history is per-customer |
| IoT platform | device_id | Queries are typically per-device |
| Analytics | timestamp + entity_id | Time-range queries with entity filtering |

#### Sharding Strategies

**1. Range-Based Sharding**
Data is divided by ranges of the shard key:
- Shard 1: user_id 1-1,000,000
- Shard 2: user_id 1,000,001-2,000,000
- etc.

*Pros:* Range queries are efficient within a shard
*Cons:* Can lead to hot spots if new data clusters in one range

**2. Hash-Based Sharding**
Data is distributed via a hash function:
```
shard_number = hash(shard_key) % number_of_shards
```

*Pros:* Even distribution, prevents hot spots
*Cons:* Range queries require scatter-gather across all shards

**3. Directory-Based Sharding**
A lookup service maps shard keys to shards:
```
lookup_table:
  user_123 → shard_2
  user_456 → shard_1
  user_789 → shard_3
```

*Pros:* Flexible, can optimize placement
*Cons:* Lookup service becomes a bottleneck and single point of failure

**4. Geo-Based Sharding**
Data is distributed based on geographic location:
- US shard: users in North America
- EU shard: users in Europe
- APAC shard: users in Asia-Pacific

*Pros:* Reduces latency for users, helps with data residency compliance
*Cons:* Uneven distribution if user base isn't geographically balanced

#### Physical vs. Logical Shards

A powerful pattern (used by Notion, Instagram, and others) separates logical and physical shards:

- **Logical shards:** Many virtual divisions of data (e.g., 480 logical shards)
- **Physical shards:** Fewer actual database instances (e.g., 32 physical servers)

Multiple logical shards live on each physical server. This provides:
- **Flexibility:** Move logical shards between physical servers for rebalancing
- **Future-proofing:** Add more physical servers without changing application logic
- **Easier re-sharding:** Redistribute logical shards rather than rehashing all data

```
Physical DB 1: Logical shards 0-14
Physical DB 2: Logical shards 15-29
Physical DB 3: Logical shards 30-44
...
```

#### Cross-Shard Queries

The Achilles' heel of sharding. Strategies to handle:

**1. Scatter-Gather**
Query all shards, aggregate results:
```python
results = []
for shard in all_shards:
    results.extend(shard.execute(query))
return aggregate(results)
```
*Expensive but sometimes necessary*

**2. Denormalization**
Duplicate data so queries can be satisfied within a single shard.

**3. Application-Level Joins**
Fetch data from multiple shards and join in the application layer.

**4. Avoid by Design**
Structure your data model so cross-shard queries are rare or unnecessary.

#### Re-sharding

When you need to add or redistribute shards, you have several options:

**1. Double-and-Split**
Double the number of shards, split each existing shard in half.

**2. Consistent Hashing**
Minimizes data movement when adding/removing shards. Only K/n keys move on average (K = total keys, n = number of shards).

**3. Logical Shard Migration**
If using logical/physical separation, migrate logical shards to new physical servers without application changes.

#### Trade-offs

| Benefit | Cost |
|---------|------|
| Horizontal scalability—add more servers as needed | Complex database design and management |
| Distributes both read and write load | Cross-shard queries are expensive |
| Handles massive data volumes | Application must be shard-aware |
| Can scale nearly infinitely | Re-sharding is challenging and resource-intensive |
| Geographic distribution possible | Operational complexity increases significantly |

#### Best Practices

1. **Exhaust simpler options first**—sharding adds significant complexity
2. **Choose your shard key very carefully**—it's extremely difficult to change later
3. **Use logical/physical shard separation**—provides flexibility for future growth
4. **Plan for re-sharding from day one**—design your system to handle it
5. **Implement robust monitoring**—detect hot spots and uneven distribution
6. **Use connection pooling**—manage connections across many shards efficiently
7. **Consider a sharding middleware**—Vitess, Citus, etc. handle much complexity for you

---

### 4. Replication

**Concept:** Creating copies of your primary database on different servers to improve availability, distribute read load, and enhance fault tolerance.

#### Why Replicate?

- **High availability:** If the primary fails, promote a replica
- **Read scaling:** Distribute read queries across replicas
- **Geographic distribution:** Place replicas closer to users
- **Disaster recovery:** Maintain copies in different regions
- **Backup without production impact:** Run backups from replicas

#### Replication Topologies

**1. Single-Leader (Primary-Replica)**
Most common topology:
```
Primary (read/write)
    ↓
Replica 1 (read-only)
Replica 2 (read-only)
Replica 3 (read-only)
```

**2. Multi-Leader (Primary-Primary)**
Multiple nodes accept writes:
```
Primary 1 (read/write) ←→ Primary 2 (read/write)
     ↓                           ↓
Replica 1                   Replica 2
```
*Useful for multi-region setups but introduces conflict resolution complexity*

**3. Leaderless (Peer-to-Peer)**
Any node can accept reads and writes:
```
Node 1 ←→ Node 2 ←→ Node 3
```
*Used by systems like Cassandra; requires quorum-based consistency*

#### Synchronous vs. Asynchronous Replication

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| **How it works** | Primary waits for replica(s) to confirm before committing | Primary commits immediately, replicates in background |
| **Consistency** | Strong—replicas always current | Eventual—temporary lag possible |
| **Performance** | Higher write latency | Lower write latency |
| **Durability** | Higher—data exists on multiple nodes | Lower—data could be lost if primary fails before replication |
| **Availability impact** | Replica failure can block writes | Replica failure doesn't affect writes |

**Semi-synchronous:** A hybrid approach where at least one replica must acknowledge before commit, but not all:
```
Primary commits after Replica 1 confirms
Replica 2 and 3 replicate asynchronously
```

#### Replication Lag

In asynchronous replication, replicas may be behind the primary. This creates consistency challenges:

**Read-your-writes consistency problem:**
1. User writes data to primary
2. User's next request hits a replica
3. Replica hasn't received the write yet
4. User sees stale data (or thinks their write failed)

**Solutions:**
- **Sticky sessions:** Route user to same replica for session duration
- **Read from primary after writes:** Temporarily read from primary after user writes
- **Causal consistency:** Track dependencies, ensure reads reflect user's own writes
- **Synchronous replication:** Eliminates lag (at performance cost)

#### Monitoring Replication Health

Key metrics to track:
- **Replication lag:** How far behind is each replica?
- **Replication throughput:** Write-ahead log (WAL) send/receive rate
- **Replication slot status:** Is replication keeping up or falling behind?
- **Replica connection status:** Are replicas connected and healthy?

```sql
-- PostgreSQL: Check replication lag
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

#### Failover Strategies

**Manual failover:**
- DBA promotes replica to primary
- Application configuration updated to point to new primary
- Simple but slow (minutes to hours)

**Automated failover:**
- Monitoring system detects primary failure
- Orchestration tool (Patroni, Orchestrator, etc.) promotes replica
- DNS or proxy updated automatically
- Fast (seconds to minutes) but requires careful configuration to avoid split-brain

**Preventing split-brain:**
- Use fencing (STONITH) to ensure old primary can't accept writes
- Implement quorum-based leader election
- Use distributed consensus (etcd, Consul, ZooKeeper)

#### Read Replica Routing

Strategies for distributing reads across replicas:

**1. Round-robin:** Simple rotation across replicas
```python
def get_read_connection():
    global replica_index
    conn = replicas[replica_index % len(replicas)]
    replica_index += 1
    return conn
```

**2. Least-connections:** Route to replica with fewest active connections

**3. Latency-based:** Route to replica with lowest latency

**4. Geographic:** Route to geographically closest replica

**5. Lag-aware:** Skip replicas that are too far behind
```python
def get_read_connection(max_lag_bytes=1000000):
    for replica in replicas:
        if replica.lag_bytes < max_lag_bytes:
            return replica
    return primary  # Fall back to primary if all replicas lagging
```

#### Trade-offs

| Benefit | Cost |
|---------|------|
| Improved read performance (distribute reads across replicas) | Complexity in maintaining consistency |
| High availability (failover to replica if primary fails) | Storage overhead (multiple copies of data) |
| Geographic distribution (replicas closer to users) | Replication lag in async mode |
| Fault tolerance | Network bandwidth for synchronization |
| Backup without production impact | Operational overhead of managing replicas |

#### Best Practices

1. **Monitor replication lag continuously**—set alerts for excessive lag
2. **Test failover regularly**—don't wait for a real outage to discover problems
3. **Use connection pooling**—PgBouncer, ProxySQL help manage connections efficiently
4. **Consider semi-synchronous** for balance of consistency and performance
5. **Implement lag-aware routing**—don't send reads to severely lagging replicas
6. **Plan replica placement**—consider network topology and failure domains
7. **Use streaming replication** over log shipping for lower lag

---

## Strategy Selection Guide

| Scenario | Recommended Strategies |
|----------|----------------------|
| **Read-heavy workload** | Replication → Caching → Indexing |
| **Write-heavy workload** | Sharding → Partitioning |
| **Large tables, single server** | Partitioning → Indexing |
| **Beyond single server capacity** | Sharding + Replication |
| **Need high availability** | Replication (synchronous or semi-sync) |
| **Time-series data** | Partitioning (by time range) → Indexing |
| **Multi-tenant SaaS** | Sharding (by tenant_id) |
| **Massive scale (millions of users)** | Sharding + Replication + Caching + Indexing |

---

## Combining Strategies

In production, these strategies are often combined:

```
                    Load Balancer
                         │
              ┌──────────┴──────────┐
              │                     │
         Shard 1               Shard 2
              │                     │
    ┌─────────┴─────────┐   ┌──────┴──────┐
    │                   │   │              │
Primary            Replicas    Primary    Replicas
(partitioned)      (×2)       (partitioned)  (×2)
    │
    ├── Partition Q1 (indexed)
    ├── Partition Q2 (indexed)
    ├── Partition Q3 (indexed)
    └── Partition Q4 (indexed)
```

**Example: E-commerce at scale**
- **Sharding:** Orders sharded by customer_id
- **Partitioning:** Each shard partitions orders by order_date
- **Indexing:** B-tree indexes on order_id, product_id, order_status
- **Replication:** Each shard has 2 read replicas for high availability

---

## Choosing a New Database

If you've exhausted your current database's options and must migrate:

### Principles for Selection

1. **Boring is good.** Prefer databases that have been battle-tested over years, not the newest shiny option.

2. **Check the market.** Is there a ready pool of experienced administrators and developers?

3. **Beware marketing claims.** "Infinite horizontal scalability" always has hidden costs.

4. **Read the manual, not the brochure.** Find the "Limits" and "FAQ" pages—that's where the real constraints live.

5. **Join the community.** Chat rooms, GitHub issues, and forums reveal real-world problems.

### NoSQL Trade-offs

Many NoSQL databases offer higher scale than relational databases, often claiming near-linear horizontal scalability. Common trade-offs:

- Eliminated or limited transactional guarantees
- Severely limited data modeling flexibility
- No queries across data entities
- Highly denormalized data (same data stored in many collections)

### Before You Commit

**Run a shoot-out:**
1. Create a realistic test bench using your own data
2. Use your real-world access patterns
3. Measure P99 latencies (averages are meaningless)
4. Push the system until it breaks
5. Test operational tasks: failover, network partitions, resharding

---

## Migration Checklist

1. ☐ Confirmed current database truly cannot meet needs
2. ☐ Read current database manual completely
3. ☐ Explored all configuration tuning options
4. ☐ Tried adding cache/replicas/partitions first
5. ☐ Evaluated 3+ candidate databases
6. ☐ Read each candidate's "Limits" documentation
7. ☐ Benchmarked with real data and access patterns
8. ☐ Tested failure scenarios (failover, partitions)
9. ☐ Written detailed step-by-step migration plan
10. ☐ Had plan peer-reviewed
11. ☐ Migrated a small service first as proof-of-concept

---

## Quick Reference: Scaling Strategies Summary

| Strategy | What It Does | Best For | Complexity |
|----------|--------------|----------|------------|
| **Indexing** | Speeds up data lookups via sorted data structures | Read-heavy queries, filtering, sorting | Low |
| **Partitioning** | Splits table into pieces on same server | Large tables, time-series, data lifecycle | Low-Medium |
| **Sharding** | Splits data across multiple servers | Massive scale, write-heavy, beyond single server | High |
| **Replication** | Creates database copies on multiple servers | Read scaling, high availability, fault tolerance | Medium |

---

## Case Study: How Notion Scaled to Hundreds of Millions of Users

Notion's scaling journey provides an excellent real-world example of applying these strategies under pressure. Their unique data model and explosive growth created challenges that required creative solutions.

### The Problem: A Database Ready to Explode

**Background:** In 2021, Notion's popularity skyrocketed, but their service became unbearably slow. Their PostgreSQL database had grown to terabytes of compressed data and was showing serious signs of stress.

**Notion's Unique Data Model:** Everything in Notion is a "block"—a piece of text, an image, a checkbox, or even an entire page. Each block is stored as a row in Postgres with its own unique ID. Blocks can be nested within other blocks to create complex tree-like structures. This provides incredible flexibility but means even a simple document can result in hundreds or thousands of database rows.

**The symptoms:**
- Increased latency when requesting page data
- VACUUM processes consistently stalling
- Tables becoming bloated with dead tuples
- Approaching transaction ID wraparound—a catastrophic scenario where PostgreSQL enters read-only mode

> **PostgreSQL VACUUM:** A critical maintenance operation that reclaims storage from deleted/updated rows. When VACUUM can't keep up, tables bloat and performance degrades.

> **Transaction ID Wraparound:** PostgreSQL assigns sequential transaction IDs. If IDs exhaust (after ~4 billion transactions without VACUUM), the database must go read-only to prevent data loss. For a note-taking app, this would mean users couldn't edit or delete anything.

### Phase 1: Initial Sharding (32 Physical Shards)

**Why not just scale up?** Vertical scaling (bigger servers) was considered, but:
- Physical hardware limits exist
- Costs increase exponentially at the high end
- Query performance and maintenance often degrade before hitting hardware limits
- Single point of failure remains

**The sharding decision:** Notion chose to shard all tables linked to the block table via foreign keys—workspaces, discussion threads, comments—keeping related data together in the same shard.

#### Choosing the Shard Key: Workspace ID

Notion chose `workspace_id` as their shard key because:
- Users typically request data for a single workspace at a time
- Keeps all related data (blocks, comments, discussions) on the same shard
- Avoids expensive cross-shard queries for the most common operations
- High cardinality—many unique workspaces

#### Physical vs. Logical Shard Architecture

Rather than simply creating 32 databases, Notion implemented a **logical/physical shard separation**:

| Component | Count | Purpose |
|-----------|-------|---------|
| Physical database instances | 32 | Actual PostgreSQL servers |
| Logical shards per physical instance | 15 | PostgreSQL schemas within each database |
| Total logical shards | 480 | Virtual divisions of data |

Each logical shard has its own tables (block, workspace, comments) represented as PostgreSQL schemas within a physical database.

**Why this architecture?**
- **Flexibility:** Can move logical shards between physical servers without application changes
- **Rebalancing:** Easier to redistribute load by moving logical shards
- **Future-proofing:** Adding physical capacity doesn't require changing application logic

#### Sizing the Infrastructure

Requirements calculated for 2+ year growth:
- Instance type needed at least **60K total IOPS** (read/write operations per second)
- Set limits of **500GB per table** and **10TB per physical instance** to maintain RDS replication health

#### Routing Mechanism

Routing happens at the application level using a two-step process:

```
workspace_id 
    → hash(workspace_id) % 32 → Physical database (1 of 32)
    → hash(workspace_id) % 15 → Logical schema (1 of 15)
```

#### Connection Pooling with PgBouncer

With 32 databases, connection management became critical. Notion used **PgBouncer** as an intermediary:

- **What PgBouncer does:** Maintains a pool of active connections to PostgreSQL, allowing applications to reuse connections rather than establishing new ones for each query
- **Why it matters:** PostgreSQL connections are expensive (memory, process overhead). Connection pooling dramatically reduces this overhead.

```
Application → PgBouncer Pool → PostgreSQL Shards
```

#### The Migration Process

**Challenge:** Syncing existing data to new shards while the system remains operational.

**Options considered:**

| Approach | Pros | Cons |
|----------|------|------|
| Dual writes (write to both old and new) | Simple concept | Flaky data if any write fails |
| PostgreSQL logical replication | Built-in, reliable | Couldn't add workspace_id during migration |
| Audit log + catch-up script | Flexible, can transform data | Required custom implementation |

**Chosen approach: Audit log + catch-up script**
1. Log all writes to old database
2. Use a script to replay changes to new databases with schema modifications
3. Migration took ~3 days using an m5.24xlarge instance (96 CPUs)

**Version comparison:** During migration, record versions were compared to ensure newer data wasn't overwritten by older replayed data.

**The switch:** 
1. Updated PgBouncer to route queries to new shards
2. Carefully orchestrated cutover during low-traffic period

### Phase 2: Re-sharding to 96 Physical Shards

**Timeline:** Late 2022—less than two years later

**New symptoms:**
- Some shards hitting 90% CPU utilization during peak traffic
- Approaching disk bandwidth (IOPS) limits
- PgBouncer connection limits being reached
- New Year traffic spikes looming

#### The Re-sharding Strategy

**Goal:** Increase from 32 to 96 physical databases while maintaining the logical shard structure.

| Old Architecture | New Architecture |
|------------------|------------------|
| 32 physical instances | 96 physical instances |
| 15 logical schemas each | 5 logical schemas each |
| 480 total logical shards | 480 total logical shards (unchanged) |

Each old instance (15 schemas) split into 3 new instances (5 schemas each).

**Smaller instance benefit:** New instances could use smaller instance types since they managed less data, reducing both CPU/IOPS pressure and costs.

#### Data Synchronization: PostgreSQL Logical Replication

Unlike the first migration, no schema changes were needed, enabling use of PostgreSQL's native logical replication:

1. Created 3 **publications** on each existing database (each covering 5 logical schemas)
2. New databases created **subscriptions** to consume their relevant publication
3. Data continuously replicated to new databases during migration

#### Critical Optimization: Deferred Index Creation

**Problem:** Creating indexes during data sync dramatically slows down the process.

**Solution:** Created indexes *after* data transfer completed.

**Result:** Reduced sync time from **3 days to 12 hours**.

> **Why this works:** Index creation requires sorting and organizing data. Doing this while data is streaming in means constant reorganization. Waiting until data is complete allows a single, efficient index build.

#### The PgBouncer Scaling Challenge

**Problem:** The migration required temporarily having both old and new database entries in PgBouncer configuration.

Original setup:
- 100 PgBouncer instances
- Each managing 32 database entries
- Up to 6 connections per database per PgBouncer instance
- Maximum 600 connections per database

**The math problem:** Each old shard maps to 3 new shards. Options:
1. **Increase connections 3x:** 18 connections × 100 instances = 1,800 connections per shard (would overload PostgreSQL)
2. **Reduce connections per instance:** Wouldn't handle the traffic, causing query backlogs

**Solution: Shard the PgBouncer cluster itself**

Created 4 new PgBouncer clusters, each managing 24 databases:
- 8 connections per PgBouncer per shard
- Total 200 connections per PostgreSQL instance
- Isolated failures to 25% of fleet

#### Pre-Production Validation: Dark Reads

Before switching production traffic, Notion implemented **dark reads** for validation:

1. For each request, fetch data from *both* old and new databases
2. Compare results for consistency
3. Log any discrepancies
4. Limited to queries returning ≤5 rows to minimize performance impact
5. Sampled only a portion of requests
6. Added 1-second delay before dark read to allow replication catch-up

**Result:** Nearly 100% identical data, validating the migration.

#### The Failover Process

1. **Traffic pause:** Halted new connections, allowed ongoing queries to complete
2. **Replication check:** Verified new databases fully caught up
3. **Configuration update:**
   - Revoked application access to old databases
   - Updated PgBouncer to point to new databases
   - Reversed replication direction (new → old) as rollback insurance
4. **Resume traffic:** Directed to new shards

### Key Outcomes

| Metric | Before | After |
|--------|--------|-------|
| Peak CPU utilization | ~90% | ~20% |
| IOPS utilization | Near limits | Well within capacity |
| Connection headroom | Tight | Comfortable |
| Future scalability | Limited | Positioned for continued growth |

### Notable Strategies and Lessons

#### 1. Logical vs. Physical Shard Separation
Keeping 480 logical shards constant while changing physical infrastructure allowed Notion to scale without application-level changes. This is a powerful pattern for long-term scalability.

#### 2. Shard Key Selection
Choosing `workspace_id` aligned perfectly with access patterns—users work within a single workspace, so all their data lives on one shard.

#### 3. Connection Pooling as Infrastructure
PgBouncer wasn't just an optimization—it was essential infrastructure that itself needed to be sharded as the system grew.

#### 4. Index Creation Timing
A simple optimization (defer index creation) reduced migration time by 83%. Always consider the order of operations in large data movements.

#### 5. Dark Reads for Validation
Testing in production without impacting users provided confidence in the migration. This pattern is valuable for any major infrastructure change.

#### 6. Reversible Migrations
By reversing replication direction (new → old), Notion maintained a rollback path. Always plan for the possibility that a migration needs to be undone.

#### 7. Incremental Scaling
Notion didn't try to build for "infinite scale" from day one. They scaled in response to actual growth, learning from each iteration.

### Architecture Evolution Summary

```
2021 (Before)              2021 (After Phase 1)         2022 (After Phase 2)
┌─────────────┐            ┌──────────────────┐         ┌────────────────────┐
│  Single     │            │   32 Physical    │         │   96 Physical      │
│  PostgreSQL │     →      │   Databases      │    →    │   Databases        │
│  (terabytes)│            │   (15 schemas    │         │   (5 schemas       │
│             │            │    each = 480    │         │    each = 480      │
│             │            │    logical)      │         │    logical)        │
└─────────────┘            └──────────────────┘         └────────────────────┘
                                    │                            │
                           ┌────────┴────────┐          ┌────────┴────────┐
                           │   PgBouncer     │          │  4 PgBouncer    │
                           │   (100 nodes)   │          │  Clusters       │
                           └─────────────────┘          │  (24 DBs each)  │
                                                        └─────────────────┘
```

---

## Additional Resources

- ByteByteGo System Design Newsletter: blog.bytebytego.com
- Database vendor documentation—especially the "Limits" pages
- Open-source project GitHub issues for real-world insights
- PostgreSQL documentation on partitioning and replication
- Vitess documentation for application-level sharding
- PgBouncer documentation for connection pooling

---

*Remember: There is no free lunch in database scaling. Every strategy has trade-offs. The best solution depends on your specific workload, growth trajectory, and operational capabilities. Start simple, measure everything, and scale incrementally based on real data.*
