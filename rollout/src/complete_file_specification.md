# Complete Claude Code Preparation Specification
## All Files and Artifacts Doc-Agent Should Generate

**Purpose:** Eliminate the need for developers to run `/init` or manually configure Claude Code. Everything should be ready from day one.

---

## 📋 File Structure Overview

```
repository/
├── .claude/                           # Claude Code configuration directory
│   ├── commands/                      # Custom commands
│   │   ├── add_feature.md
│   │   ├── fix_bug.md
│   │   ├── add_test.md
│   │   ├── refactor_code.md
│   │   └── update_docs.md
│   ├── context/                       # Additional context files
│   │   ├── architecture.md
│   │   ├── patterns.md
│   │   ├── gotchas.md
│   │   ├── security.md
│   │   └── performance.md
│   ├── examples/                      # Code examples
│   │   ├── good_patterns/
│   │   ├── bad_patterns/
│   │   └── common_tasks/
│   ├── templates/                     # Code templates
│   │   ├── component_template.py
│   │   ├── test_template.py
│   │   ├── api_endpoint_template.py
│   │   └── model_template.py
│   └── workflows/                     # Common workflows
│       ├── feature_development.md
│       ├── bug_fixing.md
│       └── code_review.md
├── CLAUDE.md                          # Primary context file
├── .clinerules                        # Claude Code rules file
├── ARCHITECTURE.md                    # System architecture
├── API_REFERENCE.md                   # API documentation
├── TESTING_GUIDE.md                   # Testing standards
├── DEPENDENCIES.md                    # Dependency documentation
├── CONTRIBUTING.md                    # Contribution guidelines
├── SECURITY.md                        # Security guidelines
└── TROUBLESHOOTING.md                 # Common issues and solutions
```

---

## 🎯 Critical Files (Must Generate)

### 1. CLAUDE.md
**Location:** Repository root  
**Priority:** HIGHEST  
**Purpose:** Primary context file that Claude Code reads first

**Sections to Include:**

