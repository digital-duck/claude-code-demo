# Project Context for Claude Code

## Project Overview

**Project Name:** [Your Project Name]  
**Version:** 1.0.0  
**Purpose:** [Brief description of what this project does]

This document serves as the primary context file for Claude Code when working on this project. It provides essential information about the project structure, conventions, and development practices.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Project Structure

```
project-root/
├── src/
│   ├── components/     # Reusable UI components
│   ├── services/       # Business logic and API services
│   ├── utils/          # Helper functions and utilities
│   ├── types/          # TypeScript type definitions
│   └── config/         # Configuration files
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end tests
├── docs/               # Additional documentation
├── public/             # Static assets
└── scripts/            # Build and utility scripts
```

## Technology Stack

### Core Technologies
- **Language:** TypeScript 5.x
- **Runtime:** Node.js 20.x
- **Framework:** [React/Vue/Express/etc.]
- **Build Tool:** Vite/Webpack

### Key Dependencies
- See `DEPENDENCIES.md` for detailed information
- Package manager: npm/yarn/pnpm

## Development Guidelines

### Code Style
- **Formatting:** Prettier with project config
- **Linting:** ESLint with TypeScript support
- **Naming Conventions:**
  - Files: kebab-case (`user-service.ts`)
  - Classes: PascalCase (`UserService`)
  - Functions/Variables: camelCase (`getUserData`)
  - Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)

### File Organization
- One component/class per file
- Co-locate tests with source files (optional)
- Group related functionality in directories
- Use barrel exports (index.ts) for clean imports

### Testing Strategy
- Unit tests required for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Minimum 80% code coverage

See `TESTING_GUIDE.md` for detailed testing guidelines.

## Architecture Principles

1. **Separation of Concerns:** Keep business logic separate from UI
2. **Single Responsibility:** Each module should have one clear purpose
3. **Dependency Injection:** Use DI for better testability
4. **Error Handling:** Comprehensive error handling at all layers
5. **Type Safety:** Leverage TypeScript for type safety

See `ARCHITECTURE.md` for detailed architecture documentation.

## Common Tasks

### Adding a New Feature
1. Create feature branch: `git checkout -b feature/feature-name`
2. Implement feature with tests
3. Update documentation
4. Submit pull request
5. See `CONTRIBUTING.md` for full guidelines

### Debugging
1. Check logs in `logs/` directory
2. Use debugger configuration in `.vscode/launch.json`
3. See `TROUBLESHOOTING.md` for common issues

### API Integration
1. Define types in `src/types/`
2. Implement service in `src/services/`
3. Add error handling
4. Write integration tests
5. See `API_REFERENCE.md` for API documentation

## Environment Configuration

### Required Environment Variables
```bash
NODE_ENV=development|production|test
API_BASE_URL=https://api.example.com
DATABASE_URL=postgresql://localhost:5432/dbname
SECRET_KEY=your-secret-key
LOG_LEVEL=debug|info|warn|error
```

### Configuration Files
- `.env.development` - Development environment
- `.env.production` - Production environment
- `.env.test` - Test environment
- `config/default.json` - Default configuration

## Security Considerations

- Never commit sensitive data (API keys, passwords)
- Use environment variables for secrets
- Follow OWASP security guidelines
- See `SECURITY.md` for detailed security guidelines

## Performance Guidelines

- Lazy load components where appropriate
- Implement caching strategies
- Optimize database queries
- Monitor bundle size
- Use performance profiling tools
- See `performance.md` for detailed performance guidelines

## Documentation

- Keep documentation up-to-date
- Document all public APIs
- Include JSDoc comments for complex functions
- Update `README.md` for user-facing changes

## Additional Resources

- **Architecture:** See `ARCHITECTURE.md`
- **API Reference:** See `API_REFERENCE.md`
- **Testing:** See `TESTING_GUIDE.md`
- **Dependencies:** See `DEPENDENCIES.md`
- **Contributing:** See `CONTRIBUTING.md`
- **Security:** See `SECURITY.md`
- **Performance:** See `performance.md`
- **Best Practice:** See `patterns.md` and `gotchas.md`
- **Troubleshooting:** See `TROUBLESHOOTING.md`

## Contact & Support

- **Team Lead:** [Name] ([email])
- **Tech Lead:** [Name] ([email])
- **Documentation:** [Link to wiki/docs]
- **Issues:** [Link to issue tracker]

## Version History

### 1.0.0 (Current)
- Initial release
- Core features implemented
- Documentation established

---

*Last Updated: 2024-11-21*
*Maintained by: [Team Name]*
