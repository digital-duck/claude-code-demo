# Performance Optimization Guide

## Table of Contents
1. [Frontend Performance](#frontend-performance)
2. [Backend Performance](#backend-performance)
3. [Database Performance](#database-performance)
4. [Caching Strategies](#caching-strategies)
5. [Network Optimization](#network-optimization)
6. [React Performance](#react-performance)
7. [Bundle Optimization](#bundle-optimization)
8. [Monitoring & Profiling](#monitoring--profiling)

## Frontend Performance

### Code Splitting

Split your bundle to reduce initial load time.

```typescript
// ✅ Route-based code splitting
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

### Component-Level Code Splitting

```typescript
// ✅ Split heavy components
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <HeavyChart data={data} />
        </Suspense>
      )}
    </div>
  );
}
```

### Image Optimization

```typescript
// ✅ Lazy load images
<img 
  src="image.jpg" 
  loading="lazy" 
  alt="Description"
  width="800"
  height="600"
/>

// ✅ Use appropriate formats
// - WebP for photos (smaller size)
// - SVG for icons and logos
// - PNG for images with transparency

// ✅ Responsive images
<picture>
  <source 
    media="(min-width: 800px)" 
    srcSet="large.webp" 
    type="image/webp" 
  />
  <source 
    media="(min-width: 400px)" 
    srcSet="medium.webp" 
    type="image/webp" 
  />
  <img src="small.jpg" alt="Description" />
</picture>

// ✅ Use next/image or similar optimized components
import Image from 'next/image';

<Image
  src="/photo.jpg"
  width={800}
  height={600}
  alt="Description"
  loading="lazy"
  placeholder="blur"
/>
```

### Virtual Scrolling for Large Lists

```typescript
// ✅ Use react-window for large lists
import { FixedSizeList } from 'react-window';

function LargeList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: CSSProperties }) => (
    <div style={style}>
      <ItemCard item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Debounce & Throttle

```typescript
// ✅ Debounce search input
import { useMemo } from 'react';
import { debounce } from 'lodash-es';

function SearchInput() {
  const [query, setQuery] = useState('');

  const debouncedSearch = useMemo(
    () => debounce((value: string) => {
      // Perform search
      performSearch(value);
    }, 300),
    []
  );

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return <input value={query} onChange={handleChange} />;
}

// ✅ Throttle scroll handler
const throttledScroll = useMemo(
  () => throttle(() => {
    // Handle scroll
    handleScroll();
  }, 100),
  []
);

useEffect(() => {
  window.addEventListener('scroll', throttledScroll);
  return () => window.removeEventListener('scroll', throttledScroll);
}, [throttledScroll]);
```

### Web Workers for Heavy Computation

```typescript
// worker.ts
self.onmessage = (e: MessageEvent) => {
  const { data } = e;
  
  // Heavy computation
  const result = processLargeDataset(data);
  
  self.postMessage(result);
};

// Component
function DataProcessor() {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const worker = new Worker(new URL('./worker.ts', import.meta.url));

    worker.postMessage(largeDataset);

    worker.onmessage = (e: MessageEvent) => {
      setResult(e.data);
      worker.terminate();
    };

    return () => worker.terminate();
  }, []);

  return <div>{result}</div>;
}
```

## Backend Performance

### Response Compression

```typescript
import compression from 'compression';

// ✅ Enable gzip compression
app.use(compression({
  level: 6, // Compression level (0-9)
  threshold: 1024, // Only compress responses > 1KB
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  }
}));
```

### Connection Pooling

```typescript
// ✅ Database connection pooling
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  // Connection pool settings
  pool: {
    min: 2,
    max: 10,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000,
  },
});

// ✅ Redis connection pooling
import { createClient } from 'redis';

const redis = createClient({
  url: process.env.REDIS_URL,
  socket: {
    connectTimeout: 5000,
    keepAlive: 5000,
  },
});
```

### Async Operations

```typescript
// ✅ Process tasks asynchronously
import { Queue } from 'bull';

const emailQueue = new Queue('emails', process.env.REDIS_URL);

// Process emails in background
emailQueue.process(async (job) => {
  await sendEmail(job.data);
});

// Add job to queue (returns immediately)
app.post('/api/users', async (req, res) => {
  const user = await createUser(req.body);
  
  // Don't wait for email
  await emailQueue.add('welcome', { userId: user.id });
  
  res.json(user);
});
```

### Batch Operations

```typescript
// ❌ Bad: Multiple individual queries
async function updateUsers(updates: UserUpdate[]) {
  for (const update of updates) {
    await prisma.user.update({
      where: { id: update.id },
      data: update.data
    });
  }
}

// ✅ Good: Batch update
async function updateUsers(updates: UserUpdate[]) {
  await prisma.$transaction(
    updates.map(update =>
      prisma.user.update({
        where: { id: update.id },
        data: update.data
      })
    )
  );
}
```

### Streaming Large Responses

```typescript
// ✅ Stream large files
app.get('/api/export', async (req, res) => {
  const stream = await generateLargeCSV();
  
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename="data.csv"');
  
  stream.pipe(res);
});

// ✅ Stream database results
app.get('/api/users/export', async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.write('[');
  
  let first = true;
  const cursor = prisma.user.findMany({
    take: 100,
    orderBy: { id: 'asc' }
  });

  for await (const user of cursor) {
    if (!first) res.write(',');
    res.write(JSON.stringify(user));
    first = false;
  }
  
  res.write(']');
  res.end();
});
```

## Database Performance

### Indexing

```sql
-- ✅ Index frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- ✅ Composite indexes for multi-column queries
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);

-- ✅ Partial indexes for filtered queries
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Check index usage
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

### Query Optimization

```typescript
// ❌ Bad: Select all columns
const users = await prisma.user.findMany();

// ✅ Good: Select only needed columns
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true
  }
});

