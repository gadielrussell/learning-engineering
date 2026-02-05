# Distributed Messaging Systems: A Deep Dive for System Design Interviews

Messaging systems form the backbone of modern distributed architectures, enabling asynchronous communication, event-driven patterns, and real-time data streaming at massive scale. **Apache Kafka dominates the enterprise landscape**, processing trillions of messages daily at companies like LinkedIn, Netflix, and Uber, but cloud-native alternatives from AWS, Azure, and GCP offer compelling managed experiences with different architectural trade-offs.

This guide covers the five most prevalent messaging technologies: Apache Kafka, Apache Pulsar, Amazon Kinesis, Azure Event Hubs, and Google Cloud Pub/Sub. Understanding their architectures, limitations, and appropriate use cases will prepare you for system design discussions around event streaming, real-time analytics, and distributed data pipelines.

## Technology deep dive

### Apache Kafka: The industry standard for high-throughput streaming

Kafka pioneered the log-based messaging paradigm and remains the most widely deployed streaming platform. Its architecture centers on **brokers** (servers handling reads/writes), **topics** (logical channels), and **partitions** (the unit of parallelism and ordering). Messages within a partition receive sequential offsets, enabling replay and exactly-once processing.

**Architecture fundamentals:**
- Single-leader replication with configurable In-Sync Replicas (ISR)
- ZooKeeper dependency being replaced by KRaft mode (controller quorum)
- Segment-based storage with configurable retention by time or size
- Consumer groups enable parallel processing with automatic partition assignment

**Strengths that drive adoption:** Kafka delivers **millions of messages per second** with sub-10ms latency. LinkedIn processes over 7 trillion messages daily across 100+ clusters. The ecosystem spans Kafka Connect (data integration), Kafka Streams (stream processing), and ksqlDB (SQL-based streaming). Enterprise support through Confluent adds schema registry, governance, and multi-region capabilities.

**Critical limitations to understand:** Partition count decisions are difficult to change post-creation—a common interview discussion point. Rebalancing when scaling consumers causes temporary processing pauses. Operational complexity requires dedicated expertise; self-managed Kafka clusters demand significant investment in monitoring, capacity planning, and failure handling.

| Specification | Limit |
|--------------|-------|
| Message size | 1 MB default (configurable to ~10 MB) |
| Partitions per cluster | ~200,000 recommended maximum |
| Write throughput | ~1 MB/sec per partition leader |
| Retention | Configurable; unlimited with tiered storage |

**Cloud-managed variants:** Amazon MSK, Confluent Cloud, and Azure Event Hubs (Kafka protocol compatible) eliminate operational burden but introduce vendor considerations. MSK maintains Kafka API compatibility while adding AWS integrations. Confluent Cloud provides the richest Kafka ecosystem but at premium pricing.

### Apache Pulsar: Separation of compute and storage

Pulsar's distinctive architecture separates **stateless brokers** from **Apache BookKeeper** storage (bookies), enabling independent scaling of compute and storage layers. This design eliminates Kafka's partition rebalancing pain—a significant operational advantage.

**Architecture differentiators:**
- BookKeeper provides storage with configurable Ensemble, Write Quorum, and Ack Quorum
- Segment-oriented architecture allows unlimited partitions per topic
- Native multi-tenancy with namespace isolation
- Built-in geo-replication without external tools

**When Pulsar excels:** Organizations needing **massive topic counts** (up to 1 million per cluster) or requiring multi-tenant isolation find Pulsar compelling. The unified messaging model supports both streaming and traditional queue semantics. Tiered storage automatically offloads cold data to object storage.

**Trade-offs to consider:** The three-component architecture (broker, BookKeeper, ZooKeeper) increases deployment complexity. Smaller community and ecosystem compared to Kafka means fewer integrations and harder hiring. Companies like Yahoo!, Tencent, and Splunk have validated Pulsar at scale, but Kafka's market dominance persists.

### Amazon Kinesis: Serverless streaming for AWS-native architectures

