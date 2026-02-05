# Distributed Caching Systems: A Deep Dive for System Design Interviews

Caching sits at the heart of every high-performance distributed system, dramatically reducing latency and database load. **Redis dominates the distributed caching landscape**, but understanding when Memcached's simplicity wins, how cloud-managed services differ architecturally, and which patterns prevent cache stampedes separates strong candidates from average ones.

This guide covers Redis (including cloud variants), Memcached, Hazelcast, Apache Ignite, and CDN caching. The depth includes the architectural differences between Azure Managed Redis and Azure Cache for Redis that exemplify how cloud offerings can vary significantly despite similar names.

## Technology deep dive

### Redis: The versatile data structure store

Redis transcends simple key-value caching with its rich data structure support. Understanding these structures and their use cases demonstrates cache expertise:

**Data structures and use cases:**
- **Strings:** Caching, counters, rate limiters
- **Lists:** Recent activity feeds, message queues
- **Hashes:** Object storage, session data
- **Sets:** Tags, unique visitors, social graphs
- **Sorted Sets:** Leaderboards, time-series, priority queues
- **Streams:** Event sourcing, activity logs
- **HyperLogLog:** Cardinality estimation (unique counts)
- **Bitmaps:** Feature flags, user activity tracking

**Memory management:** Redis uses **jemalloc** to minimize fragmentation. Internal structures like SDS (Simple Dynamic Strings), ziplists (compact encoding for small structures), and intsets (small integer sets) optimize memory usage. The `maxmemory` configuration caps usage; eviction policies handle overflow.

**Persistence options:**

| Mode | Mechanism | Trade-off |
|------|-----------|-----------|
| **RDB** | Point-in-time snapshots via fork | Compact, potential data loss between snapshots |
| **AOF** | Log every write operation | Durable, larger files, three sync modes |
| **Hybrid** | AOF for durability, RDB for faster restart | Best of both |

**AOF sync modes:** `always` (safest, slowest), `everysec` (balanced, default), `no` (fastest, OS-controlled flush).

**Replication architecture:** Primary-replica with asynchronous replication by default. Replicas are read-only, enabling read scaling. Up to 5 replicas per primary in most configurations.

**Cluster mode vs standalone:**
- **Standalone:** Single node, simpler, limited by single machine capacity
- **Cluster:** Data partitioned across 16,384 hash slots distributed among shards. Automatic failover, horizontal scaling, but multi-key operations limited to same slot.

### Cloud-managed Redis: Architectural differences matter

The Azure Redis offerings exemplify how managed services can differ architecturally despite similar functionality:

**Azure Cache for Redis (Basic/Standard/Premium):**
- Runs **community edition Redis**
- **Single-threaded** architecture
- Two VMs: primary and replica with asynchronous replication
- Scaling adds memory but doesn't utilize additional vCPUs efficiently

**Azure Managed Redis (new offering):**
- Runs **Redis Enterprise stack**
- **Multi-threaded** with multiple shards per node
- Up to **15x higher throughput** than equivalent Standard tier
- Three clustering policies: OSS (highest throughput), Enterprise (RediSearch support), Non-Clustered (≤25 GB only)
- Zone redundant with HA enabled
- Up to **99.999% availability SLA** with active geo-replication

**Why this matters for interviews:** Understanding that "Azure Redis" isn't monolithic demonstrates sophistication. The single-threaded vs multi-threaded difference fundamentally affects capacity planning and cost.

**AWS ElastiCache for Redis:**
- Cluster mode enabled: up to 500 shards, 6 nodes per shard
- Cluster mode disabled: single shard with up to 5 replicas
- ElastiCache Serverless: proxy-based architecture with auto-scaling
- Global Datastore for cross-region replication

**Key cloud Redis limitations:**