```markdown
# [Repository Name] - Claude Code Context

**Last Updated:** [Auto-generated timestamp]
**Primary Language:** [Detected language]
**Framework:** [Detected framework]
**Architecture:** [Detected pattern]

## Quick Start for Claude Code
- Main entry points: [List]
- Key modules: [List]
- Common commands: See .claude/commands/
- Examples: See .claude/examples/

## Repository Overview
### Purpose
[What this codebase does - 2-3 sentences]

### Key Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

### Architecture Summary
[High-level architecture - 3-4 sentences]

## Code Organization
### Directory Structure
```
[Visual tree of key directories with explanations]
```

### Module Responsibilities
- **[Module 1]**: [Purpose and key files]
- **[Module 2]**: [Purpose and key files]
- **[Module 3]**: [Purpose and key files]

### Entry Points
1. **[Main entry point]** - [What it does]
2. **[Secondary entry point]** - [What it does]

## Coding Standards & Patterns

### Language-Specific Guidelines
[Language-specific best practices from analysis]

### Design Patterns Used
1. **[Pattern 1]** - Used in [location], for [purpose]
2. **[Pattern 2]** - Used in [location], for [purpose]

### Naming Conventions
- Classes: [Convention]
- Functions: [Convention]
- Variables: [Convention]
- Files: [Convention]

### Code Style
- Formatting: [Style guide used]
- Imports: [How to organize]
- Comments: [When and how]
- Documentation: [Docstring style]

## Key Modules & Components

### Core Modules
1. **[Module Name]** (`path/to/module`)
   - **Purpose:** [What it does]
   - **Key Classes:** [List]
   - **Key Functions:** [List]
   - **Used By:** [Which modules depend on this]
   - **Dependencies:** [What this depends on]

[Repeat for each core module]

### Utility Modules
[List of utility modules with brief descriptions]

## Dependencies & Integration

### External Dependencies
- **[Dependency 1]** - [Why we use it, how we use it]
- **[Dependency 2]** - [Why we use it, how we use it]

### Internal Dependencies
- **[Module A]** → **[Module B]** - [Relationship]

### Integration Points
- **[External System 1]** - [How we integrate]
- **[External System 2]** - [How we integrate]

## Testing Strategy

### Test Framework
- **Unit Tests:** [Framework and location]
- **Integration Tests:** [Framework and location]
- **E2E Tests:** [Framework and location]

### Running Tests
```bash
[Commands to run tests]
```

### Test Coverage
- Current: [X%]
- Target: [Y%]
- Critical paths: [Must be 100%]

### Writing Tests
- Location: [Where to put tests]
- Naming: [Test naming convention]
- Structure: [Test structure pattern]
- Fixtures: [How to use fixtures]

## Common Tasks

### Adding a New Feature
1. [Step 1]
2. [Step 2]
3. [Step 3]

See: `.claude/workflows/feature_development.md` for detailed workflow

### Fixing a Bug
1. [Step 1]
2. [Step 2]
3. [Step 3]

See: `.claude/workflows/bug_fixing.md` for detailed workflow

### Refactoring Code
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Known Issues & Gotchas

### Common Pitfalls
1. **[Issue 1]** - [Why it happens, how to avoid]
2. **[Issue 2]** - [Why it happens, how to avoid]

### TODOs & Technical Debt
- [TODO 1 with location]
- [TODO 2 with location]
- [Technical debt item 1]

See: `.claude/context/gotchas.md` for complete list

## Performance Considerations

### Bottlenecks
- [Known bottleneck 1] - [Impact and mitigation]
- [Known bottleneck 2] - [Impact and mitigation]

### Optimization Patterns
- [Pattern 1] - [When to use]
- [Pattern 2] - [When to use]

See: `.claude/context/performance.md` for details

## Security & Compliance

### Security Rules
- [Rule 1]
- [Rule 2]
- [Rule 3]

### Sensitive Data Handling
- [How to handle PII]
- [How to handle credentials]
- [How to handle secrets]

See: `.claude/context/security.md` for complete guidelines

## Deployment & Operations

### Deployment Process
[Brief overview of deployment]

### Monitoring
- Metrics: [What we track]
- Logs: [Where to find logs]
- Alerts: [What triggers alerts]

### Troubleshooting
See: `TROUBLESHOOTING.md` for common issues

## Resources & References

### Documentation
- Architecture: `ARCHITECTURE.md`
- API Reference: `API_REFERENCE.md`
- Testing Guide: `TESTING_GUIDE.md`
- Dependencies: `DEPENDENCIES.md`

### Examples
- Good patterns: `.claude/examples/good_patterns/`
- Common tasks: `.claude/examples/common_tasks/`

### Team Resources
- Team chat: [Link]
- Wiki: [Link]
- Issue tracker: [Link]

## Claude Code Usage Tips

### Custom Commands Available
- `/add-feature` - Scaffold a new feature
- `/fix-bug` - Fix a bug with context
- `/add-test` - Add tests for existing code
- `/refactor` - Refactor code while preserving behavior
- `/update-docs` - Update documentation

See: `.claude/commands/` for all custom commands

### Best Practices
1. **Always read context first** - Review relevant .md files
2. **Follow existing patterns** - Don't introduce new patterns without discussion
3. **Write tests** - New code needs tests
4. **Update docs** - Keep documentation current
5. **Check security** - Review security implications

---

*This file is auto-generated by doc-agent. Last updated: [Timestamp]*
*For detailed information, explore the .claude/ directory*
```

---

### 2. .clinerules
**Location:** Repository root  
**Priority:** HIGHEST  
**Purpose:** Coding rules that Claude Code enforces

**Complete Template:**