Kinesis provides fully managed streaming without infrastructure provisioning. **Streams** contain **shards**—the unit of capacity and parallelism. Two modes exist: Provisioned (manual shard management) and On-Demand (automatic scaling).

**Architectural characteristics:**
- Partition key hashing determines shard assignment
- Multi-AZ replication by default
- Enhanced fan-out provides dedicated 2 MB/sec throughput per consumer
- Deep integration with Lambda, Firehose, and Analytics services

**Capacity planning considerations:** Each shard supports **1 MB/sec or 1,000 records/sec for writes** and **2 MB/sec for reads**. On-Demand mode scales to 200 MB/sec write throughput. The 20,000 shard limit per account (US regions) accommodates most workloads.

**AWS lock-in implications:** Kinesis offers the lowest operational overhead for AWS-native applications but creates significant portability constraints. Pricing can exceed self-managed Kafka at very high scale, though operational savings often offset this.

### Azure Event Hubs: Kafka compatibility meets Azure integration

Event Hubs provides managed event streaming with **native Kafka protocol support** (1.0+), enabling lift-and-shift migrations. The architecture uses **namespaces** containing **event hubs** (topics) with **partitions** and **consumer groups**.

**Tiered capacity model:**

| Tier | Capacity Unit | Key Features |
|------|---------------|--------------|
| Standard | Throughput Units (TUs) | 1-20 TUs, auto-inflate available |
| Premium | Processing Units (PUs) | Dynamic partitions, JMS 2.0 |
| Dedicated | Capacity Units (CUs) | Single-tenant, highest throughput |

**Event Hubs Capture** automatically archives events to Blob Storage or Data Lake—a differentiating feature for analytics pipelines. Premium tier supports **up to 100 partitions** and allows partition count changes, addressing a Kafka limitation.

**Migration considerations:** Existing Kafka applications can connect via Kafka protocol endpoints with minimal code changes. However, some Kafka features (compacted topics, exactly-once semantics) have limited support.

### Google Cloud Pub/Sub: True serverless messaging

Pub/Sub eliminates partition management entirely—a genuinely **serverless** approach. Topics and subscriptions (push or pull) form the core model, with messages containing up to **10 MB** of data and attributes.

**Unique architectural properties:**
- Global by default with automatic cross-region replication
- No throughput caps on topics
- Ordering keys provide FIFO guarantees within a key
- Exactly-once delivery supported for pull subscriptions (single region)

**Serverless trade-offs:** The lack of partitions simplifies operations but removes fine-grained control over parallelism and ordering. Best-effort ordering without ordering keys may not suit all use cases. Spotify famously migrated from Kafka to Pub/Sub, validating its scalability for demanding workloads.

## CAP theorem positioning

Understanding how each technology balances consistency, availability, and partition tolerance reveals fundamental design philosophies:

| System | CAP Position | Key Behavior |
|--------|-------------|--------------|
| **Kafka** | CP (configurable) | Consistency prioritized; `unclean.leader.election.enable=false` prevents data loss |
| **Pulsar** | CP | BookKeeper quorum ensures strong consistency |
| **Kinesis** | AP | Eventual consistency; prioritizes availability across AZs |
| **Event Hubs** | CP | Strong consistency within partitions |
| **Pub/Sub** | AP | High availability globally; at-least-once delivery |

Kafka's configurability deserves special attention: `acks=all` with `min.insync.replicas=2` provides strong durability, while `acks=1` trades durability for latency. This tuning often appears in interview discussions.

## Implementation strategies

### Semantic partition key design

Partition keys determine message distribution and ordering scope. Poor key selection causes **hot partitions**—a critical performance antipattern.

**Effective key patterns:**
- **Entity-based:** User ID, order ID, or device ID ensures related events co-locate
- **High cardinality:** Keys should distribute evenly across partitions
- **Avoid temporal keys:** Timestamps create sequential writes to single partitions

**Hash tag patterns in Kafka:** Using consistent hash algorithms, keys like `order-{orderId}` ensure related events (order created, updated, fulfilled) maintain ordering.

### Consumer idempotency patterns

