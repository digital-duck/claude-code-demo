# Security Guidelines

## Table of Contents
1. [Security Policy](#security-policy)
2. [Reporting Vulnerabilities](#reporting-vulnerabilities)
3. [Security Best Practices](#security-best-practices)
4. [Authentication & Authorization](#authentication--authorization)
5. [Data Protection](#data-protection)
6. [Input Validation](#input-validation)
7. [Common Vulnerabilities](#common-vulnerabilities)
8. [Secure Development](#secure-development)
9. [Dependency Security](#dependency-security)

## Security Policy

### Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

### Security Updates

- **Critical:** Patched within 24 hours
- **High:** Patched within 7 days
- **Medium:** Patched in next minor release
- **Low:** Patched in next major release

## Reporting Vulnerabilities

### DO NOT create public GitHub issues for security vulnerabilities

### How to Report

**Email:** security@example.com

**Include:**
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)
5. Your contact information

### What to Expect

1. **Acknowledgment:** Within 24 hours
2. **Initial Assessment:** Within 72 hours
3. **Regular Updates:** Every 7 days until resolved
4. **Credit:** Recognition in security advisory (if desired)

### Disclosure Policy

- We follow coordinated disclosure
- Public disclosure after patch is released
- Minimum 90-day embargo period
- Earlier disclosure if actively exploited

## Security Best Practices

### General Principles

1. **Defense in Depth:** Multiple layers of security
2. **Least Privilege:** Minimum necessary permissions
3. **Fail Securely:** Secure defaults, safe failure modes
4. **Security by Design:** Security considered from the start
5. **Keep it Simple:** Complexity is the enemy of security

### Security Checklist

- [ ] All user inputs validated and sanitized
- [ ] Authentication and authorization implemented
- [ ] Sensitive data encrypted at rest and in transit
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Dependencies regularly updated
- [ ] Security testing performed
- [ ] Logging and monitoring enabled
- [ ] Secrets not in source code
- [ ] Error messages don't leak sensitive info

## Authentication & Authorization

### Password Security

#### Hashing

```typescript
import bcrypt from 'bcrypt';

// ✅ Good - Strong password hashing
const SALT_ROUNDS = 10;

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(
  password: string, 
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ❌ Bad - Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex');
```

#### Password Requirements

```typescript
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

function validatePassword(password: string): boolean {
  if (password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }
  
  if (!PASSWORD_REGEX.test(password)) {
    throw new ValidationError(
      'Password must contain uppercase, lowercase, number, and special character'
    );
  }
  
  return true;
}
```

#### Password Storage

```typescript
// ✅ Good - Never store plain passwords
interface User {
  id: string;
  email: string;
  passwordHash: string; // Hashed password
}

// ❌ Bad - Never store plain passwords
interface User {
  id: string;
  email: string;
  password: string; // Plain password
}
```

### JWT Token Security

#### Token Configuration

```typescript
import jwt from 'jsonwebtoken';

// ✅ Good - Secure JWT configuration
const JWT_CONFIG = {
  accessToken: {
    secret: process.env.JWT_ACCESS_SECRET!, // Strong, random secret
    expiresIn: '15m' // Short expiration
  },
  refreshToken: {
    secret: process.env.JWT_REFRESH_SECRET!, // Different secret
    expiresIn: '7d' // Longer expiration
  }
};

function generateAccessToken(userId: string): string {
  return jwt.sign(
    { userId, type: 'access' },
    JWT_CONFIG.accessToken.secret,
    { expiresIn: JWT_CONFIG.accessToken.expiresIn }
  );
}

// ❌ Bad - Insecure configuration
function generateToken(userId: string): string {
  return jwt.sign(
    { userId },
    'hardcoded-secret', // Never hardcode secrets
    { expiresIn: '30d' } // Too long
  );
}
```

#### Token Validation

```typescript
// ✅ Good - Proper token validation
function verifyAccessToken(token: string): TokenPayload {
  try {
    const payload = jwt.verify(
      token,
      JWT_CONFIG.accessToken.secret
    ) as TokenPayload;
    
    if (payload.type !== 'access') {
      throw new Error('Invalid token type');
    }
    
    return payload;
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}

// ❌ Bad - No validation
function verifyToken(token: string) {
  return jwt.decode(token); // Never use decode for validation
}
```

#### Token Storage (Frontend)

```typescript
// ✅ Good - HttpOnly cookies (most secure)
// Set by server with httpOnly, secure, sameSite flags

// ✅ Acceptable - Memory storage (lost on refresh)
let accessToken: string | null = null;

// ⚠️ Caution - localStorage (vulnerable to XSS)
// Only use if absolutely necessary
localStorage.setItem('token', token);

// ❌ Bad - Regular cookies (vulnerable to XSS)
document.cookie = `token=${token}`;
```

### Authorization

#### Role-Based Access Control (RBAC)

```typescript
enum Role {
  USER = 'user',
  ADMIN = 'admin',
  MODERATOR = 'moderator'
}

interface User {
  id: string;
  role: Role;
}

// ✅ Good - Explicit authorization checks
function requireRole(allowedRoles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user as User;
    
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!allowedRoles.includes(user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

// Usage
app.delete('/api/users/:id', 
  authenticate,
  requireRole([Role.ADMIN]),
  deleteUser
);
```

#### Resource-Based Access Control

```typescript
// ✅ Good - Check resource ownership
async function updatePost(req: Request, res: Response) {
  const { postId } = req.params;
  const userId = req.user!.id;
  
  const post = await postRepository.findById(postId);
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  // Check ownership
  if (post.authorId !== userId && req.user!.role !== Role.ADMIN) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  // Update post
  const updated = await postRepository.update(postId, req.body);
  res.json(updated);
}
```

## Data Protection

### Encryption at Rest

```typescript
import crypto from 'crypto';

const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');
const ALGORITHM = 'aes-256-gcm';

// ✅ Good - Encrypt sensitive data
function encrypt(text: string): EncryptedData {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

function decrypt(data: EncryptedData): string {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    ENCRYPTION_KEY,
    Buffer.from(data.iv, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(data.authTag, 'hex'));
  
  let decrypted = decipher.update(data.encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Usage - Store sensitive fields encrypted
interface UserSecrets {
  id: string;
  encryptedSSN: EncryptedData;
  encryptedCreditCard: EncryptedData;
}
```

### Encryption in Transit

#### HTTPS Configuration

```typescript
import https from 'https';
import fs from 'fs';

// ✅ Good - HTTPS with strong ciphers
const httpsOptions = {
  key: fs.readFileSync('path/to/private-key.pem'),
  cert: fs.readFileSync('path/to/certificate.pem'),
  ciphers: [
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES128-SHA256',
    'ECDHE-RSA-AES256-SHA384'
  ].join(':'),
  honorCipherOrder: true,
  minVersion: 'TLSv1.2'
};

https.createServer(httpsOptions, app).listen(443);
```

### Sensitive Data Handling

```typescript
// ✅ Good - Exclude sensitive fields
interface User {
  id: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
}

function sanitizeUser(user: User): PublicUser {
  const { passwordHash, ...publicData } = user;
  return publicData;
}

// ❌ Bad - Exposing sensitive data
app.get('/api/users/:id', async (req, res) => {
  const user = await userRepository.findById(req.params.id);
  res.json(user); // Includes passwordHash!
});

// ✅ Good - Only expose public data
app.get('/api/users/:id', async (req, res) => {
  const user = await userRepository.findById(req.params.id);
  res.json(sanitizeUser(user));
});
```

### Logging

```typescript
// ✅ Good - Safe logging
logger.info('User login', {
  userId: user.id,
  email: user.email,
  ip: req.ip
});

// ❌ Bad - Logging sensitive data
logger.info('User login', {
  userId: user.id,
  password: req.body.password, // Never log passwords
  creditCard: user.creditCard  // Never log PII
});
```

## Input Validation

### Server-Side Validation

```typescript
import { z } from 'zod';

// ✅ Good - Comprehensive validation
const createUserSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .max(255, 'Email too long'),
  
  username: z.string()
    .min(3, 'Username too short')
    .max(50, 'Username too long')
    .regex(/^[a-zA-Z0-9_]+$/, 'Invalid characters in username'),
  
  password: z.string()
    .min(8, 'Password too short')
    .regex(PASSWORD_REGEX, 'Password too weak'),
  
  age: z.number()
    .int('Age must be an integer')
    .min(13, 'Must be at least 13')
    .max(120, 'Invalid age')
});

// Validation middleware
function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors
        });
      }
      next(error);
    }
  };
}

// Usage
app.post('/api/users',
  validate(createUserSchema),
  createUser
);
```

### SQL Injection Prevention

```typescript
// ✅ Good - Parameterized queries
async function getUser(email: string): Promise<User | null> {
  const result = await db.query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );
  return result.rows[0] || null;
}

// ❌ Bad - String concatenation
async function getUser(email: string) {
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  return db.query(query);
}

// ✅ Good - ORM with parameterization
const user = await prisma.user.findUnique({
  where: { email: email }
});
```

### XSS Prevention

```typescript
// ✅ Good - Sanitize HTML input
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHTML(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  });
}

// Usage
const cleanContent = sanitizeHTML(userInput);

// React - Avoid dangerouslySetInnerHTML
// ❌ Bad
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Good - Let React escape
<div>{userInput}</div>
```

### Path Traversal Prevention

```typescript
import path from 'path';

// ✅ Good - Validate and sanitize file paths
function getFile(filename: string): string {
  // Remove path traversal attempts
  const sanitized = path.basename(filename);
  
  // Construct safe path
  const filePath = path.join('/safe/directory', sanitized);
  
  // Verify path is within allowed directory
  if (!filePath.startsWith('/safe/directory')) {
    throw new Error('Invalid file path');
  }
  
  return filePath;
}

// ❌ Bad - Direct path construction
function getFile(filename: string) {
  return `/files/${filename}`; // Vulnerable to ../../../etc/passwd
}
```

## Common Vulnerabilities

### CSRF Protection

```typescript
import csrf from 'csurf';

// ✅ Good - CSRF protection
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/process', csrfProtection, (req, res) => {
  // Process form
});

// Frontend - Include CSRF token
<form method="POST" action="/process">
  <input type="hidden" name="_csrf" value="{{ csrfToken }}" />
  {/* Form fields */}
</form>
```

### Clickjacking Protection

```typescript
import helmet from 'helmet';

// ✅ Good - X-Frame-Options header
app.use(helmet.frameguard({ action: 'deny' }));

// Or allow specific origins
app.use(helmet.frameguard({ 
  action: 'allow-from',
  domain: 'https://trusted-site.com'
}));
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// ✅ Good - Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests, please try again later'
    });
  }
});

app.use('/api/', limiter);

// Stricter limit for sensitive endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5
});

app.post('/api/auth/login', authLimiter, login);
```

### Command Injection Prevention

```typescript
import { spawn } from 'child_process';

// ✅ Good - Use parameterized commands
function processImage(filename: string) {
  // Whitelist validation
  if (!/^[a-zA-Z0-9_\-\.]+$/.test(filename)) {
    throw new Error('Invalid filename');
  }
  
  // Use array of arguments
  const process = spawn('convert', [filename, 'output.jpg'], {
    shell: false // Important: don't use shell
  });
  
  return new Promise((resolve, reject) => {
    process.on('close', code => {
      code === 0 ? resolve() : reject();
    });
  });
}

// ❌ Bad - Shell injection risk
function processImage(filename: string) {
  exec(`convert ${filename} output.jpg`, callback);
}
```

## Secure Development

### Environment Variables

```bash
# .env (never commit this file)
NODE_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/db
JWT_ACCESS_SECRET=long-random-string-here
JWT_REFRESH_SECRET=another-long-random-string
ENCRYPTION_KEY=hex-encoded-32-byte-key
API_KEY=your-api-key

# Use strong, random secrets
# Generate with: openssl rand -hex 32
```

```typescript
// ✅ Good - Environment variable usage
const config = {
  jwtSecret: process.env.JWT_SECRET!,
  databaseUrl: process.env.DATABASE_URL!,
  apiKey: process.env.API_KEY!
};

// Validate required variables on startup
function validateEnv() {
  const required = [
    'JWT_SECRET',
    'DATABASE_URL',
    'API_KEY'
  ];
  
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`Missing env variables: ${missing.join(', ')}`);
  }
}
```

### Security Headers

```typescript
import helmet from 'helmet';

// ✅ Good - Comprehensive security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  noSniff: true,
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));
```

### Error Handling

```typescript
// ✅ Good - Safe error messages
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  // Log full error for debugging
  logger.error('Request error', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method
  });
  
  // Return safe error to client
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({
      error: 'Internal server error'
    });
  } else {
    // Include details in development
    res.status(500).json({
      error: error.message,
      stack: error.stack
    });
  }
});

// ❌ Bad - Exposing sensitive information
app.use((error: Error, req: Request, res: Response) => {
  res.status(500).json({
    error: error.message,
    stack: error.stack, // Never expose in production
    query: req.query,   // Might contain sensitive data
    body: req.body      // Might contain sensitive data
  });
});
```

## Dependency Security

### Regular Updates

```bash
# Check for vulnerabilities
npm audit

# Fix automatically
npm audit fix

# Check for outdated packages
npm outdated

# Update dependencies
npm update
```

### Automated Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm audit
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Dependency Review

Before adding a dependency:

- [ ] Check npm download statistics
- [ ] Review GitHub activity and maintenance
- [ ] Check for known vulnerabilities
- [ ] Review license compatibility
- [ ] Assess bundle size impact
- [ ] Consider alternatives

---

*Last Updated: 2024-11-21*
*Security is everyone's responsibility*
