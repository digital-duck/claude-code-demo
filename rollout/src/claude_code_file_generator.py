"""
Complete Claude Code File Generator
Generates all files needed for optimal Claude Code experience
"""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import yaml


@dataclass
class GenerationConfig:
    """Configuration for file generation."""
    priority_level: int  # 1=Critical, 2=High-value, 3=Enhancement
    generate_examples: bool = True
    generate_templates: bool = True
    generate_workflows: bool = True
    max_generation_time: int = 300  # seconds per repo


class ClaudeCodeFileGenerator:
    """
    Generates all files needed for Claude Code preparation.
    
    This replaces the need for developers to run /init.
    """
    
    def __init__(self, kg_builder, config: GenerationConfig = None):
        """
        Initialize generator.
        
        Args:
            kg_builder: Your existing UnifiedKnowledgeGraphBuilder
            config: Generation configuration
        """
        self.kg_builder = kg_builder
        self.config = config or GenerationConfig(priority_level=2)
    
    def generate_all_files(self, repo_path: Path) -> Dict[str, Path]:
        """
        Generate all Claude Code preparation files.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            Dictionary mapping file type to file path
        """
        repo_path = Path(repo_path)
        generated_files = {}
        
        print(f"\n{'='*70}")
        print(f"Generating Claude Code files for: {repo_path.name}")
        print(f"Priority level: {self.config.priority_level}")
        print(f"{'='*70}\n")
        
        # Step 1: Analyze repository
        print("Step 1: Analyzing repository...")
        kg_data = self.kg_builder.process_directory(repo_path)
        repo_context = self._analyze_repo_context(repo_path, kg_data)
        
        # Step 2: Generate Priority 1 (Critical) files
        print("\nStep 2: Generating critical files...")
        generated_files.update(self._generate_priority_1(repo_path, repo_context))
        
        # Step 3: Generate Priority 2 (High-value) files
        if self.config.priority_level >= 2:
            print("\nStep 3: Generating high-value files...")
            generated_files.update(self._generate_priority_2(repo_path, repo_context))
        
        # Step 4: Generate Priority 3 (Enhancement) files
        if self.config.priority_level >= 3:
            print("\nStep 4: Generating enhancement files...")
            generated_files.update(self._generate_priority_3(repo_path, repo_context))
        
        print(f"\n✓ Generated {len(generated_files)} files")
        print(f"{'='*70}\n")
        
        return generated_files
    
    # ========================================================================
    # Priority 1: Critical Files (Must Generate)
    # ========================================================================
    
    def _generate_priority_1(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate critical files that Claude Code needs."""
        files = {}
        
        # 1. CLAUDE.md - Primary context
        files['CLAUDE.md'] = self._generate_claude_md(repo_path, context)
        
        # 2. .clinerules - Coding rules
        files['.clinerules'] = self._generate_clinerules(repo_path, context)
        
        # 3. Core commands
        commands_dir = repo_path / '.claude' / 'commands'
        commands_dir.mkdir(parents=True, exist_ok=True)
        
        files['commands/add_feature.md'] = self._generate_add_feature_command(
            commands_dir, context
        )
        files['commands/fix_bug.md'] = self._generate_fix_bug_command(
            commands_dir, context
        )
        files['commands/add_test.md'] = self._generate_add_test_command(
            commands_dir, context
        )
        
        # 4. Critical context
        context_dir = repo_path / '.claude' / 'context'
        context_dir.mkdir(parents=True, exist_ok=True)
        
        files['context/gotchas.md'] = self._generate_gotchas(
            context_dir, context
        )
        
        return files
    
    def _generate_claude_md(self, repo_path: Path, context: Dict) -> Path:
        """Generate comprehensive CLAUDE.md file."""
        
        content = f"""# {context['repo_name']} - Claude Code Context

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Primary Language:** {context['primary_language']}
**Framework:** {context.get('framework', 'Not detected')}

## Quick Start for Claude Code

### Main Entry Points
{self._format_entry_points(context['entry_points'])}

### Key Modules
{self._format_key_modules(context['key_modules'])}

### Custom Commands Available
- `/add-feature` - Scaffold new features (see .claude/commands/add_feature.md)
- `/fix-bug` - Fix bugs systematically (see .claude/commands/fix_bug.md)
- `/add-test` - Add comprehensive tests (see .claude/commands/add_test.md)

### Important Files
- Architecture details: `.claude/context/architecture.md`
- Code patterns: `.claude/context/patterns.md`
- Common pitfalls: `.claude/context/gotchas.md`
- Security rules: `.claude/context/security.md`

---

## Repository Overview

### Purpose
{context['purpose']}

### Key Capabilities
{self._format_capabilities(context['capabilities'])}

### Architecture Summary
{context['architecture_summary']}

---

## Code Organization

### Directory Structure
```
{self._format_directory_tree(context['structure'])}
```

### Module Responsibilities
{self._format_module_responsibilities(context['modules'])}

### Entry Points
{self._format_detailed_entry_points(context['entry_points'])}

---

## Coding Standards & Patterns

### Language-Specific Guidelines
{self._format_language_guidelines(context['primary_language'])}

### Design Patterns Used
{self._format_design_patterns(context['patterns'])}

### Naming Conventions
{self._format_naming_conventions(context['naming'])}

### Code Style
{self._format_code_style(context['style'])}

---

## Key Modules & Components

{self._format_detailed_modules(context['modules'])}

---

## Dependencies & Integration

### External Dependencies
{self._format_dependencies(context['dependencies']['external'])}

### Internal Dependencies
{self._format_internal_deps(context['dependencies']['internal'])}

### Integration Points
{self._format_integration_points(context['integrations'])}

---

## Testing Strategy

### Test Framework
{self._format_test_framework(context['testing'])}

### Running Tests
```bash
{self._format_test_commands(context['testing'])}
```

### Test Coverage
- Current: {context['testing']['coverage_current']}%
- Target: {context['testing']['coverage_target']}%
- Critical paths must be: {context['testing']['coverage_critical']}%

### Writing Tests
{self._format_test_guidelines(context['testing'])}

---

## Common Tasks

### Adding a New Feature
{self._format_feature_workflow(context)}

See: `.claude/workflows/feature_development.md` for detailed workflow

### Fixing a Bug
{self._format_bug_workflow(context)}

See: `.claude/workflows/bug_fixing.md` for detailed workflow

### Refactoring Code
{self._format_refactor_workflow(context)}

---

## Known Issues & Gotchas

{self._format_known_issues(context['known_issues'])}

See: `.claude/context/gotchas.md` for complete list

---

## Performance Considerations

### Bottlenecks
{self._format_bottlenecks(context['performance']['bottlenecks'])}

### Optimization Patterns
{self._format_optimization_patterns(context['performance']['patterns'])}

See: `.claude/context/performance.md` for details

---

## Security & Compliance

### Security Rules
{self._format_security_rules(context['security']['rules'])}

### Sensitive Data Handling
{self._format_data_handling(context['security']['data_handling'])}

See: `.claude/context/security.md` for complete guidelines

---

## Deployment & Operations

### Deployment Process
{self._format_deployment(context['deployment'])}

### Monitoring
{self._format_monitoring(context['monitoring'])}

### Troubleshooting
See: `TROUBLESHOOTING.md` for common issues

---

## Resources & References

### Documentation
- Architecture: `ARCHITECTURE.md`
- API Reference: `API_REFERENCE.md`
- Testing Guide: `TESTING_GUIDE.md`
- Dependencies: `DEPENDENCIES.md`
- Contributing: `CONTRIBUTING.md`
- Security: `SECURITY.md`

### Examples
- Good patterns: `.claude/examples/good_patterns/`
- Common tasks: `.claude/examples/common_tasks/`
- Templates: `.claude/templates/`

### Team Resources
- Team chat: {context.get('team_chat', '[Add team chat link]')}
- Wiki: {context.get('wiki', '[Add wiki link]')}
- Issue tracker: {context.get('issues', '[Add issue tracker link]')}

---

## Claude Code Usage Tips

### Best Practices
1. **Always read context first** - Review relevant .md files before coding
2. **Follow existing patterns** - Match established conventions
3. **Write tests** - All new code needs tests
4. **Update docs** - Keep documentation synchronized
5. **Check security** - Review security implications

### Common Patterns
- **Adding features:** Use `/add-feature` command
- **Fixing bugs:** Use `/fix-bug` command
- **Adding tests:** Use `/add-test` command
- **Refactoring:** Use `/refactor` command
- **Updating docs:** Use `/update-docs` command

### When to Ask for Help
- Architectural changes
- Security-critical code
- Performance-sensitive code
- Breaking changes
- External API integrations

---

*This file is auto-generated by doc-agent.*
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*For detailed information, explore the `.claude/` directory*
"""
        
        output_path = repo_path / 'CLAUDE.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated CLAUDE.md")
        return output_path
    
    def _generate_clinerules(self, repo_path: Path, context: Dict) -> Path:
        """Generate .clinerules file."""
        
        rules = {
            'language': context['primary_language'],
            'framework': context.get('framework'),
            'version': context.get('language_version'),
            
            'style': {
                'guide': context['style']['guide'],
                'line_length': context['style']['line_length'],
                'indent': context['style']['indent'],
                'quotes': context['style']['quotes']
            },
            
            'naming': context['naming'],
            
            'imports': {
                'order': ['stdlib', 'third_party', 'local'],
                'preferred': context['preferred_libraries'],
                'avoid': context['avoid_libraries']
            },
            
            'patterns': {
                'required': context['required_patterns'],
                'avoid': context['avoid_patterns']
            },
            
            'testing': {
                'framework': context['testing']['framework'],
                'coverage': {
                    'minimum': context['testing']['coverage_target'],
                    'critical_paths': 100
                },
                'required_for': context['testing']['required_for']
            },
            
            'documentation': {
                'required_for': context['documentation']['required_for'],
                'style': context['documentation']['style']
            },
            
            'security': {
                'required': context['security']['rules'],
                'sensitive_data': context['security']['data_handling']
            },
            
            'performance': {
                'required': context['performance']['rules']
            },
            
            'error_handling': {
                'required': context['error_handling']['rules']
            },
            
            'logging': {
                'required': context['logging']['rules'],
                'levels': context['logging']['levels']
            }
        }
        
        output_path = repo_path / '.clinerules'
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(rules, f, default_flow_style=False, sort_keys=False)
        
        print(f"✓ Generated .clinerules")
        return output_path
    
    def _generate_add_feature_command(self, commands_dir: Path, context: Dict) -> Path:
        """Generate add-feature command documentation."""
        
        content = f"""# Add Feature Command

This command helps scaffold a new feature following {context['repo_name']}'s patterns.

## Usage
```
/add-feature <feature-name> <feature-type>
```

## Feature Types

{self._format_feature_types(context)}

## What Gets Generated

{self._format_generated_structure(context)}

## Pattern Detection

Claude Code will analyze {len(context.get('similar_features', []))} similar features in this codebase to:
1. Extract common patterns
2. Apply consistent structure
3. Use established conventions
4. Maintain code style

## Files Modified

- New feature files in appropriate location
- Test files following test structure
- Documentation updates (API_REFERENCE.md, etc.)
- Configuration/routing updates if needed

## Best Practices

{self._format_feature_best_practices(context)}

## Examples

See `.claude/examples/common_tasks/add_feature_examples.md` for detailed examples.
"""
        
        output_path = commands_dir / 'add_feature.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated add_feature command")
        return output_path
    
    def _generate_fix_bug_command(self, commands_dir: Path, context: Dict) -> Path:
        """Generate fix-bug command documentation."""
        # Similar structure to add_feature
        pass
    
    def _generate_add_test_command(self, commands_dir: Path, context: Dict) -> Path:
        """Generate add-test command documentation."""
        # Similar structure to add_feature
        pass
    
    def _generate_gotchas(self, context_dir: Path, context: Dict) -> Path:
        """Generate gotchas.md with known issues and pitfalls."""
        
        content = f"""# Common Gotchas and Pitfalls for {context['repo_name']}

## Known Issues

{self._format_known_issues_detailed(context['known_issues'])}

## Tricky Parts of the Codebase

{self._format_tricky_parts(context['tricky_modules'])}

## Performance Traps

{self._format_performance_traps(context['performance']['traps'])}

## Security Concerns

{self._format_security_concerns(context['security']['concerns'])}

## Common Mistakes

{self._format_common_mistakes(context['common_mistakes'])}

## How to Avoid Issues

{self._format_avoidance_strategies(context)}
"""
        
        output_path = context_dir / 'gotchas.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated gotchas.md")
        return output_path
    
    # ========================================================================
    # Priority 2: High-Value Files
    # ========================================================================
    
    def _generate_priority_2(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate high-value files."""
        files = {}
        
        context_dir = repo_path / '.claude' / 'context'
        
        # Context files
        files['context/architecture.md'] = self._generate_architecture_context(
            context_dir, context
        )
        files['context/patterns.md'] = self._generate_patterns_context(
            context_dir, context
        )
        files['context/security.md'] = self._generate_security_context(
            context_dir, context
        )
        
        # Supporting documentation
        files['ARCHITECTURE.md'] = self._generate_architecture_doc(
            repo_path, context
        )
        files['API_REFERENCE.md'] = self._generate_api_reference(
            repo_path, context
        )
        files['TESTING_GUIDE.md'] = self._generate_testing_guide(
            repo_path, context
        )
        
        return files
    
    # ========================================================================
    # Priority 3: Enhancement Files
    # ========================================================================
    
    def _generate_priority_3(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate enhancement files."""
        files = {}
        
        if self.config.generate_examples:
            files.update(self._generate_examples(repo_path, context))
        
        if self.config.generate_templates:
            files.update(self._generate_templates(repo_path, context))
        
        if self.config.generate_workflows:
            files.update(self._generate_workflows(repo_path, context))
        
        # Additional documentation
        files['DEPENDENCIES.md'] = self._generate_dependencies_doc(repo_path, context)
        files['CONTRIBUTING.md'] = self._generate_contributing_doc(repo_path, context)
        files['TROUBLESHOOTING.md'] = self._generate_troubleshooting_doc(repo_path, context)
        
        return files
    
    def _generate_examples(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate code examples."""
        files = {}
        
        examples_dir = repo_path / '.claude' / 'examples'
        
        # Extract good patterns from codebase
        good_patterns = self._extract_good_patterns(context)
        for pattern_name, pattern_code in good_patterns.items():
            path = examples_dir / 'good_patterns' / f"{pattern_name}.{context['file_ext']}"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(pattern_code)
            files[f'examples/good_patterns/{pattern_name}'] = path
        
        # Document common tasks
        # ... similar approach
        
        return files
    
    def _generate_templates(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate code templates."""
        # Generate templates based on detected patterns
        pass
    
    def _generate_workflows(self, repo_path: Path, context: Dict) -> Dict[str, Path]:
        """Generate workflow documentation."""
        # Generate workflow docs
        pass
    
    # ========================================================================
    # Context Analysis
    # ========================================================================
    
    def _analyze_repo_context(self, repo_path: Path, kg_data: Dict) -> Dict:
        """
        Analyze repository and extract all context needed for file generation.
        
        This is where doc-agent's knowledge graph gets transformed into
        actionable context for Claude Code.
        """
        
        context = {
            'repo_name': repo_path.name,
            'repo_path': str(repo_path),
            
            # Language and framework
            'primary_language': self._detect_primary_language(kg_data),
            'framework': self._detect_framework(kg_data),
            'language_version': self._detect_language_version(kg_data),
            'file_ext': self._get_file_extension(kg_data),
            
            # Structure
            'structure': self._analyze_structure(kg_data),
            'modules': self._analyze_modules(kg_data),
            'entry_points': self._find_entry_points(kg_data),
            'key_modules': self._identify_key_modules(kg_data),
            
            # Patterns and conventions
            'patterns': self._identify_patterns(kg_data),
            'naming': self._analyze_naming_conventions(kg_data),
            'style': self._analyze_code_style(kg_data),
            
            # Dependencies
            'dependencies': {
                'external': self._analyze_external_deps(kg_data),
                'internal': self._analyze_internal_deps(kg_data)
            },
            'preferred_libraries': self._identify_preferred_libraries(kg_data),
            'avoid_libraries': self._identify_avoided_libraries(kg_data),
            
            # Testing
            'testing': self._analyze_testing(kg_data),
            
            # Architecture
            'architecture_summary': self._generate_arch_summary(kg_data),
            'purpose': self._infer_purpose(kg_data),
            'capabilities': self._identify_capabilities(kg_data),
            
            # Quality and issues
            'known_issues': self._extract_known_issues(kg_data),
            'common_mistakes': self._identify_common_mistakes(kg_data),
            'tricky_modules': self._identify_tricky_modules(kg_data),
            
            # Performance and security
            'performance': self._analyze_performance(kg_data),
            'security': self._analyze_security(kg_data),
            
            # Patterns to enforce
            'required_patterns': self._extract_required_patterns(kg_data),
            'avoid_patterns': self._extract_avoid_patterns(kg_data),
            
            # Documentation requirements
            'documentation': self._analyze_documentation_needs(kg_data),
            
            # Error handling and logging
            'error_handling': self._analyze_error_handling(kg_data),
            'logging': self._analyze_logging(kg_data),
            
            # Integration
            'integrations': self._identify_integrations(kg_data),
            
            # Deployment and operations
            'deployment': self._analyze_deployment(kg_data),
            'monitoring': self._analyze_monitoring(kg_data),
        }
        
        return context
    
    # ========================================================================
    # Helper Methods (Formatting)
    # ========================================================================
    
    def _format_entry_points(self, entry_points: List) -> str:
        """Format entry points as markdown list."""
        return '\n'.join(f"- `{ep['file']}` - {ep['description']}" 
                        for ep in entry_points[:5])
    
    def _format_key_modules(self, modules: List) -> str:
        """Format key modules as markdown list."""
        return '\n'.join(f"- **{m['name']}** - {m['purpose']}" 
                        for m in modules[:10])
    
    # ... many more formatting helper methods
    
    # ========================================================================
    # Analysis Methods (Extract from Knowledge Graph)
    # ========================================================================
    
    def _detect_primary_language(self, kg_data: Dict) -> str:
        """Detect primary programming language."""
        # Count files by extension
        file_counts = {}
        for file in kg_data.get('files_processed', []):
            ext = Path(file).suffix
            file_counts[ext] = file_counts.get(ext, 0) + 1
        
        if not file_counts:
            return 'unknown'
        
        primary_ext = max(file_counts, key=file_counts.get)
        
        ext_to_language = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.rs': 'Rust'
        }
        
        return ext_to_language.get(primary_ext, 'unknown')
    
    def _detect_framework(self, kg_data: Dict) -> Optional[str]:
        """Detect framework being used."""
        # Look for common framework indicators in dependencies
        entities = kg_data.get('entities', [])
        
        framework_indicators = {
            'django': 'Django',
            'flask': 'Flask',
            'fastapi': 'FastAPI',
            'react': 'React',
            'vue': 'Vue',
            'angular': 'Angular',
            'express': 'Express',
            'spring': 'Spring Boot'
        }
        
        for entity in entities:
            if entity.get('type') == 'import':
                name = entity.get('name', '').lower()
                for indicator, framework in framework_indicators.items():
                    if indicator in name:
                        return framework
        
        return None
    
    def _identify_patterns(self, kg_data: Dict) -> List[Dict]:
        """Identify design patterns used in codebase."""
        # Analyze relationships and structure to identify patterns
        patterns = []
        
        # Look for Factory pattern
        # Look for Singleton pattern
        # Look for Strategy pattern
        # etc.
        
        return patterns
    
    def _extract_known_issues(self, kg_data: Dict) -> List[Dict]:
        """Extract TODO, FIXME, XXX comments as known issues."""
        issues = []
        
        for file_path, metadata in kg_data.get('metadata', {}).items():
            # Parse code for TODO/FIXME comments
            # Extract issue descriptions
            pass
        
        return issues
    
    # ... many more analysis methods


# Example usage
if __name__ == "__main__":
    from unified_kg_builder import UnifiedKnowledgeGraphBuilder
    
    # Initialize
    kg_builder = UnifiedKnowledgeGraphBuilder()
    
    # Configure for different scenarios
    
    # Minimum viable (Priority 1 only, fastest)
    config_fast = GenerationConfig(priority_level=1)
    generator_fast = ClaudeCodeFileGenerator(kg_builder, config_fast)
    
    # Recommended (Priority 1+2)
    config_recommended = GenerationConfig(priority_level=2)
    generator_recommended = ClaudeCodeFileGenerator(kg_builder, config_recommended)
    
    # Complete (all priorities)
    config_complete = GenerationConfig(
        priority_level=3,
        generate_examples=True,
        generate_templates=True,
        generate_workflows=True
    )
    generator_complete = ClaudeCodeFileGenerator(kg_builder, config_complete)
    
    # Generate for a repository
    repo_path = Path("./my-repo")
    files = generator_recommended.generate_all_files(repo_path)
    
    print(f"\nGenerated {len(files)} files:")
    for file_type, file_path in files.items():
        print(f"  - {file_type}: {file_path}")