// ❌ Bad: N+1 query
const posts = await prisma.post.findMany();
for (const post of posts) {
  post.author = await prisma.user.findUnique({
    where: { id: post.authorId }
  });
}

// ✅ Good: Join in single query
const posts = await prisma.post.findMany({
  include: {
    author: {
      select: {
        id: true,
        name: true
      }
    }
  }
});

// ✅ Good: Use raw SQL for complex queries
const result = await prisma.$queryRaw`
  SELECT p.*, u.name as author_name
  FROM posts p
  JOIN users u ON p.author_id = u.id
  WHERE p.status = 'published'
  ORDER BY p.created_at DESC
  LIMIT 20
`;
```

### Connection Management

```typescript
// ✅ Reuse Prisma client instance
// db.ts
export const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'error', 'warn'] 
    : ['error'],
});

// Graceful shutdown
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});

// ✅ Use read replicas for read-heavy workloads
const readPrisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_READ_REPLICA_URL,
    },
  },
});

// Read from replica
const users = await readPrisma.user.findMany();

// Write to primary
const user = await prisma.user.create({ data });
```

### Pagination

```typescript
// ✅ Cursor-based pagination (efficient for large datasets)
async function getUsersPaginated(cursor?: string, limit: number = 20) {
  return prisma.user.findMany({
    take: limit,
    ...(cursor && {
      skip: 1, // Skip the cursor
      cursor: { id: cursor }
    }),
    orderBy: { id: 'asc' }
  });
}

// ✅ Offset pagination (simpler but slower)
async function getUsersPaginated(page: number = 1, limit: number = 20) {
  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip: (page - 1) * limit,
      take: limit
    }),
    prisma.user.count()
  ]);

  return {
    users,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  };
}
```

## Caching Strategies

### Multi-Level Caching

```typescript
class CacheService {
  constructor(
    private redis: RedisClient,
    private memoryCache: Map<string, CacheEntry>
  ) {}