| Service | Max Memory | Max Shards | Notable Constraints |
|---------|------------|------------|---------------------|
| Azure Cache Premium | 120 GB | 10 | Single-threaded |
| Azure Managed Redis | 4.5 TB | Abstracted | Clustering policy affects features |
| AWS ElastiCache | Varies by node | 500 | Cluster mode affects availability |

### Memcached: Simplicity at scale

Memcached focuses on one thing: high-performance key-value caching. Its constraints are features for specific use cases.

**Architecture characteristics:**
- **Multi-threaded:** Better CPU utilization than single-threaded Redis
- **Slab allocation:** Pre-allocated memory pages prevent fragmentation
- **No replication:** Each server is independent; clients handle distribution
- **No persistence:** Pure cache; data loss on restart is expected

**Client-side sharding:** Consistent hashing distributes keys across servers. Clients (not servers) determine which server holds each key. Adding/removing servers causes cache misses but no data movement.

| Specification | Limit |
|--------------|-------|
| Key size | 250 characters |
| Value size | 1 MB default |
| Eviction | LRU only (per slab class) |

**When Memcached wins:**
- Simple caching without complex data structures
- Multi-threaded performance on multi-core systems
- Lower memory overhead per key
- Established codebases already using Memcached

**Who uses Memcached:** Facebook (TAO, the social graph cache), YouTube, Wikipedia, Reddit—all validating Memcached at massive scale.

### Hazelcast: Distributed computing meets caching

Hazelcast extends beyond caching into in-memory data grid (IMDG) territory with distributed computing capabilities.

**Architecture:**
- **Peer-to-peer network:** No master node; symmetric architecture
- **Embedded or client-server:** Deploy within application JVM or as separate cluster
- **271 partitions** distributed across cluster with configurable backup count
- **JCache (JSR-107)** standard compliance

**Distributed data structures:** Map, Set, List, Queue, MultiMap, Topic (pub/sub), RingBuffer, Lock, Semaphore, AtomicLong—all distributed transparently across cluster.

**Near cache:** Client-side caching of frequently accessed entries reduces network round trips while Hazelcast manages invalidation.

**Jet engine:** Stream processing and batch processing built into Hazelcast platform.

**Use cases:** Session clustering across application servers, distributed caching for Java applications, real-time stream processing, in-memory computing.

### Apache Ignite: When cache meets database

Ignite blurs the line between cache and database with **ACID transactions**, **SQL support**, and **native persistence**.

**Durable Memory architecture:**
- Page-based memory management (similar to OS virtual memory)
- Off-heap storage in RAM
- Automatic paging to disk when memory exceeded
- Native persistence with WAL (Write-Ahead Logging)

**SQL capabilities:** ANSI-99 compliant SQL with JOINs, JDBC/ODBC drivers, making Ignite usable as a distributed SQL database, not just cache.

**Compute grid:** Execute arbitrary code close to data, enabling distributed computing patterns beyond caching.

**When Ignite fits:**
- ACID transactions required across distributed cache
- SQL access to cached data
- Hybrid transactional/analytical (HTAP) workloads
- Data exceeds RAM but needs cache-like performance

### CDN caching: Edge delivery comparison

| Provider | PoPs | Edge Compute | Best For |
|----------|------|--------------|----------|
| CloudFront | 400+ | Lambda@Edge, CloudFront Functions | AWS-native |
| Cloudflare | 330+ | Cloudflare Workers | Multi-cloud, DDoS |
| Azure CDN | 116+ | Limited | Azure-native |

**Cache hierarchy:** Request → Edge PoP → Regional Edge Cache → Origin. Tiered caching reduces origin load.

**When CDN vs application cache:**
- **CDN:** Static assets, geographically distributed users, public content
- **Application cache:** Dynamic data, user-specific content, complex invalidation

## CAP theorem positioning

| System | CAP Position | Consistency Model |
|--------|-------------|-------------------|
| **Redis (standalone)** | CP | Strong for single-key operations |
| **Redis (cluster)** | CP (configurable) | Eventual due to async replication |
| **Memcached** | AP | No consistency (independent servers) |
| **Hazelcast** | AP (configurable) | CP subsystem available for strong consistency |
| **Ignite** | CP | Strong with ACID transactions |

