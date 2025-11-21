# data-processing-pipeline - AI Agent Context

**Generated**: 2024-11-19 14:30:00  
**Primary Language**: .py (Python)  
**Repository Type**: Data Processing Service

---

## Repository Overview

This is a Python-based data processing pipeline that handles ETL operations for our analytics platform. The architecture follows a modular design with clear separation between data ingestion, transformation, and loading phases. The system processes approximately 10GB of data daily from multiple sources including REST APIs, S3 buckets, and database exports.

**Key Characteristics:**
- Event-driven architecture using message queues
- Containerized deployment (Docker/Kubernetes)
- Heavily tested (85% coverage)
- Active maintenance with daily commits

---

## Tech Stack

### Core Technologies
- Python 3.9+
- Apache Airflow (workflow orchestration)
- PostgreSQL (metadata store)
- Redis (caching layer)
- AWS S3 (data lake)
- Docker/Kubernetes (deployment)

### Key Libraries
- pandas (data manipulation)
- SQLAlchemy (database ORM)
- boto3 (AWS SDK)
- pytest (testing)
- celery (distributed task queue)
- pydantic (data validation)

---

## Key Components

### 1. **data_ingestion/** (Importance: 47 connections)
Handles data collection from various sources. Implements retry logic and error handling.

**Entry Points:**
- `ingestion/api_collector.py` - REST API data collection
- `ingestion/s3_reader.py` - S3 bucket data reading
- `ingestion/db_exporter.py` - Database export handling

**Patterns Used:**
- Factory pattern for source-specific collectors
- Circuit breaker for external API calls
- Batch processing for efficiency

### 2. **data_transformation/** (Importance: 52 connections)
Core transformation logic including cleaning, normalization, and enrichment.

**Entry Points:**
- `transformation/cleaner.py` - Data cleaning and validation
- `transformation/normalizer.py` - Schema normalization
- `transformation/enricher.py` - Data enrichment with external sources

**Patterns Used:**
- Pipeline pattern for transformation stages
- Strategy pattern for different data types
- Decorator pattern for logging/monitoring

### 3. **data_loading/** (Importance: 38 connections)
Loads processed data into target systems (data warehouse, analytics DB).

**Entry Points:**
- `loading/warehouse_loader.py` - Data warehouse loading
- `loading/batch_writer.py` - Batch write operations
- `loading/index_builder.py` - Search index building

**Patterns Used:**
- Bulk operations for performance
- Transaction management
- Idempotent operations for reliability

### 4. **orchestration/** (Importance: 41 connections)
Airflow DAGs and workflow coordination.

**Entry Points:**
- `orchestration/dags/daily_pipeline.py` - Main daily pipeline
- `orchestration/dags/hourly_updates.py` - Hourly incremental updates
- `orchestration/operators/` - Custom operators

### 5. **utils/** (Importance: 63 connections)
Shared utilities and helper functions used across the project.

**Key Modules:**
- `utils/logging.py` - Centralized logging
- `utils/config.py` - Configuration management
- `utils/validators.py` - Data validation
- `utils/metrics.py` - Metrics and monitoring

---

## Architecture & Patterns

### Code Organization

```
data-processing-pipeline/
├── src/
│   ├── ingestion/          # Data collection
│   ├── transformation/     # Data processing
│   ├── loading/            # Data persistence
│   ├── orchestration/      # Workflow DAGs
│   └── utils/              # Shared utilities
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test data
├── config/
│   ├── dev.yaml            # Dev configuration
│   ├── staging.yaml        # Staging configuration
│   └── prod.yaml           # Production configuration
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── docs/
    ├── architecture.md
    └── deployment.md
```

### Common Patterns

#### 1. Pipeline Pattern
All data flows through standardized pipeline stages:
```python
# Pattern used in transformation/
data -> validate() -> clean() -> transform() -> enrich() -> output
```

#### 2. Configuration-Driven Design
All pipeline behavior is configurable via YAML:
```python
# Pattern used throughout
config = load_config(environment)
pipeline = Pipeline.from_config(config)
```

#### 3. Retry with Exponential Backoff
External operations use consistent retry logic:
```python
# Pattern in ingestion/
@retry(max_attempts=3, backoff=exponential)
def fetch_data(source):
    ...
```

#### 4. Structured Logging
All components use structured logging:
```python
# Pattern throughout codebase
logger.info("processing_started", 
           source=source, 
           record_count=count,
           correlation_id=id)
```

#### 5. Pydantic Models for Validation
All data structures are validated:
```python
# Pattern in transformation/
class DataRecord(BaseModel):
    id: str
    timestamp: datetime
    value: float
    # ... with automatic validation
```

### Dependencies

#### Internal Dependencies
- `ingestion` → `utils` (logging, config, validators)
- `transformation` → `ingestion` (data models)
- `transformation` → `utils` (all utilities)
- `loading` → `transformation` (transformed data models)
- `orchestration` → all modules (workflow coordination)