  async get<T>(key: string): Promise<T | null> {
    // Level 1: Memory cache (fastest)
    const memoryEntry = this.memoryCache.get(key);
    if (memoryEntry && Date.now() < memoryEntry.expiry) {
      return memoryEntry.data as T;
    }

    // Level 2: Redis cache
    const cached = await this.redis.get(key);
    if (cached) {
      const data = JSON.parse(cached);
      
      // Store in memory cache
      this.memoryCache.set(key, {
        data,
        expiry: Date.now() + 60000 // 1 minute
      });
      
      return data as T;
    }

    return null;
  }

  async set<T>(key: string, value: T, ttl: number = 300): Promise<void> {
    const serialized = JSON.stringify(value);
    
    // Store in Redis
    await this.redis.setEx(key, ttl, serialized);
    
    // Store in memory
    this.memoryCache.set(key, {
      data: value,
      expiry: Date.now() + Math.min(ttl * 1000, 60000)
    });
  }

  async invalidate(pattern: string): Promise<void> {
    // Clear from Redis
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(keys);
    }

    // Clear from memory
    for (const key of this.memoryCache.keys()) {
      if (key.match(pattern)) {
        this.memoryCache.delete(key);
      }
    }
  }
}
```

### Cache-Aside Pattern

```typescript
async function getUser(id: string): Promise<User> {
  const cacheKey = `user:${id}`;
  
  // Try cache first
  const cached = await cacheService.get<User>(cacheKey);
  if (cached) {
    return cached;
  }
  
  // Cache miss - fetch from database
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) {
    throw new NotFoundError('User not found');
  }
  
  // Store in cache
  await cacheService.set(cacheKey, user, 300);
  
  return user;
}
```

### Write-Through Cache

```typescript
async function updateUser(id: string, data: UpdateUserDTO): Promise<User> {
  // Update database
  const user = await prisma.user.update({
    where: { id },
    data
  });
  
  // Update cache immediately
  await cacheService.set(`user:${id}`, user, 300);
  
  // Invalidate related caches
  await cacheService.invalidate(`user:${id}:*`);
  
  return user;
}
```

### HTTP Caching Headers

```typescript
// ✅ Set appropriate cache headers
app.get('/api/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  
  // Cache for 5 minutes
  res.set({
    'Cache-Control': 'public, max-age=300',
    'ETag': generateETag(user),
    'Last-Modified': user.updatedAt.toUTCString()
  });
  
  // Check if client has fresh cache
  if (req.headers['if-none-match'] === generateETag(user)) {
    return res.status(304).end();
  }
  
  res.json(user);
});

// Static assets - cache for 1 year
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true
}));
```

## Network Optimization

### Request Batching

```typescript
// ✅ Batch multiple API calls
class DataLoader {
  private queue: Map<string, Promise<any>> = new Map();
  private timer: NodeJS.Timeout | null = null;

  load(id: string): Promise<any> {
    if (this.queue.has(id)) {
      return this.queue.get(id)!;
    }

    const promise = new Promise((resolve, reject) => {
      this.queue.set(id, promise);

      if (!this.timer) {
        this.timer = setTimeout(() => this.flush(), 10);
      }
    });

    return promise;
  }

  private async flush() {
    const ids = Array.from(this.queue.keys());
    this.timer = null;

    // Batch load all IDs
    const results = await fetchMultiple(ids);

    // Resolve all promises
    results.forEach((result, index) => {
      const id = ids[index];
      const promise = this.queue.get(id);
      // Resolve promise with result
    });

    this.queue.clear();
  }
}
```

### GraphQL DataLoader

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await prisma.user.findMany({
    where: { id: { in: ids } }
  });
  
  // Return in same order as requested
  return ids.map(id => users.find(u => u.id === id));
});

// Usage
const user1 = await userLoader.load('id1');
const user2 = await userLoader.load('id2');
// Only one database query!
```

### Request Deduplication