**Redis cluster consistency nuance:** During failover, writes acknowledged by failed primary but not yet replicated may be lost. `WAIT` command can enforce synchronous replication for critical writes at latency cost.

## Caching patterns

Understanding caching patterns—and when each applies—is essential interview material.

### Cache-aside (lazy loading)

**Flow:**
1. Application checks cache
2. On miss, reads from database
3. Writes result to cache
4. Returns data

**Characteristics:**
- Only caches data that's actually requested
- First request always hits database (cold start)
- Potential for stale data if database updated without cache invalidation
- Application owns caching logic

**Best for:** General-purpose caching, read-heavy workloads, when missing data is acceptable temporarily.

### Write-through

**Flow:**
1. Application writes to cache
2. Cache synchronously writes to database
3. Returns after both complete

**Characteristics:**
- Strong consistency between cache and database
- Higher write latency (both writes in path)
- Cache pollution (writes may never be read)

**Best for:** Consistency-critical applications, when read-after-write consistency required.

### Write-behind (write-back)

**Flow:**
1. Application writes to cache
2. Cache acknowledges immediately
3. Cache asynchronously writes to database (batched)

**Characteristics:**
- Very fast writes
- Reduced database load through batching
- Data loss risk if cache fails before database write
- Complex failure handling

**Best for:** Write-heavy workloads where eventual consistency acceptable.

### Read-through

**Flow:**
1. Application requests data from cache
2. Cache fetches from database on miss (not application)
3. Cache stores and returns data

**Characteristics:**
- Simplified application code
- Cache provider dependency
- Used by specialized caching solutions and CDNs

### Refresh-ahead

**Flow:**
1. Track access patterns
2. Proactively refresh cache entries before expiration
3. Users always hit cache with fresh data

**Characteristics:**
- Eliminates cache miss latency for predicted data
- Complexity in predicting access patterns
- Wasted refreshes for unpredicted data

**Best for:** Predictable access patterns, latency-critical applications.

## Implementation strategies

### Semantic key design

Well-designed keys improve debuggability and enable efficient operations:

**Naming conventions:**
- Structure: `{entity}:{id}:{field}` → `user:12345:profile`
- Include version for schema changes: `v2:user:12345:profile`
- Use prefixes for namespacing: `session:abc123`, `cache:product:456`

**Hash tags for cluster slot locality:**
In Redis Cluster, `{user:12345}:profile` and `{user:12345}:settings` hash to same slot (curly braces define hash key portion), enabling multi-key operations.

**Avoid in keys:**
- Sensitive data (keys appear in logs)
- Unpredictable data (defeats pattern-based operations)
- Excessive length (memory overhead)

### Serialization strategies

| Format | Pros | Cons |
|--------|------|------|
| JSON | Human-readable, widely supported | Larger size, slower parsing |
| Protocol Buffers | Compact, fast, schema evolution | Requires schema definition |
| MessagePack | Compact, faster than JSON | Less human-readable |
| Native types | No serialization overhead | Limited to primitive types |

**Recommendation:** Use native Redis types when possible; otherwise Protocol Buffers or MessagePack for performance-critical paths.

### Connection pooling

- Maintain persistent connections (TCP handshake is expensive)
- Size pool based on concurrent request patterns
- Configure connection timeout and health checks
- Monitor pool exhaustion as capacity signal

**Common mistake:** Creating connections per request—dramatically impacts latency and can exhaust server connections.

### Distributed locking with Redis

**SETNX pattern:**
1. `SET lock:resource value NX PX 30000` (set if not exists, 30s expiry)
2. If acquired, perform work
3. Release with Lua script that checks value before deleting

