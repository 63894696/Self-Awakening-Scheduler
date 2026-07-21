# Examples

## Overview

This document provides practical examples of using Self-Awakening-Scheduler.

## Basic Examples

### Example 1: Simple Task

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Simple task: Summarize an article
result = scheduler.select_optimal_model("simple", "Summarize this article in 3 sentences")

print(f"Selected model: {result['selected_model']}")
print(f"Platform: {result['platform']}")
print(f"Score: {result['score']}")
print(f"Alternatives: {result['alternatives']}")
```

**Expected Output:**
```
Selected model: gpt-oss:20b
Platform: ollama
Score: 12
Alternatives: ['nvidia/nemotron-nano-9b-v2:free', 'agnes-2.0-flash', 'ollama-gpt-oss:120b']
```

### Example 2: Complex Task

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Complex task: Refactor multiple files
result = scheduler.select_optimal_model("complex", "Refactor 15 files with OAuth2 and JWT")

print(f"Selected model: {result['selected_model']}")
print(f"Platform: {result['platform']}")
print(f"Score: {result['score']}")
print(f"Breakdown: {result['breakdown']}")
```

**Expected Output:**
```
Selected model: nemotron-3-ultra
Platform: ollama
Score: 14
Breakdown: {'base': 7, 'match': 4, 'cost': 0, 'availability': 3, 'usage': 0}
```

### Example 3: GUI Operation

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# GUI operation: Browser automation
result = scheduler.select_optimal_model("gui_operation", "Open browser and fill form")

print(f"Selected model: {result['selected_model']}")
print(f"Platform: {result['platform']}")
print(f"Score: {result['score']}")
```

**Expected Output:**
```
Selected model: gpt-oss:120b
Platform: ollama
Score: 12
```

### Example 4: Voice Media

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Voice media: TTS generation
result = scheduler.select_optimal_model("voice_media", "Generate TTS for 127 chapters")

print(f"Selected model: {result['selected_model']}")
print(f"Platform: {result['platform']}")
print(f"Score: {result['score']}")
```

**Expected Output:**
```
Selected model: minimax-m3
Platform: ollama
Score: 16
```

## Advanced Examples

### Example 5: Batch Processing

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Process multiple tasks
tasks = [
    {"type": "simple", "prompt": "Summarize this article"},
    {"type": "complex", "prompt": "Refactor 15 files"},
    {"type": "gui_operation", "prompt": "Fill form in browser"},
    {"type": "voice_media", "prompt": "Generate TTS"}
]

for task in tasks:
    result = scheduler.select_optimal_model(task["type"], task["prompt"])
    print(f"Task: {task['type']}, Model: {result['selected_model']}, Score: {result['score']}")
```

**Expected Output:**
```
Task: simple, Model: gpt-oss:20b, Score: 12
Task: complex, Model: nemotron-3-ultra, Score: 14
Task: gui_operation, Model: gpt-oss:120b, Score: 12
Task: voice_media, Model: minimax-m3, Score: 16
```

### Example 6: Cost Optimization

```python
from src.smart_scheduler import SmartScheduler

scheduler = SmartScheduler()

# Compare costs for different task types
task_types = ["simple", "medium", "complex"]

for task_type in task_types:
    result = scheduler.select_optimal_model(task_type, "test task")

    # Estimate cost
    cost_type = result.get("breakdown", {}).get("cost", 0)
    cost = "Free" if cost_type == 0 else f"${abs(cost_type) * 0.01:.2f}"

    print(f"Task: {task_type}, Model: {result['selected_model']}, Cost: {cost}")
```

**Expected Output:**
```
Task: simple, Model: gpt-oss:20b, Cost: Free
Task: medium, Model: kimi-k3-monthly, Cost: $0.01
Task: complex, Model: nemotron-3-ultra, Cost: Free
```

### Example 7: Usage Monitoring

```python
from src.usage_monitor import UsageMonitor

monitor = UsageMonitor()

# Analyze usage
analysis = monitor.analyze_usage()

if "error" not in analysis:
    print(f"Total calls: {analysis['summary']['total_calls']}")
    print(f"Total tokens: {analysis['summary']['total_tokens']}")

    # Print suggestions
    for suggestion in analysis.get("suggestions", []):
        print(f"• {suggestion['message']}")
```

**Expected Output:**
```
Total calls: 4
Total tokens: 48
• Consider using these free/available models: agnes-2.0-flash, kimi-k3-monthly, kimi-k3-payg
```

### Example 8: Model Pool Update

```python
from src.model_pool_updater import ModelPoolUpdater

updater = ModelPoolUpdater()

# Update model pool
updater.update()