At-least-once delivery (the common default) requires consumers to handle duplicate messages gracefully:

- **Idempotency keys in storage:** Track processed message IDs in a database or cache
- **Versioned updates:** Only apply changes if the version is newer than current state
- **Deduplication windows:** Cache recent message IDs with TTL matching maximum retry period
- **Inbox pattern:** Record message IDs transactionally alongside business logic
- **Natural idempotency:** Design operations that produce identical results regardless of execution count

### Dead letter queue handling

Failed messages require careful routing to prevent infinite retry loops:

- Configure maximum delivery attempts (Kafka: via consumer logic; Kinesis: Lambda destination; Event Hubs: custom implementation)
- Include original topic, partition, offset, and failure reason in DLQ messages
- Monitor DLQ depth as a critical operational metric
- Implement replay tooling for reprocessing after fixes

### Exactly-once vs at-least-once semantics

**At-least-once** (commit after processing) is the practical default for most systems. Duplicates are handled at the consumer level through idempotency.

**Exactly-once** requires coordination between producer, broker, and consumer:
- Kafka: Idempotent producers (`enable.idempotence=true`) + transactions + Kafka Streams
- Pub/Sub: Supported for pull subscriptions within single region
- Others: Requires application-level implementation

The performance overhead of exactly-once processing is significant. Interview discussions often explore when this guarantee actually matters versus when at-least-once with idempotent consumers suffices.

### Connection pooling and producer configuration

- Reuse producer and consumer instances (thread-safe in most clients)
- Configure `batch.size` and `linger.ms` to balance latency and throughput
- Monitor connection metrics to detect pool exhaustion
- Use async sends with callbacks rather than synchronous blocking

## Architecture design patterns

### Event sourcing with message brokers

Store state changes as immutable events in a topic, treating the event log as the source of truth. Current state is derived by replaying events.

**Implementation considerations:**
- Topics should use log compaction for efficient storage of latest state per key
- Snapshots reduce replay time for entities with long histories
- Event schemas require careful versioning (Avro with schema registry)
- Natural fit with Kafka and Pulsar; less common with Kinesis or Pub/Sub

### CQRS (Command Query Responsibility Segregation)

Separate write (command) and read (query) models, using events to synchronize:

- Command model handles business transactions with full validation
- Query model is a materialized view optimized for read patterns
- Event-driven updates flow from command to query model
- Enables independent scaling and optimization of each model

### Saga pattern for distributed transactions

Coordinate multi-service transactions without distributed locks:

**Choreography approach:** Services publish events; other services react. No central coordinator but harder to track overall progress.

**Orchestration approach:** A saga orchestrator directs steps via messages, receiving results and determining next actions or compensations.

Both approaches require **compensating transactions** to undo partial progress on failure. Idempotent saga steps are critical—processing a step twice should not corrupt state.

### Stream processing patterns

Modern messaging platforms enable real-time transformations:

- **Windowing:** Tumbling (fixed, non-overlapping), hopping (fixed, overlapping), sliding (event-triggered), and session (activity-based) windows
- **Stream-stream joins:** Correlate events from different topics within time windows
- **Stream-table joins:** Enrich streaming data with reference data
- **Aggregations:** Count, sum, average over windows with configurable triggers

Kafka Streams, Apache Flink, and cloud services (Kinesis Analytics, Stream Analytics) implement these patterns with different trade-offs.

### Fan-out and fan-in patterns

**Fan-out:** Single producer publishes to topic; multiple consumer groups each receive all messages. Common for notifications, audit logging, and multi-system synchronization.

**Fan-in:** Multiple producers publish to single topic; single consumer aggregates. Used for log aggregation, metrics collection, and unified event processing.

## Scaling strategies

### Horizontal scaling through partitioning

Partitions are the fundamental unit of parallelism. Maximum consumer parallelism equals partition count.

**Scaling decisions:**
- Over-provision partitions initially (changing later is costly in Kafka)
- Monitor partition size to ensure even distribution
- Consider separate topics for different data types rather than mega-topics
- Kinesis and Event Hubs allow online partition/shard modifications (with limitations)

