# AI Code Modernization Platform - Quick Reference

## 🚀 Quick Start Commands

### Single Repository Processing
```python
from unified_kg_builder import UnifiedKnowledgeGraphBuilder
from context_doc_generator import ContextualDocumentationGenerator

# Initialize
kg_builder = UnifiedKnowledgeGraphBuilder()
doc_gen = ContextualDocumentationGenerator(kg_builder)

# Generate documentation
docs = doc_gen.generate_repo_documentation("./my-repo")
```

### Batch Processing (Command Line)
```bash
# Process all repos with 8 parallel workers
python batch_repo_processor.py /path/to/repos --workers 8

# Process only specific repos
python batch_repo_processor.py /path/to/repos --filter "data-"

# Sequential processing (for debugging)
python batch_repo_processor.py /path/to/repos --parallel False

# Custom output location
python batch_repo_processor.py /path/to/repos --output custom_report.json
```

### Batch Processing (Python)
```python
from batch_repo_processor import BatchRepoDocumentationGenerator

batch_processor = BatchRepoDocumentationGenerator(kg_builder)

# Process all repos in parallel
results = batch_processor.process_organization_repos(
    repos_root="/path/to/repos",
    parallel=True,
    max_workers=8,
    filter_pattern="data-*"  # Optional
)

# Generate reports
batch_processor.results = results
batch_processor.generate_summary_report("report.json")
batch_processor.export_repo_index("index.md")
```

---

## 📁 Generated Files Reference

### Per Repository
```
repository/
├── CLAUDE.md                 # AI agent primary context
├── AGENT_INSTRUCTIONS.md     # Agent-specific guidelines
├── ARCHITECTURE.md           # Architecture details
├── API_REFERENCE.md          # API documentation
├── TESTING_GUIDE.md          # Testing strategy
└── DEPENDENCIES.md           # Dependency analysis
```

### Organization-Wide
```
output/
├── documentation_report.json     # Processing results
├── repo_index.md                # Repository listing
└── conversion_log.json          # Detailed processing log
```

---

## 🎯 Common Workflows

### Workflow 1: Initial Assessment (Pilot)
```python
# Step 1: Select 10 pilot repos
pilot_repos = [
    "/repos/data-pipeline",
    "/repos/api-service",
    # ... 8 more
]

# Step 2: Process each
for repo in pilot_repos:
    docs = doc_gen.generate_repo_documentation(repo)
    print(f"✓ {repo}: {len(docs)} files generated")

# Step 3: Review output manually
# Check CLAUDE.md files for quality
```

### Workflow 2: Incremental Rollout
```python
# Week 1: Process 50 repos
results_week1 = batch_processor.process_organization_repos(
    repos_root="/repos",
    filter_pattern="team-a-*",
    max_workers=4
)

# Week 2: Process next 50 repos
results_week2 = batch_processor.process_organization_repos(
    repos_root="/repos",
    filter_pattern="team-b-*",
    max_workers=4
)

# Continue until all repos are processed
```

### Workflow 3: Update Existing Documentation
```python
# Re-process repos that have changed
changed_repos = get_recently_modified_repos(days=7)

for repo in changed_repos:
    docs = doc_gen.generate_repo_documentation(repo)
    print(f"✓ Updated: {repo}")
```

### Workflow 4: Full Organization Processing
```python
# One-time full processing
batch_processor = BatchRepoDocumentationGenerator(kg_builder)

results = batch_processor.process_organization_repos(
    repos_root="/all-repos",
    parallel=True,
    max_workers=8
)

# Generate comprehensive report
summary = batch_processor.generate_summary_report()
print(f"Processed: {summary['metadata']['successful']} repos")
```

---

## 📊 Monitoring & Metrics

### Check Processing Status
```python
# View summary statistics
summary = batch_processor.generate_summary_report()

print(f"Total: {summary['metadata']['total_repos']}")
print(f"Success: {summary['metadata']['successful']}")
print(f"Failed: {summary['metadata']['failed']}")
print(f"Avg Duration: {summary['statistics']['avg_duration']:.1f}s")
```

### View Failed Repositories
```python
failed_repos = [
    r for r in batch_processor.results 
    if r['status'] == 'failed'
]

for repo in failed_repos:
    print(f"❌ {repo['repo_name']}: {repo['error']}")
```

### Calculate Coverage
```python
total_repos = count_all_repos("/repos")
processed = len(batch_processor.results)
coverage = (processed / total_repos) * 100

print(f"Documentation Coverage: {coverage:.1f}%")
```

---

## 🔧 Configuration Examples

### Adjust Parallel Workers
```python
# Low resources: 2-4 workers
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    max_workers=2
)

# Medium resources: 4-8 workers
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    max_workers=6
)

# High resources: 8-16 workers
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    max_workers=12
)
```

### Filter Specific Repositories
```python
# By naming pattern
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    filter_pattern="microservice-"
)

# By team
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    filter_pattern="team-data-"
)

# By project
results = batch_processor.process_organization_repos(
    repos_root="/repos",
    filter_pattern="project-alpha-"
)
```

---

## 🐛 Troubleshooting

### Issue: Out of Memory
```python
# Solution 1: Reduce parallel workers
max_workers=2  # Instead of 8

# Solution 2: Process in smaller batches
batch_size = 50
for i in range(0, len(all_repos), batch_size):
    batch = all_repos[i:i+batch_size]
    process_batch(batch)
```

