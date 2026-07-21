# Methodology

## Overview

Self-Awakening-Scheduler uses a multi-dimensional scoring system to select the optimal model for each task. The system considers:

1. **Quality**: Model capability for the specific task type
2. **Cost**: Financial cost of using the model
3. **Availability**: Current availability and resource limits
4. **Usage**: Historical usage patterns to avoid overuse

## Scoring Formula

```
Total Score = Base Score + Match Bonus - Cost Penalty + Availability Bonus - Usage Penalty
```

### Components

#### Base Score (4-8 points)
- Based on model quality benchmarks
- Higher for more capable models
- Examples:
  - GPT-4: 8 points
  - Claude 3.5: 8 points
  - Kimi K3: 7 points
  - MiniMax M3: 6 points
  - Small models (7B-13B): 4-5 points

#### Match Bonus (0-4 points)
- Task type matching with model strengths
- +2 points per matching strength
- Task types:
  - **Simple**: Summary, translation, simple Q&A
  - **Medium**: Code review, documentation, short code
  - **Complex**: Multi-file refactoring, architecture, deep reasoning
  - **GUI Operation**: Browser automation, desktop GUI, Android emulator
  - **Voice Media**: TTS, video generation, audio generation

#### Cost Penalty (0-3 points)
- **Free**: 0 points
- **Subscription**: -1 point
- **Pay-as-you-go**: -3 points

#### Availability Bonus (0-3 points)
- **Available**: +3 points
- **Rate Limited**: 0 points
- **Unavailable**: -5 points

#### Usage Penalty (0-3 points)
- Prevents overuse of a single model
- Penalty increases with daily usage
- Capped at 3 points

## Task Classification

The system automatically classifies tasks based on keywords:

### Simple Tasks
- Keywords: 总结， summarize, 翻译， translate, 简单， simple, 解释， explain
- Examples: "Summarize this article", "Translate to English"

### Medium Tasks
- Keywords: 代码审查， code review, 文档， documentation, 短代码， short code
- Examples: "Review this code", "Generate documentation"

### Complex Tasks
- Keywords: 重构， refactor, 架构， architecture, 多文件， multiple files, oauth, jwt
- Examples: "Refactor 15 files", "Design system architecture"

### GUI Operation Tasks
- Keywords: 浏览器， browser, 点击， click, 表单， form, 桌面， desktop, android
- Examples: "Open browser and fill form", "Click submit button"

### Voice Media Tasks
- Keywords: tts, 语音， 音频， audio, 视频， video, 有声书， audiobook
- Examples: "Generate TTS for 127 chapters", "Create video"

## Fallback Chains

When a preferred model is unavailable, the system falls back to alternatives:

```
Tier 1 (Preferred) → Tier 2 (Fallback) → Tier 3 (Emergency)
```

### Example Fallback Chain for Complex Tasks

1. **Kimi K3 PayG** (highest quality, pay-as-you-go)
2. **Kimi K3 Monthly** (good quality, subscription)
3. **NVIDIA Nemotron 3 Ultra** (free, available)
4. **MiniMax M3** (subscription, TTS/video)

## Resource Management

### Rate Limiting

The system tracks rate limits for each model:
- **Requests per minute**: Prevents hitting API rate limits
- **Daily quota**: Prevents exceeding daily usage limits
- **Concurrent requests**: Prevents overwhelming the API

### Usage Tracking

The system tracks usage patterns:
- **Daily calls**: Number of API calls per day
- **Token usage**: Total tokens consumed per day
- **Cost estimation**: Rough cost calculation based on token usage

### Optimization Suggestions

The system provides optimization suggestions:
- **Underutilized models**: Suggests free/available models not being used
- **Overused models**: Suggests reducing usage of frequently used models
- **Cost optimization**: Suggests free alternatives to paid models

## Dynamic Model Discovery

The system automatically discovers new models from:
- **OpenRouter**: Free models (`:free` suffix)
- **Ollama Cloud**: Cloud models (free tier)

New models are automatically added to the model pool with:
- Provider information
- API endpoint
- Context window size
- Strengths and capabilities

## Best Practices

### 1. Model Pool Configuration

- Keep the model pool up to date
- Remove unavailable models
- Add new models as they become available
- Use meaningful strength tags

### 2. Resource Profiles

- Set realistic quality scores
- Configure rate limits based on provider documentation
- Track daily quotas to avoid overuse
- Use cost tracking for budget management

### 3. Routing Rules

- Define clear routing rules for each task type
- Use fallback chains for reliability
- Consider cost vs. quality tradeoffs
- Test routing decisions with real tasks

### 4. Usage Monitoring

- Monitor usage patterns regularly
- Identify underutilized models
- Optimize for cost and quality
- Adjust routing rules based on usage data

## Example Workflow

1. **User submits a task**: "Refactor 15 files with OAuth2"
2. **Task classification**: Complex task (keywords: refactor, 15 files, OAuth2)
3. **Model scoring**:
   - Kimi K3 PayG: 8 (base) + 4 (match) - 3 (cost) + 3 (available) = 12
   - Kimi K3 Monthly: 7 (base) + 4 (match) - 1 (cost) + 3 (available) = 13
   - NVIDIA Nemotron 3 Ultra: 7 (base) + 4 (match) - 0 (cost) + 3 (available) = 14
4. **Model selection**: NVIDIA Nemotron 3 Ultra (highest score)
5. **Task execution**: Use selected model for the task
6. **Usage tracking**: Update usage statistics
7. **Optimization**: Provide suggestions for future tasks

## Advanced Features

### Custom Scoring

You can customize the scoring system by modifying the `score_model` method:

```python
def custom_score_model(model_id, profile, task_type, usage_stats):
    base_score = profile.get("quality_score", 5)

    # Your custom logic here
    if task_type == "complex" and "long-context" in profile.get("strengths", []):
        base_score += 2

    return base_score
```

### Custom Task Types

You can add custom task types by modifying the `task_match` dictionary:

```python
task_match = {
    "custom_task": ["custom", "keywords", "here"],
    # ... existing task types
}
```

### Custom Fallback Chains

You can define custom fallback chains in the configuration:

```json
{
  "fallback_chain": {
    "custom-model": ["fallback-1", "fallback-2", "fallback-3"]
  }
}
```

## Troubleshooting

### Model Not Available

**Problem**: Model is marked as unavailable but should be available.

**Solution**:
1. Check API key is set in environment variables
2. Check API endpoint is correct
3. Check rate limits and quotas
4. Manually test the model with a simple request

### High Costs

**Problem**: Costs are higher than expected.

**Solution**:
1. Review routing rules to prefer free models
2. Check usage patterns for overused models
3. Use cost optimization suggestions
4. Consider using subscription models for frequent tasks

### Poor Quality

**Problem**: Selected model produces poor quality results.

**Solution**:
1. Review quality scores in resource profiles
2. Check task type classification
3. Verify model strengths match task requirements
4. Consider using higher quality models for complex tasks

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
