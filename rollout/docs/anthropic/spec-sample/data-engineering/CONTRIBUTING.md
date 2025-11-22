# Contributing Guidelines

## Table of Contents
1. [Welcome](#welcome)
2. [Code of Conduct](#code-of-conduct)
3. [Getting Started](#getting-started)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Commit Guidelines](#commit-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Issue Reporting](#issue-reporting)
9. [Review Process](#review-process)

## Welcome

Thank you for considering contributing to this project! We appreciate your time and effort. This document provides guidelines to help make the contribution process smooth and effective for everyone involved.

### Ways to Contribute

- 🐛 **Report bugs**
- ✨ **Suggest new features**
- 📝 **Improve documentation**
- 🔧 **Fix issues**
- ✅ **Add tests**
- 🎨 **Improve UI/UX**
- 🌐 **Translate**

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- **Be respectful:** Treat everyone with respect and consideration
- **Be collaborative:** Work together constructively
- **Be patient:** Help others learn and grow
- **Be professional:** Focus on what is best for the project
- **Be accountable:** Take responsibility for your actions

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Public or private harassment
- Publishing others' private information
- Other conduct that could be considered inappropriate

### Enforcement

Violations of the Code of Conduct may result in:
1. Warning from maintainers
2. Temporary ban from the project
3. Permanent ban from the project

Report violations to: [project-email@example.com]

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Node.js 20.x** or higher
- **npm 10.x** or higher
- **Git** installed and configured
- **PostgreSQL 15** (for backend development)
- **Redis** (optional, for caching features)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/project-name.git
   cd project-name
   ```
3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/project-name.git
   ```

### Initial Setup

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Run database migrations
npm run db:migrate

# Start development server
npm run dev
```

### Verify Setup

```bash
# Run tests
npm test

# Check linting
npm run lint

# Check types
npm run type-check
```

If all commands succeed, you're ready to contribute! 🎉

## Development Workflow

### Creating a Branch

Always create a new branch for your work:

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix branch
git checkout -b fix/bug-description
```

### Branch Naming Convention

Use descriptive branch names:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes
- `chore/` - Maintenance tasks

**Examples:**
- `feature/user-authentication`
- `fix/login-validation-error`
- `docs/api-reference-update`
- `refactor/user-service-cleanup`

### Development Process

1. **Write Code:**
   - Follow coding standards (see below)
   - Add/update tests
   - Update documentation

2. **Test Your Changes:**
   ```bash
   # Run all tests
   npm test
   
   # Run specific test file
   npm test -- path/to/test.ts
   
   # Watch mode for TDD
   npm test -- --watch
   ```

3. **Check Code Quality:**
   ```bash
   # Run linter
   npm run lint
   
   # Fix linting issues
   npm run lint:fix
   
   # Check types
   npm run type-check
   ```

4. **Commit Changes:**
   ```bash
   git add .
   git commit -m "feat: add user authentication"
   ```

5. **Keep Branch Updated:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push to Your Fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### TypeScript

#### Type Safety

```typescript
// ✅ Good - Explicit types
function getUser(id: string): Promise<User> {
  return userRepository.findById(id);
}

// ❌ Bad - No types
function getUser(id) {
  return userRepository.findById(id);
}
```

#### Avoid `any`

```typescript
// ✅ Good - Use proper types
function processData(data: UserData): Result {
  return transform(data);
}

// ❌ Bad - Using any
function processData(data: any): any {
  return transform(data);
}
```

#### Use Type Inference When Obvious

```typescript
// ✅ Good - Type is obvious
const users = ['Alice', 'Bob']; // string[]

// ❌ Bad - Redundant type annotation
const users: string[] = ['Alice', 'Bob'];
```

### Code Style

#### Naming Conventions

```typescript
// Classes, Interfaces, Types - PascalCase
class UserService {}
interface UserData {}
type UserId = string;

// Functions, Variables - camelCase
function getUserById() {}
const userData = {};

// Constants - UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';
const MAX_RETRY_ATTEMPTS = 3;

// Files - kebab-case
// user-service.ts
// authentication-middleware.ts
```

#### Function Length

Keep functions focused and small:

```typescript
// ✅ Good - Single responsibility
async function createUser(data: CreateUserDTO): Promise<User> {
  await validateUserData(data);
  const user = await saveUser(data);
  await sendWelcomeEmail(user);
  return user;
}

// ❌ Bad - Too many responsibilities
async function createUser(data: any) {
  // 100+ lines of validation, saving, email sending, logging, etc.
}
```

#### Error Handling

Always handle errors appropriately:

```typescript
// ✅ Good - Proper error handling
async function getUser(id: string): Promise<User> {
  try {
    const user = await userRepository.findById(id);
    if (!user) {
      throw new NotFoundError(`User ${id} not found`);
    }
    return user;
  } catch (error) {
    logger.error('Failed to get user', { id, error });
    throw error;
  }
}

// ❌ Bad - Silent failures
async function getUser(id: string) {
  try {
    return await userRepository.findById(id);
  } catch (error) {
    console.log(error);
    return null;
  }
}
```

#### Async/Await vs Promises

Prefer async/await for readability:

```typescript
// ✅ Good - Async/await
async function getUserWithPosts(userId: string) {
  const user = await getUser(userId);
  const posts = await getPosts(userId);
  return { user, posts };
}

// ❌ Bad - Promise chains (for simple cases)
function getUserWithPosts(userId: string) {
  return getUser(userId)
    .then(user => {
      return getPosts(userId)
        .then(posts => ({ user, posts }));
    });
}
```

### React Best Practices

#### Component Structure

```typescript
// ✅ Good - Clear, organized component
import { useState, useEffect } from 'react';
import type { User } from '@/types';

interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

export function UserProfile({ userId, onUpdate }: UserProfileProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, [userId]);

  async function loadUser() {
    setLoading(true);
    try {
      const data = await fetchUser(userId);
      setUser(data);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <LoadingSpinner />;
  if (!user) return <NotFound />;

  return (
    <div>
      <h1>{user.name}</h1>
      {/* Component JSX */}
    </div>
  );
}
```

#### Hooks Best Practices

```typescript
// ✅ Good - Custom hook with clear purpose
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    
    async function load() {
      try {
        setLoading(true);
        const data = await fetchUser(userId);
        if (!cancelled) {
          setUser(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [userId]);

  return { user, loading, error };
}
```

### Documentation

#### Function Documentation

```typescript
/**
 * Creates a new user account
 * 
 * @param data - User registration data
 * @param options - Optional configuration
 * @returns Newly created user with tokens
 * @throws {ValidationError} When data is invalid
 * @throws {ConflictError} When email already exists
 * 
 * @example
 * ```typescript
 * const user = await createUser({
 *   email: 'user@example.com',
 *   password: 'secure123',
 *   username: 'johndoe'
 * });
 * ```
 */
async function createUser(
  data: CreateUserDTO,
  options?: CreateUserOptions
): Promise<UserWithTokens> {
  // Implementation
}
```

#### Inline Comments

```typescript
// Use comments to explain "why", not "what"

// ✅ Good - Explains reasoning
// Using exponential backoff to avoid overwhelming the API
// during high traffic periods
await retryWithBackoff(apiCall);

// ❌ Bad - States the obvious
// Retry the API call
await retryWithBackoff(apiCall);
```

## Commit Guidelines

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies updates
- `ci`: CI/CD changes

### Examples

#### Simple Commit

```bash
git commit -m "feat(auth): add JWT token refresh mechanism"
```

#### Detailed Commit

```bash
git commit -m "fix(api): resolve user data race condition

The user update endpoint had a race condition when multiple
requests were made simultaneously. This fix implements
optimistic locking using version numbers.

Fixes #123"
```

#### Breaking Change

```bash
git commit -m "feat(api): redesign authentication API

BREAKING CHANGE: Authentication endpoints have been restructured.
- POST /auth/login now returns { accessToken, refreshToken }
- The previous /auth/token endpoint has been removed
- See migration guide in docs/migration/v2-auth.md"
```

### Commit Best Practices

1. **Make atomic commits:** Each commit should represent a single logical change
2. **Write meaningful messages:** Explain what and why, not how
3. **Reference issues:** Include issue numbers when applicable
4. **Keep commits small:** Easier to review and revert if needed

```bash
# ✅ Good - Atomic commits
git commit -m "feat(auth): add user registration"
git commit -m "test(auth): add registration tests"
git commit -m "docs(auth): update API documentation"

# ❌ Bad - Everything in one commit
git commit -m "add registration, tests, and docs"
```

## Pull Request Process

### Before Creating PR

- ✅ Code follows project standards
- ✅ All tests pass
- ✅ No linting errors
- ✅ Documentation updated
- ✅ Branch is up-to-date with main

### Creating a Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### PR Title

Follow the same format as commit messages:

```
feat(auth): add JWT token refresh mechanism
fix(api): resolve user data race condition
docs(readme): update installation instructions
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the project's code style
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)

## Additional Notes
Any additional information for reviewers
```

### PR Size Guidelines

Keep PRs manageable:

- **Small:** < 200 lines (ideal)
- **Medium:** 200-500 lines
- **Large:** > 500 lines (should be split if possible)

**Breaking up large PRs:**
1. Split into multiple logical PRs
2. Create separate PRs for refactoring
3. Use feature flags for incomplete features

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues:** Check if it's already reported
2. **Check documentation:** Ensure it's not already documented
3. **Verify it's reproducible:** Test on latest version

### Bug Report Template

```markdown
## Bug Description
A clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 13.0]
- Browser: [e.g., Chrome 120]
- Node version: [e.g., 20.10.0]
- Project version: [e.g., 1.2.3]

## Additional Context
Any other relevant information

## Possible Solution
(Optional) Suggest a fix/reason for the bug
```

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other solutions did you consider?

## Additional Context
Any other relevant information
```

## Review Process

### For Contributors

When your PR is under review:

1. **Be responsive:** Address feedback promptly
2. **Be open:** Welcome constructive criticism
3. **Ask questions:** If feedback is unclear, ask for clarification
4. **Make requested changes:** Update your PR based on feedback

### For Reviewers

When reviewing PRs:

1. **Be respectful:** Provide constructive feedback
2. **Be specific:** Point to exact lines when possible
3. **Be thorough:** Check code, tests, and documentation
4. **Be timely:** Review within 24-48 hours when possible

### Review Checklist

- [ ] Code follows project standards
- [ ] Tests are present and comprehensive
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance implications considered
- [ ] Error handling is appropriate
- [ ] Edge cases are handled
- [ ] Code is maintainable

### Approval Process

1. **Initial Review:** At least one maintainer reviews
2. **Changes Requested:** Author addresses feedback
3. **Re-review:** Reviewer checks updates
4. **Approval:** At least one approval required
5. **Merge:** Maintainer merges the PR

### After Merge

- Your changes are included in the next release
- Congratulations! 🎉
- You're credited in the changelog
- Consider contributing more!

## Questions?

If you have questions about contributing:

- 📧 Email: [project-email@example.com]
- 💬 Discord: [Discord invite link]
- 📖 Docs: [Documentation link]
- 💡 Discussions: [GitHub Discussions link]

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🙏

---

*Last Updated: 2024-11-21*
*These guidelines are subject to change as the project evolves*
