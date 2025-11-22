# Documentation Review Guide

## How to Review These Files

This guide will help you understand what to look for in each documentation file and how Claude Code uses them.

## Review Order (Recommended)

### 1. Start Here: CLAUDE.md (5 min)
**Purpose:** High-level project overview

**What to look for:**
- Does the project structure match your actual project?
- Are the technology stack details correct?
- Do the quick start commands work for your setup?
- Are the environment variables listed complete?

**Customize for your project:**
- Update project name and description
- Adjust technology stack if different
- Add project-specific quick start steps
- Update team contact information

---

### 2. Next: .clinerules (10 min)
**Purpose:** Claude Code's code generation rules

**What to look for:**
- Code style preferences (spaces vs tabs, quotes, etc.)
- File naming conventions
- Import organization rules
- Component/service structure patterns

**Key sections:**
- **General Preferences:** Basic code style
- **Code Generation Rules:** What Claude Code should do when creating files
- **Error Handling Pattern:** How errors should be structured
- **Documentation Requirements:** JSDoc format

**Customize:**
- Adjust code style to match your team's preferences
- Add project-specific patterns
- Define your commit message format
- Add tool-specific configurations

---

### 3. Core Architecture: ARCHITECTURE.md (15 min)
**Purpose:** System design and structure

**What to look for:**
- High-level architecture diagram
- Layer separation (presentation, business logic, data)
- Design patterns used
- Technology choices and rationale

**Important sections:**
- **System Components:** How your app is organized
- **Data Flow:** How requests move through the system
- **Design Patterns:** Which patterns to use when
- **Scalability:** How the system handles growth

**Use this when:**
- Adding new major features
- Refactoring large sections
- Onboarding new developers
- Making architectural decisions

---

### 4. API Reference: API_REFERENCE.md (10 min)
**Purpose:** Complete API documentation

**What to look for:**
- Endpoint structure and naming
- Request/response formats
- Authentication flow
- Error handling approach

**Key sections:**
- **Authentication:** How auth works in detail
- **API Endpoints:** All available endpoints with examples
- **Error Handling:** Standard error format
- **Pagination:** How to handle large datasets

**Customize:**
- Update base URLs
- Add your actual endpoints
- Document your specific error codes
- Include your API versioning strategy

---

### 5. Development: TESTING_GUIDE.md (15 min)
**Purpose:** How to write and run tests

**What to look for:**
- Test structure (AAA pattern)
- What to test vs what not to test
- Mock vs real implementations
- Coverage requirements

**Important sections:**
- **Test Types:** Unit, integration, component, E2E
- **Testing Setup:** Configuration for test runners
- **Best Practices:** How to write good tests
- **Coverage Requirements:** Minimum thresholds

**Use this when:**
- Writing new tests
- Reviewing test PRs
- Setting up CI/CD
- Debugging test failures

---

### 6. Dependencies: DEPENDENCIES.md (10 min)
**Purpose:** Why each dependency exists

**What to look for:**
- Core dependencies and their purpose
- Why specific packages were chosen
- Security practices
- Update guidelines

**Key sections:**
- **Frontend/Backend Dependencies:** What each package does
- **Why Chosen:** Rationale for each major dependency
- **Security:** How to handle vulnerabilities
- **Upgrade Guidelines:** How to safely update

**Use this when:**
- Adding new dependencies
- Updating existing ones
- Debugging dependency issues
- Security audits

---

### 7. Team Collaboration: CONTRIBUTING.md (10 min)
**Purpose:** How to contribute code

**What to look for:**
- Git workflow (branches, commits, PRs)
- Code review process
- Coding standards enforcement
- How to report issues

**Important sections:**
- **Development Workflow:** Branch naming, commit format
- **Coding Standards:** What's enforced
- **Pull Request Process:** How to submit changes
- **Review Process:** What reviewers check

