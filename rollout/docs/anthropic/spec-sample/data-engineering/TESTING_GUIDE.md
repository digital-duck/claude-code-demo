# Testing Guide

## Table of Contents
1. [Overview](#overview)
2. [Testing Philosophy](#testing-philosophy)
3. [Test Types](#test-types)
4. [Testing Setup](#testing-setup)
5. [Writing Tests](#writing-tests)
6. [Best Practices](#best-practices)
7. [Coverage Requirements](#coverage-requirements)
8. [CI/CD Integration](#cicd-integration)

## Overview

This guide outlines the testing standards and practices for the project. All code changes must include appropriate tests and maintain the minimum coverage requirements.

### Testing Stack

#### Frontend
- **Test Runner:** Vitest
- **Testing Library:** React Testing Library
- **Mocking:** Vitest mocks
- **E2E Testing:** Playwright / Cypress
- **Coverage:** Vitest coverage (c8)

#### Backend
- **Test Runner:** Jest
- **API Testing:** Supertest
- **Mocking:** Jest mocks
- **Database:** In-memory database for testing
- **Coverage:** Jest coverage (Istanbul)

## Testing Philosophy

### Testing Pyramid

```
        /\
       /  \
      /E2E \          Fewer, slower tests
     /------\         Test complete flows
    /        \
   /Integration\      Medium number, medium speed
  /------------\      Test component interactions
 /              \
/   Unit Tests   \    Many, fast tests
/________________\    Test individual units
```

### Guidelines
1. **Write tests first** (TDD when appropriate)
2. **Test behavior, not implementation**
3. **Keep tests simple and focused**
4. **Make tests independent**
5. **Use descriptive test names**
6. **Maintain fast test execution**

## Test Types

### 1. Unit Tests

Unit tests verify individual functions, classes, or components in isolation.

#### Example: Testing a Utility Function

```typescript
// src/utils/string.utils.ts
export function capitalize(str: string): string {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// src/utils/string.utils.test.ts
import { describe, it, expect } from 'vitest';
import { capitalize } from './string.utils';

describe('capitalize', () => {
  it('should capitalize first letter of lowercase string', () => {
    const result = capitalize('hello');
    expect(result).toBe('Hello');
  });

  it('should handle uppercase strings', () => {
    const result = capitalize('HELLO');
    expect(result).toBe('Hello');
  });

  it('should handle empty string', () => {
    const result = capitalize('');
    expect(result).toBe('');
  });

  it('should handle single character', () => {
    const result = capitalize('a');
    expect(result).toBe('A');
  });

  it('should handle strings with spaces', () => {
    const result = capitalize('hello world');
    expect(result).toBe('Hello world');
  });
});
```

#### Example: Testing a Service Class

```typescript
// src/services/user.service.ts
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDTO): Promise<User> {
    const existingUser = await this.userRepository.findByEmail(data.email);
    if (existingUser) {
      throw new ConflictError('User already exists');
    }

    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcomeEmail(user.email);
    
    return user;
  }
}

// src/services/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './user.service';
import { ConflictError } from '../errors';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: any;
  let mockEmailService: any;

  beforeEach(() => {
    // Create mocks
    mockUserRepository = {
      findByEmail: vi.fn(),
      create: vi.fn()
    };
    
    mockEmailService = {
      sendWelcomeEmail: vi.fn()
    };

    // Create service instance with mocks
    userService = new UserService(mockUserRepository, mockEmailService);
  });

  describe('createUser', () => {
    const userData = {
      email: 'test@example.com',
      username: 'testuser',
      password: 'password123'
    };

    it('should create a new user successfully', async () => {
      // Arrange
      const expectedUser = { id: '123', ...userData };
      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.create.mockResolvedValue(expectedUser);
      mockEmailService.sendWelcomeEmail.mockResolvedValue(undefined);

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(userData.email);
      expect(mockUserRepository.create).toHaveBeenCalledWith(userData);
      expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(userData.email);
    });

    it('should throw ConflictError if user already exists', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue({ id: '456' });

      // Act & Assert
      await expect(userService.createUser(userData)).rejects.toThrow(ConflictError);
      expect(mockUserRepository.create).not.toHaveBeenCalled();
      expect(mockEmailService.sendWelcomeEmail).not.toHaveBeenCalled();
    });
  });
});
```

### 2. Integration Tests

Integration tests verify that multiple components work together correctly.

#### Example: Testing API Endpoints

```typescript
// src/routes/users.integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { setupTestDatabase, teardownTestDatabase } from '../test-utils';

describe('User API Integration Tests', () => {
  let authToken: string;

  beforeAll(async () => {
    await setupTestDatabase();
    
    // Create and login test user
    const response = await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'test@example.com',
        username: 'testuser',
        password: 'Password123!',
        firstName: 'Test',
        lastName: 'User'
      });
    
    authToken = response.body.data.tokens.accessToken;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('GET /api/v1/users/me', () => {
    it('should return current user data', async () => {
      const response = await request(app)
        .get('/api/v1/users/me')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toMatchObject({
        email: 'test@example.com',
        username: 'testuser',
        firstName: 'Test',
        lastName: 'User'
      });
    });

    it('should return 401 without authentication', async () => {
      await request(app)
        .get('/api/v1/users/me')
        .expect(401);
    });
  });

  describe('PATCH /api/v1/users/me', () => {
    it('should update user data', async () => {
      const response = await request(app)
        .patch('/api/v1/users/me')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          firstName: 'Updated',
          bio: 'Test bio'
        })
        .expect(200);

      expect(response.body.data).toMatchObject({
        firstName: 'Updated',
        bio: 'Test bio'
      });
    });

    it('should validate input data', async () => {
      const response = await request(app)
        .patch('/api/v1/users/me')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'invalid-email'
        })
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

### 3. Component Tests (Frontend)

Component tests verify React components in isolation.

```typescript
// src/components/LoginForm/LoginForm.tsx
import { useState } from 'react';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onSubmit(email, password);
    } catch (err) {
      setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <div role="alert">{error}</div>}
      <button type="submit" disabled={loading}>
        {loading ? 'Loading...' : 'Login'}
      </button>
    </form>
  );
}

// src/components/LoginForm/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render form fields', () => {
    const mockSubmit = vi.fn();
    render(<LoginForm onSubmit={mockSubmit} />);

    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('should submit form with valid data', async () => {
    const mockSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockSubmit} />);

    await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  it('should display error message on failed login', async () => {
    const mockSubmit = vi.fn().mockRejectedValue(new Error('Login failed'));
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockSubmit} />);

    await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'wrong');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Invalid credentials');
    });
  });

  it('should disable button during submission', async () => {
    const mockSubmit = vi.fn().mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockSubmit} />);

    await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
    await user.type(screen.getByPlaceholderText('Password'), 'password123');
    
    const button = screen.getByRole('button', { name: /login/i });
    await user.click(button);

    expect(button).toBeDisabled();
    expect(button).toHaveTextContent('Loading...');

    await waitFor(() => {
      expect(button).not.toBeDisabled();
    });
  });
});
```

### 4. End-to-End Tests

E2E tests verify complete user flows through the application.

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should allow user to register and login', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');

    // Fill registration form
    await page.fill('input[name="email"]', 'newuser@example.com');
    await page.fill('input[name="username"]', 'newuser');
    await page.fill('input[name="password"]', 'Password123!');
    await page.fill('input[name="confirmPassword"]', 'Password123!');
    
    // Submit form
    await page.click('button[type="submit"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');

    // Logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');

    // Should redirect to login
    await expect(page).toHaveURL('/login');

    // Login again
    await page.fill('input[name="email"]', 'newuser@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');

    // Should be back on dashboard
    await expect(page).toHaveURL('/dashboard');
  });

  test('should show validation errors', async ({ page }) => {
    await page.goto('/register');

    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', '123');
    await page.click('button[type="submit"]');

    await expect(page.locator('[role="alert"]')).toContainText('Invalid email');
    await expect(page.locator('[role="alert"]')).toContainText('Password must be at least');
  });
});
```