```yaml
# Claude Code Rules for [Repository Name]
# Auto-generated by doc-agent

# Language and framework
language: python  # or javascript, typescript, etc.
framework: django  # or react, express, etc.
version: "3.9+"  # language version

# Code style and formatting
style:
  guide: pep8  # or airbnb, google, etc.
  line_length: 100
  indent: 4  # or 2 for JS/TS
  quotes: double  # or single
  trailing_comma: true

# Naming conventions
naming:
  classes: PascalCase
  functions: snake_case
  variables: snake_case
  constants: UPPER_SNAKE_CASE
  files: snake_case
  directories: snake_case

# Import organization
imports:
  order:
    - stdlib
    - third_party
    - local
  style: absolute  # or relative
  
  # Preferred libraries (use these over alternatives)
  preferred:
    - pandas: "Data manipulation"
    - requests: "HTTP client"
    - pytest: "Testing"
  
  # Avoid these libraries
  avoid:
    - urllib: "Use requests instead"
    - nose: "Use pytest instead"

# Code patterns and practices
patterns:
  required:
    - "Use type hints for all function signatures"
    - "Write docstrings for public functions and classes"
    - "Use context managers for resource handling"
    - "Prefer composition over inheritance"
    - "Use list comprehensions for simple transformations"
    - "Handle exceptions explicitly, avoid bare except"
  
  avoid:
    - "Global variables"
    - "Mutable default arguments"
    - "Wildcard imports (from x import *)"
    - "Long functions (>50 lines)"
    - "Deep nesting (>3 levels)"

# Testing requirements
testing:
  framework: pytest
  coverage:
    minimum: 80
    target: 90
    critical_paths: 100
  
  required_for:
    - "All new functions and classes"
    - "Bug fixes (regression tests)"
    - "API endpoints"
    - "Data transformations"
  
  structure:
    location: tests/
    naming: "test_*.py or *_test.py"
    fixtures: tests/fixtures/
  
  practices:
    - "One test file per module"
    - "Use fixtures for test data"
    - "Mock external dependencies"
    - "Test edge cases and error paths"

# Documentation requirements
documentation:
  required_for:
    - "Public APIs"
    - "Complex algorithms"
    - "Configuration options"
    - "Integration points"
  
  style: google  # or numpy, sphinx
  
  include:
    - "Purpose/description"
    - "Arguments with types"
    - "Return values with types"
    - "Raises (exceptions)"
    - "Examples for complex functions"

# Security rules
security:
  required:
    - "Never hardcode secrets or credentials"
    - "Validate all user input"
    - "Use parameterized queries (no SQL injection)"
    - "Sanitize data before logging"
    - "Use HTTPS for external calls"
  
  sensitive_data:
    - "PII must be encrypted at rest"
    - "Credentials in environment variables only"
    - "API keys in secrets manager"
  
  dependencies:
    - "Keep dependencies up to date"
    - "Review security advisories"
    - "No dependencies with known vulnerabilities"

# Performance guidelines
performance:
  required:
    - "Use bulk operations for database queries"
    - "Cache expensive computations"
    - "Use pagination for large datasets"
    - "Profile before optimizing"
  
  limits:
    - "Functions should complete in <100ms (web requests)"
    - "Database queries should use indexes"
    - "Batch size limit: 1000 items"

# Error handling
error_handling:
  required:
    - "Use specific exception types"
    - "Provide meaningful error messages"
    - "Log errors with context"
    - "Don't expose internal details to users"
  
  practices:
    - "Fail fast for invalid input"
    - "Retry transient failures (with backoff)"
    - "Clean up resources in finally blocks"

# Logging
logging:
  required:
    - "Use structured logging"
    - "Include correlation IDs"
    - "Log at appropriate levels"
    - "Don't log sensitive data"
  
  levels:
    - "DEBUG: Detailed diagnostic info"
    - "INFO: General informational messages"
    - "WARNING: Warning messages"
    - "ERROR: Error messages"
    - "CRITICAL: Critical failures"

# Git and version control
git:
  commits:
    format: "type(scope): description"
    types:
      - "feat: New feature"
      - "fix: Bug fix"
      - "docs: Documentation"
      - "refactor: Code refactoring"
      - "test: Adding tests"
      - "chore: Maintenance"
  
  branches:
    main: "Production code"
    develop: "Development integration"
    feature: "feature/description"
    bugfix: "bugfix/description"
    hotfix: "hotfix/description"

# Code review requirements
review:
  required_for:
    - "All code changes"
  
  checklist:
    - "Tests pass"
    - "Coverage maintained/improved"
    - "Documentation updated"
    - "No security issues"
    - "Follows coding standards"
    - "No performance regressions"

# Architecture rules
architecture:
  boundaries:
    - "Don't bypass abstraction layers"
    - "Keep business logic separate from infrastructure"
    - "Use dependency injection"
  
  patterns:
    - "Factory pattern for object creation"
    - "Repository pattern for data access"
    - "Strategy pattern for algorithms"

# File organization
file_organization:
  max_lines: 500
  max_functions: 20
  structure:
    - "Imports at top"
    - "Constants after imports"
    - "Classes/functions in logical order"
    - "Main execution at bottom (if __name__ == '__main__')"

# Dependencies
dependencies:
  rules:
    - "Pin major and minor versions"
    - "Document why each dependency is needed"
    - "Review license compatibility"
    - "Minimize dependency count"
  
  updates:
    - "Update monthly (security patches)"
    - "Test before updating major versions"
    - "Document breaking changes"

# Special rules for this repository
custom_rules:
  - "[Custom rule 1 specific to this repo]"
  - "[Custom rule 2 specific to this repo]"

# Exceptions (document carefully)
exceptions:
  - path: "legacy/old_module.py"
    reason: "Legacy code, scheduled for refactor"
    rules_ignored: ["line_length", "type_hints"]
```

