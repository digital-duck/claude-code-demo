# Dependencies

## Table of Contents
1. [Overview](#overview)
2. [Frontend Dependencies](#frontend-dependencies)
3. [Backend Dependencies](#backend-dependencies)
4. [Development Dependencies](#development-dependencies)
5. [Dependency Management](#dependency-management)
6. [Security](#security)
7. [Upgrade Guidelines](#upgrade-guidelines)

## Overview

This document provides comprehensive information about project dependencies, their purposes, versions, and management practices.

### Dependency Philosophy
- **Minimize dependencies:** Only add dependencies that provide significant value
- **Prefer maintained packages:** Choose actively maintained libraries
- **Check bundle size:** Consider impact on application size
- **Security first:** Regular security audits and updates
- **Type safety:** Prefer packages with TypeScript support

## Frontend Dependencies

### Core Framework & Runtime

#### React
```json
"react": "^18.2.0",
"react-dom": "^18.2.0"
```
**Purpose:** UI library for building component-based interfaces  
**Documentation:** https://react.dev/  
**License:** MIT  
**Why chosen:** Industry standard, excellent ecosystem, strong TypeScript support

#### TypeScript
```json
"typescript": "^5.3.0"
```
**Purpose:** Static type checking for JavaScript  
**Documentation:** https://www.typescriptlang.org/  
**License:** Apache-2.0  
**Why chosen:** Type safety, better IDE support, fewer runtime errors

### Build Tools

#### Vite
```json
"vite": "^5.0.0",
"@vitejs/plugin-react": "^4.2.0"
```
**Purpose:** Fast build tool and development server  
**Documentation:** https://vitejs.dev/  
**License:** MIT  
**Why chosen:** Fast HMR, efficient builds, excellent developer experience  
**Configuration:** `vite.config.ts`

### State Management

#### Redux Toolkit
```json
"@reduxjs/toolkit": "^2.0.0",
"react-redux": "^9.0.0"
```
**Purpose:** Global state management  
**Documentation:** https://redux-toolkit.js.org/  
**License:** MIT  
**Why chosen:** Simplified Redux API, built-in best practices, TypeScript support  
**Usage pattern:**
```typescript
// store/slices/userSlice.ts
import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: { data: null, loading: false },
  reducers: {
    setUser: (state, action) => {
      state.data = action.payload;
    }
  }
});
```

#### React Query
```json
"@tanstack/react-query": "^5.0.0"
```
**Purpose:** Server state management and data fetching  
**Documentation:** https://tanstack.com/query/latest  
**License:** MIT  
**Why chosen:** Automatic caching, background refetching, optimistic updates  
**Usage pattern:**
```typescript
const { data, isLoading } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId)
});
```

### Routing

#### React Router
```json
"react-router-dom": "^6.20.0"
```
**Purpose:** Client-side routing  
**Documentation:** https://reactrouter.com/  
**License:** MIT  
**Why chosen:** De facto standard for React routing, good TypeScript support

### Forms

#### React Hook Form
```json
"react-hook-form": "^7.48.0"
```
**Purpose:** Form state management and validation  
**Documentation:** https://react-hook-form.com/  
**License:** MIT  
**Why chosen:** Performant, minimal re-renders, great developer experience

#### Zod
```json
"zod": "^3.22.0"
```
**Purpose:** Schema validation  
**Documentation:** https://zod.dev/  
**License:** MIT  
**Why chosen:** TypeScript-first, composable schemas, excellent type inference  
**Usage pattern:**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
});

type User = z.infer<typeof userSchema>;
```

### UI Libraries

#### Tailwind CSS
```json
"tailwindcss": "^3.3.0"
```
**Purpose:** Utility-first CSS framework  
**Documentation:** https://tailwindcss.com/  
**License:** MIT  
**Why chosen:** Rapid development, consistent design, small production bundle  
**Configuration:** `tailwind.config.js`

#### Headless UI
```json
"@headlessui/react": "^1.7.0"
```
**Purpose:** Unstyled, accessible UI components  
**Documentation:** https://headlessui.com/  
**License:** MIT  
**Why chosen:** Accessibility built-in, works great with Tailwind

#### Lucide React
```json
"lucide-react": "^0.294.0"
```
**Purpose:** Icon library  
**Documentation:** https://lucide.dev/  
**License:** ISC  
**Why chosen:** Modern icons, tree-shakeable, TypeScript support

### HTTP Client

#### Axios
```json
"axios": "^1.6.0"
```
**Purpose:** HTTP client for API requests  
**Documentation:** https://axios-http.com/  
**License:** MIT  
**Why chosen:** Interceptors, request/response transformation, automatic JSON parsing  
**Configuration:**
```typescript
// src/lib/axios.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.VITE_API_URL,
  timeout: 10000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Date & Time

#### date-fns
```json
"date-fns": "^2.30.0"
```
**Purpose:** Date utility library  
**Documentation:** https://date-fns.org/  
**License:** MIT  
**Why chosen:** Functional, immutable, tree-shakeable, comprehensive  
**Alternative:** `dayjs` (smaller bundle size)

### Utilities

#### clsx
```json
"clsx": "^2.0.0"
```
**Purpose:** Conditional className utility  
**License:** MIT  
**Why chosen:** Tiny, fast, simple

#### lodash-es
```json
"lodash-es": "^4.17.21"
```
**Purpose:** Utility functions  
**Documentation:** https://lodash.com/  
**License:** MIT  
**Why chosen:** Tree-shakeable ES modules, comprehensive utilities  
**Note:** Import specific functions to minimize bundle size
```typescript
import { debounce } from 'lodash-es';
```

## Backend Dependencies

### Core Framework

#### Express
```json
"express": "^4.18.0"
```
**Purpose:** Web application framework  
**Documentation:** https://expressjs.com/  
**License:** MIT  
**Why chosen:** Mature, extensive middleware ecosystem, flexible

#### TypeScript
```json
"typescript": "^5.3.0",
"@types/node": "^20.10.0",
"@types/express": "^4.17.0"
```
**Purpose:** Type safety for backend code  
**License:** Apache-2.0

### Database

#### Prisma
```json
"prisma": "^5.7.0",
"@prisma/client": "^5.7.0"
```
**Purpose:** Database ORM and migration tool  
**Documentation:** https://www.prisma.io/  
**License:** Apache-2.0  
**Why chosen:** Type-safe queries, excellent DX, migration management  
**Configuration:** `prisma/schema.prisma`  
**Commands:**
```bash
npx prisma migrate dev    # Create and apply migration
npx prisma generate       # Generate client
npx prisma studio         # GUI for database
```

#### PostgreSQL Client
```json
"pg": "^8.11.0"
```
**Purpose:** PostgreSQL database driver  
**License:** MIT  
**Note:** Used by Prisma

### Authentication

#### Passport
```json
"passport": "^0.7.0",
"passport-jwt": "^4.0.0",
"passport-local": "^1.0.0"
```
**Purpose:** Authentication middleware  
**Documentation:** http://www.passportjs.org/  
**License:** MIT  
**Why chosen:** Strategy-based authentication, extensive strategy ecosystem

#### JSON Web Token
```json
"jsonwebtoken": "^9.0.0"
```
**Purpose:** JWT generation and verification  
**Documentation:** https://github.com/auth0/node-jsonwebtoken  
**License:** MIT  
**Usage pattern:**
```typescript
import jwt from 'jsonwebtoken';

const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET!,
  { expiresIn: '15m' }
);
```

#### bcrypt
```json
"bcrypt": "^5.1.0"
```
**Purpose:** Password hashing  
**Documentation:** https://github.com/kelektiv/node.bcrypt.js  
**License:** MIT  
**Why chosen:** Industry standard, secure password hashing  
**Usage pattern:**
```typescript
const hash = await bcrypt.hash(password, 10);
const isValid = await bcrypt.compare(password, hash);
```

### Validation

#### Zod
```json
"zod": "^3.22.0"
```
**Purpose:** Request validation  
**License:** MIT  
**Usage pattern:**
```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    password: z.string().min(8)
  })
});

// Middleware
const validate = (schema) => (req, res, next) => {
  try {
    schema.parse({ body: req.body, query: req.query });
    next();
  } catch (error) {
    res.status(400).json({ error: error.errors });
  }
};
```

### Logging

#### Winston
```json
"winston": "^3.11.0"
```
**Purpose:** Logging library  
**Documentation:** https://github.com/winstonjs/winston  
**License:** MIT  
**Why chosen:** Flexible transports, log levels, structured logging  
**Configuration:**
```typescript
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Email

#### Nodemailer
```json
"nodemailer": "^6.9.0"
```
**Purpose:** Email sending  
**Documentation:** https://nodemailer.com/  
**License:** MIT  
**Why chosen:** Reliable, supports various transports

### Caching

#### Redis Client
```json
"redis": "^4.6.0"
```
**Purpose:** Redis client for caching  
**Documentation:** https://github.com/redis/node-redis  
**License:** MIT  
**Usage pattern:**
```typescript
import { createClient } from 'redis';

const redis = createClient({
  url: process.env.REDIS_URL
});

await redis.set('key', 'value', { EX: 3600 });
const value = await redis.get('key');
```

### HTTP Utilities

#### Helmet
```json
"helmet": "^7.1.0"
```
**Purpose:** Security headers middleware  
**Documentation:** https://helmetjs.github.io/  
**License:** MIT  
**Why chosen:** Easy security header configuration

#### CORS
```json
"cors": "^2.8.5"
```
**Purpose:** CORS middleware  
**License:** MIT

#### Express Rate Limit
```json
"express-rate-limit": "^7.1.0"
```
**Purpose:** Rate limiting middleware  
**Documentation:** https://github.com/express-rate-limit/express-rate-limit  
**License:** MIT  
**Configuration:**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});

app.use('/api/', limiter);
```

## Development Dependencies

### Testing

#### Frontend Testing
```json
"vitest": "^1.0.0",
"@testing-library/react": "^14.1.0",
"@testing-library/user-event": "^14.5.0",
"@testing-library/jest-dom": "^6.1.0",
"happy-dom": "^12.10.0"
```

#### Backend Testing
```json
"jest": "^29.7.0",
"ts-jest": "^29.1.0",
"supertest": "^6.3.0",
"@types/supertest": "^2.0.0"
```

#### E2E Testing
```json
"@playwright/test": "^1.40.0"
```

### Code Quality

#### ESLint
```json
"eslint": "^8.54.0",
"@typescript-eslint/eslint-plugin": "^6.13.0",
"@typescript-eslint/parser": "^6.13.0",
"eslint-plugin-react": "^7.33.0",
"eslint-plugin-react-hooks": "^4.6.0"
```
**Configuration:** `.eslintrc.json`

#### Prettier
```json
"prettier": "^3.1.0"
```
**Configuration:** `.prettierrc`

### Git Hooks

#### Husky
```json
"husky": "^8.0.0",
"lint-staged": "^15.1.0"
```
**Purpose:** Git hooks management  
**Configuration:**
```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

## Dependency Management

### Installation

```bash
# Install all dependencies
npm install

# Add new dependency
npm install package-name

# Add dev dependency
npm install -D package-name

# Install specific version
npm install package-name@1.2.3
```

### Updates

```bash
# Check for outdated packages
npm outdated

# Update all packages to latest within semver range
npm update

# Update to latest version (breaking changes possible)
npm install package-name@latest

# Interactive update tool
npx npm-check-updates -i
```

### Auditing

```bash
# Check for security vulnerabilities
npm audit

# Fix vulnerabilities automatically
npm audit fix

# Force fix (may introduce breaking changes)
npm audit fix --force
```

## Security

### Security Practices

1. **Regular Updates**
   - Weekly dependency updates
   - Monthly major version reviews
   - Immediate security patches

2. **Vulnerability Scanning**
   - `npm audit` in CI/CD
   - Dependabot alerts enabled
   - Snyk integration (optional)

3. **Dependency Review**
   - Check package popularity
   - Review maintainer activity
   - Check for known vulnerabilities
   - Verify license compatibility

### License Compliance

All dependencies use permissive licenses:
- MIT
- Apache-2.0
- ISC
- BSD-3-Clause

Check licenses:
```bash
npx license-checker --summary
```

## Upgrade Guidelines

### Before Upgrading

1. **Read Changelog:** Check breaking changes
2. **Review Migration Guide:** Follow official guides
3. **Check Dependencies:** Ensure compatibility
4. **Backup:** Commit current state

### Upgrade Process

1. **Create Branch:**
   ```bash
   git checkout -b upgrade/package-name
   ```

2. **Update Package:**
   ```bash
   npm install package-name@latest
   ```

3. **Update Code:**
   - Fix breaking changes
   - Update types if needed
   - Adjust configurations

4. **Test Thoroughly:**
   ```bash
   npm run test
   npm run type-check
   npm run lint
   ```

5. **Test Manually:**
   - Run development server
   - Test affected features
   - Check console for errors

6. **Document Changes:**
   - Update CHANGELOG.md
   - Note breaking changes
   - Update documentation

### Major Version Upgrades

For major version upgrades (React, TypeScript, etc.):

1. **Read Release Notes:** Understand all changes
2. **Use Codemods:** Automate refactoring when available
3. **Incremental Approach:** One major dependency at a time
4. **Extended Testing:** Run full test suite multiple times
5. **Staged Rollout:** Deploy to staging first

### Emergency Security Updates

1. **Assess Impact:** Understand the vulnerability
2. **Update Immediately:**
   ```bash
   npm audit fix
   ```
3. **Test Critical Paths:** Verify no breakage
4. **Deploy ASAP:** Fast-track to production
5. **Document:** Note reason for emergency update

## Deprecated Dependencies

### Removed/Replaced Packages

| Old Package | Replaced With | Reason |
|------------|---------------|---------|
| `moment` | `date-fns` | Bundle size, immutability |
| `request` | `axios` | Deprecated, no longer maintained |
| `tslint` | `eslint` | TSLint deprecated |

### Avoid These Packages

- **Moment.js:** Large bundle, use date-fns or day.js
- **Request:** Deprecated, use axios or fetch
- **Node-sass:** Deprecated, use dart-sass
- **TSLint:** Deprecated, use ESLint with TypeScript

## Troubleshooting

### Common Issues

#### Peer Dependency Warnings
```bash
# Install with legacy peer deps
npm install --legacy-peer-deps
```

#### Lock File Conflicts
```bash
# Delete lock file and node_modules
rm -rf node_modules package-lock.json
npm install
```

#### Cache Issues
```bash
# Clear npm cache
npm cache clean --force
```

#### Type Definition Issues
```bash
# Install type definitions
npm install -D @types/package-name

# Check if types are available
npm search @types/package-name
```

---

*Last Updated: 2024-11-21*
*Dependencies reviewed and audited regularly*