### Replication strategies

**Synchronous replication:** Producer waits for acknowledgment from replicas. Higher durability, higher latency. Kafka's `acks=all` implements this.

**Asynchronous replication:** Producer receives acknowledgment before replication completes. Lower latency, risk of data loss on leader failure.

**Cross-region replication:** Kafka MirrorMaker 2, Pulsar native geo-replication, Kinesis cross-region, Event Hubs Geo-DR provide disaster recovery capabilities with varying RPO/RTO characteristics.

### Consumer group scaling

Adding consumers to a group automatically redistributes partitions. Key considerations:

- Maximum consumers equals partition count (excess consumers are idle)
- Rebalancing causes temporary processing pauses
- Cooperative rebalancing (Kafka 2.4+) reduces rebalance impact
- Consumer lag monitoring drives scaling decisions

### High availability configurations

Production deployments require:

- **Minimum 3 brokers/nodes** across availability zones
- **Replication factor ≥ 3** for critical topics
- `min.insync.replicas = 2` ensures quorum writes
- Monitoring for under-replicated partitions and ISR shrink events
- Automated failover testing

## Operational best practices

### Critical monitoring metrics

| Metric | Significance | Alert Threshold |
|--------|--------------|-----------------|
| Under-replicated partitions | Data loss risk | Any > 0 |
| Offline partitions | Unavailable data | Any > 0 |
| Consumer lag | Processing delay | Trend-based |
| Request latency (P99) | Client experience | > SLA target |
| ISR shrink rate | Replication health | Sustained increase |
| Active controller count | Cluster health | ≠ 1 |

Consumer lag deserves special attention. **Offset lag** (messages behind) is simple but misleading with variable message rates. **Time lag** (seconds behind real-time) better reflects actual delay.

### Security considerations

- **Encryption in transit:** TLS for all client-broker and inter-broker communication
- **Encryption at rest:** Managed services provide this; self-managed requires disk encryption
- **Authentication:** SASL/SCRAM, mTLS, or OAuth depending on platform
- **Authorization:** Topic-level ACLs controlling produce/consume permissions
- **Network isolation:** VPC, private endpoints, firewall rules

### Cost optimization

- Right-size partition/shard counts for actual throughput
- Enable compression (snappy, lz4, or zstd)
- Use tiered storage for long retention requirements
- Monitor and alert on over-provisioned capacity
- Reserved capacity for predictable workloads; on-demand for variable

## Decision framework

### When to choose each technology

| Requirement | Recommended Choice |
|-------------|-------------------|
| Maximum throughput, stream processing | Apache Kafka |
| Separation of compute/storage, multi-tenancy | Apache Pulsar |
| AWS-native, minimal operations | Amazon Kinesis |
| Azure integration, Kafka compatibility | Azure Event Hubs |
| True serverless, global distribution | Google Cloud Pub/Sub |

### When NOT to use streaming platforms

- **Simple request-reply:** Use synchronous APIs or queues
- **Low volume, no replay needed:** Traditional message queues simpler
- **Strict transactional requirements:** Consider databases with outbox pattern
- **Budget constraints at low scale:** Managed queues (SQS) often cheaper

### Streaming vs traditional messaging

| Choose Streaming When | Choose Queues When |
|----------------------|-------------------|
| Event replay required | Messages consumed once |
| Multiple consumers need same data | Point-to-point delivery |
| Long retention needed | Immediate processing |
| Time-series or log data | Task distribution |
| High throughput priority | Routing flexibility needed |

### Common antipatterns to avoid

- **Unbounded consumer lag:** Indicates insufficient consumer capacity or processing issues
- **Single-partition topics:** Eliminates parallelism benefits
- **Synchronous publishing in request path:** Creates latency and availability coupling
- **Ignoring backpressure:** Leads to producer memory exhaustion
- **Timestamp-based partition keys:** Creates hot partitions
- **Oversized messages:** Should stay well under limits; use claim-check pattern for large payloads