**Redlock algorithm:** Acquire locks on majority of independent Redis instances for stronger guarantees. Controversial—Martin Kleppmann's analysis suggests potential failures; suitable for efficiency (preventing duplicate work) but not correctness (preventing data corruption).

### Pipeline and batch operations

Reduce round trips dramatically:
- **Pipeline:** Send multiple commands without waiting for responses
- **MGET/MSET:** Batch get/set operations
- **Lua scripts:** Atomic multi-step operations server-side

Pipelining 100 commands: ~100 round trips → 1 round trip. Massive latency reduction.

## Consistency patterns

### Cache stampede prevention

When cached data expires, many concurrent requests hit the database simultaneously.

**Solutions:**

| Technique | Mechanism |
|-----------|-----------|
| **Locking** | First request acquires lock, others wait |
| **Probabilistic early expiration** | Requests probabilistically refresh before expiry |
| **External refresh** | Background process refreshes, requests never hit DB |

**Probabilistic early expiration formula:** Refresh probability increases as TTL approaches, spreading refreshes over time.

### Thundering herd mitigation

Similar to stampede, but triggered by cache failure or restart.

**Strategies:**
- **Request coalescing:** Deduplicate concurrent requests for same key
- **Staggered TTLs:** Add randomness to TTL to prevent synchronized expiration
- **Circuit breaker:** Limit concurrent backend requests

### Stale-while-revalidate

Serve stale data immediately while refreshing in background:
1. Request arrives for expired entry
2. Return stale data immediately
3. Trigger async refresh
4. Subsequent requests get fresh data

**Trade-off:** Users see slightly stale data but never experience cache miss latency.

### Cache invalidation strategies

**"There are only two hard things in Computer Science: cache invalidation and naming things."**

| Strategy | When to Use |
|----------|-------------|
| **TTL-based** | When staleness acceptable; simplest approach |
| **Event-driven** | When consistency critical; database change triggers invalidation |
| **Version-based** | When multiple cache layers exist; increment version on change |
| **Pattern-based** | When invalidating groups; use key patterns |

**Event-driven invalidation:** Use CDC (Change Data Capture) or outbox pattern to publish database changes, triggering cache invalidation. Uber's CacheFront uses this approach at 150M reads/second.

## Scaling strategies

### Horizontal scaling

**Redis Cluster:** Add shards, data redistributes across hash slots. Online resharding supported but impacts performance during migration.

**Memcached:** Add servers, update client configuration. No automatic rebalancing—new server starts empty, gradually warms through misses.

**Hazelcast/Ignite:** Add nodes, automatic rebalancing of partitions.

### Read scaling with replicas

- Add read replicas to offload read traffic from primary
- Configure read-from-replica in client (stale read risk)
- Replicas provide HA during primary failure

### Hot key handling

Popular keys (celebrities, viral content) overwhelm single shard:

**Solutions:**
- **Key sharding:** Split `hotkey` into `hotkey:1`, `hotkey:2`, etc.; aggregate reads
- **Local caching:** Application-level cache for hot keys
- **Read replicas:** Distribute reads (if eventual consistency acceptable)
- **Rate limiting:** Protect backend from excessive load

### Multi-region caching

| Approach | Consistency | Complexity |
|----------|-------------|------------|
| **Active-Passive** | Strong (single writer) | Lower |
| **Active-Active** | Eventual (conflict resolution) | Higher |
| **Read replicas per region** | Eventual | Medium |

**Redis Enterprise CRDT:** Conflict-free replicated data types enable active-active with automatic conflict resolution. Available in Azure Managed Redis and Redis Enterprise.

## Eviction policies

Understanding eviction is crucial for capacity planning:

| Policy | Behavior | Use Case |
|--------|----------|----------|
| **noeviction** | Return errors when full | When data loss unacceptable |
| **allkeys-lru** | Evict least recently used | General caching |
| **allkeys-lfu** | Evict least frequently used | Frequency matters more than recency |
| **volatile-lru** | LRU among keys with TTL | Mixed persistent/cached data |
| **volatile-ttl** | Evict closest to expiration | When TTL correlates with importance |
| **allkeys-random** | Random eviction | When access patterns unpredictable |