**Use this for:**
- Team onboarding
- Setting up Git hooks
- PR templates
- Code review checklists

---

### 8. Security: SECURITY.md (15 min)
**Purpose:** Security best practices

**What to look for:**
- Common vulnerabilities to avoid
- Authentication/authorization patterns
- Data protection strategies
- Security checklist

**Critical sections:**
- **Password Security:** Hashing, storage, validation
- **JWT Token Security:** Token configuration and validation
- **Input Validation:** Preventing SQL injection, XSS
- **Error Handling:** Not leaking sensitive info

**Review this when:**
- Implementing authentication
- Handling user data
- Preparing for security audits
- Debugging security issues

---

### 9. Problem Solving: TROUBLESHOOTING.md (20 min)
**Purpose:** Common issues and solutions

**What to look for:**
- Issues you've encountered before
- Quick diagnostic commands
- Step-by-step solutions
- When to ask for help

**Key sections:**
- **Installation Problems:** npm, dependencies, permissions
- **Development Server:** Port conflicts, hot reload
- **Database Issues:** Connection, migrations, Prisma
- **Performance Issues:** Slow loads, memory leaks

**Use this when:**
- Something breaks
- Onboarding new developers
- Before asking for help
- Documenting new solutions

---

### 10. Context Files (30 min total)

#### context/patterns.md (15 min)
**Purpose:** Code patterns to follow

**What to look for:**
- Repository pattern examples
- Service layer structure
- React patterns (hooks, compound components)
- Error handling patterns

**Use when:**
- Creating new features
- Refactoring code
- Ensuring consistency
- Code reviews

#### context/gotchas.md (10 min)
**Purpose:** Mistakes to avoid

**What to look for:**
- Common TypeScript pitfalls
- React anti-patterns
- Async/await mistakes
- Database gotchas

**Use when:**
- Learning the stack
- Debugging mysterious issues
- Code reviews
- Training new developers

#### context/performance.md (15 min)
**Purpose:** Optimization techniques

**What to look for:**
- Frontend optimization (code splitting, lazy loading)
- Backend optimization (caching, batching)
- Database optimization (indexes, query optimization)
- Monitoring strategies

**Use when:**
- App feels slow
- Optimizing existing features
- Building new features
- Performance reviews

---

## How Claude Code Uses These Files

### 1. **Context Loading**
When you start Claude Code on a project, it:
1. Looks for `CLAUDE.md` first
2. Reads `.clinerules` for coding standards
3. Scans other documentation as needed

### 2. **Code Generation**
When generating code, Claude Code:
- Follows patterns from `patterns.md`
- Avoids pitfalls from `gotchas.md`
- Applies optimizations from `performance.md`
- Matches style from `.clinerules`

### 3. **Problem Solving**
When fixing issues, Claude Code:
- Checks `TROUBLESHOOTING.md` for known solutions
- Follows security guidelines from `SECURITY.md`
- References architecture from `ARCHITECTURE.md`

### 4. **Consistency**
Claude Code uses these files to:
- Maintain consistent code style
- Follow established patterns
- Use the same dependencies
- Match project conventions

---

## Customization Checklist

As you review, mark what needs customization:

### High Priority (Do First)
- [ ] Update project name in CLAUDE.md
- [ ] Set correct technology stack
- [ ] Update environment variables
- [ ] Adjust code style preferences in .clinerules
- [ ] Add actual API endpoints to API_REFERENCE.md
- [ ] Update base URLs and secrets

### Medium Priority (Do Soon)
- [ ] Customize architecture diagrams
- [ ] Add project-specific patterns
- [ ] Document your actual dependencies
- [ ] Add team-specific gotchas you've discovered
- [ ] Update troubleshooting with your known issues

### Low Priority (Ongoing)
- [ ] Add more examples to patterns.md
- [ ] Document new performance optimizations
- [ ] Expand testing examples
- [ ] Add new troubleshooting entries
- [ ] Update as dependencies change

