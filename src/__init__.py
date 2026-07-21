# Self-Awakening Scheduler

Universal model resource scheduler for AI applications.

## Installation

```bash
pip install self-awakening-scheduler
```

## Quick Start

```python
from self_awakening_scheduler import SmartScheduler

# Initialize scheduler
scheduler = SmartScheduler()

# Select optimal model
result = scheduler.select_optimal_model("complex", "Refactor 15 files")
print(f"Selected: {result['selected_model']}")
```

## Features

- **Smart Model Selection**: Automatically selects the best model for each task
- **Multi-Platform Support**: Works with OpenRouter, Ollama, Moonshot, MiniMax
- **Dynamic Model Discovery**: Automatically discovers new models
- **Usage Tracking**: Monitors model usage and costs
- **Fallback Chains**: Graceful degradation when preferred models are unavailable

## Documentation

- [Methodology](https://github.com/63894696/Self-Awakening-Scheduler/blob/master/docs/METHODOLOGY.md)
- [Integration Guide](https://github.com/63894696/Self-Awakening-Scheduler/blob/master/docs/INTEGRATION.md)
- [Examples](https://github.com/63894696/Self-Awakening-Scheduler/blob/master/docs/EXAMPLES.md)

## License

MIT License