#### External Dependencies
- **AWS S3** - Data lake storage
- **PostgreSQL** - Metadata and results storage
- **Redis** - Distributed locking and caching
- **Airflow** - Workflow orchestration
- **Prometheus** - Metrics collection

#### Circular Dependencies
⚠️ **Warning:** Detected potential circular dependency:
- `transformation.enricher` ↔ `ingestion.api_collector`
- **Action Needed:** Refactor to use dependency injection

---

## Testing Strategy

### Test Framework
- **Primary:** pytest with fixtures
- **Coverage:** 85% overall, 95% target for critical paths
- **Tools:** pytest-cov, pytest-mock, pytest-asyncio

### Test Organization
```
tests/
├── unit/                  # Fast, isolated tests (3,247 tests)
├── integration/           # Component integration (421 tests)
├── e2e/                   # End-to-end scenarios (67 tests)
└── performance/           # Load and performance tests (23 tests)
```

### Key Test Patterns
1. **Fixture-based test data** - Consistent, reusable test data
2. **Mocking external services** - S3, APIs, databases mocked in unit tests
3. **Contract testing** - Validate interface contracts between modules
4. **Property-based testing** - Using Hypothesis for edge cases

### Running Tests
```bash
# All tests
pytest

# Unit tests only (fast)
pytest tests/unit

# With coverage
pytest --cov=src --cov-report=html

# Integration tests (requires docker)
docker-compose up -d
pytest tests/integration
```

### Coverage Gaps
- `loading/index_builder.py` - Only 67% covered, needs more edge case tests
- `orchestration/operators/custom_operators.py` - 71% covered
- Error handling paths in `ingestion/api_collector.py` - Needs failure scenario tests

---

## Known Issues & TODOs

### High Priority
- **TODO:** Implement proper circuit breaker for external API calls (ingestion/api_collector.py:145)
- **FIXME:** Memory leak in batch processing for large datasets (transformation/cleaner.py:289)
- **ISSUE:** Occasional deadlock in concurrent loading operations (loading/warehouse_loader.py:201)

### Medium Priority
- **TODO:** Add retry logic to S3 operations (ingestion/s3_reader.py:78)
- **TODO:** Improve error messages for validation failures (utils/validators.py:45)
- **TODO:** Add metrics for pipeline stage durations (orchestration/dags/daily_pipeline.py:92)

### Low Priority / Technical Debt
- **REFACTOR:** Extract common validation logic into base class (multiple files)
- **OPTIMIZE:** Consider using multiprocessing for CPU-intensive transformations
- **DOCS:** Update API documentation for new endpoints (various files)

### Performance Concerns
- Large dataset processing (>50GB) causes memory issues
- S3 read performance degrades with many small files
- Database connection pool sometimes exhausts under load

---

## Agent Guidelines

### Code Quality Improvements

**DO:**
- Follow PEP 8 style guide strictly
- Use type hints for all function signatures
- Write docstrings for public functions (Google style)
- Maintain test coverage above 80%
- Use structured logging with context
- Implement proper error handling with specific exceptions
- Add configuration options rather than hardcoding values

**DON'T:**
- Add dependencies without updating requirements.txt
- Bypass validation layers
- Use global state or singletons unless absolutely necessary
- Commit commented-out code
- Mix sync and async code without proper handling

**Preferred Patterns:**
```python
# Good: Type hints and docstrings
def process_records(records: List[DataRecord], 
                   batch_size: int = 1000) -> ProcessingResult:
    """
    Process records in batches.
    
    Args:
        records: List of data records to process
        batch_size: Number of records per batch
        
    Returns:
        ProcessingResult with success count and errors
    """
    ...

# Good: Structured logging
logger.info("batch_processing_complete",
           batch_id=batch_id,
           records_processed=count,
           duration_ms=duration)

# Bad: Untyped, no docs, print debugging
def process(data):
    print("processing...")
    result = do_stuff(data)
    return result
```

### Feature Development

**Before Adding Features:**
1. Check if similar functionality exists elsewhere
2. Review architecture to ensure proper layer
3. Consider configuration-driven approach first
4. Plan for testability from the start
5. Update documentation and configuration templates

**Integration Points to Consider:**
- `orchestration/` - Will this be a new DAG or part of existing?
- `utils/` - Should this be a shared utility?
- Configuration files - What new config is needed?
- Monitoring - What metrics should be tracked?

**Example Feature Addition:**
```python
# New data source? Follow this pattern:

1. Add source config to config/sources.yaml
2. Create collector in ingestion/ following existing pattern
3. Register with factory in ingestion/factory.py
4. Add unit tests in tests/unit/ingestion/
5. Add integration test with mocked source
6. Update DEPENDENCIES.md with any new libraries
7. Add metrics for source health
```

### Bug Fixes

**Investigation Steps:**
1. Check logs for error patterns (use correlation IDs)
2. Review related code in the module
3. Check if issue exists in tests (should fail)
4. Verify in similar codepaths
5. Check for race conditions or timing issues