**LFU (Redis 4.0+):** Tracks access frequency, not just recency. Better for workloads where some keys are consistently popular.

## Operational best practices

### Key metrics to monitor

| Metric | Target/Alert |
|--------|--------------|
| **Hit rate** | >95% indicates effective caching |
| **Memory usage** | Alert before hitting maxmemory |
| **Evictions** | Non-zero indicates memory pressure |
| **Latency (P99)** | Should be sub-millisecond |
| **Connections** | Monitor vs max connections |
| **Replication lag** | Alert on sustained lag |

### Security considerations

- **Encryption in transit:** TLS (default in managed services)
- **Encryption at rest:** Available in managed services
- **Authentication:** Redis AUTH, ACLs (Redis 6+)
- **Network isolation:** VPC, private endpoints
- **No sensitive data in keys:** Keys appear in logs, metrics

### Cache warming strategies

Cold caches cause latency spikes after deployment or failure:

- **Preload from database:** Batch load predicted hot data on startup
- **Shadow traffic:** Route read traffic to new cache before cutover
- **ML-based prediction:** Netflix predicts popular content before launches
- **Gradual traffic shift:** Slowly migrate traffic, allowing natural warming

## Decision framework

### Redis vs Memcached

| Choose Redis | Choose Memcached |
|-------------|------------------|
| Need data structures beyond strings | Simple key-value sufficient |
| Persistence required | Transient cache acceptable |
| Replication/HA needed | Can tolerate single point of failure |
| Pub/sub, Lua scripting needed | Maximum simplicity |
| Single-threaded acceptable | Multi-threaded performance critical |

### Distributed vs local cache

| Distributed | Local |
|------------|-------|
| Data exceeds single node | Fits in single node memory |
| Multiple application instances | Single instance or acceptable inconsistency |
| Need durability | Pure performance cache |
| Shared state across services | Service-local state |

### When NOT to use caching

- **Write-heavy workloads:** Cache provides limited benefit
- **Highly dynamic data:** Invalidation overhead exceeds benefit
- **Large objects:** Better served from object storage
- **Security-critical data:** Additional attack surface
- **When consistency is paramount:** Cache introduces staleness

### Antipatterns to avoid

- **Caching everything:** Caches have finite capacity; prioritize hot data
- **No expiration:** Data grows unbounded; set appropriate TTLs
- **Ignoring cache failures:** Implement fallbacks, circuit breakers
- **Cache as primary store:** Without persistence, cache loss means data loss
- **Synchronous invalidation in write path:** Adds latency; consider async
- **Large values:** Impacts eviction, replication; use claim-check pattern

## Real-world case studies

### Netflix EVCache and Redis

Netflix's **EVCache** (extended volatile cache) builds on Memcached for massive scale: **400M+ operations/second**. Multi-tiered architecture: L1 (in-process), L2 (EVCache), L3 (database).

**Timestone** uses Redis for priority queue system, demonstrating Redis's versatility beyond caching.

ML-based cache warming predicts popular content before releases, ensuring cache hits from first requests.

### Uber CacheFront

Uber's **CacheFront** integrates Redis caching with Docstore (MySQL), achieving:
- **150M reads/second**
- **>99.9% cache hit rate**
- CDC-based invalidation via Flux (change data capture)
- Cross-region cache replication

Architecture demonstrates event-driven invalidation at scale: database changes flow through CDC, trigger cache invalidation, maintaining consistency without TTL-based staleness.

### Twitter trending topics

Twitter caches trending topics with:
- Hot key replication across multiple nodes
- Write-through strategy for consistency
- Consistent hashing for load distribution

The viral nature of trending topics exemplifies hot key challenges at extreme scale.