---

### 3. .claude/commands/
**Location:** `.claude/commands/`  
**Priority:** HIGH  
**Purpose:** Custom commands for common tasks

**Files to Generate:**

#### .claude/commands/add_feature.md
```markdown
# Add Feature Command

This command helps scaffold a new feature following our patterns.

## Usage
```
/add-feature <feature-name> <feature-type>
```

## What This Command Does

1. **Analyzes existing patterns** in similar features
2. **Creates directory structure** following conventions
3. **Generates boilerplate code** with proper imports
4. **Creates test file** with basic test structure
5. **Updates documentation** with new feature

## Feature Types

### API Endpoint
```
/add-feature user-profile api-endpoint
```
- Creates route handler
- Adds request/response models
- Generates OpenAPI documentation
- Creates integration tests

### Data Model
```
/add-feature user-profile data-model
```
- Creates model class
- Adds database migration
- Generates serializers
- Creates model tests

### Service/Business Logic
```
/add-feature notification service
```
- Creates service class
- Adds interface/protocol
- Generates unit tests
- Documents public methods

### Component (Frontend)
```
/add-feature user-card component
```
- Creates component file
- Adds props interface
- Generates storybook story
- Creates component tests

## What Gets Generated

### For Python API Endpoint:
```python
# src/api/endpoints/[feature_name].py
from typing import List
from fastapi import APIRouter, Depends
from src.models.[feature_name] import [FeatureName]Model
from src.services.[feature_name] import [FeatureName]Service

router = APIRouter()

@router.get("/[feature-name]")
async def get_[feature_name](
    service: [FeatureName]Service = Depends()
) -> List[[FeatureName]Model]:
    """
    Get [feature_name] data.
    
    Returns:
        List of [feature_name] objects
    """
    return await service.get_all()

# tests/api/test_[feature_name].py
import pytest
from fastapi.testclient import TestClient

def test_get_[feature_name](client: TestClient):
    """Test getting [feature_name] data."""
    response = client.get("/[feature-name]")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Pattern Detection

Claude Code will:
1. Find similar features in the codebase
2. Extract common patterns
3. Apply those patterns to new feature
4. Ensure consistency with existing code

## Files Modified

- New feature files created
- Test files created
- `API_REFERENCE.md` updated
- Router/routes file updated (if applicable)
- `__init__.py` updated for exports

## Best Practices

1. **Use descriptive names** - Clear, not abbreviated
2. **Follow existing patterns** - Maintain consistency
3. **Write tests first** - TDD approach recommended
4. **Document as you go** - Update docs immediately
5. **Keep it simple** - Start minimal, enhance later

## Examples

See `.claude/examples/common_tasks/add_feature_examples.md` for detailed examples.
```

#### .claude/commands/fix_bug.md
```markdown
# Fix Bug Command

This command helps fix bugs systematically with proper testing and documentation.

## Usage
```
/fix-bug <bug-description-or-issue-number>
```

## What This Command Does

1. **Locates relevant code** based on bug description
2. **Analyzes the issue** in context of codebase
3. **Proposes a fix** following our patterns
4. **Creates regression test** to prevent recurrence
5. **Updates documentation** if behavior changed

## Workflow

### Step 1: Understand the Bug
Claude Code will:
- Search for related code
- Check git blame for context
- Review similar past fixes
- Analyze dependencies

### Step 2: Reproduce the Issue
- Create failing test that demonstrates bug
- Verify test fails with current code
- Document reproduction steps

### Step 3: Implement Fix
- Minimal change to fix issue
- Preserve existing behavior where possible
- Follow coding standards
- Add comments explaining fix

### Step 4: Verify Fix
- Ensure new test passes
- Run all existing tests
- Check for side effects
- Test edge cases

### Step 5: Document
- Update TROUBLESHOOTING.md if applicable
- Add comments explaining why
- Update changelog

