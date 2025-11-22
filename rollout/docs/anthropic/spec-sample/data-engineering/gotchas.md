# Common Gotchas and Pitfalls

## Table of Contents
1. [TypeScript Gotchas](#typescript-gotchas)
2. [React Gotchas](#react-gotchas)
3. [Async/Await Gotchas](#asyncawait-gotchas)
4. [Database Gotchas](#database-gotchas)
5. [Authentication Gotchas](#authentication-gotchas)
6. [Testing Gotchas](#testing-gotchas)
7. [Build & Deployment Gotchas](#build--deployment-gotchas)
8. [Performance Gotchas](#performance-gotchas)

## TypeScript Gotchas

### Type Narrowing Issues

```typescript
// ❌ GOTCHA: Type doesn't narrow in callbacks
function processUser(user: User | null) {
  if (user) {
    // user is User here
    setTimeout(() => {
      console.log(user.name); // Still User | null in callback!
    }, 1000);
  }
}

// ✅ FIX: Assign to const
function processUser(user: User | null) {
  if (user) {
    const validUser = user; // Now validUser is User
    setTimeout(() => {
      console.log(validUser.name); // Type is User
    }, 1000);
  }
}
```

### Optional Chaining with Functions

```typescript
// ❌ GOTCHA: Optional chaining doesn't work on function calls
const result = obj?.method(); // TypeScript error if method is optional

// ✅ FIX: Use parentheses
const result = obj?.method?.(); // Correct
```

### Array Type Inference

```typescript
// ❌ GOTCHA: Empty array inferred as never[]
const items = []; // Type: never[]
items.push({ id: 1 }); // Error!

// ✅ FIX: Specify type explicitly
const items: Item[] = [];
items.push({ id: 1 }); // Works!
```

### Non-Null Assertion Pitfall

```typescript
// ❌ GOTCHA: Non-null assertion can hide bugs
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  return user!; // Runtime error if not found!
}

// ✅ FIX: Handle null case
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  if (!user) {
    throw new NotFoundError('User not found');
  }
  return user;
}
```

### Enum Value Confusion

```typescript
enum Status {
  PENDING, // 0
  ACTIVE,  // 1
  INACTIVE // 2
}

// ❌ GOTCHA: Numeric enums accept any number
function setStatus(status: Status) {
  console.log(status);
}

setStatus(999); // No error! But invalid status

// ✅ FIX: Use string enums
enum Status {
  PENDING = 'pending',
  ACTIVE = 'active',
  INACTIVE = 'inactive'
}

setStatus('invalid' as Status); // Still type error
```

## React Gotchas

### Stale Closures in useEffect

```typescript
// ❌ GOTCHA: Stale closure - count is always 0
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      console.log(count); // Always logs 0!
      setCount(count + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []); // Empty dependency array

  return <div>{count}</div>;
}

// ✅ FIX: Use functional update
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1); // Uses current value
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div>{count}</div>;
}
```

### Conditional Hooks

```typescript
// ❌ GOTCHA: Hooks must be called unconditionally
function Component({ shouldFetch }: Props) {
  if (shouldFetch) {
    const data = useQuery(['data'], fetchData); // Error!
  }
}

// ✅ FIX: Use enabled option
function Component({ shouldFetch }: Props) {
  const { data } = useQuery(['data'], fetchData, {
    enabled: shouldFetch
  });
}
```

### useEffect Cleanup Timing

```typescript
// ❌ GOTCHA: Cleanup runs after component unmounts
function Component() {
  useEffect(() => {
    const controller = new AbortController();
    
    fetchData(controller.signal).then(data => {
      setData(data); // Error if component unmounted!
    });

    return () => controller.abort();
  }, []);
}

// ✅ FIX: Check if still mounted
function Component() {
  useEffect(() => {
    let mounted = true;
    const controller = new AbortController();
    
    fetchData(controller.signal).then(data => {
      if (mounted) {
        setData(data);
      }
    });

    return () => {
      mounted = false;
      controller.abort();
    };
  }, []);
}
```

### Key Prop Issues

```typescript
// ❌ GOTCHA: Using index as key
{items.map((item, index) => (
  <Item key={index} data={item} /> // Causes issues when items reorder
))}

// ✅ FIX: Use unique identifier
{items.map(item => (
  <Item key={item.id} data={item} />
))}
```

### State Update Batching

```typescript
// ❌ GOTCHA: Multiple state updates might not batch outside events
setTimeout(() => {
  setCount(count + 1);
  setFlag(true);
  // Two re-renders in React 17
}, 1000);

// ✅ FIX: Use ReactDOM.unstable_batchedUpdates (React 17)
// or upgrade to React 18 where this is automatic
import { unstable_batchedUpdates } from 'react-dom';

setTimeout(() => {
  unstable_batchedUpdates(() => {
    setCount(count + 1);
    setFlag(true);
  });
}, 1000);
```

### Derived State Anti-Pattern

```typescript
// ❌ GOTCHA: Unnecessary state for derived values
function Component({ items }: Props) {
  const [items, setItems] = useState(props.items);
  const [count, setCount] = useState(items.length);

  useEffect(() => {
    setCount(items.length); // Unnecessary!
  }, [items]);
}

// ✅ FIX: Calculate during render
function Component({ items }: Props) {
  const count = items.length; // Simple!
}
```

## Async/Await Gotchas

### Unhandled Promise Rejections

```typescript
// ❌ GOTCHA: Silent failures
async function fetchData() {
  const response = await fetch('/api/data');
  return response.json();
}

// If fetch fails, error is lost!
fetchData();

// ✅ FIX: Always handle errors
fetchData().catch(error => {
  console.error('Failed to fetch data:', error);
});

// ✅ BETTER: Use try-catch
async function fetchDataSafe() {
  try {
    const response = await fetch('/api/data');
    return response.json();
  } catch (error) {
    logger.error('Fetch failed', error);
    throw error;
  }
}
```

### Async forEach Doesn't Work

```typescript
// ❌ GOTCHA: forEach doesn't wait for async
async function processItems(items: Item[]) {
  items.forEach(async (item) => {
    await processItem(item); // Doesn't wait!
  });
  console.log('Done'); // Logs immediately!
}

// ✅ FIX: Use for...of
async function processItems(items: Item[]) {
  for (const item of items) {
    await processItem(item);
  }
  console.log('Done'); // Logs after all items
}

// ✅ OR: Process in parallel
async function processItems(items: Item[]) {
  await Promise.all(items.map(item => processItem(item)));
  console.log('Done');
}
```

### Promise Constructor Anti-Pattern

```typescript
// ❌ GOTCHA: Wrapping promises unnecessarily
async function getUser(id: string) {
  return new Promise(async (resolve, reject) => {
    try {
      const user = await userRepository.findById(id);
      resolve(user);
    } catch (error) {
      reject(error);
    }
  });
}

// ✅ FIX: Just return the promise
async function getUser(id: string) {
  return userRepository.findById(id);
}
```

### Race Conditions

```typescript
// ❌ GOTCHA: Last request might not be last to complete
function SearchInput() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query) return;
    
    // If user types fast, multiple requests in flight
    fetchResults(query).then(data => {
      setResults(data); // Wrong results if not latest query!
    });
  }, [query]);
}

// ✅ FIX: Use cleanup to cancel stale requests
function SearchInput() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query) return;
    
    let cancelled = false;
    const controller = new AbortController();

    fetchResults(query, controller.signal).then(data => {
      if (!cancelled) {
        setResults(data);
      }
    });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [query]);
}
```

## Database Gotchas

### N+1 Query Problem

```typescript
// ❌ GOTCHA: N+1 queries
async function getPosts() {
  const posts = await prisma.post.findMany();
  
  // This runs a separate query for EACH post!
  for (const post of posts) {
    post.author = await prisma.user.findUnique({
      where: { id: post.authorId }
    });
  }
  
  return posts;
}

// ✅ FIX: Use include or eager loading
async function getPosts() {
  return prisma.post.findMany({
    include: {
      author: true // Single query with join
    }
  });
}
```

### Transaction Gotchas

```typescript
// ❌ GOTCHA: Not using transactions for related operations
async function transferFunds(fromId: string, toId: string, amount: number) {
  await accountRepo.withdraw(fromId, amount);
  // If this fails, money disappears!
  await accountRepo.deposit(toId, amount);
}

// ✅ FIX: Use transactions
async function transferFunds(fromId: string, toId: string, amount: number) {
  await prisma.$transaction(async (tx) => {
    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    });
    
    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    });
  });
}
```

### Connection Pool Exhaustion

```typescript
// ❌ GOTCHA: Creating new client for each request
app.get('/api/users', async (req, res) => {
  const prisma = new PrismaClient(); // New connection!
  const users = await prisma.user.findMany();
  res.json(users);
});

// ✅ FIX: Reuse single client instance
const prisma = new PrismaClient();

app.get('/api/users', async (req, res) => {
  const users = await prisma.user.findMany();
  res.json(users);
});
```

### Case-Sensitive Searches

```typescript
// ❌ GOTCHA: Case-sensitive search by default
const users = await prisma.user.findMany({
  where: {
    email: 'USER@EXAMPLE.COM' // Won't match 'user@example.com'
  }
});

// ✅ FIX: Use case-insensitive mode
const users = await prisma.user.findMany({
  where: {
    email: {
      equals: 'USER@EXAMPLE.COM',
      mode: 'insensitive'
    }
  }
});
```

## Authentication Gotchas

### JWT Secret in Code

```typescript
// ❌ GOTCHA: Hardcoded secrets
const token = jwt.sign(payload, 'my-secret-key');

// ✅ FIX: Use environment variables
const token = jwt.sign(payload, process.env.JWT_SECRET!);
```

### Token Expiration Not Checked

```typescript
// ❌ GOTCHA: Decoding without verification
const payload = jwt.decode(token); // No verification!
req.user = payload;

// ✅ FIX: Always verify
try {
  const payload = jwt.verify(token, process.env.JWT_SECRET!);
  req.user = payload;
} catch (error) {
  throw new UnauthorizedError('Invalid token');
}
```

### Password Comparison Timing Attack

```typescript
// ❌ GOTCHA: String comparison is not constant-time
if (password === storedPassword) {
  // Vulnerable to timing attacks
}

// ✅ FIX: Use bcrypt compare
const isValid = await bcrypt.compare(password, hashedPassword);
```

### Session Fixation

```typescript
// ❌ GOTCHA: Not regenerating session after login
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  req.session.userId = user.id; // Session ID stays same!
  res.json({ success: true });
});

// ✅ FIX: Regenerate session
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  req.session.regenerate((err) => {
    req.session.userId = user.id;
    res.json({ success: true });
  });
});
```

## Testing Gotchas

### Shared Test State

```typescript
// ❌ GOTCHA: Tests affecting each other
let testUser;

beforeAll(async () => {
  testUser = await createUser({ email: 'test@example.com' });
});

it('updates user', async () => {
  await updateUser(testUser.id, { name: 'New Name' });
});

it('gets user', async () => {
  const user = await getUser(testUser.id);
  expect(user.name).toBe('Test User'); // Fails! Name was changed
});

// ✅ FIX: Create fresh data for each test
it('updates user', async () => {
  const user = await createUser({ email: 'test@example.com' });
  await updateUser(user.id, { name: 'New Name' });
  // Test assertions
});
```

### Fake Timers Not Restored

```typescript
// ❌ GOTCHA: Fake timers affect other tests
it('waits for timeout', () => {
  vi.useFakeTimers();
  // Test code
  // Forgot to restore!
});

it('another test', async () => {
  await waitFor(() => {
    // Never resolves! Timers are still fake
  });
});

// ✅ FIX: Always restore
it('waits for timeout', () => {
  vi.useFakeTimers();
  try {
    // Test code
  } finally {
    vi.useRealTimers();
  }
});

// ✅ BETTER: Use afterEach
afterEach(() => {
  vi.useRealTimers();
});
```

### Not Waiting for Async

```typescript
// ❌ GOTCHA: Test completes before async operation
it('loads data', () => {
  render(<DataComponent />);
  
  // Test finishes before data loads!
  expect(screen.getByText('Data loaded')).toBeInTheDocument();
});

// ✅ FIX: Wait for async operations
it('loads data', async () => {
  render(<DataComponent />);
  
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});
```

### Mocks Persist Between Tests

```typescript
// ❌ GOTCHA: Mock state persists
it('test 1', () => {
  vi.spyOn(api, 'fetchData').mockResolvedValue({ id: 1 });
  // Test code
});

it('test 2', () => {
  // api.fetchData still mocked!
});

// ✅ FIX: Clear mocks in beforeEach
beforeEach(() => {
  vi.clearAllMocks();
  // or vi.restoreAllMocks();
});
```

## Build & Deployment Gotchas

### Environment Variables in Client

```typescript
// ❌ GOTCHA: Backend env vars not available in client
// .env
DATABASE_URL=postgresql://...

// client/src/config.ts
const dbUrl = process.env.DATABASE_URL; // undefined in browser!

// ✅ FIX: Use VITE_ prefix for client vars
// .env
VITE_API_URL=https://api.example.com

// client/src/config.ts
const apiUrl = import.meta.env.VITE_API_URL; // Available!
```

### Path Case Sensitivity

```typescript
// ❌ GOTCHA: Works on Mac/Windows, fails on Linux
import { Component } from './Component'; // File is actually component.tsx

// ✅ FIX: Match exact case
import { Component } from './component';
```

### Missing Production Dependencies

```typescript
// ❌ GOTCHA: Package in devDependencies but used in production
{
  "devDependencies": {
    "express": "^4.18.0" // Should be in dependencies!
  }
}

// ✅ FIX: Check which dependencies are needed at runtime
{
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

### Build Output Not Gitignored

```bash
# ❌ GOTCHA: Committing build artifacts
git add dist/
git commit -m "Add build files"

# ✅ FIX: Add to .gitignore
echo "dist/" >> .gitignore
echo "build/" >> .gitignore
echo ".next/" >> .gitignore
```

## Performance Gotchas

### Expensive Calculations in Render

```typescript
// ❌ GOTCHA: Recalculating on every render
function Component({ items }: Props) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  // This runs on EVERY render, even if items haven't changed!
  
  return <div>Total: {total}</div>;
}

// ✅ FIX: Use useMemo
function Component({ items }: Props) {
  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price, 0),
    [items]
  );
  
  return <div>Total: {total}</div>;
}
```

### Creating Functions in Render

```typescript
// ❌ GOTCHA: New function on every render
function Parent() {
  return (
    <Child onUpdate={(data) => {
      // New function every render! Child re-renders unnecessarily
      console.log(data);
    }} />
  );
}

// ✅ FIX: Use useCallback
function Parent() {
  const handleUpdate = useCallback((data) => {
    console.log(data);
  }, []);
  
  return <Child onUpdate={handleUpdate} />;
}
```

### Not Using Pagination

```typescript
// ❌ GOTCHA: Loading all data at once
async function getUsers() {
  return prisma.user.findMany(); // Could be millions!
}

// ✅ FIX: Implement pagination
async function getUsers(page: number = 1, limit: number = 20) {
  return prisma.user.findMany({
    skip: (page - 1) * limit,
    take: limit
  });
}
```

### Memory Leaks from Event Listeners

```typescript
// ❌ GOTCHA: Event listener never removed
useEffect(() => {
  window.addEventListener('resize', handleResize);
  // Memory leak!
}, []);

// ✅ FIX: Clean up in useEffect return
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

### Large Bundle Size

```typescript
// ❌ GOTCHA: Importing entire libraries
import _ from 'lodash'; // Imports everything!
import * as dateFns from 'date-fns'; // Imports everything!

// ✅ FIX: Import only what you need
import { debounce } from 'lodash-es';
import { format } from 'date-fns';
```

---

## Quick Reference: Common Mistakes

| Area | Gotcha | Fix |
|------|--------|-----|
| React | Stale closures in useEffect | Use functional updates |
| Async | forEach with async | Use for...of or Promise.all |
| TypeScript | Empty array type | Specify type explicitly |
| Database | N+1 queries | Use include/joins |
| Auth | Hardcoded secrets | Use environment variables |
| Testing | Shared state | Create fresh data per test |
| Build | Wrong dependencies section | Check runtime vs dev needs |
| Performance | Calculations in render | Use useMemo |

---

*Last Updated: 2024-11-21*
*Learn from these mistakes so you don't repeat them!*
