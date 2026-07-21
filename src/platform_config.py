#!/usr/bin/env python3
"""
Platform-Specific Model Configurations
Supports Anthropic, OpenAI, Google, and other OpenAI-compatible APIs.
"""

import json
import os
import urllib.request
import urllib.error

class PlatformConfig:
    """Configuration for different AI platforms."""

    # Anthropic
    ANTHROPIC = {
        "name": "Anthropic",
        "base_url": "https://api.anthropic.com/v1",
        "models": {
            "claude-3-5-sonnet-20241022": {
                "context_window": 200000,
                "strengths": ["reasoning", "code", "long-context"],
                "cost_per_mtok": {"input": 3.0, "output": 15.0}
            },
            "claude-3-5-haiku-20241022": {
                "context_window": 200000,
                "strengths": ["fast", "code", "cost-effective"],
                "cost_per_mtok": {"input": 0.8, "output": 4.0}
            },
            "claude-3-opus-20240229": {
                "context_window": 200000,
                "strengths": ["reasoning", "code", "complex-tasks"],
                "cost_per_mtok": {"input": 15.0, "output": 75.0}
            }
        }
    }

    # OpenAI
    OPENAI = {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": {
            "gpt-4o": {
                "context_window": 128000,
                "strengths": ["reasoning", "code", "multimodal"],
                "cost_per_mtok": {"input": 2.5, "output": 10.0}
            },
            "gpt-4o-mini": {
                "context_window": 128000,
                "strengths": ["fast", "code", "cost-effective"],
                "cost_per_mtok": {"input": 0.15, "output": 0.6}
            },
            "gpt-4-turbo": {
                "context_window": 128000,
                "strengths": ["reasoning", "code", "long-context"],
                "cost_per_mtok": {"input": 10.0, "output": 30.0}
            }
        }
    }

    # Google
    GOOGLE = {
        "name": "Google",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "models": {
            "gemini-1.5-pro": {
                "context_window": 2097152,
                "strengths": ["long-context", "reasoning", "multimodal"],
                "cost_per_mtok": {"input": 3.5, "output": 10.5}
            },
            "gemini-1.5-flash": {
                "context_window": 1048576,
                "strengths": ["fast", "code", "cost-effective"],
                "cost_per_mtok": {"input": 0.075, "output": 0.3}
            }
        }
    }

    # DeepSeek
    DEEPSEEK = {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "models": {
            "deepseek-chat": {
                "context_window": 64000,
                "strengths": ["code", "reasoning", "cost-effective"],
                "cost_per_mtok": {"input": 0.14, "output": 0.28}
            },
            "deepseek-coder": {
                "context_window": 64000,
                "strengths": ["code", "programming", "cost-effective"],
                "cost_per_mtok": {"input": 0.14, "output": 0.28}
            }
        }
    }

    # Qwen
    QWEN = {
        "name": "Qwen",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": {
            "qwen-max": {
                "context_window": 32768,
                "strengths": ["reasoning", "code", "multilingual"],
                "cost_per_mtok": {"input": 0.04, "output": 0.12}
            },
            "qwen-plus": {
                "context_window": 131072,
                "strengths": ["reasoning", "code", "long-context"],
                "cost_per_mtok": {"input": 0.02, "output": 0.06}
            },
            "qwen-turbo": {
                "context_window": 8192,
                "strengths": ["fast", "cost-effective"],
                "cost_per_mtok": {"input": 0.008, "output": 0.02}
            }
        }
    }

    # Zhipu
    ZHIPU = {
        "name": "Zhipu",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "models": {
            "glm-4": {
                "context_window": 131072,
                "strengths": ["reasoning", "code", "multilingual"],
                "cost_per_mtok": {"input": 0.1, "output": 0.1}
            },
            "glm-4-flash": {
                "context_window": 131072,
                "strengths": ["fast", "cost-effective"],
                "cost_per_mtok": {"input": 0.01, "output": 0.01}
            }
        }
    }

    # Baichuan
    BAICHUAN = {
        "name": "Baichuan",
        "base_url": "https://api.baichuan-ai.com/v1",
        "models": {
            "Baichuan4": {
                "context_window": 32768,
                "strengths": ["reasoning", "code", "multilingual"],
                "cost_per_mtok": {"input": 0.1, "output": 0.1}
            },
            "Baichuan3-Turbo": {
                "context_window": 32768,
                "strengths": ["fast", "cost-effective"],
                "cost_per_mtok": {"input": 0.012, "output": 0.012}
            }
        }
    }

    # Yi
    YI = {
        "name": "Yi",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "models": {
            "yi-large": {
                "context_window": 32768,
                "strengths": ["reasoning", "code", "multilingual"],
                "cost_per_mtok": {"input": 0.02, "output": 0.02}
            },
            "yi-medium": {
                "context_window": 16384,
                "strengths": ["fast", "cost-effective"],
                "cost_per_mtok": {"input": 0.005, "output": 0.005}
            }
        }
    }

    @classmethod
    def get_platform(cls, platform_name):
        """Get platform configuration by name."""
        platforms = {
            "anthropic": cls.ANTHROPIC,
            "openai": cls.OPENAI,
            "google": cls.GOOGLE,
            "deepseek": cls.DEEPSEEK,
            "qwen": cls.QWEN,
            "zhipu": cls.ZHIPU,
            "baichuan": cls.BAICHUAN,
            "yi": cls.YI
        }
        return platforms.get(platform_name.lower())

    @classmethod
    def get_all_platforms(cls):
        """Get all platform configurations."""
        return {
            "anthropic": cls.ANTHROPIC,
            "openai": cls.OPENAI,
            "google": cls.GOOGLE,
            "deepseek": cls.DEEPSEEK,
            "qwen": cls.QWEN,
            "zhipu": cls.ZHIPU,
            "baichuan": cls.BAICHUAN,
            "yi": cls.YI
        }

    @classmethod
    def test_platform_availability(cls, platform_name, api_key):
        """Test if a platform is available with the given API key."""
        platform = cls.get_platform(platform_name)
        if not platform:
            return {"available": False, "reason": "unknown platform"}

        # Test with the first model
        model_id = list(platform["models"].keys())[0]
        model_config = platform["models"][model_id]

        test_data = json.dumps({
            "model": model_id,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5
        }).encode()

        try:
            req = urllib.request.Request(
                f"{platform['base_url']}/chat/completions",
                data=test_data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            resp = urllib.request.urlopen(req, timeout=10)
            return {"available": True, "status": resp.status, "model": model_id}
        except urllib.error.HTTPError as e:
            return {"available": False, "reason": f"HTTP {e.code}", "model": model_id}
        except Exception as e:
            return {"available": False, "reason": str(e), "model": model_id}

    @classmethod
    def discover_models(cls, platform_name, api_key):
        """Discover available models from a platform."""
        platform = cls.get_platform(platform_name)
        if not platform:
            return []

        # For now, return the hardcoded models
        # In the future, we can query the platform's model list API
        return [
            {
                "id": model_id,
                "name": model_id,
                "context_window": config["context_window"],
                "strengths": config["strengths"],
                "cost_per_mtok": config["cost_per_mtok"]
            }
            for model_id, config in platform["models"].items()
        ]