```typescript
// ✅ Deduplicate identical requests
class RequestCache {
  private pending = new Map<string, Promise<any>>();

  async fetch<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    // Return existing promise if already fetching
    if (this.pending.has(key)) {
      return this.pending.get(key)!;
    }

    // Create new promise
    const promise = fetcher().finally(() => {
      this.pending.delete(key);
    });

    this.pending.set(key, promise);
    return promise;
  }
}

const requestCache = new RequestCache();

// Multiple calls return same promise
const data1 = requestCache.fetch('users', () => fetchUsers());
const data2 = requestCache.fetch('users', () => fetchUsers());
// Only one API call!
```

## React Performance

### Memoization

```typescript
// ✅ Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// ✅ Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// ✅ Memoize components
const MemoizedComponent = memo(function Component({ data }: Props) {
  return <div>{data}</div>;
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.data.id === nextProps.data.id;
});
```

### Code Organization for Performance

```typescript
// ❌ Bad: Heavy component re-renders everything
function Dashboard() {
  const [filter, setFilter] = useState('all');
  const data = useExpensiveData();
  
  return (
    <div>
      <FilterButtons value={filter} onChange={setFilter} />
      <HeavyChart data={data} />
      <DataTable data={data} />
    </div>
  );
}

// ✅ Good: Split into smaller components
function Dashboard() {
  return (
    <div>
      <Filters />
      <DataDisplay />
    </div>
  );
}

function Filters() {
  const [filter, setFilter] = useState('all');
  return <FilterButtons value={filter} onChange={setFilter} />;
}

function DataDisplay() {
  const data = useExpensiveData();
  return (
    <>
      <HeavyChart data={data} />
      <DataTable data={data} />
    </>
  );
}
```

### Lazy State Initialization

```typescript
// ❌ Bad: Runs on every render
function Component() {
  const [state, setState] = useState(expensiveComputation());
}

// ✅ Good: Only runs once
function Component() {
  const [state, setState] = useState(() => expensiveComputation());
}
```

## Bundle Optimization

### Analyze Bundle Size

```bash
# Vite
npm run build
npx vite-bundle-visualizer

# Webpack
npm install -D webpack-bundle-analyzer
```

### Tree Shaking

```typescript
// ✅ Use ES6 imports (tree-shakeable)
import { debounce } from 'lodash-es';

// ❌ Avoid CommonJS (not tree-shakeable)
const _ = require('lodash');
```

### Dynamic Imports

```typescript
// ✅ Load only when needed
async function showModal() {
  const { Modal } = await import('./Modal');
  return <Modal />;
}
```

## Monitoring & Profiling

### Performance Monitoring

```typescript
// ✅ Track Core Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### API Response Time Monitoring

```typescript
// ✅ Measure response times
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    logger.info('Request completed', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration
    });
    
    // Alert if slow
    if (duration > 1000) {
      logger.warn('Slow request detected', { url: req.url, duration });
    }
  });
  
  next();
});
```

### React DevTools Profiler

```typescript
// ✅ Wrap app in Profiler
import { Profiler } from 'react';

function App() {
  return (
    <Profiler
      id="App"
      onRender={(id, phase, actualDuration) => {
        console.log(`${id} took ${actualDuration}ms to render`);
      }}
    >
      <Router>
        {/* App content */}
      </Router>
    </Profiler>
  );
}
```

---

## Performance Checklist

### Frontend
- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] Components memoized appropriately
- [ ] Virtual scrolling for large lists
- [ ] Bundle size analyzed and optimized
- [ ] Service worker for offline support

### Backend
- [ ] Database queries optimized
- [ ] Proper indexes created
- [ ] Caching implemented
- [ ] Connection pooling configured
- [ ] Response compression enabled
- [ ] Async operations for slow tasks

### Database
- [ ] Indexes on frequently queried columns
- [ ] N+1 queries eliminated
- [ ] Query execution plans reviewed
- [ ] Connection pool sized appropriately
- [ ] Read replicas for read-heavy loads

### Monitoring
- [ ] Performance metrics tracked
- [ ] Slow query logging enabled
- [ ] Error tracking configured
- [ ] Core Web Vitals monitored
- [ ] API response times logged

---

*Last Updated: 2024-11-21*
*Performance is a feature, not an afterthought*