## Bug Categories

### Logic Bug
```
/fix-bug "Calculation returns wrong value for negative numbers"
```
- Analyzes logic flow
- Checks edge cases
- Verifies mathematical correctness

### Performance Bug
```
/fix-bug "Query takes 30 seconds on large dataset"
```
- Profiles the code
- Suggests optimizations
- Adds performance test

### Integration Bug
```
/fix-bug "External API call fails intermittently"
```
- Checks error handling
- Adds retry logic
- Improves logging

### UI Bug
```
/fix-bug "Button doesn't work on mobile"
```
- Checks responsive design
- Tests on different viewports
- Verifies accessibility

## Example Fix Pattern

### Python Bug Fix:
```python
# Before (buggy):
def calculate_discount(price, discount_percent):
    return price - (price * discount_percent)  # Wrong for percentages > 100

# After (fixed):
def calculate_discount(price, discount_percent):
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount as percentage (0-100)
        
    Returns:
        Discounted price (minimum 0)
    """
    # Bug fix: Handle edge cases for discount > 100%
    discount = price * (discount_percent / 100)
    return max(0, price - discount)

# Regression test:
def test_calculate_discount_edge_cases():
    """Test discount calculation edge cases."""
    assert calculate_discount(100, 150) == 0  # Discount > 100%
    assert calculate_discount(100, 0) == 100  # No discount
    assert calculate_discount(0, 50) == 0  # Zero price
```

## Common Pitfalls to Avoid

1. **Don't just patch symptoms** - Fix root cause
2. **Don't break existing functionality** - Run all tests
3. **Don't skip documentation** - Future you will thank you
4. **Don't forget edge cases** - Test boundaries
5. **Don't ignore performance** - Check impact

## Checklist

Before marking bug as fixed:
- [ ] Failing test created
- [ ] Fix implemented
- [ ] Test now passes
- [ ] All other tests pass
- [ ] Edge cases tested
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Performance checked
```

#### .claude/commands/add_test.md
```markdown
# Add Test Command

This command helps add comprehensive tests for existing code.

## Usage
```
/add-test <file-path> [test-type]
```

## What This Command Does

1. **Analyzes the code** to understand functionality
2. **Identifies test gaps** in coverage
3. **Generates test cases** for untested code
4. **Follows testing patterns** from existing tests
5. **Achieves target coverage** (80%+ minimum)

## Test Types

### Unit Tests
```
/add-test src/services/user_service.py unit
```
- Tests individual functions/methods
- Mocks external dependencies
- Fast execution
- High coverage

### Integration Tests
```
/add-test src/api/endpoints/users.py integration
```
- Tests multiple components together
- Uses test database
- Tests real integrations
- End-to-end scenarios

### E2E Tests
```
/add-test src/workflows/checkout.py e2e
```
- Tests complete user flows
- Uses staging environment
- Browser/API automation
- Critical path verification

## What Gets Generated

### For Python Module:
```python
# tests/unit/services/test_user_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.user_service import UserService
from src.models.user import User

class TestUserService:
    """Test suite for UserService."""
    
    @pytest.fixture
    def service(self):
        """Create UserService instance for testing."""
        return UserService()
    
    @pytest.fixture
    def mock_user(self):
        """Create mock user for testing."""
        return User(id=1, name="Test User", email="test@example.com")
    
    def test_get_user_by_id_success(self, service, mock_user):
        """Test getting user by ID successfully."""
        with patch.object(service, 'db') as mock_db:
            mock_db.query.return_value = mock_user
            
            result = service.get_user_by_id(1)
            
            assert result == mock_user
            mock_db.query.assert_called_once_with(User, id=1)
    
    def test_get_user_by_id_not_found(self, service):
        """Test getting user that doesn't exist."""
        with patch.object(service, 'db') as mock_db:
            mock_db.query.return_value = None
            
            with pytest.raises(UserNotFoundError):
                service.get_user_by_id(999)
    
    def test_get_user_by_id_invalid_id(self, service):
        """Test getting user with invalid ID."""
        with pytest.raises(ValueError):
            service.get_user_by_id(-1)
    
    @pytest.mark.parametrize("user_id,expected", [
        (1, True),
        (999, False),
        (0, False),
    ])
    def test_user_exists(self, service, user_id, expected):
        """Test checking if user exists."""
        with patch.object(service, 'db') as mock_db:
            mock_db.exists.return_value = expected
            
            result = service.user_exists(user_id)
            
            assert result == expected
```

