# Troubleshooting Guide

## Table of Contents
1. [Common Issues](#common-issues)
2. [Installation Problems](#installation-problems)
3. [Development Server Issues](#development-server-issues)
4. [Build Problems](#build-problems)
5. [Database Issues](#database-issues)
6. [Authentication Problems](#authentication-problems)
7. [Performance Issues](#performance-issues)
8. [Testing Problems](#testing-problems)
9. [Deployment Issues](#deployment-issues)
10. [Getting Help](#getting-help)

## Common Issues

### Quick Diagnostic Commands

Run these commands to diagnose common issues:

```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Check project dependencies
npm list --depth=0

# Clear npm cache
npm cache clean --force

# Check for outdated packages
npm outdated

# Run health check
npm run health-check

# View logs
npm run logs
```

## Installation Problems

### Issue: `npm install` Fails

**Symptoms:**
- Error messages during `npm install`
- Missing dependencies
- Permission errors

**Solutions:**

#### 1. Clear npm cache
```bash
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install
```

#### 2. Use correct Node.js version
```bash
# Check current version
node --version

# Should be 20.x or higher
# Use nvm to switch versions
nvm use 20

# Or install correct version
nvm install 20
nvm use 20
```

#### 3. Fix permission errors (Unix/Mac)
```bash
# Don't use sudo with npm!
# Instead, fix npm permissions:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# Add to ~/.profile or ~/.zshrc:
# export PATH=~/.npm-global/bin:$PATH

# Reload profile
source ~/.profile
```

#### 4. Network/proxy issues
```bash
# Check npm registry
npm config get registry

# Set to default if different
npm config set registry https://registry.npmjs.org/

# For corporate proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080
```

### Issue: Peer Dependency Conflicts

**Symptoms:**
- Warning about peer dependencies
- Incompatible version errors

**Solutions:**

```bash
# Option 1: Use legacy peer deps
npm install --legacy-peer-deps

# Option 2: Force install (use with caution)
npm install --force

# Option 3: Update conflicting packages
npm update package-name
```

### Issue: TypeScript Errors After Install

**Symptoms:**
- TypeScript compilation errors
- Missing type definitions

**Solutions:**

```bash
# Install missing type definitions
npm install -D @types/node @types/react @types/react-dom

# Regenerate tsconfig.json
npx tsc --init

# Check TypeScript version
npm list typescript
```

## Development Server Issues

### Issue: Port Already in Use

**Symptoms:**
- `Error: listen EADDRINUSE: address already in use`
- Server won't start

**Solutions:**

#### 1. Kill process using the port
```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use npx kill-port
npx kill-port 3000
```

#### 2. Use different port
```bash
# Set PORT environment variable
PORT=3001 npm run dev

# Or update .env file
PORT=3001
```

### Issue: Hot Reload Not Working

**Symptoms:**
- Changes not reflected in browser
- Must manually refresh

**Solutions:**

#### 1. Check file watchers
```bash
# Increase file watcher limit (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### 2. Check Vite configuration
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    watch: {
      usePolling: true // Enable for some file systems
    }
  }
});
```

#### 3. Clear browser cache
```bash
# Chrome/Edge: Ctrl+Shift+Delete
# Firefox: Ctrl+Shift+Delete
# Or hard refresh: Ctrl+Shift+R
```

### Issue: Module Not Found

**Symptoms:**
- `Cannot find module` errors
- Import errors

**Solutions:**

#### 1. Check import path
```typescript
// ❌ Wrong
import { Component } from 'components/Component';

// ✅ Correct - Use alias
import { Component } from '@/components/Component';

// ✅ Correct - Relative path
import { Component } from './components/Component';
```

#### 2. Check tsconfig paths
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

#### 3. Restart development server
```bash
# Stop server (Ctrl+C)
# Clear cache and restart
rm -rf node_modules/.vite
npm run dev
```

## Build Problems

### Issue: Build Fails with Memory Error

**Symptoms:**
- `JavaScript heap out of memory`
- Build process crashes

**Solutions:**

```bash
# Increase Node.js memory limit
NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Or add to package.json scripts
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' vite build"
  }
}
```

### Issue: TypeScript Type Errors in Build

**Symptoms:**
- Types work in development
- Errors only during build

**Solutions:**

```bash
# Check types explicitly
npm run type-check

# Clear TypeScript cache
rm -rf tsconfig.tsbuildinfo

# Reinstall types
npm install -D @types/node @types/react

# Check for conflicting versions
npm list @types/react
```

### Issue: Build Size Too Large

**Symptoms:**
- Large bundle sizes
- Slow loading times

**Solutions:**

#### 1. Analyze bundle
```bash
# Install bundle analyzer
npm install -D rollup-plugin-visualizer

# Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({ open: true })
  ]
});
```

#### 2. Code splitting
```typescript
// Use dynamic imports
const Component = lazy(() => import('./Component'));

// Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

#### 3. Optimize dependencies
```typescript
// Import only what you need
import { debounce } from 'lodash-es'; // ✅ Good
import _ from 'lodash'; // ❌ Bad - imports everything
```

## Database Issues

### Issue: Cannot Connect to Database

**Symptoms:**
- Connection timeout errors
- Authentication failures

**Solutions:**

#### 1. Check database is running
```bash
# PostgreSQL
sudo systemctl status postgresql
# Or
pg_isready

# Start if not running
sudo systemctl start postgresql
```

#### 2. Verify connection string
```bash
# Check .env file
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Test connection
psql $DATABASE_URL
```

#### 3. Check firewall/network
```bash
# Test port connectivity
telnet localhost 5432

# Check listening ports
netstat -tuln | grep 5432
```

### Issue: Migration Failures

**Symptoms:**
- `Migration failed` errors
- Database schema out of sync

**Solutions:**

#### 1. Check migration status
```bash
# View migration status
npx prisma migrate status

# View migration history
npx prisma migrate history
```

#### 2. Reset database (development only)
```bash
# ⚠️ WARNING: This deletes all data
npx prisma migrate reset

# Or manually
dropdb mydb
createdb mydb
npx prisma migrate deploy
```

#### 3. Fix failed migration
```bash
# Mark as resolved (if already applied manually)
npx prisma migrate resolve --applied "migration_name"

# Or roll back
npx prisma migrate resolve --rolled-back "migration_name"
```

### Issue: Prisma Client Out of Sync

**Symptoms:**
- Type errors with Prisma client
- `Unknown field` errors

**Solutions:**

```bash
# Regenerate Prisma client
npx prisma generate

# After schema changes
npx prisma db push
npx prisma generate

# Clear node_modules if still issues
rm -rf node_modules/.prisma
npm install
npx prisma generate
```

## Authentication Problems

### Issue: JWT Token Invalid

**Symptoms:**
- `Invalid token` errors
- Unexpected logouts

**Solutions:**

#### 1. Check token expiration
```typescript
// Decode token to check
import jwt from 'jsonwebtoken';

const decoded = jwt.decode(token);
console.log('Expires at:', new Date(decoded.exp * 1000));
```

#### 2. Verify secret key
```bash
# Check .env file
JWT_SECRET=your-secret-key-here

# Ensure same secret in all environments
# Secret must be same length and format
```

#### 3. Check token format
```typescript
// Token should be: "Bearer <token>"
const authHeader = req.headers.authorization;

if (!authHeader || !authHeader.startsWith('Bearer ')) {
  throw new Error('Invalid authorization header');
}

const token = authHeader.substring(7);
```

### Issue: CORS Errors

**Symptoms:**
- `Access to fetch blocked by CORS policy`
- Cross-origin request errors

**Solutions:**

```typescript
// backend/src/app.ts
import cors from 'cors';

// Development
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}));

// Production
app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### Issue: Session/Cookie Problems

**Symptoms:**
- User logged out unexpectedly
- Cookies not being sent

**Solutions:**

#### 1. Check cookie settings
```typescript
res.cookie('token', token, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production', // HTTPS only
  sameSite: 'lax', // or 'strict' or 'none'
  maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
});
```

#### 2. Check domain and path
```typescript
// For subdomains
res.cookie('token', token, {
  domain: '.example.com', // Works for all subdomains
  path: '/'
});
```

## Performance Issues

### Issue: Slow Page Load

**Symptoms:**
- Long initial load times
- High network waterfall

**Solutions:**

#### 1. Check bundle size
```bash
npm run build
# Check dist/ folder size

# Analyze bundle
npm run build -- --analyze
```

#### 2. Implement code splitting
```typescript
// Route-based splitting
const routes = [
  {
    path: '/dashboard',
    component: lazy(() => import('./pages/Dashboard'))
  }
];
```

#### 3. Optimize images
```typescript
// Use appropriate formats
// WebP for photos, SVG for icons
// Lazy load images
<img loading="lazy" src="image.jpg" />
```

### Issue: Slow API Responses

**Symptoms:**
- High response times
- Timeout errors

**Solutions:**

#### 1. Check database queries
```typescript
// Enable query logging
// Prisma
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error']
});

// Look for N+1 queries
// Use includes/select to optimize
const posts = await prisma.post.findMany({
  include: {
    author: true // Instead of separate queries
  }
});
```

#### 2. Add caching
```typescript
import { createClient } from 'redis';

const redis = createClient();

async function getCachedUser(id: string) {
  // Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  // Fetch from database
  const user = await userRepository.findById(id);
  
  // Cache for 5 minutes
  await redis.setEx(`user:${id}`, 300, JSON.stringify(user));
  
  return user;
}
```

#### 3. Add indexes
```sql
-- Check slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
```

### Issue: Memory Leaks

**Symptoms:**
- Increasing memory usage
- Application crashes

**Solutions:**

#### 1. Check for event listeners
```typescript
// ✅ Good - Clean up listeners
useEffect(() => {
  const handler = () => console.log('resize');
  window.addEventListener('resize', handler);
  
  return () => {
    window.removeEventListener('resize', handler);
  };
}, []);

// ❌ Bad - Listener never removed
useEffect(() => {
  window.addEventListener('resize', handler);
}, []);
```

#### 2. Check for timers
```typescript
// ✅ Good - Clear timers
useEffect(() => {
  const timer = setInterval(() => {
    // Do something
  }, 1000);
  
  return () => clearInterval(timer);
}, []);
```

#### 3. Profile memory
```bash
# Node.js
node --inspect index.js
# Open chrome://inspect

# React DevTools
# Use Profiler tab to check re-renders
```

## Testing Problems

### Issue: Tests Failing Randomly

**Symptoms:**
- Tests pass/fail inconsistently
- Different results locally vs CI

**Solutions:**

#### 1. Check for async issues
```typescript
// ✅ Good - Wait for async operations
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// ❌ Bad - Not waiting
expect(screen.getByText('Loaded')).toBeInTheDocument();
```

#### 2. Reset state between tests
```typescript
beforeEach(() => {
  // Clear mocks
  vi.clearAllMocks();
  
  // Reset modules
  vi.resetModules();
  
  // Clear storage
  localStorage.clear();
  sessionStorage.clear();
});
```

#### 3. Check test dependencies
```typescript
// ❌ Bad - Tests depend on each other
let userId;

it('creates user', async () => {
  userId = await createUser();
});

it('updates user', async () => {
  await updateUser(userId); // Depends on previous test
});

// ✅ Good - Independent tests
it('updates user', async () => {
  const userId = await createUser();
  await updateUser(userId);
});
```

### Issue: Mock Not Working

**Symptoms:**
- Real implementation called instead of mock
- Mock functions not tracked

**Solutions:**

```typescript
// ✅ Good - Proper mocking
vi.mock('./userService', () => ({
  getUserById: vi.fn().mockResolvedValue({ id: '123' })
}));

// Check mock was called
expect(getUserById).toHaveBeenCalledWith('123');

// Reset mock between tests
beforeEach(() => {
  vi.clearAllMocks();
});
```

## Deployment Issues

### Issue: Environment Variables Not Working

**Symptoms:**
- `undefined` values in production
- Configuration errors

**Solutions:**

```bash
# Check variables are set
echo $DATABASE_URL

# Set in deployment platform
# Vercel: Project Settings > Environment Variables
# Heroku: heroku config:set KEY=value
# Docker: Use .env file or -e flags

# Check variable names
# Vite requires VITE_ prefix for client-side
VITE_API_URL=https://api.example.com
```

### Issue: Build Works Locally, Fails in CI

**Symptoms:**
- Local build succeeds
- CI build fails

**Solutions:**

#### 1. Match Node.js versions
```yaml
# .github/workflows/deploy.yml
- uses: actions/setup-node@v3
  with:
    node-version: '20' # Match local version
```

#### 2. Check for case-sensitive paths
```typescript
// ❌ Bad - May work on Mac/Windows, fail on Linux
import { Component } from './Component';
// But file is component.tsx

// ✅ Good - Match exact case
import { Component } from './component';
```

#### 3. Check for missing dependencies
```bash
# Run with production deps only
npm ci --only=production
npm run build
```

### Issue: Application Crashes in Production

**Symptoms:**
- Works in development
- Crashes in production

**Solutions:**

#### 1. Check logs
```bash
# View application logs
npm run logs

# Or platform-specific
heroku logs --tail
docker logs container-name
```

#### 2. Enable error tracking
```typescript
// Use error tracking service
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});
```

#### 3. Add health checks
```typescript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});
```

## Getting Help

### Before Asking for Help

1. **Search existing issues** on GitHub
2. **Check documentation** thoroughly
3. **Try the solutions above**
4. **Collect diagnostic information**

### When Asking for Help

Include the following information:

```markdown
**Environment:**
- OS: [e.g., macOS 13.0]
- Node.js version: [run `node --version`]
- npm version: [run `npm --version`]
- Project version: [e.g., 1.2.3]

**Issue Description:**
[Clear description of the problem]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
```
[Full error message with stack trace]
```

**What I've Tried:**
- [List solutions you've attempted]

**Additional Context:**
[Any other relevant information]
```

### Support Channels

- 📧 **Email:** support@example.com
- 💬 **Discord:** [Discord invite link]
- 🐛 **GitHub Issues:** [GitHub issues link]
- 📖 **Documentation:** [Docs link]
- 💡 **Discussions:** [GitHub Discussions link]

### Emergency Issues

For critical production issues:

1. **Email:** emergency@example.com
2. **Include:** "[URGENT]" in subject
3. **Provide:** Full context and error logs
4. **Expected response:** Within 2 hours during business hours

---

*Last Updated: 2024-11-21*
*If you find a solution not listed here, please contribute!*
