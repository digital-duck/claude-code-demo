"""
Contextual Documentation Generator for AI Agent Consumption
Generates CLAUDE.md and other contextual files from knowledge graph data
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class RepoContext:
    """Structured context for a repository."""
    repo_path: Path
    repo_name: str
    primary_language: str
    tech_stack: List[str]
    architecture_summary: str
    key_modules: List[Dict]
    dependencies: Dict
    coding_patterns: List[str]
    common_issues: List[str]
    test_coverage: Dict
    documentation_status: str


class ContextualDocumentationGenerator:
    """
    Generate CLAUDE.md and contextual documentation for AI agent consumption.
    Transforms knowledge graph into agent-ready context.
    """
    
    def __init__(self, doc_agent_kg_builder):
        """
        Initialize with your existing doc-agent KG builder.
        
        Parameters:
        -----------
        doc_agent_kg_builder : UnifiedKnowledgeGraphBuilder
            Your existing knowledge graph builder
        """
        self.kg_builder = doc_agent_kg_builder
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load documentation templates."""
        return {
            'claude_md': self._get_claude_md_template(),
            'architecture': self._get_architecture_template(),
            'api_reference': self._get_api_template(),
            'testing_guide': self._get_testing_template()
        }
    
    def generate_repo_documentation(self, repo_path: Path, 
                                    output_dir: Optional[Path] = None) -> Dict[str, Path]:
        """
        Generate complete contextual documentation for a repository.
        
        Returns:
        --------
        Dict mapping document type to file path
        """
        repo_path = Path(repo_path)
        output_dir = output_dir or repo_path
        
        print(f"\n{'='*70}")
        print(f"Generating contextual documentation for: {repo_path.name}")
        print(f"{'='*70}\n")
        
        # Step 1: Extract knowledge graph from all files in repo
        print("Step 1: Building knowledge graph...")
        kg_data = self.kg_builder.process_directory(repo_path, recursive=True)
        
        # Step 2: Analyze and synthesize repo context
        print("Step 2: Analyzing repository structure...")
        repo_context = self._analyze_repo(repo_path, kg_data)
        
        # Step 3: Generate documentation files
        print("Step 3: Generating documentation files...")
        docs = {}
        
        # Generate CLAUDE.md - Primary context file for AI agents
        docs['CLAUDE.md'] = self._generate_claude_md(repo_context, output_dir)
        
        # Generate supplementary context files
        docs['ARCHITECTURE.md'] = self._generate_architecture_md(repo_context, output_dir)
        docs['API_REFERENCE.md'] = self._generate_api_reference(repo_context, output_dir)
        docs['TESTING_GUIDE.md'] = self._generate_testing_guide(repo_context, output_dir)
        docs['DEPENDENCIES.md'] = self._generate_dependencies_md(repo_context, output_dir)
        
        # Generate agent-specific instruction files
        docs['AGENT_INSTRUCTIONS.md'] = self._generate_agent_instructions(repo_context, output_dir)
        
        print(f"\n✓ Documentation generated successfully!")
        print(f"Files created: {len(docs)}")
        for doc_type, path in docs.items():
            print(f"  - {doc_type}: {path}")
        
        return docs
    
    def _analyze_repo(self, repo_path: Path, kg_data: Dict) -> RepoContext:
        """Analyze repository and create structured context."""
        
        # Extract key information from KG
        entities = kg_data.get('entities', [])
        relationships = kg_data.get('relationships', [])
        metadata = kg_data.get('metadata', {})
        
        # Detect primary language
        file_types = self._count_file_types(kg_data)
        primary_language = max(file_types, key=file_types.get) if file_types else 'unknown'
        
        # Extract tech stack
        tech_stack = self._extract_tech_stack(entities, metadata)
        
        # Identify key modules/components
        key_modules = self._identify_key_modules(entities, relationships)
        
        # Analyze dependencies
        dependencies = self._analyze_dependencies(entities, relationships)
        
        # Identify coding patterns
        coding_patterns = self._identify_patterns(entities, metadata)
        
        # Extract common issues (from comments, TODOs, etc.)
        common_issues = self._extract_common_issues(metadata)
        
        # Generate architecture summary
        architecture_summary = self._generate_architecture_summary(
            key_modules, relationships, tech_stack
        )
        
        return RepoContext(
            repo_path=repo_path,
            repo_name=repo_path.name,
            primary_language=primary_language,
            tech_stack=tech_stack,
            architecture_summary=architecture_summary,
            key_modules=key_modules,
            dependencies=dependencies,
            coding_patterns=coding_patterns,
            common_issues=common_issues,
            test_coverage=self._analyze_test_coverage(entities),
            documentation_status=self._assess_documentation(metadata)
        )
    
    def _generate_claude_md(self, context: RepoContext, output_dir: Path) -> Path:
        """
        Generate CLAUDE.md - Primary context file for AI agents.
        
        This is the main file that downstream agents will read to understand the repo.
        """
        
        claude_md_content = f"""# {context.repo_name} - AI Agent Context

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Primary Language**: {context.primary_language}

## Repository Overview

{context.architecture_summary}

## Tech Stack

{self._format_tech_stack(context.tech_stack)}

## Key Components

{self._format_key_modules(context.key_modules)}

## Architecture & Patterns

### Code Organization
{self._format_code_organization(context)}

### Common Patterns
{self._format_patterns(context.coding_patterns)}

### Dependencies
{self._format_dependencies(context.dependencies)}

## Testing Strategy

{self._format_testing_info(context.test_coverage)}

## Known Issues & TODOs

{self._format_issues(context.common_issues)}

## Agent Guidelines

### Code Quality Improvements
- Follow existing patterns identified above
- Maintain consistency with established coding style
- Ensure test coverage for new code
- Update documentation when making changes

### Feature Development
- Review existing modules before adding new ones
- Consider integration points with key components
- Follow established architectural patterns
- Add appropriate tests

### Bug Fixes
- Check related issues in the list above
- Verify fixes don't break existing patterns
- Add regression tests
- Update documentation if behavior changes

## Important Files & Entry Points

{self._format_important_files(context)}

## Developer Notes

{self._format_developer_notes(context)}

---

*This documentation was auto-generated by doc-agent. For more detailed information, see supplementary documentation files.*
"""
        
        output_path = output_dir / "CLAUDE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(claude_md_content)
        
        return output_path
    
    def _generate_agent_instructions(self, context: RepoContext, output_dir: Path) -> Path:
        """
        Generate specific instructions for AI agents operating on this repo.
        """
        
        instructions = f"""# Agent Instructions for {context.repo_name}

## Mission
You are an AI agent tasked with maintaining and improving this codebase. Your responsibilities include:
1. Code quality improvements
2. Feature development
3. Bug fixes
4. Documentation updates
5. Test coverage improvements

## Rules of Engagement

### DO:
- Read and understand CLAUDE.md before making changes
- Follow existing patterns and conventions
- Write tests for new functionality
- Update documentation when changing behavior
- Use semantic commit messages
- Check for breaking changes
- Maintain backward compatibility when possible

### DON'T:
- Make changes without understanding context
- Break existing tests
- Introduce new dependencies without justification
- Modify core architecture without review
- Remove functionality without deprecation period

## Code Quality Standards

### {context.primary_language} Specific Guidelines
{self._generate_language_specific_guidelines(context.primary_language)}

### Style Guidelines
- Follow existing code style in the repository
- Use consistent naming conventions
- Keep functions focused and small
- Add docstrings/comments for complex logic

## Testing Requirements

{self._generate_testing_requirements(context)}

## Review Checklist

Before submitting changes, verify:
- [ ] Code follows existing patterns
- [ ] Tests pass (existing + new)
- [ ] Documentation updated
- [ ] No new security vulnerabilities
- [ ] Performance impact considered
- [ ] Breaking changes documented

## Integration Points

{self._format_integration_points(context)}

## Emergency Contacts

If you encounter issues beyond your capabilities:
1. Flag for human review
2. Document the issue clearly
3. Preserve existing functionality
4. Don't deploy partial solutions

---

*Remember: Your goal is to improve the codebase while maintaining its integrity and existing functionality.*
"""
        
        output_path = output_dir / "AGENT_INSTRUCTIONS.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        return output_path
    
    def _generate_architecture_md(self, context: RepoContext, output_dir: Path) -> Path:
        """Generate detailed architecture documentation."""
        
        arch_content = f"""# {context.repo_name} Architecture

## High-Level Architecture

{context.architecture_summary}

## Component Breakdown

{self._format_detailed_components(context.key_modules)}

## Data Flow

{self._format_data_flow(context)}

## Integration Architecture

{self._format_integration_architecture(context)}

## Scalability Considerations

{self._format_scalability_notes(context)}
"""
        
        output_path = output_dir / "ARCHITECTURE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(arch_content)
        
        return output_path
    
    # Helper methods for analysis
    
    def _count_file_types(self, kg_data: Dict) -> Dict[str, int]:
        """Count files by type from KG data."""
        counts = {}
        for file_path in kg_data.get('files_processed', []):
            ext = Path(file_path).suffix
            counts[ext] = counts.get(ext, 0) + 1
        return counts
    
    def _extract_tech_stack(self, entities: List, metadata: Dict) -> List[str]:
        """Extract technology stack from entities."""
        tech_stack = set()
        
        # Look for import statements
        for entity in entities:
            if entity.get('type') == 'import':
                tech_stack.add(entity.get('name', '').split('.')[0])
        
        return sorted(list(tech_stack))
    
    def _identify_key_modules(self, entities: List, relationships: List) -> List[Dict]:
        """Identify key modules/components based on centrality in KG."""
        module_importance = {}
        
        for rel in relationships:
            from_module = rel.get('from')
            to_module = rel.get('to')
            module_importance[from_module] = module_importance.get(from_module, 0) + 1
            module_importance[to_module] = module_importance.get(to_module, 0) + 1
        
        top_modules = sorted(
            module_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return [{'name': name, 'importance': score} for name, score in top_modules]
    
    def _analyze_dependencies(self, entities: List, relationships: List) -> Dict:
        """Analyze dependency structure."""
        return {
            'internal': [],
            'external': [],
            'circular': []
        }
    
    def _identify_patterns(self, entities: List, metadata: Dict) -> List[str]:
        """Identify common coding patterns."""
        patterns = []
        # Your pattern detection logic here
        return patterns
    
    def _extract_common_issues(self, metadata: Dict) -> List[str]:
        """Extract TODOs, FIXMEs, known issues from code."""
        issues = []
        # Your issue extraction logic here
        return issues
    
    def _generate_architecture_summary(self, modules: List, relationships: List, 
                                       tech_stack: List) -> str:
        """Generate high-level architecture summary."""
        return f"""This is a {tech_stack[0] if tech_stack else 'multi-language'} project with {len(modules)} key components. 
The architecture follows a modular design with clear separation of concerns."""
    
    def _analyze_test_coverage(self, entities: List) -> Dict:
        """Analyze test coverage from entities."""
        return {
            'has_tests': False,
            'test_framework': 'unknown',
            'coverage': 'unknown'
        }
    
    def _assess_documentation(self, metadata: Dict) -> str:
        """Assess current documentation status."""
        doc_files = [f for f in metadata.keys() if any(
            doc in f.lower() for doc in ['readme', '.md', 'doc']
        )]
        return f"Found {len(doc_files)} documentation files"
    
    # Formatting methods
    
    def _format_tech_stack(self, tech_stack: List[str]) -> str:
        return '\n'.join(f"- {tech}" for tech in tech_stack) if tech_stack else "- Not detected"
    
    def _format_key_modules(self, modules: List[Dict]) -> str:
        if not modules:
            return "- Key modules will be identified as analysis progresses"
        return '\n'.join(
            f"- **{m['name']}**: Core component (importance: {m.get('importance', 0)})"
            for m in modules[:10]
        )
    
    def _format_code_organization(self, context: RepoContext) -> str:
        return "Standard project structure with separation of concerns."
    
    def _format_patterns(self, patterns: List[str]) -> str:
        return '\n'.join(f"- {pattern}" for pattern in patterns) if patterns else "- Patterns will be identified as analysis progresses"
    
    def _format_dependencies(self, deps: Dict) -> str:
        return f"- Internal: {len(deps.get('internal', []))}\n- External: {len(deps.get('external', []))}"
    
    def _format_testing_info(self, coverage: Dict) -> str:
        return f"- Test framework: {coverage.get('test_framework', 'To be determined')}\n- Coverage: {coverage.get('coverage', 'To be measured')}"
    
    def _format_issues(self, issues: List[str]) -> str:
        if not issues:
            return "- No major issues detected in initial scan"
        return '\n'.join(f"- {issue}" for issue in issues[:20])
    
    def _format_important_files(self, context: RepoContext) -> str:
        return "- See ARCHITECTURE.md for detailed file structure"
    
    def _format_developer_notes(self, context: RepoContext) -> str:
        return "Additional context and notes will be populated as development progresses."
    
    def _generate_language_specific_guidelines(self, language: str) -> str:
        guidelines = {
            '.py': """
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for public functions
- Prefer list comprehensions for simple transformations
""",
            '.js': """
- Use ES6+ features
- Follow Airbnb style guide
- Use async/await over callbacks
- Add JSDoc comments for public APIs
""",
            '.ts': """
- Leverage TypeScript's type system
- Use interfaces for object shapes
- Enable strict mode
- Document complex types
"""
        }
        return guidelines.get(language, "Follow established conventions in the codebase.")
    
    def _generate_testing_requirements(self, context: RepoContext) -> str:
        return """
- Write unit tests for new functions
- Add integration tests for new features
- Maintain or improve test coverage
- Ensure tests are deterministic
"""
    
    def _format_integration_points(self, context: RepoContext) -> str:
        return "- Integration points will be documented as they are identified"
    
    def _format_detailed_components(self, modules: List[Dict]) -> str:
        if not modules:
            return "Components will be documented as analysis progresses."
        return '\n\n'.join(
            f"### {m['name']}\n\nCore component with {m.get('importance', 0)} connections"
            for m in modules[:10]
        )
    
    def _format_data_flow(self, context: RepoContext) -> str:
        return "Data flow will be documented as patterns are identified."
    
    def _format_integration_architecture(self, context: RepoContext) -> str:
        return "Integration architecture details will be added as system is analyzed."
    
    def _format_scalability_notes(self, context: RepoContext) -> str:
        return "Scalability considerations will be documented as bottlenecks are identified."
    
    def _get_claude_md_template(self) -> str:
        return ""
    
    def _get_architecture_template(self) -> str:
        return ""
    
    def _get_api_template(self) -> str:
        return ""
    
    def _get_testing_template(self) -> str:
        return ""
    
    def _generate_api_reference(self, context: RepoContext, output_dir: Path) -> Path:
        """Generate API reference documentation."""
        content = f"""# API Reference for {context.repo_name}

## Overview
This document provides API reference for the {context.repo_name} project.

## Endpoints
API endpoints will be documented as they are identified.

## Authentication
Authentication methods will be documented as they are identified.

## Error Handling
Error handling patterns will be documented as they are identified.
"""
        output_path = output_dir / "API_REFERENCE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path
    
    def _generate_testing_guide(self, context: RepoContext, output_dir: Path) -> Path:
        """Generate testing guide."""
        content = f"""# Testing Guide for {context.repo_name}

## Overview
This document provides testing guidelines for the {context.repo_name} project.

## Running Tests
Test execution instructions will be documented as they are identified.

## Writing Tests
Test writing guidelines will be documented based on existing patterns.

## Test Coverage
Coverage targets and measurement will be documented.
"""
        output_path = output_dir / "TESTING_GUIDE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path
    
    def _generate_dependencies_md(self, context: RepoContext, output_dir: Path) -> Path:
        """Generate dependencies documentation."""
        content = f"""# Dependencies for {context.repo_name}

## Overview
{self._format_tech_stack(context.tech_stack)}

## Dependency Analysis
{self._format_dependencies(context.dependencies)}

## Version Requirements
Version requirements will be documented as they are identified.

## Update Policy
Dependency update policies will be documented.
"""
        output_path = output_dir / "DEPENDENCIES.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return output_path


# Example usage
if __name__ == "__main__":
    # This assumes you have your UnifiedKnowledgeGraphBuilder
    # from your doc-agent implementation
    
    print("Context Documentation Generator")
    print("=" * 70)
    print("\nThis script requires your UnifiedKnowledgeGraphBuilder instance.")
    print("Example usage:")
    print("""
    from unified_kg_builder import UnifiedKnowledgeGraphBuilder
    
    kg_builder = UnifiedKnowledgeGraphBuilder()
    doc_gen = ContextualDocumentationGenerator(kg_builder)
    docs = doc_gen.generate_repo_documentation("./my-repo")
    """)