## Testing Setup

### Test Configuration

#### Vitest Configuration (Frontend)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.test.ts',
        '**/*.spec.ts'
      ]
    }
  }
});
```

#### Jest Configuration (Backend)

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts',
    '!src/test/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts']
};
```

### Test Utilities

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret';

// Setup test database
export async function setupTestDatabase() {
  // Initialize test database
}

export async function teardownTestDatabase() {
  // Clean up test database
}

// Common test utilities
export function createMockUser(overrides = {}) {
  return {
    id: '123',
    email: 'test@example.com',
    username: 'testuser',
    createdAt: new Date(),
    ...overrides
  };
}
```

## Best Practices

### 1. Test Structure (AAA Pattern)

```typescript
it('should create user with valid data', async () => {
  // Arrange - Set up test data and mocks
  const userData = { email: 'test@example.com', password: 'pass123' };
  mockRepository.create.mockResolvedValue({ id: '123', ...userData });

  // Act - Execute the code under test
  const result = await userService.createUser(userData);

  // Assert - Verify the results
  expect(result).toEqual({ id: '123', ...userData });
  expect(mockRepository.create).toHaveBeenCalledWith(userData);
});
```

### 2. Descriptive Test Names

```typescript
// ❌ Bad
it('test1', () => { ... });
it('works', () => { ... });