## Test Coverage Analysis

Claude Code will:
1. **Analyze current coverage** - Identify untested code
2. **Prioritize gaps** - Focus on critical paths first
3. **Generate tests** - Cover all branches and edge cases
4. **Verify coverage** - Ensure targets are met

## Test Patterns by Language

### Python (pytest)
- Use fixtures for setup
- Parametrize similar tests
- Mock external dependencies
- Use context managers for cleanup

### JavaScript (Jest)
- Use describe/it blocks
- Mock modules with jest.mock()
- Use beforeEach for setup
- Test async code properly

### TypeScript (Jest + Testing Library)
- Type-safe test data
- Use Testing Library queries
- Test user interactions
- Verify accessibility

## Edge Cases to Test

1. **Boundary values** - Min, max, zero
2. **Invalid input** - Null, undefined, wrong type
3. **Error conditions** - Network failures, timeouts
4. **Concurrent access** - Race conditions
5. **Large datasets** - Performance under load

## Best Practices

1. **Test behavior, not implementation** - Don't test internals
2. **One assertion per test** - Keep tests focused
3. **Descriptive test names** - Clear what's being tested
4. **Arrange-Act-Assert** - Follow AAA pattern
5. **Fast tests** - Mock slow operations
6. **Independent tests** - No test should depend on another
7. **Clean up** - Remove test data after tests

## Examples

See `.claude/examples/good_patterns/testing/` for comprehensive examples.
```

#### .claude/commands/refactor_code.md
#### .claude/commands/update_docs.md

(Similar detailed specifications)

---

### 4. .claude/context/
**Location:** `.claude/context/`  
**Priority:** HIGH  
**Purpose:** Detailed context files for specific topics

**Files to Generate:**

#### .claude/context/architecture.md
```markdown
# Architecture Deep Dive

## System Architecture

### High-Level Overview
[Detailed architecture description from knowledge graph]

### Component Diagram
```
[ASCII art or description of components and relationships]
```

### Data Flow
[Detailed data flow through the system]

### Integration Points
[How this system integrates with others]

## Design Decisions

### Architectural Patterns
1. **[Pattern 1]**
   - Why we use it
   - Where it's applied
   - Benefits and tradeoffs
   
2. **[Pattern 2]**
   - Why we use it
   - Where it's applied
   - Benefits and tradeoffs

### Technology Choices
- **[Technology 1]**: [Why we chose it, alternatives considered]
- **[Technology 2]**: [Why we chose it, alternatives considered]

## Scalability

### Current Scale
- Requests per second: [Number]
- Data volume: [Amount]
- User base: [Number]

### Scaling Strategy
- Horizontal scaling: [How]
- Vertical scaling: [Limits]
- Database scaling: [Strategy]
- Caching strategy: [Approach]

## Evolution

### Past Architecture
[How the architecture evolved]

### Future Plans
[Planned architectural improvements]

### Migration Strategy
[How to migrate to new architecture]
```

#### .claude/context/patterns.md
```markdown
# Code Patterns and Conventions

## Design Patterns Used

### [Pattern 1 Name]
**When to use:** [Scenarios]
**Implementation:** [How we implement it]
**Example locations:** [Where to find examples]

**Good Example:**
```[language]
[Code example]
```

**Why this is good:**
- [Reason 1]
- [Reason 2]

### [Pattern 2 Name]
[Similar structure]

## Anti-Patterns to Avoid