**Fix Implementation:**
1. Write failing test that reproduces bug
2. Implement minimal fix
3. Verify test passes
4. Check for similar patterns in codebase
5. Add regression test if needed
6. Update docs if behavior changed

**Common Bug Patterns in This Repo:**
- Race conditions in concurrent loading operations
- Memory issues with large batch sizes
- Connection pool exhaustion under load
- Timeout errors with external services

### Testing Requirements

**Required for All Changes:**
- Unit tests for new functions/classes
- Integration test for new components
- Update existing tests if behavior changed
- Maintain coverage above 80%

**Test Data Guidelines:**
- Use fixtures from tests/fixtures/
- Keep test data small and focused
- Use factories for complex object creation
- Mock external services (S3, APIs, DBs)

**Performance Testing:**
- Add performance test for data processing changes
- Benchmark against baseline (see tests/performance/)
- Document any performance implications

---

## Important Files & Entry Points

### Main Entry Points
- `src/main.py` - CLI entry point
- `src/orchestration/dags/daily_pipeline.py` - Main workflow
- `docker/Dockerfile` - Container definition

### Configuration Files
- `config/prod.yaml` - Production configuration (CRITICAL)
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup

### Critical Modules (High Change Risk)
⚠️ **Handle with care - used by many components:**
- `src/utils/config.py` - Configuration management
- `src/utils/logging.py` - Logging setup
- `src/utils/validators.py` - Validation logic
- `src/transformation/base.py` - Base transformation class

### Recently Changed (High Activity)
📊 **Frequently modified - may have ongoing work:**
- `src/ingestion/api_collector.py` (15 commits this month)
- `src/orchestration/dags/daily_pipeline.py` (12 commits this month)
- `src/loading/warehouse_loader.py` (9 commits this month)

---

## Developer Notes

### Getting Started
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Start local environment
docker-compose up -d
python src/main.py --config config/dev.yaml
```

### Common Development Tasks

**Adding a New Data Source:**
1. Create collector in `src/ingestion/`
2. Register in `SourceFactory`
3. Add config schema to `config/sources.yaml`
4. Add tests

**Modifying Transformation Logic:**
1. Update transformer in `src/transformation/`
2. Update corresponding tests
3. Check impact on downstream loading
4. Run integration tests

**Deploying Changes:**
1. All PRs require tests and review
2. Deploy to staging first
3. Monitor metrics for 24 hours
4. Deploy to production if stable

### Performance Considerations
- Batch processing recommended for >1000 records
- Use async operations for I/O bound tasks
- Monitor memory usage with large datasets
- Consider partitioning for datasets >10GB

### Debugging Tips
- Use correlation IDs to trace requests through pipeline
- Check CloudWatch logs for production issues
- Redis keys prefixed with `pipeline:` for cache inspection
- Airflow UI shows DAG execution history

---

## Monitoring & Observability

### Key Metrics
- **Pipeline Success Rate** - Target: >99%
- **Processing Duration** - Target: <2 hours for daily pipeline
- **Error Rate** - Target: <0.1%
- **Memory Usage** - Alert if >80% of container limit

### Dashboards
- Grafana: Main pipeline metrics
- Airflow UI: DAG execution status
- CloudWatch: Infrastructure metrics
- Sentry: Error tracking

### Alerts
- Pipeline failure (PagerDuty)
- High error rate (Slack)
- Memory threshold exceeded (Email)
- Data quality issues (Slack)

---

## Security & Compliance

### Sensitive Data Handling
- PII data is encrypted at rest and in transit
- Access to production data requires VPN + 2FA
- Data retention policy: 90 days in hot storage

### Secrets Management
- AWS Secrets Manager for database credentials
- Environment variables for non-sensitive config
- Never commit secrets to git

### Audit Requirements
- All data access is logged
- Logs retained for 1 year
- Regular security scans via Snyk

---

## Change History

### Recent Major Changes
- **v2.3.0** (2024-11-01) - Added real-time streaming capability
- **v2.2.0** (2024-10-15) - Improved error handling and retry logic
- **v2.1.0** (2024-09-20) - Migrated to Kubernetes deployment

### Upcoming Changes
- **Q4 2024** - Add support for additional data sources
- **Q1 2025** - Implement ML-based data quality checks
- **Q2 2025** - Scale to handle 100GB+ daily volume

---

*This documentation was auto-generated by doc-agent on 2024-11-19. For more detailed information, see supplementary documentation files (ARCHITECTURE.md, API_REFERENCE.md, TESTING_GUIDE.md).*

---

## Quick Reference

**Repository:** `data-processing-pipeline`  
**Primary Contact:** Data Engineering Team  
**Slack Channel:** #data-pipeline  
**Documentation:** [Internal Wiki Link]  
**CI/CD:** GitHub Actions  
**Deployment:** Kubernetes on AWS EKS
