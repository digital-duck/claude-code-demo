# Project Patterns

## Table of Contents
1. [Design Patterns](#design-patterns)
2. [Code Organization Patterns](#code-organization-patterns)
3. [React Patterns](#react-patterns)
4. [API Patterns](#api-patterns)
5. [Error Handling Patterns](#error-handling-patterns)
6. [State Management Patterns](#state-management-patterns)
7. [Testing Patterns](#testing-patterns)

## Design Patterns

### Repository Pattern

We use the repository pattern to abstract data access logic.

```typescript
// src/repositories/base.repository.ts
export abstract class BaseRepository<T> {
  constructor(protected db: PrismaClient) {}

  abstract findById(id: string): Promise<T | null>;
  abstract findAll(options?: QueryOptions): Promise<T[]>;
  abstract create(data: Partial<T>): Promise<T>;
  abstract update(id: string, data: Partial<T>): Promise<T>;
  abstract delete(id: string): Promise<void>;
}

// src/repositories/user.repository.ts
export class UserRepository extends BaseRepository<User> {
  async findById(id: string): Promise<User | null> {
    return this.db.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.db.user.findUnique({ where: { email } });
  }

  async findAll(options: QueryOptions = {}): Promise<User[]> {
    return this.db.user.findMany({
      skip: options.offset,
      take: options.limit,
      orderBy: options.orderBy
    });
  }

  async create(data: CreateUserDTO): Promise<User> {
    return this.db.user.create({ data });
  }

  async update(id: string, data: UpdateUserDTO): Promise<User> {
    return this.db.user.update({
      where: { id },
      data
    });
  }

  async delete(id: string): Promise<void> {
    await this.db.user.delete({ where: { id } });
  }
}
```

### Service Layer Pattern

Business logic lives in service classes, separated from controllers.

```typescript
// src/services/user.service.ts
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService,
    private cacheService: CacheService
  ) {}

  async createUser(data: CreateUserDTO): Promise<User> {
    // Validation
    await this.validateUserData(data);
    
    // Check duplicates
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('Email already exists');
    }
    
    // Hash password
    const passwordHash = await hashPassword(data.password);
    
    // Create user
    const user = await this.userRepository.create({
      ...data,
      passwordHash
    });
    
    // Side effects
    await this.emailService.sendWelcomeEmail(user);
    await this.cacheService.invalidate(`user:${user.id}`);
    
    return user;
  }

  async getUserById(id: string): Promise<User> {
    // Check cache
    const cached = await this.cacheService.get<User>(`user:${id}`);
    if (cached) return cached;
    
    // Fetch from database
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundError('User not found');
    }
    
    // Cache result
    await this.cacheService.set(`user:${id}`, user, 300);
    
    return user;
  }

  private async validateUserData(data: CreateUserDTO): Promise<void> {
    // Implement validation logic
  }
}
```

### Factory Pattern

Use factories for complex object creation.

```typescript
// src/factories/service.factory.ts
export class ServiceFactory {
  private static instances = new Map<string, any>();

  static getUserService(): UserService {
    if (!this.instances.has('UserService')) {
      const db = new PrismaClient();
      const userRepo = new UserRepository(db);
      const emailService = new EmailService();
      const cacheService = new CacheService();
      
      this.instances.set(
        'UserService',
        new UserService(userRepo, emailService, cacheService)
      );
    }
    
    return this.instances.get('UserService');
  }

  static getAuthService(): AuthService {
    if (!this.instances.has('AuthService')) {
      const userService = this.getUserService();
      const tokenService = new TokenService();
      
      this.instances.set(
        'AuthService',
        new AuthService(userService, tokenService)
      );
    }
    
    return this.instances.get('AuthService');
  }
}
```

### Strategy Pattern

Use strategies for interchangeable algorithms.

```typescript
// src/strategies/payment/payment.strategy.ts
export interface PaymentStrategy {
  processPayment(amount: number, data: PaymentData): Promise<PaymentResult>;
}

// src/strategies/payment/credit-card.strategy.ts
export class CreditCardStrategy implements PaymentStrategy {
  async processPayment(amount: number, data: CreditCardData): Promise<PaymentResult> {
    // Process credit card payment
    return {
      success: true,
      transactionId: 'cc-123',
      amount
    };
  }
}

// src/strategies/payment/paypal.strategy.ts
export class PayPalStrategy implements PaymentStrategy {
  async processPayment(amount: number, data: PayPalData): Promise<PaymentResult> {
    // Process PayPal payment
    return {
      success: true,
      transactionId: 'pp-456',
      amount
    };
  }
}

// src/services/payment.service.ts
export class PaymentService {
  private strategies = new Map<PaymentMethod, PaymentStrategy>();

  constructor() {
    this.strategies.set(PaymentMethod.CREDIT_CARD, new CreditCardStrategy());
    this.strategies.set(PaymentMethod.PAYPAL, new PayPalStrategy());
  }

  async processPayment(
    method: PaymentMethod,
    amount: number,
    data: PaymentData
  ): Promise<PaymentResult> {
    const strategy = this.strategies.get(method);
    if (!strategy) {
      throw new Error('Unsupported payment method');
    }
    
    return strategy.processPayment(amount, data);
  }
}
```

### Decorator Pattern

Use decorators for cross-cutting concerns.

```typescript
// src/decorators/cache.decorator.ts
export function Cache(ttl: number = 300) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const cache = new Map<string, { data: any; expiry: number }>();

    descriptor.value = async function (...args: any[]) {
      const key = JSON.stringify(args);
      const cached = cache.get(key);

      if (cached && Date.now() < cached.expiry) {
        return cached.data;
      }

      const result = await originalMethod.apply(this, args);
      cache.set(key, {
        data: result,
        expiry: Date.now() + ttl * 1000
      });

      return result;
    };

    return descriptor;
  };
}

// Usage
export class UserService {
  @Cache(300)
  async getUserById(id: string): Promise<User> {
    return this.userRepository.findById(id);
  }
}
```

## Code Organization Patterns

### Feature-Based Structure

Organize code by feature, not by type.

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── auth.service.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts
│   ├── users/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   └── posts/
└── shared/
    ├── components/
    ├── hooks/
    └── utils/
```

### Barrel Exports

Use index files for clean imports.

```typescript
// src/features/auth/index.ts
export { LoginForm } from './components/LoginForm';
export { RegisterForm } from './components/RegisterForm';
export { useAuth } from './hooks/useAuth';
export type { AuthState, LoginCredentials } from './types/auth.types';

// Usage in other files
import { LoginForm, useAuth, type AuthState } from '@/features/auth';
```

### Dependency Injection

Use constructor injection for dependencies.

```typescript
// ✅ Good - Dependency injection
export class OrderService {
  constructor(
    private orderRepository: OrderRepository,
    private paymentService: PaymentService,
    private emailService: EmailService
  ) {}

  async createOrder(data: CreateOrderDTO): Promise<Order> {
    const order = await this.orderRepository.create(data);
    await this.paymentService.processPayment(order);
    await this.emailService.sendOrderConfirmation(order);
    return order;
  }
}

// ❌ Bad - Hard dependencies
export class OrderService {
  async createOrder(data: CreateOrderDTO): Promise<Order> {
    const orderRepo = new OrderRepository();
    const paymentService = new PaymentService();
    const emailService = new EmailService();
    // ...
  }
}
```

## React Patterns

### Custom Hooks Pattern

Extract reusable logic into custom hooks.

```typescript
// src/hooks/useAsync.ts
export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  dependencies: any[] = []
) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({
    data: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      setState({ data: null, loading: true, error: null });

      try {
        const data = await asyncFunction();
        if (!cancelled) {
          setState({ data, loading: false, error: null });
        }
      } catch (error) {
        if (!cancelled) {
          setState({ data: null, loading: false, error: error as Error });
        }
      }
    }

    loadData();

    return () => {
      cancelled = true;
    };
  }, dependencies);

  return state;
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useAsync(
    () => fetchUser(userId),
    [userId]
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <div>{user.name}</div>;
}
```

### Compound Components Pattern

Create components that work together.

```typescript
// src/components/Tabs/Tabs.tsx
interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | undefined>(undefined);

export function Tabs({ children, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

export function TabList({ children }: TabListProps) {
  return <div className="tab-list">{children}</div>;
}

export function Tab({ id, children }: TabProps) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  const { activeTab, setActiveTab } = context;

  return (
    <button
      className={activeTab === id ? 'active' : ''}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

export function TabPanel({ id, children }: TabPanelProps) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  const { activeTab } = context;

  if (activeTab !== id) return null;

  return <div className="tab-panel">{children}</div>;
}

// Usage
<Tabs defaultTab="profile">
  <TabList>
    <Tab id="profile">Profile</Tab>
    <Tab id="settings">Settings</Tab>
  </TabList>
  <TabPanel id="profile">
    <ProfileContent />
  </TabPanel>
  <TabPanel id="settings">
    <SettingsContent />
  </TabPanel>
</Tabs>
```

### Render Props Pattern

Share code using render props.

```typescript
// src/components/DataFetcher.tsx
interface DataFetcherProps<T> {
  url: string;
  children: (data: {
    data: T | null;
    loading: boolean;
    error: Error | null;
  }) => ReactNode;
}

export function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const { data, loading, error } = useAsync<T>(() => fetch(url).then(r => r.json()));

  return <>{children({ data, loading, error })}</>;
}

// Usage
<DataFetcher<User> url="/api/users/123">
  {({ data, loading, error }) => {
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage error={error} />;
    if (!data) return <NotFound />;
    return <UserProfile user={data} />;
  }}
</DataFetcher>
```

### Higher-Order Component Pattern

Wrap components with additional functionality.

```typescript
// src/hoc/withAuth.tsx
export function withAuth<P extends object>(
  Component: ComponentType<P>
) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth();

    if (loading) {
      return <LoadingSpinner />;
    }

    if (!user) {
      return <Navigate to="/login" />;
    }

    return <Component {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

## API Patterns

### Request/Response Wrapper

Consistent API response structure.

```typescript
// src/utils/api-response.ts
export class ApiResponse<T> {
  constructor(
    public success: boolean,
    public data?: T,
    public error?: ApiError,
    public message?: string
  ) {}

  static success<T>(data: T, message?: string): ApiResponse<T> {
    return new ApiResponse(true, data, undefined, message);
  }

  static error(error: ApiError): ApiResponse<never> {
    return new ApiResponse(false, undefined, error);
  }
}

// Usage in controller
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    res.json(ApiResponse.success(user));
  } catch (error) {
    if (error instanceof NotFoundError) {
      res.status(404).json(ApiResponse.error({
        code: 'NOT_FOUND',
        message: error.message
      }));
    } else {
      res.status(500).json(ApiResponse.error({
        code: 'INTERNAL_ERROR',
        message: 'Something went wrong'
      }));
    }
  }
});
```

### Middleware Chain Pattern

Compose middleware for request processing.

```typescript
// src/middleware/authenticate.ts
export const authenticate = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const token = extractToken(req);
    const payload = await verifyToken(token);
    req.user = payload;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

// src/middleware/authorize.ts
export const authorize = (roles: Role[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    next();
  };
};

// Usage
app.delete(
  '/api/users/:id',
  authenticate,
  authorize([Role.ADMIN]),
  deleteUser
);
```

### Query Builder Pattern

Flexible query construction.

```typescript
// src/utils/query-builder.ts
export class QueryBuilder<T> {
  private query: any = {};
  private selectFields: string[] = [];
  private includeRelations: any = {};

  where(conditions: Partial<T>): this {
    this.query.where = { ...this.query.where, ...conditions };
    return this;
  }

  select(...fields: (keyof T)[]): this {
    this.selectFields.push(...(fields as string[]));
    return this;
  }

  include(relation: string): this {
    this.includeRelations[relation] = true;
    return this;
  }

  orderBy(field: keyof T, direction: 'asc' | 'desc' = 'asc'): this {
    this.query.orderBy = { [field]: direction };
    return this;
  }

  limit(count: number): this {
    this.query.take = count;
    return this;
  }

  offset(count: number): this {
    this.query.skip = count;
    return this;
  }

  build() {
    const query: any = { ...this.query };

    if (this.selectFields.length > 0) {
      query.select = Object.fromEntries(
        this.selectFields.map(field => [field, true])
      );
    }

    if (Object.keys(this.includeRelations).length > 0) {
      query.include = this.includeRelations;
    }

    return query;
  }
}

// Usage
const query = new QueryBuilder<User>()
  .where({ status: 'active' })
  .select('id', 'name', 'email')
  .include('posts')
  .orderBy('createdAt', 'desc')
  .limit(10)
  .build();

const users = await prisma.user.findMany(query);
```

## Error Handling Patterns

### Custom Error Classes

Define specific error types.

```typescript
// src/errors/app-error.ts
export abstract class AppError extends Error {
  abstract statusCode: number;
  abstract code: string;

  constructor(message: string) {
    super(message);
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

export class NotFoundError extends AppError {
  statusCode = 404;
  code = 'NOT_FOUND';
}

export class ValidationError extends AppError {
  statusCode = 400;
  code = 'VALIDATION_ERROR';
  
  constructor(message: string, public details?: any) {
    super(message);
  }
}

export class UnauthorizedError extends AppError {
  statusCode = 401;
  code = 'UNAUTHORIZED';
}

export class ConflictError extends AppError {
  statusCode = 409;
  code = 'CONFLICT';
}
```

### Global Error Handler

Centralized error handling.

```typescript
// src/middleware/error-handler.ts
export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  logger.error('Request error', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method
  });

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: (error as any).details
      }
    });
  }

  // Unknown error
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'Something went wrong'
        : error.message
    }
  });
};
```

## State Management Patterns

### Redux Slice Pattern

Organize Redux state by feature.

```typescript
// src/store/slices/userSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string) => {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    data: null as User | null,
    loading: false,
    error: null as string | null
  },
  reducers: {
    clearUser: (state) => {
      state.data = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch user';
      });
  }
});

export const { clearUser } = userSlice.actions;
export default userSlice.reducer;
```

### React Query Pattern

Server state management with React Query.

```typescript
// src/hooks/useUser.ts
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000 // 10 minutes
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateUserDTO) => updateUser(data),
    onSuccess: (user) => {
      // Update cache
      queryClient.setQueryData(['user', user.id], user);
      
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId);
  const updateMutation = useUpdateUser();

  const handleUpdate = async (data: UpdateUserDTO) => {
    await updateMutation.mutateAsync(data);
  };

  if (isLoading) return <LoadingSpinner />;

  return <UserForm user={user} onSubmit={handleUpdate} />;
}
```

## Testing Patterns

### Test Data Builders

Create test data with builders.

```typescript
// src/test/builders/user.builder.ts
export class UserBuilder {
  private user: Partial<User> = {
    id: 'test-id',
    email: 'test@example.com',
    username: 'testuser',
    createdAt: new Date()
  };

  withId(id: string): this {
    this.user.id = id;
    return this;
  }

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withRole(role: Role): this {
    this.user.role = role;
    return this;
  }

  build(): User {
    return this.user as User;
  }
}

// Usage
const user = new UserBuilder()
  .withEmail('admin@example.com')
  .withRole(Role.ADMIN)
  .build();
```

### Page Object Pattern

Organize E2E tests with page objects.

```typescript
// tests/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async fillEmail(email: string) {
    await this.page.fill('[name="email"]', email);
  }

  async fillPassword(password: string) {
    await this.page.fill('[name="password"]', password);
  }

  async submit() {
    await this.page.click('[type="submit"]');
  }

  async login(email: string, password: string) {
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.submit();
  }

  async expectError(message: string) {
    await expect(this.page.locator('[role="alert"]')).toContainText(message);
  }
}

// Usage
test('login with invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await loginPage.goto();
  await loginPage.login('invalid@example.com', 'wrongpassword');
  await loginPage.expectError('Invalid credentials');
});
```

---

*Last Updated: 2024-11-21*
*These patterns are established conventions for this project*