### Issue: Slow Processing
```python
# Check average duration
stats = batch_processor._calculate_statistics()
print(f"Avg duration: {stats['avg_duration']:.1f}s")
print(f"Max duration: {stats['max_duration']:.1f}s")

# If too slow, increase parallelism
max_workers=12  # Increase from default
```

### Issue: Failed Repositories
```python
# Get detailed error information
failed = [r for r in results if r['status'] == 'failed']

for repo in failed:
    print(f"\nRepo: {repo['repo_name']}")
    print(f"Error: {repo['error']}")
    print(f"Path: {repo['repo']}")
    
# Retry failed repos
for repo in failed:
    try:
        docs = doc_gen.generate_repo_documentation(repo['repo'])
        print(f"✓ Retry successful: {repo['repo_name']}")
    except Exception as e:
        print(f"✗ Still failing: {repo['repo_name']}")
```

### Issue: Missing Files
```python
# Verify KG builder is working
kg_data = kg_builder.process_directory("./test-repo")
print(f"Files processed: {len(kg_data['files_processed'])}")
print(f"Entities: {len(kg_data['entities'])}")

# Check if specific file types are being processed
file_types = {}
for file in kg_data['files_processed']:
    ext = Path(file).suffix
    file_types[ext] = file_types.get(ext, 0) + 1
print(f"File types: {file_types}")
```

---

## 📈 Performance Tips

### Optimize for Speed
```python
# Use maximum safe parallelism
import os
max_workers = os.cpu_count() - 1  # Leave one core free

# Process in batches
batch_processor.process_organization_repos(
    repos_root="/repos",
    parallel=True,
    max_workers=max_workers
)
```

### Optimize for Memory
```python
# Lower parallelism, sequential processing
batch_processor.process_organization_repos(
    repos_root="/repos",
    parallel=False  # Or max_workers=2
)

# Clear results between batches
batch_processor.results = []  # Clear memory
```

### Optimize for Large Scale
```python
# Process incrementally
from pathlib import Path

repos = list(Path("/repos").rglob(".git"))
batch_size = 100

for i in range(0, len(repos), batch_size):
    batch = repos[i:i+batch_size]
    print(f"Processing batch {i//batch_size + 1}")
    
    # Process batch
    batch_results = process_batch(batch)
    
    # Save intermediate results
    save_results(f"results_batch_{i//batch_size}.json", batch_results)
    
    # Clear memory
    del batch_results
```

---

## 🎯 Pre-Flight Checklist

### Before Pilot (10-20 repos)
- [ ] Your KG builder is working correctly
- [ ] Selected diverse pilot repositories
- [ ] Tested on 1-2 repos manually
- [ ] Review generated CLAUDE.md files
- [ ] Stakeholders are informed

### Before Scale (100+ repos)
- [ ] Pilot was successful (>80% success rate)
- [ ] Infrastructure can handle load
- [ ] Monitoring is in place
- [ ] Backup/rollback plan exists
- [ ] Team is trained

### Before Full Deployment (1000+ repos)
- [ ] Controlled rollout was successful
- [ ] Performance is acceptable
- [ ] Error rate is low (<5%)
- [ ] Documentation quality is high
- [ ] Management approval secured

---

## 📚 Key Metrics to Track

### Processing Metrics
```python
metrics = {
    'total_repos': len(all_repos),
    'processed': len(successful),
    'failed': len(failed),
    'success_rate': len(successful) / len(all_repos) * 100,
    'avg_duration': sum(durations) / len(durations),
    'total_time': total_elapsed_time
}
```

### Quality Metrics
```python
quality = {
    'repos_with_tests': count_repos_with_tests(),
    'avg_coverage': calculate_avg_coverage(),
    'documented_apis': count_api_docs(),
    'issues_identified': count_todos_and_fixmes()
}
```

### Business Metrics
```python
business = {
    'repos_ready_for_agents': count_fully_documented(),
    'technical_debt_identified': sum_technical_debt(),
    'modernization_opportunities': count_improvement_areas(),
    'estimated_value': calculate_estimated_value()
}
```

---

## 💡 Best Practices Summary

### Do's ✅
- Start with a small pilot (10-20 repos)
- Review generated docs for quality
- Adjust parallelism based on resources
- Save intermediate results frequently
- Monitor progress and errors
- Communicate with stakeholders

### Don'ts ❌
- Don't process all repos at once initially
- Don't ignore failed repositories
- Don't skip the pilot phase
- Don't forget to backup existing docs
- Don't over-provision workers (resource exhaustion)
- Don't deploy without testing

---

## 🔗 Quick Links

### Documentation
- Full README: `README.md`
- Executive Pitch: `executive_pitch.md`
- Pipeline Diagrams: `pipeline_diagrams.md`
- Sample Output: `CLAUDE_md_sample.md`

### Code
- Main Generator: `context_doc_generator.py`
- Batch Processor: `batch_repo_processor.py`

### Support
- GitHub Issues: [Your Repo]
- Team Slack: #ai-modernization
- Documentation: [Wiki Link]

---

## 📞 Getting Help

### Common Questions
**Q: How long does processing take?**
A: Average 30-60 seconds per repo, depending on size.

**Q: What if processing fails?**
A: Check logs, retry individually, reduce parallelism.

**Q: How often should I re-run?**
A: Weekly for active repos, monthly for stable repos.

**Q: Can I customize the output?**
A: Yes, modify templates in `context_doc_generator.py`.

### Support Channels
- Slack: #ai-code-modernization
- Email: ai-platform-team@company.com
- Office Hours: Tuesdays 2-3pm

---

*Last Updated: 2024-11-19*
