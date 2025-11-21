# Architecture Documentation
## data-processing-service

**Version:** 2.1.0  
**Last Updated:** 2025-11-19  
**Status:** Production

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Decisions](#design-decisions)
7. [Scalability](#scalability)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)

---

## System Overview

### Purpose
The data-processing-service is a microservice responsible for ingesting data from multiple sources (S3, REST APIs, databases), transforming it according to business rules, and loading it into our data warehouse for analytics.

### Key Characteristics
- **Throughput:** ~10GB/day across 50+ data sources
- **Latency:** <5 minutes from source to warehouse (p95)
- **Availability:** 99.9% SLA
- **Scalability:** Horizontally scalable via Kubernetes
- **Event-Driven:** Async processing with Celery task queue

### System Boundaries
- **Upstream Dependencies:** Customer API, S3 Data Lake, Legacy Database
- **Downstream Dependencies:** Data Warehouse (PostgreSQL)
- **Supporting Services:** Redis (cache/queue), Prometheus (metrics), Sentry (errors)

---

## Architecture Diagram

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                       Data Sources                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐         │
│  │Customer  │  │   S3     │  │     Legacy       │         │
│  │   API    │  │Data Lake │  │    Database      │         │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘         │
└───────┼─────────────┼─────────────────┼───────────────────┘
        │             │                 │
        ▼             ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│              data-processing-service                         │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │              API Layer (FastAPI)                 │      │
│  │  ┌──────────────┐  ┌──────────────┐             │      │
│  │  │ Job Endpoints│  │Health Checks │             │      │
│  │  └──────┬───────┘  └──────────────┘             │      │
│  └─────────┼────────────────────────────────────────┘      │
│            │                                                │
│  ┌─────────▼────────────────────────────────────────┐      │
│  │           Service Layer                          │      │
│  │  ┌──────────────┐  ┌────────────────────┐       │      │
│  │  │ Job Service  │  │Notification Service│       │      │
│  │  └──────┬───────┘  └────────────────────┘       │      │
│  └─────────┼──────────────────────────────────────  │      │
│            │                                                │
│  ┌─────────▼────────────────────────────────────────┐      │
│  │         Processing Layer (Celery Tasks)          │      │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────┐  │      │
│  │  │Ingestion │  │Transformation│  │  Loading │  │      │
│  │  │  Tasks   │  │    Tasks     │  │   Tasks  │  │      │
│  │  └────┬─────┘  └──────┬───────┘  └────┬─────┘  │      │
│  └───────┼────────────────┼───────────────┼────────┘      │
│          │                │               │                │
│  ┌───────▼────────────────▼───────────────▼────────┐      │
│  │            Data Layer                            │      │
│  │  ┌──────────────┐  ┌──────────────────────┐    │      │
│  │  │  PostgreSQL  │  │      Redis           │    │      │
│  │  │  (Metadata)  │  │  (Cache + Queue)     │    │      │
│  │  └──────────────┘  └──────────────────────┘    │      │
│  └──────────────────────────────────────────────────┘      │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Warehouse                            │
│                   (PostgreSQL)                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow
```
1. API Request → FastAPI Endpoint
2. Endpoint → Service Layer (validation, business logic)
3. Service → Create Celery Task (async processing)
4. Celery Worker → Ingestion Task (fetch data)
5. Ingestion → Transformation Task (clean, validate)
6. Transformation → Loading Task (bulk insert to warehouse)
7. Loading → Update Job Status (complete/failed)
8. Service → Notification (on completion/failure)
```

---

## Component Details

### 1. API Layer (FastAPI)

**Responsibilities:**
- Expose HTTP endpoints for job management
- Handle authentication and authorization
- Validate incoming requests (Pydantic)
- Return appropriate HTTP responses

**Key Endpoints:**
- `POST /jobs` - Create new processing job
- `GET /jobs/{job_id}` - Get job status
- `DELETE /jobs/{job_id}` - Cancel job
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

**Technologies:**
- FastAPI 0.104.1 (async web framework)
- Uvicorn (ASGI server)
- Pydantic 2.5.0 (validation)

**Scaling:** Stateless, horizontally scalable

### 2. Service Layer

**Responsibilities:**
- Implement business logic
- Orchestrate between components
- Manage job lifecycle
- Handle errors and retries

**Key Services:**
- `JobService` - Job CRUD operations, status management
- `NotificationService` - Send alerts on job completion/failure

**Technologies:**
- Pure Python business logic
- Async/await for I/O operations

**Design Pattern:** Service pattern with dependency injection

### 3. Processing Layer (Celery Workers)

**Responsibilities:**
- Execute async data processing tasks
- Handle retries with exponential backoff
- Process data in batches
- Update job progress

**Key Tasks:**
- **Ingestion Tasks** - Fetch data from sources (S3, APIs, DB)
- **Transformation Tasks** - Clean, validate, normalize data
- **Loading Tasks** - Bulk insert into warehouse

**Technologies:**
- Celery 5.3.4 (distributed task queue)
- Redis (message broker)

**Scaling:** 
- Worker pool size: 10 workers per node
- Auto-scale: 2-20 nodes based on queue depth
- Task timeout: 5 minutes default

### 4. Data Layer

#### PostgreSQL (Metadata)
**Purpose:** Store job metadata, configuration, audit logs

**Schema:**
- `jobs` - Job records with status
- `job_runs` - Job execution history
- `data_sources` - Source configuration
- `audit_logs` - Audit trail

**Connection Pool:** 20 connections, max overflow 10

#### Redis
**Purpose:** 
- Cache (10 min TTL for frequently accessed data)
- Celery message broker
- Distributed locks

**Configuration:**
- Memory: 8GB
- Eviction policy: allkeys-lru
- Persistence: AOF (append-only file)

---

## Data Flow

### Typical Job Flow

```
1. User creates job via POST /jobs
   ├─ Validate request (Pydantic)
   ├─ Create job record (PostgreSQL)
   ├─ Enqueue ingestion task (Celery)
   └─ Return job_id to user

2. Ingestion Task executes
   ├─ Fetch data from source (S3/API/DB)
   ├─ Stream data in chunks (memory efficient)
   ├─ Store raw data temporarily (S3)
   ├─ Enqueue transformation task
   └─ Update job status: INGESTING → TRANSFORMING

3. Transformation Task executes
   ├─ Load raw data in batches
   ├─ Clean data (remove duplicates, handle nulls)
   ├─ Validate against schema (Pydantic)
   ├─ Enrich with external data (if configured)
   ├─ Store transformed data (S3)
   ├─ Enqueue loading task
   └─ Update job status: TRANSFORMING → LOADING

4. Loading Task executes
   ├─ Load transformed data in batches
   ├─ Begin database transaction
   ├─ Bulk insert using COPY command
   ├─ Verify row counts match
   ├─ Commit transaction
   ├─ Update job status: LOADING → COMPLETED
   └─ Trigger notification

5. Notification sent
   ├─ Determine notification channel (email, Slack)
   ├─ Format message with job summary
   └─ Send notification
```

### Error Handling Flow

```
If any task fails:
1. Log error with full context
2. Update job status: FAILED
3. Store error message in job record
4. Check retry policy
   ├─ If retryable (network error, timeout)
   │  ├─ Increment retry count
   │  ├─ Wait (exponential backoff)
   │  └─ Re-enqueue task
   └─ If not retryable (validation error)
      ├─ Mark job as FAILED (permanent)
      └─ Send failure notification
```

---

## Technology Stack

### Core Framework
- **Python 3.11+** - Primary language
- **FastAPI 0.104.1** - Web framework
- **Pydantic 2.5.0** - Data validation
- **SQLAlchemy 2.0.23** - ORM
- **Celery 5.3.4** - Task queue

### Data Processing
- **Pandas 2.1.4** - Data manipulation
- **PyArrow 14.0.1** - Parquet support

### Infrastructure
- **PostgreSQL 15** - Metadata + Data Warehouse
- **Redis 7.2** - Cache + Message broker
- **Kubernetes 1.28** - Container orchestration
- **Docker** - Containerization

### AWS Services
- **S3** - Data lake storage
- **EKS** - Managed Kubernetes
- **Secrets Manager** - Secrets storage
- **CloudWatch** - Logs

### Monitoring & Observability
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards
- **Sentry** - Error tracking
- **Structlog** - Structured logging

---

## Design Decisions

### 1. Why FastAPI over Flask?
**Decision:** Use FastAPI

**Rationale:**
- Native async/await support
- Automatic OpenAPI documentation
- Pydantic integration for validation
- Better performance (async I/O)
- Modern Python 3.6+ features

**Trade-offs:**
- Smaller ecosystem than Flask
- Team learning curve (async patterns)
- Worth it for: performance, type safety, documentation

### 2. Why Celery over AWS Lambda?
**Decision:** Use Celery

**Rationale:**
- Long-running tasks (>15 min)
- Better observability and monitoring
- More control over worker configuration
- Lower cost at our scale
- Easier local development

**Trade-offs:**
- More infrastructure to manage
- Need to handle worker scaling
- Worth it for: long tasks, cost, control

### 3. Why PostgreSQL for Data Warehouse?
**Decision:** Use PostgreSQL

**Rationale:**
- Excellent for OLAP workloads
- Strong SQL support
- Good performance with proper indexing
- Team expertise
- Cost-effective

**Trade-offs:**
- Not as scalable as Snowflake/BigQuery
- Requires manual optimization
- Worth it for: cost, control, simplicity

### 4. Why Pydantic V2?
**Decision:** Upgrade to Pydantic V2

**Rationale:**
- 5-10x faster validation
- Better error messages
- Improved type support
- Better JSON schema generation

**Trade-offs:**
- Breaking changes from V1
- Migration effort required
- Worth it for: performance, better DX

### 5. Why Repository Pattern?
**Decision:** Use Repository pattern for data access

**Rationale:**
- Separation of concerns
- Easier testing (mock repositories)
- Database agnostic (can swap PostgreSQL)
- Clear data access layer

**Trade-offs:**
- More boilerplate code
- Extra abstraction layer
- Worth it for: testability, maintainability

---

## Scalability

### Current Capacity
- **API:** 1,000 requests/second
- **Processing:** 10GB/day
- **Jobs:** 500 concurrent jobs
- **Workers:** 20 Celery workers (2 nodes × 10 workers)

### Scaling Strategies

#### Horizontal Scaling
- **API Layer:** Add more FastAPI pods (currently 3)
- **Processing Layer:** Add more Celery workers (scale to 100 workers)
- **Database:** Read replicas for queries, write to primary

#### Vertical Scaling
- **Database:** Increase instance size (currently db.r5.xlarge)
- **Redis:** Increase memory (currently 8GB)

#### Auto-Scaling Configuration
```yaml
API Pods:
  min: 3
  max: 20
  target_cpu: 70%
  target_memory: 80%

Celery Workers:
  min: 2 nodes (10 workers each)
  max: 10 nodes (10 workers each)
  scale_metric: queue_depth
  scale_threshold: 100 tasks
```

### Performance Bottlenecks

**Current Bottlenecks:**
1. **Database Connection Pool** - Limit: 20 connections
   - Solution: Increase pool size or add PgBouncer
   
2. **S3 List Operations** - 100-200ms per call
   - Solution: Cache listings, use S3 inventory

3. **Data Validation** - CPU-intensive for large batches
   - Solution: Use Pydantic V2 (faster), batch validation

**Future Bottlenecks (at 10x scale):**
- Database write throughput
- Network bandwidth (S3 → service)
- Worker compute resources

### Scaling Plan
- **Current:** 10GB/day
- **Q1 2026:** 50GB/day (5x) - Add workers, increase DB size
- **Q2 2026:** 100GB/day (10x) - Add read replicas, optimize queries
- **Q3 2026:** 500GB/day (50x) - Consider sharding, optimize pipeline

---

## Security Architecture

### Authentication & Authorization
- **API Authentication:** JWT tokens (30 min expiry)
- **Service-to-Service:** mTLS certificates
- **Database:** Role-based access control (RBAC)

### Network Security
- **VPC:** Private subnets for services
- **Security Groups:** Least privilege access
- **TLS:** TLS 1.3 for all communication
- **WAF:** AWS WAF for API layer

### Data Security
- **At Rest:** AES-256 encryption (S3, EBS)
- **In Transit:** TLS 1.3
- **PII:** Encrypted in database, masked in logs
- **Secrets:** AWS Secrets Manager

### Audit & Compliance
- **Audit Logs:** All data access logged
- **Retention:** 1 year
- **Compliance:** SOC2 Type II, GDPR

---

## Deployment Architecture

### Kubernetes Deployment

```yaml
Namespace: data-processing

Deployments:
  - api-deployment (3 replicas)
  - celery-worker-deployment (20 replicas)
  
Services:
  - api-service (LoadBalancer)
  - redis-service (ClusterIP)
  
ConfigMaps:
  - app-config
  
Secrets:
  - db-credentials
  - api-keys
  
PersistentVolumeClaims:
  - redis-data (8Gi)
```

### CI/CD Pipeline

```
1. Developer pushes to GitHub
2. GitHub Actions triggers
3. Run tests (pytest)
4. Build Docker image
5. Push to ECR
6. Deploy to staging (auto)
7. Run integration tests
8. Manual approval for production
9. Deploy to production (blue-green)
10. Health check validation
11. Switch traffic
```

### Environments
- **Development:** Local (Docker Compose)
- **Staging:** EKS (staging cluster)
- **Production:** EKS (production cluster)

### Disaster Recovery
- **RTO:** 15 minutes
- **RPO:** 5 minutes
- **Backup:** Daily database snapshots
- **Replication:** Multi-AZ deployment

---

## Future Architecture Evolution

### Planned Improvements

**Q1 2026:**
- [ ] Add gRPC API for high-performance clients
- [ ] Implement caching layer (Redis Cluster)
- [ ] Add read replicas for queries

**Q2 2026:**
- [ ] Migrate to event streaming (Kafka)
- [ ] Implement CQRS pattern
- [ ] Add GraphQL API

**Q3 2026:**
- [ ] Microservices split (ingestion, transformation, loading)
- [ ] Service mesh (Istio)
- [ ] Multi-region deployment

---

## Appendix

### References
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Celery Documentation](https://docs.celeryq.dev)
- [Kubernetes Documentation](https://kubernetes.io/docs)

### Change Log
- **2025-11-19:** Updated architecture with Pydantic V2
- **2025-10-15:** Added Celery worker auto-scaling
- **2025-09-01:** Migrated to Kubernetes from ECS

### Contact
- **Team:** #data-processing-team on Slack
- **On-Call:** See PagerDuty schedule
- **Documentation:** https://wiki.company.com/data-processing