// ✅ Good
it('should return user data when valid ID is provided', () => { ... });
it('should throw NotFoundError when user does not exist', () => { ... });
```

### 3. Test Independence

```typescript
// ❌ Bad - Tests depend on each other
let user;

it('creates user', async () => {
  user = await createUser({ email: 'test@example.com' });
});

it('updates user', async () => {
  await updateUser(user.id, { name: 'Updated' });
});

// ✅ Good - Each test is independent
it('creates user', async () => {
  const user = await createUser({ email: 'test@example.com' });
  expect(user).toBeDefined();
});

it('updates user', async () => {
  const user = await createUser({ email: 'test@example.com' });
  const updated = await updateUser(user.id, { name: 'Updated' });
  expect(updated.name).toBe('Updated');
});
```

### 4. Use Test Doubles Appropriately

```typescript
// Spy - Track calls to real implementation
const logger = {
  info: vi.spyOn(console, 'log')
};

// Stub - Return predetermined values
const stub = vi.fn().mockReturnValue('fixed value');

// Mock - Replace entire object
const mock = {
  getData: vi.fn().mockResolvedValue({ id: 1 }),
  saveData: vi.fn().mockResolvedValue(true)
};
```

### 5. Test Edge Cases

```typescript
describe('divide function', () => {
  it('should divide positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  it('should handle zero numerator', () => {
    expect(divide(0, 5)).toBe(0);
  });

  it('should throw error for division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });

  it('should handle decimal results', () => {
    expect(divide(10, 3)).toBeCloseTo(3.33, 2);
  });
});
```

## Coverage Requirements

### Minimum Coverage Thresholds
- **Statements:** 80%
- **Branches:** 80%
- **Functions:** 80%
- **Lines:** 80%

### What to Test
✅ **DO test:**
- Business logic
- Data transformations
- API endpoints
- User interactions
- Error handling
- Edge cases

❌ **DON'T test:**
- Third-party libraries
- Framework internals
- Simple getters/setters
- Configuration files

### Viewing Coverage

```bash
# Run tests with coverage
npm run test:coverage

# View coverage report
open coverage/index.html
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run linter
        run: npm run lint
        
      - name: Run type check
        run: npm run type-check
        
      - name: Run tests
        run: npm run test:coverage
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

### Pre-commit Hook

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm run type-check
npm run test:changed
```

---

*Last Updated: 2024-11-21*
*Testing standards are enforced in CI/CD pipeline*
