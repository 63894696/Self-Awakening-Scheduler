# Self-Awakening-Scheduler

> Universal model resource scheduler for AI applications — intelligently routes tasks to optimal models based on quality, cost, and availability.

## Features

- **Smart Model Selection**: Automatically selects the best model for each task based on quality, cost, and availability
- **Multi-Platform Support**: Works with OpenRouter, Ollama, Moonshot, MiniMax, and any OpenAI-compatible API
- **Dynamic Model Discovery**: Automatically discovers new models from OpenRouter and Ollama Cloud
- **Usage Tracking**: Monitors model usage, costs, and provides optimization suggestions
- **Fallback Chains**: Graceful degradation when preferred models are unavailable
- **Resource Profiles**: Configurable resource limits, quality scores, and cost tracking

## Quick Start

### 1. Installation

```bash
git clone https://github.com/63894696/Self-Awakening-Scheduler.git
cd Self-Awakening-Scheduler
pip install -r requirements.txt
```

### 2. Configuration

Copy the example configuration files and customize with your API keys:

```bash
cp config/model_pool.example.json config/model_pool.json
cp config/resource_profiles.example.json config/resource_profiles.json
```

Edit `config/model_pool.json` with your API keys and model preferences:

```json
{
  "models": {
    "your-model-id": {
      "provider": "your-provider",
      "base_url": "https://api.example.com/v1",
      "key_env": "YOUR_API_KEY",
      "payment_type": "free|subscription|payasyougo",
      "context_window": 131072,
      "strengths": ["code", "reasoning"],
      "cost_per_mtok": "free"
    }
  }
}
```

### 3. Usage

```python
from src.smart_scheduler import SmartScheduler

# Initialize scheduler
scheduler = SmartScheduler()

# Select optimal model for a task
result = scheduler.select_optimal_model("complex", "Refactor 15 files with OAuth2")
print(f"Selected model: {result['selected_model']}")
print(f"Platform: {result['platform']}")
print(f"Score: {result['score']}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Application                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Smart Scheduler                             │
│  - Task classification (simple/medium/complex/gui/voice)   │
│  - Model scoring (quality + cost + availability + usage)   │
│  - Optimal selection with fallback chains                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Model Pool Manager                          │
│  - Dynamic model discovery (OpenRouter, Ollama)            │
│  - Availability checking                                    │
│  - Resource limit tracking                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Model Providers                             │
│  - OpenRouter (free models)                                │
│  - Ollama Cloud (free models)                              │
│  - Moonshot (Kimi K3)                                      │
│  - MiniMax (TTS/Video)                                     │
│  - Custom OpenAI-compatible APIs                           │
└─────────────────────────────────────────────────────────────┘
```

## Documentation

- [Methodology](docs/METHODOLOGY.md) — How the scheduler works
- [Integration Guide](docs/INTEGRATION.md) — How to integrate into your project
- [Examples](docs/EXAMPLES.md) — Usage examples and best practices
- [API Reference](docs/API.md) — Complete API documentation

## Configuration

### Model Pool Configuration

`config/model_pool.json` defines your available models:

```json
{
  "version": "0.1",
  "updated": "2026-07-21",
  "models": {
    "agnes-2.0-flash": {
      "provider": "AgnesAI",
      "base_url": "https://apihub.agnes-ai.com/v1",
      "key_env": "AGNES_API_KEY",
      "payment_type": "subscription",
      "context_window": 131072,
      "strengths": ["code-review", "simple-routing"],
      "cost_per_mtok": "free-monthly"
    }
  },
  "routing_rules": {
    "simple": {"preferred_router": "agnes-2.0-flash"},
    "complex": {"preferred_router": "kimi-k3-payg"}
  }
}
```

### Resource Profiles Configuration

`config/resource_profiles.json` defines resource limits and quality scores:

```json
{
  "resource_profiles": {
    "openrouter": {
      "platform": "OpenRouter",
      "models": {
        "nvidia/nemotron-3-ultra-550b-a55b:free": {
          "status": "available",
          "quality_score": 7,
          "strengths": ["large-model", "reasoning"],
          "cost": "free"
        }
      }
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by the need for intelligent model routing in AI applications
- Built for the AI community to optimize model usage and costs
- Special thanks to OpenRouter and Ollama for providing free model access
