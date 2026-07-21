# Integration Guide

## Overview

This guide shows how to integrate Self-Awakening-Scheduler into your project.

## Quick Start

### 1. Installation

```bash
git clone https://github.com/63894696/Self-Awakening-Scheduler.git
cd Self-Awakening-Scheduler
pip install -r requirements.txt
```

### 2. Configuration

Copy example configuration files and customize:

```bash
cp config/model_pool.example.json config/model_pool.json
cp config/resource_profiles.example.json config/resource_profiles.json
```

### 3. Basic Usage

```python
from src.smart_scheduler import SmartScheduler

# Initialize scheduler
scheduler = SmartScheduler()

# Select optimal model
result = scheduler.select_optimal_model("complex", "Refactor 15 files")
print(f"Selected: {result['selected_model']}")
```

## Integration Patterns

### Pattern 1: Direct Integration

Use the scheduler directly in your code:

```python
from src.smart_scheduler import SmartScheduler

def process_task(task_type, user_prompt):
    scheduler = SmartScheduler()
    result = scheduler.select_optimal_model(task_type, user_prompt)

    if "error" in result:
        # Handle error
        return None

    model_id = result["selected_model"]
    # Use model_id to call your AI API
    return call_ai_api(model_id, user_prompt)
```

### Pattern 2: Hook Integration

Integrate with Claude Code hooks:

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
            "system_prompt": f"Use model: {result['selected_model']}"
        }))

if __name__ == "__main__":
    main()
```

### Pattern 3: API Integration

Create a REST API for model selection:

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

### Pattern 4: Batch Processing

Process multiple tasks in batch:

```python
from src.smart_scheduler import SmartScheduler

def process_batch(tasks):
    scheduler = SmartScheduler()
    results = []

    for task in tasks:
        result = scheduler.select_optimal_model(task["type"], task["prompt"])
        results.append({
            "task": task,
            "selected_model": result.get("selected_model"),
            "score": result.get("score")
        })

    return results

# Usage
tasks = [
    {"type": "simple", "prompt": "Summarize this article"},
    {"type": "complex", "prompt": "Refactor 15 files"},
    {"type": "gui_operation", "prompt": "Fill form in browser"}
]

results = process_batch(tasks)
for r in results:
    print(f"Task: {r['task']['type']}, Model: {r['selected_model']}")
```

## Configuration

### Model Pool Configuration

Edit `config/model_pool.json`:

```json
{
  "models": {
    "your-model": {
      "provider": "your-provider",
      "base_url": "https://api.example.com/v1",
      "key_env": "YOUR_API_KEY",
      "payment_type": "free|subscription|payasyougo",
      "context_window": 131072,
      "strengths": ["code", "reasoning"],
      "cost_per_mtok": "free"
    }
  },
  "routing_rules": {
    "simple": {"preferred_router": "your-model"},
    "complex": {"preferred_router": "your-model"}
  }
}
```

### Resource Profiles Configuration

Edit `config/resource_profiles.json`:

```json
{
  "resource_profiles": {
    "your-platform": {
      "platform": "Your Platform",
      "models": {
        "your-model": {
          "status": "available",
          "quality_score": 7,
          "strengths": ["code", "reasoning"],
          "cost": "free",
          "rate_limit": "unknown",
          "daily_quota": "unknown"
        }
      }
    }
  }
}
```

## Environment Variables

Set these environment variables for API keys:

```bash
# OpenRouter
export OPENROUTER_API_KEY="your-openrouter-key"

# Ollama
export OLLAMA_API_KEY="your-ollama-key"
export OLLAMA_API_KEY2="your-second-ollama-key"  # Optional

# Moonshot
export MOONSHOT_API_KEY="your-moonshot-key"
export KIMI_CODING_KEY="your-kimi-coding-key"

# MiniMax
export MINIMAX_API_KEY="your-minimax-key"

# Agnes
export AGNES_API_KEY="your-agnes-key"
export AGNES_API_KEY2="your-second-agnes-key"  # Optional

# Bailian
export BAILIAN_API_KEY="your-bailian-key"
```

## Advanced Usage

### Custom Task Classification

```python
from src.smart_scheduler import SmartScheduler

class CustomScheduler(SmartScheduler):
    def classify_task(self, prompt):
        # Your custom classification logic
        if "custom" in prompt.lower():
            return "custom_type"
        return super().classify_task(prompt)

scheduler = CustomScheduler()
result = scheduler.select_optimal_model("custom_type", "custom task")
```

### Custom Scoring

```python
from src.smart_scheduler import SmartScheduler

class CustomScheduler(SmartScheduler):
    def score_model(self, model_id, profile, task_type, usage_stats):
        # Your custom scoring logic
        base_score, breakdown = super().score_model(model_id, profile, task_type, usage_stats)

        # Add custom bonus
        if task_type == "complex" and "long-context" in profile.get("strengths", []):
            base_score += 2

        return base_score, breakdown

scheduler = CustomScheduler()
result = scheduler.select_optimal_model("complex", "complex task")
```

### Custom Fallback Chains

```python
from src.gradient_router import GradientRouter

class CustomRouter(GradientRouter):
    def get_router_chain(self, task_type, pool):
        # Your custom fallback chain
        chain = super().get_router_chain(task_type, pool)

        # Add custom fallbacks
        chain.append({"model": "custom-fallback", "tier": 99, "cost": "free"})

        return chain

router = CustomRouter()
result = router.route_task("complex task")
```

## Testing

### Unit Tests

```python
import unittest
from src.smart_scheduler import SmartScheduler

class TestSmartScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = SmartScheduler()

    def test_select_optimal_model(self):
        result = self.scheduler.select_optimal_model("complex", "test task")
        self.assertIn("selected_model", result)
        self.assertIn("score", result)

    def test_classify_task(self):
        task_type = self.scheduler.classify_task("refactor 15 files")
        self.assertEqual(task_type, "complex")

if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
import unittest
from src.smart_scheduler import SmartScheduler

class TestIntegration(unittest.TestCase):
    def test_end_to_end(self):
        scheduler = SmartScheduler()

        # Test with real task
        result = scheduler.select_optimal_model("complex", "Refactor 15 files with OAuth2")

        self.assertNotIn("error", result)
        self.assertIn("selected_model", result)
        self.assertIn("score", result)
        self.assertIn("alternatives", result)

if __name__ == "__main__":
    unittest.main()
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

CMD ["python", "src/smart_scheduler.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: self-awakening-scheduler
spec:
  replicas: 3
  selector:
    matchLabels:
      app: self-awakening-scheduler
  template:
    metadata:
      labels:
        app: self-awakening-scheduler
    spec:
      containers:
      - name: scheduler
        image: self-awakening-scheduler:latest
        env:
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openrouter
        - name: OLLAMA_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: ollama
```

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