# Check for new models
print("Model pool updated successfully")
```

**Expected Output:**
```
=== Checking existing models ===
✅ agnes-2.0-flash: OK
❌ kimi-k3-monthly: HTTP 503
✅ minimax-m3: OK

=== Discovering new models ===
🆕 Found new model: openrouter-nvidia/nemotron-3-ultra-550b-a55b:free
🆕 Found new model: ollama-gpt-oss:120b

✅ Model pool updated: 42 models
```

## Integration Examples

### Example 9: Claude Code Hook

```python
# ~/.claude/hooks/user_prompt_submit_router.py
import sys
import json
from src.smart_scheduler import SmartScheduler

def main():
    user_prompt = sys.stdin.read().strip()

    scheduler = SmartScheduler()
    result = scheduler.select_optimal_model("complex", user_prompt)

    if "error" not in result:
        print(json.dumps({
            "action": "inject",
            "system_prompt": f"Use model: {result['selected_model']}",
            "router_decision": {
                "task_type": result["task_type"],
                "router": result["selected_model"],
                "score": result["score"]
            }
        }))

if __name__ == "__main__":
    main()
```

### Example 10: REST API

```python
from flask import Flask, request, jsonify
from src.smart_scheduler import SmartScheduler

app = Flask(__name__)
scheduler = SmartScheduler()

@app.route("/select-model", methods=["POST"])
def select_model():
    data = request.json
    task_type = data.get("task_type")
    user_prompt = data.get("user_prompt", "")

    result = scheduler.select_optimal_model(task_type, user_prompt)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**Usage:**
```bash
curl -X POST http://localhost:5000/select-model \
  -H "Content-Type: application/json" \
  -d '{"task_type": "complex", "user_prompt": "Refactor 15 files"}'
```

**Response:**
```json
{
  "task_type": "complex",
  "selected_model": "nemotron-3-ultra",
  "platform": "ollama",
  "score": 14,
  "breakdown": {
    "base": 7,
    "match": 4,
    "cost": 0,
    "availability": 3,
    "usage": 0
  },
  "alternatives": [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nemotron-3-super",
    "nvidia/nemotron-3-super-120b-a12b:free"
  ]
}
```

### Example 11: CLI Tool

```python
#!/usr/bin/env python3
import sys
import json
from src.smart_scheduler import SmartScheduler

def main():
    if len(sys.argv) < 2:
        print("Usage: cli.py <task_type> [user_prompt]")
        sys.exit(1)

    task_type = sys.argv[1]
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else ""

    scheduler = SmartScheduler()
    result = scheduler.select_optimal_model(task_type, user_prompt)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python cli.py complex "Refactor 15 files"
```

**Output:**
```json
{
  "task_type": "complex",
  "selected_model": "nemotron-3-ultra",
  "platform": "ollama",
  "score": 14,
  "breakdown": {
    "base": 7,
    "match": 4,
    "cost": 0,
    "availability": 3,
    "usage": 0
  },
  "alternatives": [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nemotron-3-super",
    "nvidia/nemotron-3-super-120b-a12b:free"
  ]
}
```

## Best Practices

### 1. Model Pool Management

- **Regular Updates**: Run `model_pool_updater.py` daily to discover new models
- **Availability Checks**: Verify model availability before adding to pool
- **Quality Scores**: Set realistic quality scores based on benchmarks
- **Cost Tracking**: Track costs for budget management

### 2. Task Classification

- **Keyword Matching**: Use specific keywords for accurate classification
- **Context Awareness**: Consider task context for better classification
- **Custom Types**: Add custom task types for specific use cases
- **Fallback Rules**: Define fallback rules for ambiguous tasks

### 3. Resource Management

- **Rate Limiting**: Respect API rate limits
- **Quota Tracking**: Monitor daily quotas
- **Usage Patterns**: Avoid overusing a single model
- **Cost Optimization**: Prefer free models for simple tasks

### 4. Error Handling

- **Graceful Degradation**: Fall back to alternative models when preferred models fail
- **Retry Logic**: Implement retry logic for transient failures
- **Logging**: Log errors for debugging
- **Monitoring**: Monitor model health and availability

## Troubleshooting

### Common Issues

**Issue**: Model not found
**Solution**: Check `config/model_pool.json` and ensure model is defined

**Issue**: API key not working
**Solution**: Check environment variables are set correctly

**Issue**: Rate limit exceeded
**Solution**: Check `resource_profiles.json` for rate limit settings

**Issue**: High costs
**Solution**: Review routing rules and prefer free models

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

scheduler = SmartScheduler()
result = scheduler.select_optimal_model("complex", "test task")
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](../LICENSE) for details.