---

## Tips for Effective Use

### 1. Keep It Updated
- Update docs when you make architectural changes
- Add new gotchas as you discover them
- Document solutions to problems you solve
- Keep dependency list current

### 2. Be Specific
- Use actual code examples from your project
- Reference real file paths
- Include actual error messages you've seen
- Document your specific conventions

### 3. Make It Accessible
- Store in project root for easy access
- Link between documents
- Use clear section headers
- Include table of contents

### 4. Use Version Control
- Commit documentation with code changes
- Review doc changes in PRs
- Tag documentation versions
- Keep changelog of doc updates

---

## What to Look For While Reviewing

### ✅ Good Signs
- Examples match your project structure
- Patterns you actually use
- Clear, actionable guidance
- Specific to your tech stack
- Solutions to problems you've had

### ⚠️ Needs Work
- Generic examples that don't fit
- Missing project-specific details
- Patterns you don't follow
- Outdated dependency versions
- Missing important workflows

### ❌ Remove/Replace
- Examples from wrong framework
- Patterns you explicitly avoid
- Deprecated approaches
- Incorrect information
- Irrelevant sections

---

## Questions to Ask Yourself

1. **CLAUDE.md**
   - Does this accurately describe my project?
   - Would a new developer understand the project from this?
   - Are all setup steps included?

2. **.clinerules**
   - Do these match our team's coding style?
   - Are there project-specific rules missing?
   - Do we have different preferences?

3. **ARCHITECTURE.md**
   - Is this our actual architecture?
   - Are design decisions explained?
   - Would this guide architectural decisions?

4. **API_REFERENCE.md**
   - Are all endpoints documented?
   - Is authentication flow correct?
   - Are error codes accurate?

5. **TESTING_GUIDE.md**
   - Do we follow these testing practices?
   - Are coverage requirements realistic?
   - Are test examples helpful?

6. **Context Files**
   - Are these patterns we actually use?
   - Have we encountered these gotchas?
   - Are optimizations relevant to our app?

---

## Next Steps After Review

1. **Create Issues:** For customizations needed
2. **Prioritize:** What needs updating immediately
3. **Assign:** Who will update each section
4. **Schedule:** When to review again
5. **Test:** Try using Claude Code with updated docs
6. **Iterate:** Keep improving based on experience

---

## Getting Maximum Value

### For New Projects
- Start with these templates
- Customize as you build
- Add examples from your actual code
- Document decisions as you make them

### For Existing Projects
- Compare templates to your current docs
- Merge useful sections
- Add missing documentation
- Standardize format across docs

### For Teams
- Review together
- Discuss patterns and conventions
- Agree on standards
- Document team decisions
- Keep everyone aligned

---

## Remember

These documents are **living documentation**:
- They should evolve with your project
- Update them as you learn
- Add examples from real issues
- Document solutions you discover
- Keep them relevant and accurate

The better your documentation, the more effective Claude Code will be at:
- Understanding your project
- Following your conventions  
- Generating appropriate code
- Solving problems correctly
- Maintaining consistency

---

## Quick Reference

**Daily Use:**
- `.clinerules` - Check before writing code
- `patterns.md` - Reference when implementing features
- `gotchas.md` - Check when debugging

**Weekly Use:**
- `TROUBLESHOOTING.md` - When issues arise
- `TESTING_GUIDE.md` - When writing tests
- `performance.md` - When optimizing

**Monthly Use:**
- `ARCHITECTURE.md` - When planning features
- `DEPENDENCIES.md` - During dependency updates
- `SECURITY.md` - During security reviews

**Project Milestones:**
- `API_REFERENCE.md` - When API changes
- `CONTRIBUTING.md` - When onboarding
- `CLAUDE.md` - When project evolves

---

Happy reviewing! Take your time and make these documents truly yours. 🚀

*Remember: Good documentation is an investment that pays dividends every day.*