### [Anti-Pattern 1]
**Problem:** [What's wrong with it]
**Why we avoid it:** [Reasons]
**What to do instead:** [Better approach]

**Bad Example:**
```[language]
[Code example to avoid]
```

**Good Alternative:**
```[language]
[Better code example]
```

## Common Conventions

### Error Handling
[How we handle errors consistently]

### Logging
[How we log consistently]

### Configuration
[How we manage configuration]

### State Management
[How we manage state]
```

#### .claude/context/gotchas.md
```markdown
# Common Gotchas and Pitfalls

## Known Issues

### [Issue 1]
**Symptom:** [What you'll see]
**Cause:** [Why it happens]
**Solution:** [How to fix]
**Prevention:** [How to avoid]

**Example:**
```[language]
# This will cause the issue:
[Bad code]

# Do this instead:
[Good code]
```

### [Issue 2]
[Similar structure]

## Tricky Parts of the Codebase

### [Module/Component Name]
**What's tricky:** [Description]
**Common mistakes:** [List]
**Best practices:** [How to work with it safely]

## Performance Traps

### [Performance Issue 1]
**Problem:** [What causes slowness]
**Solution:** [How to optimize]
**Measurement:** [How to verify improvement]

## Security Concerns

### [Security Issue 1]
**Vulnerability:** [What to watch for]
**Mitigation:** [How to protect]
**Testing:** [How to verify security]
```

#### .claude/context/security.md
```markdown
# Security Guidelines

## Security Principles

1. **Principle 1:** [Description]
2. **Principle 2:** [Description]

## Authentication & Authorization

### Authentication
[How authentication works in this codebase]

### Authorization
[How authorization is enforced]

### Token Management
[How tokens are handled]

## Data Protection

### Encryption
- At rest: [Approach]
- In transit: [Approach]
- Keys: [How managed]

### PII Handling
[How to handle personally identifiable information]

### Secrets Management
[How to manage secrets and credentials]

## Input Validation

### Required Validations
- [Validation 1]
- [Validation 2]

### Sanitization
[How to sanitize user input]

## Security Checklist

For any code change, verify:
- [ ] No hardcoded secrets
- [ ] Input validated
- [ ] Output sanitized
- [ ] Authentication enforced
- [ ] Authorization checked
- [ ] HTTPS used
- [ ] Logs don't contain sensitive data
- [ ] Dependencies up to date
- [ ] No SQL injection possible
- [ ] No XSS possible
```

#### .claude/context/performance.md
```markdown
# Performance Guidelines

## Performance Targets

- API response time: < 200ms (p95)
- Database query time: < 50ms (p95)
- Page load time: < 2s
- Time to interactive: < 3s

## Known Bottlenecks

### [Bottleneck 1]
**Location:** [Where]
**Impact:** [Performance cost]
**Mitigation:** [How to work around]
**Future fix:** [Planned improvement]

## Optimization Patterns

### Database Queries
- Use indexes for lookups
- Batch queries when possible
- Paginate large result sets
- Use query caching

### API Calls
- Use connection pooling
- Implement retries with backoff
- Cache responses
- Use bulk endpoints

### Memory Usage
- Stream large files
- Limit batch sizes
- Clean up resources
- Profile memory usage

## Profiling

### How to Profile
```bash
[Commands to profile code]
```

### Interpreting Results
[How to read profiling output]

## Performance Testing

### Load Testing
[How to load test]

### Stress Testing
[How to stress test]

### Benchmarking
[How to benchmark changes]
```

---

### 5. .claude/examples/
**Location:** `.claude/examples/`  
**Priority:** MEDIUM  
**Purpose:** Concrete code examples

**Subdirectories and Files:**

#### .claude/examples/good_patterns/
- `api_endpoint_example.py` - Well-structured API endpoint
- `service_class_example.py` - Well-structured service class
- `test_example.py` - Well-written test
- `error_handling_example.py` - Proper error handling
- `async_example.py` - Proper async/await usage

#### .claude/examples/bad_patterns/
- `antipattern_1.py` - Common mistake with explanation
- `antipattern_2.py` - Another common mistake

#### .claude/examples/common_tasks/
- `add_endpoint_example.md` - Step-by-step example
- `add_model_example.md` - Step-by-step example
- `write_test_example.md` - Step-by-step example

---

### 6. .claude/templates/
**Location:** `.claude/templates/`  
**Priority:** MEDIUM  
**Purpose:** Boilerplate code templates

**Files to Generate:**

Based on detected patterns, create templates for:
- Component templates
- Test templates
- API endpoint templates
- Model/schema templates
- Configuration file templates

---

### 7. .claude/workflows/
**Location:** `.claude/workflows/`  
**Priority:** MEDIUM  
**Purpose:** Step-by-step workflows for common processes

**Files:**
- `feature_development.md` - Complete feature development workflow
- `bug_fixing.md` - Bug fixing workflow
- `code_review.md` - Code review checklist
- `deployment.md` - Deployment process
- `testing.md` - Testing workflow

---

## 📊 Supporting Documentation Files

### 8. ARCHITECTURE.md
**Location:** Repository root  
**Priority:** HIGH

(Detailed architecture documentation - supplement to .claude/context/architecture.md but more comprehensive)

---

### 9. API_REFERENCE.md
**Location:** Repository root  
**Priority:** HIGH

(Complete API reference with endpoints, parameters, responses)

---

### 10. TESTING_GUIDE.md
**Location:** Repository root  
**Priority:** HIGH

(Comprehensive testing guide)

---

### 11. DEPENDENCIES.md
**Location:** Repository root  
**Priority:** MEDIUM

(All dependencies with versions, purposes, and alternatives)

---

### 12. CONTRIBUTING.md
**Location:** Repository root  
**Priority:** MEDIUM

(How to contribute to the codebase)

---

### 13. SECURITY.md
**Location:** Repository root  
**Priority:** HIGH

(Security policies and practices)

---

### 14. TROUBLESHOOTING.md
**Location:** Repository root  
**Priority:** MEDIUM

(Common issues and solutions)

---

## 🎯 Priority Matrix

### Must Generate (Blocks Claude Code without these)
1. **CLAUDE.md** - Primary context
2. **.clinerules** - Coding rules
3. **.claude/commands/** - Common commands (at least top 3)
4. **.claude/context/gotchas.md** - Known issues

### Should Generate (Significantly improves experience)
5. **.claude/context/architecture.md** - Architecture details
6. **.claude/context/patterns.md** - Code patterns
7. **.claude/context/security.md** - Security guidelines
8. **ARCHITECTURE.md** - Detailed architecture
9. **API_REFERENCE.md** - API documentation
10. **TESTING_GUIDE.md** - Testing guide

### Nice to Have (Enhances further)
11. **.claude/examples/** - Code examples
12. **.claude/templates/** - Code templates
13. **.claude/workflows/** - Process workflows
14. **DEPENDENCIES.md** - Dependency docs
15. **TROUBLESHOOTING.md** - Common issues

---

## 🔄 Generation Strategy

### Phase 1: Critical Files (Always)
```python
def generate_critical_files(repo_path, kg_data):
    """Generate must-have files for Claude Code."""
    generate_claude_md(repo_path, kg_data)
    generate_clinerules(repo_path, kg_data)
    generate_top_commands(repo_path, kg_data)  # Top 3-5 commands
    generate_gotchas(repo_path, kg_data)
```

### Phase 2: High-Value Files (If time permits)
```python
def generate_highvalue_files(repo_path, kg_data):
    """Generate files that significantly improve experience."""
    generate_architecture_context(repo_path, kg_data)
    generate_patterns_guide(repo_path, kg_data)
    generate_security_guide(repo_path, kg_data)
    generate_api_reference(repo_path, kg_data)
    generate_testing_guide(repo_path, kg_data)
```

### Phase 3: Enhancement Files (Optional)
```python
def generate_enhancement_files(repo_path, kg_data):
    """Generate nice-to-have enhancement files."""
    generate_code_examples(repo_path, kg_data)
    generate_templates(repo_path, kg_data)
    generate_workflows(repo_path, kg_data)
```

---

## 📏 Quality Criteria

### For Each File:

1. **Completeness**
   - All sections present
   - No placeholder text
   - Real data from analysis

2. **Accuracy**
   - Reflects actual codebase
   - Current conventions used
   - Valid code examples

3. **Usefulness**
   - Actionable information
   - Concrete examples
   - Clear guidance

4. **Consistency**
   - Follows template structure
   - Consistent terminology
   - Cross-references work

5. **Freshness**
   - Timestamp included
   - Reflects current state
   - Update mechanism in place

---

## 🚀 Implementation Checklist

### For Doc-Agent to Implement:

- [ ] File structure creation (.claude directory, subdirectories)
- [ ] CLAUDE.md generator with all sections
- [ ] .clinerules generator with language detection
- [ ] Command generators (add-feature, fix-bug, add-test, refactor, update-docs)
- [ ] Context file generators (architecture, patterns, gotchas, security, performance)
- [ ] Example code extractors
- [ ] Template generators
- [ ] Workflow documentation
- [ ] Supporting docs (ARCHITECTURE, API_REFERENCE, etc.)
- [ ] Cross-reference linker
- [ ] Timestamp management
- [ ] Update detection and regeneration

---

*This specification ensures developers never need to run `/init` - everything is ready from day one.*
