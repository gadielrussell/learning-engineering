# Database Sharding & Partitioning: A Deep Dive

A comprehensive system design reference for understanding when, why, and how to shard your database.

## Video Reference

[![Sharding in System Design Interviews w/ Meta Staff Engineer](https://img.youtube.com/vi/L521gizea4s/maxresdefault.jpg)](https://www.youtube.com)

---

## The Fundamental Problem: Why Sharding Exists

Imagine you've launched an app with a single AWS RDS Postgres instance—a substantial one with 70TB of storage handling 10,000 writes per second. In the early days, everything runs smoothly. Traffic grows, but the database keeps up.

Then you hit a ceiling. You now need 20,000 writes per second. Storage is approaching limits. Queries slow down. Backups take forever.

**The natural first instinct: vertical scaling.** Upgrade to bigger hardware. AWS offers machines with 140TB storage and ~50,000 writes per second. This works—for a while.

But eventually, you go global. Traffic keeps growing. You've saturated CPU, storage, and I/O. No matter how big the database, it simply can't keep up.

**That's when you reach for sharding.**

---

## What Is Sharding?

Sharding is the process of splitting your data across multiple machines so that no single database holds everything.

Each shard is its own standalone database with:
- Its own CPU
- Its own memory
- Its own storage
- Its own connection pool
- Just a subset of the total data

Together, the shards form the complete dataset. You scale by adding more shards.

```
┌─────────────────────────────────────────────────────────┐
│                    BEFORE SHARDING                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Single Database                     │   │
│  │         All Users (0 - 30 million)              │   │
│  │         70TB storage, 10K writes/sec            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    AFTER SHARDING                       │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
│  │   Shard 1     │ │   Shard 2     │ │   Shard 3     │ │
│  │  Users 0-10M  │ │ Users 10M-20M │ │ Users 20M-30M │ │
│  │  23TB, 10K/s  │ │  23TB, 10K/s  │ │  23TB, 10K/s  │ │
│  └───────────────┘ └───────────────┘ └───────────────┘ │
│                                                         │
│  Combined: 70TB storage, 30K writes/sec capacity        │
└─────────────────────────────────────────────────────────┘
```

---

## Sharding vs. Partitioning: Clarifying the Terms

These terms are often used interchangeably, but there's a distinction:

| Concept | Definition | Key Characteristic |
|---------|------------|-------------------|
| **Partitioning** | Dividing data within a single database instance | Data stays on one machine; logical separation only |
| **Sharding** | Distributing data across multiple database instances | Data lives on different machines; physical separation |

**Partitioning** is a database feature (e.g., Postgres table partitioning) that helps with query performance and maintenance by logically dividing tables. The data still lives on one server.

**Sharding** is an architectural pattern that distributes data across multiple servers. It's what you need when a single machine can't handle the load.

In practice, most people use "sharding" to mean horizontal partitioning across multiple machines. That's the focus of this guide.

---

## The Two Questions of Sharding

When you decide to shard, you must answer two questions:

### Question 1: What do we shard by? (The Shard Key)

The **shard key** is the field used to group your data. All data sharing the same shard key value lives on the same shard.

Example: If you shard by `user_id`, all data for a given user lives on one shard.

### Question 2: How do we distribute values across shards? (Distribution Strategy)

The **distribution strategy** determines how shard key values map to physical shards.

Example: User IDs 0-10M go to Shard 1, or hash(user_id) % num_shards determines placement.

---

## Choosing a Shard Key

**In a system design interview, if you mention sharding, immediately state your shard key and justify it.**

### The Three Properties of a Good Shard Key

#### 1. High Cardinality
The field should have many unique values so data can spread across shards instead of piling onto a few.

```
✓ user_id      → millions of unique values
✓ order_id     → millions of unique values
✗ is_premium   → only 2 values (true/false)
✗ country_code → ~200 values (may work, depends on distribution)
```

#### 2. Even Distribution
Values should naturally spread so each shard holds roughly equal data and receives roughly equal traffic.

```
✓ user_id (if users created uniformly over time)
✓ order_id (if orders created uniformly)
✗ creation_date (if most queries hit recent data)
✗ region (if 80% of users are in one region)
```

#### 3. Query Alignment
The shard key should match how you query data. If most queries scope to a single user, shard by user_id so queries hit one shard.

```
Query: "Get all posts for user 123"
✓ Shard by user_id → hits 1 shard
✗ Shard by post_id → hits ALL shards (scatter-gather)

Query: "Get order details for order 456"
✓ Shard by order_id → hits 1 shard
✗ Shard by user_id → still hits 1 shard (if user_id in query)
```

### Good vs. Bad Shard Key Examples

| Scenario | Good Shard Key | Why |
|----------|---------------|-----|
| Social media (load user profiles) | `user_id` | High cardinality, even distribution, queries are user-centric |
| E-commerce (view order details) | `order_id` | High cardinality, even distribution, queries are order-centric |
| Multi-tenant SaaS | `tenant_id` | Isolates tenant data, queries scoped to tenant |
| Chat application | `conversation_id` | Messages in a conversation stay together |

| Scenario | Bad Shard Key | Why |
|----------|--------------|-----|
| Any | `is_premium` (boolean) | Only 2 values—caps you at 2 shards |
| Social media | `creation_date` | Hot spot on the "current" shard; old shards sit idle |
| E-commerce | `product_category` | Low cardinality; uneven if one category dominates |
| Any | `status` (enum) | Low cardinality; queries often need multiple statuses |

---

## Distribution Strategies

Once you've chosen a shard key, you need a strategy for mapping values to shards.

### Strategy 1: Range-Based Sharding

Divide the shard key into sequential ranges.

```
Shard 1: user_id 0 - 10,000,000
Shard 2: user_id 10,000,001 - 20,000,000  
Shard 3: user_id 20,000,001 - 30,000,000
```

**Pros:**
- Simple and intuitive
- Range queries within a shard are efficient
- Easy to understand which data lives where

**Cons:**
- Uneven distribution if data doesn't grow uniformly
- New users always hit the highest shard (hot spot)
- Requires manual range splitting as data grows

**When to use:** Data naturally falls into clean ranges and grows steadily. You're willing to manually rebalance.

**Reality check:** Rarely used in production for the primary distribution. Too prone to hot spots.

### Strategy 2: Hash-Based Sharding (Industry Default)

Hash the shard key and mod by number of shards.

```python
shard_number = hash(user_id) % num_shards
```

The hash function "scrambles" the input, distributing data evenly across shards.

```
hash("user_123") % 3 = 1  → Shard 1
hash("user_456") % 3 = 0  → Shard 0
hash("user_789") % 3 = 2  → Shard 2
```

**Pros:**
- Even distribution (the hash randomizes placement)
- No hot spots from sequential IDs
- Simple to implement

**Cons:**
- Range queries become expensive (data is scattered)
- Adding/removing shards requires massive data movement

**The Resharding Problem:**

```
Before: hash(key) % 3  →  key lands on shard 1
After:  hash(key) % 4  →  key lands on shard 2 (MOVED!)
```

When you change the number of shards, almost everything moves. This is operationally catastrophic.

**Solution: Consistent Hashing**

Instead of simple modulo, consistent hashing places both keys and shards on a virtual ring. Keys map to the next shard clockwise on the ring.

```
        ┌─────────────────┐
       /                   \
      /     Virtual Ring    \
     │                       │
     │    S1 ●               │
     │         ╲             │
     │          ╲  ← key_A   │
     │           ╲           │
     │            ● S2       │
     │           /           │
     │          /            │
     │    S3 ● ← key_B       │
     │                       │
      \                     /
       \                   /
        └─────────────────┘
```

When you add a shard, only keys between the new shard and its neighbor move—not everything.

**Interview tip:** When you say "shard by user_id," your interviewer assumes hash-based sharding with consistent hashing. You may not even need to say it explicitly (especially at senior+ levels). For junior/mid-level, be prepared to explain the mechanism.

### Strategy 3: Directory-Based Sharding

Use an explicit lookup table to map each key to its shard.

```
┌──────────────┬─────────┐
│   user_id    │  shard  │
├──────────────┼─────────┤
│   user_123   │    1    │
│   user_456   │    2    │
│   user_789   │    1    │
│   messi      │    4    │  ← celebrity shard
└──────────────┴─────────┘
```

**Pros:**
- Maximum flexibility
- Can move individual users to dedicated shards
- Custom logic for hot users, VIPs, etc.

**Cons:**
- Every request requires two hops (lookup → query)
- Lookup table is a single point of failure
- Added latency for every operation

**When to use:** You absolutely need per-entity control and can afford the extra hop.

**Interview warning:** Directory-based sharding is almost never the right answer in interviews. It introduces a single point of failure and extra latency, inviting follow-up questions that can derail your interview. Stick with hash-based as your default.

### Distribution Strategy Summary

| Strategy | Distribution | Flexibility | Complexity | Use Case |
|----------|-------------|-------------|------------|----------|
| Range-based | Can be uneven | Low | Low | Naturally ranged data |
| Hash-based | Even | Medium | Medium | **Default choice** |
| Directory-based | Controlled | High | High | Celebrity problem, custom routing |

---

## The Three Major Sharding Challenges

Sharding solves your scaling problem but introduces new ones. These are the follow-up questions interviewers will probe.

### Challenge 1: Hot Spots (Load Imbalance)

Even with a good shard key, some shards can receive disproportionate traffic.

**The Celebrity Problem:**

You shard by `user_id`. Lionel Messi lands on Shard 1. Every time someone views his profile, comments on his posts, or likes his content—all that traffic hits Shard 1. It becomes orders of magnitude hotter than other shards.

```
Normal shards:     ~1,000 req/sec each
Messi's shard:    ~500,000 req/sec  ← 🔥 HOT
```

**Solution 1: Compound Shard Key**

Add a suffix to distribute a single user's data across multiple shards.

```python
# Before: all Messi data on one shard
shard = hash(user_id) % num_shards

# After: Messi's posts spread across N shards
shard = hash(f"{user_id}_{post_id % N}") % num_shards

# Or time-based distribution
shard = hash(f"{user_id}_{timestamp.hour}") % num_shards
```

**Solution 2: Dedicated Celebrity Shard**

Detect high-traffic users and route them to special shards with beefier hardware.

```
┌─────────────────────────────────────────┐
│           Routing Layer                 │
│                                         │
│   if user in celebrity_list:            │
│       → route to Celebrity Shard        │
│   else:                                 │
│       → hash-based routing              │
└─────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐   ┌─────────────────┐
│ Celebrity Shard │   │ Normal Shards   │
│ (special HW)    │   │ (hash-based)    │
└─────────────────┘   └─────────────────┘
```

This uses directory-based lookup only for the outliers, keeping the common path fast.

### Challenge 2: Cross-Shard Queries

When your query doesn't align with your shard key, you must hit multiple (or all) shards.

```
Query: "Get user 123's posts"
       → Shard by user_id
       → Hits 1 shard ✓

Query: "Get top 10 trending posts globally"  
       → Must query ALL shards
       → Aggregate results
       → Expensive! ✗
```

**The Scatter-Gather Pattern:**

```
┌─────────────────────────────────────────────────────┐
│                   Application                        │
│                       │                              │
│            ┌──────────┼──────────┐                  │
│            ▼          ▼          ▼                  │
│       ┌────────┐ ┌────────┐ ┌────────┐             │
│       │Shard 1 │ │Shard 2 │ │Shard 3 │ (scatter)   │
│       │top 10  │ │top 10  │ │top 10  │             │
│       └────┬───┘ └────┬───┘ └────┬───┘             │
│            │          │          │                  │
│            └──────────┼──────────┘                  │
│                       ▼                              │
│              Aggregate & Rank                        │
│              Return top 10         (gather)          │
└─────────────────────────────────────────────────────┘
```

**Solution 1: Cache Expensive Queries**

```
┌────────┐      ┌───────────┐      ┌─────────────┐
│ Client │ ───▶ │   Cache   │ ───▶ │   Shards    │
│        │ ◀─── │  (Redis)  │ ◀─── │ (on miss)   │
└────────┘      └───────────┘      └─────────────┘
```

First request is expensive (scatter-gather), but results are cached. Subsequent requests hit the cache. Set a TTL (e.g., 5 minutes) based on acceptable staleness.

**Trade-off:** You're trading consistency for latency. Users see data that might be a few minutes old.

**Solution 2: Pre-compute with Background Jobs**

Run a periodic job that computes global aggregations and stores results.

```python
# Every 5 minutes
def compute_trending_posts():
    results = scatter_gather_all_shards("SELECT top posts")
    cache.set("trending_posts", results, ttl=300)
```

**Solution 3: Denormalize Data**

Store redundant copies so related data lives together.

```
If you frequently need: user profile + their latest posts + follower count

Option A (normalized): 3 tables, potentially 3 shards
Option B (denormalized): embed follower_count and recent_posts in user record
```

**Trade-off:** Writes become more complex (update multiple copies), but reads stay on one shard.

**Key insight for interviews:** Cross-shard queries should be the exception, not the norm. If you're constantly querying across all shards, you likely chose the wrong shard key.

### Challenge 3: Cross-Shard Transactions (Consistency)

On a single database, transactions are straightforward:

```sql
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 5 WHERE user = 'Bob';
  UPDATE accounts SET balance = balance + 5 WHERE user = 'Alice';
COMMIT;
```

Both operations succeed or both fail. Atomicity guaranteed.

But when Bob is on Shard 1 and Alice is on Shard 3? These can't be one atomic operation.

**What if we deduct from Bob but the credit to Alice fails?** Money disappears. Inconsistent state.

**The Textbook Solution: Two-Phase Commit (2PC)**

```
┌─────────────────────────────────────────────────────────┐
│                    Coordinator                          │
│                         │                               │
│    Phase 1: PREPARE     │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│    │ Shard 1 │    │ Shard 2 │    │ Shard 3 │          │
│    │"Ready?" │    │"Ready?" │    │"Ready?" │          │
│    └────┬────┘    └────┬────┘    └────┬────┘          │
│         │  YES         │  YES         │  YES           │
│         └───────────────┼───────────────┘              │
│                         ▼                               │
│    Phase 2: COMMIT      │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│    │ Shard 1 │    │ Shard 2 │    │ Shard 3 │          │
│    │ COMMIT  │    │ COMMIT  │    │ COMMIT  │          │
│    └─────────┘    └─────────┘    └─────────┘          │
└─────────────────────────────────────────────────────────┘
```

**Problem:** 2PC is slow and fragile. If any shard or the coordinator fails mid-transaction, the whole thing can get stuck in a locked state.

**Better Solution 1: Avoid Cross-Shard Transactions**

Design your shard key so transactions stay on one shard. If all of a user's data is on one shard, user-scoped transactions are local.

**Better Solution 2: The Saga Pattern**

Instead of one atomic transaction, use a sequence of local transactions with compensating actions.

```
┌─────────────────────────────────────────────────────────┐
│                    SAGA: Transfer $5                    │
│                                                         │
│  Step 1: Deduct $5 from Bob (Shard 3)                  │
│          Compensating action: Refund $5 to Bob          │
│                         │                               │
│                         ▼                               │
│  Step 2: Credit $5 to Alice (Shard 1)                  │
│          Compensating action: Deduct $5 from Alice      │
│                         │                               │
│                         ▼                               │
│  If Step 2 fails:                                       │
│      Execute Step 1's compensating action               │
│      (Refund $5 to Bob)                                │
└─────────────────────────────────────────────────────────┘
```

Each step is a local transaction. If a step fails, run the compensating actions for all completed steps in reverse order.

**Trade-off:** You get eventual consistency, not immediate consistency. There's a window where Bob has been debited but Alice hasn't been credited. Your application must handle this intermediate state.

---

## Sharding in System Design Interviews

### When to Bring Up Sharding

Sharding comes up during **deep dives**, typically when addressing non-functional requirements around scaling. You need to justify it with numbers.

**Check these capacity limits:**

| Dimension | Question | Typical Single-DB Limit |
|-----------|----------|------------------------|
| Storage | Total data size? | ~100-150 TB |
| Write throughput | Writes per second? | ~50K writes/sec |
| Read throughput | Reads per second (with replicas)? | ~500K reads/sec |

### Do the Math

**Storage example:**
```
500 million users × 5 KB each = 2.5 TB
→ Single Postgres handles this easily
→ No sharding needed (but mention you'd shard at 10-100x growth)
```

**Write throughput example:**
```
50,000 writes/sec at peak
→ Single database would struggle
→ Sharding justified
```

**Read throughput example:**
```
100 million DAU × 10 queries/day = 1 billion queries/day
= ~12,000 queries/sec average
= ~36,000 queries/sec peak (3x average)
→ Read replicas might handle this
→ But with growth, sharding for reads may be needed
```

### The Four-Step Sharding Statement

When you've justified that sharding is necessary:

**Step 1: Propose a shard key based on access pattern**
> "For this social media app, most queries are user-centric—loading feeds, profiles, posts. So I'll shard by user_id."

**Step 2: State your distribution strategy**
> "I'll use hash-based sharding with consistent hashing to distribute users evenly across shards."

(At senior+ levels, this is assumed and you may skip it.)

**Step 3: Acknowledge trade-offs**
> "The trade-off is that global queries like 'trending posts' become expensive scatter-gather operations. I'd handle this by pre-computing trending content with a background job and caching the results."

**Step 4: Address growth**
> "I'll start with 10 shards, which gives room for 10x growth. Consistent hashing makes it straightforward to add shards later without massive data movement."

### What NOT to Do

**Don't reflexively shard.** Modern hardware goes far. It can be impressive to show you did the math and sharding isn't needed yet.

**Don't forget to justify.** "I'll shard by user_id" without explaining why invites skepticism.

**Don't ignore the trade-offs.** Interviewers want to see you understand the costs, not just the benefits.

---

## Quick Reference Card

### Shard Key Checklist
- [ ] High cardinality (many unique values)
- [ ] Even distribution (no hot spots)
- [ ] Query alignment (common queries hit one shard)

### Distribution Strategy Decision
```
Need even distribution + easy scaling?  → Hash-based with consistent hashing
Data naturally ranged + limited scale?  → Range-based  
Need per-entity control?                → Directory-based (rare)
```

### Handling Common Problems
```
Hot spots?           → Compound shard key or dedicated shard
Cross-shard queries? → Cache, pre-compute, or denormalize
Cross-shard txns?    → Saga pattern or redesign shard key
```

### Interview Checklist
- [ ] Justified need with capacity math
- [ ] Stated shard key with reasoning
- [ ] Mentioned distribution strategy (if junior/mid)
- [ ] Acknowledged trade-offs
- [ ] Explained growth strategy

---

## Key Takeaways

1. **Sharding is a last resort.** Exhaust vertical scaling, caching, and read replicas first.

2. **The shard key is everything.** A bad choice creates hot spots and expensive cross-shard queries that are hard to fix later.

3. **Hash-based with consistent hashing is the default.** Know it cold. Mention others only if specifically applicable.

4. **Trade-offs are unavoidable.** Sharding solves scale but introduces complexity. Be ready to discuss hot spots, cross-shard queries, and consistency challenges.

5. **Always justify with math.** Don't shard because it sounds sophisticated. Shard because the numbers demand it.

---

*"Sharding should be the exception, not the norm. Most systems will never need it. But when you do, choose your shard key like your system depends on it—because it does."*
