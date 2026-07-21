#!/usr/bin/env python3
"""
Gradient Router
Implements tiered routing strategy: quality first, cost second, availability always.
"""

import json
import os
import urllib.request
import urllib.error

class GradientRouter:
    """Gradient router with fallback chains."""

    def __init__(self, model_pool_path=None):
        self.model_pool_path = model_pool_path or os.path.expanduser("~/.cc-switch/model_pool.json")

    def load_model_pool(self):
        """Load model pool with availability status."""
        try:
            with open(self.model_pool_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"models": {}, "routing_rules": {}}

    def get_available_models(self, pool):
        """Get list of available models (not marked as unavailable)."""
        models = pool.get("models", {})
        available = {}
        for model_id, config in models.items():
            if not config.get("_unavailable", False):
                available[model_id] = config
        return available

    def test_model_availability(self, model_id, config):
        """Test if a model is actually available by making a test call."""
        base_url = config.get("base_url", "")
        key_env = config.get("key_env", "")

        if not base_url or not key_env:
            return False

        api_key = os.environ.get(key_env, "")
        if not api_key:
            return False

        test_url = f"{base_url}/chat/completions"
        test_data = json.dumps({
            "model": model_id.split("/")[-1] if "/" in model_id else model_id,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5
        }).encode()

        try:
            req = urllib.request.Request(
                test_url,
                data=test_data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            resp = urllib.request.urlopen(req, timeout=10)
            return resp.status == 200
        except:
            return False

    def get_router_chain(self, task_type, pool):
        """Get router chain for a task type, ordered by quality and cost."""
        rules = pool.get("routing_rules", {})
        rule = rules.get(task_type, rules.get("medium", {}))

        # Build chain: preferred -> fallback -> emergency
        chain = []

        # Tier 1: Preferred router (highest quality)
        preferred = rule.get("preferred_router")
        if preferred:
            chain.append({"model": preferred, "tier": 1, "cost": "high" if "payg" in preferred else "low"})

        # Tier 2: Fallback router (good quality, lower cost)
        fallback = rule.get("fallback_router")
        if fallback and fallback != preferred:
            chain.append({"model": fallback, "tier": 2, "cost": "low"})

        # Tier 3: Emergency fallback (any available model)
        emergency = ["minimax-m3", "agnes-2.0-flash", "glm-5.2-openrouter"]
        for model in emergency:
            if model not in [c["model"] for c in chain]:
                chain.append({"model": model, "tier": 3, "cost": "free"})

        return chain

    def select_router(self, task_type, pool, test_availability=False):
        """Select the best available router for a task type."""
        chain = self.get_router_chain(task_type, pool)
        available_models = self.get_available_models(pool)

        for candidate in chain:
            model_id = candidate["model"]

            # Check if model is in available pool
            if model_id not in available_models:
                continue

            # Optionally test actual availability
            if test_availability:
                config = available_models[model_id]
                if not self.test_model_availability(model_id, config):
                    continue

            return {
                "model": model_id,
                "tier": candidate["tier"],
                "cost": candidate["cost"],
                "config": available_models[model_id]
            }

        # No router available, return None
        return None

    def route_task(self, user_prompt, task_type=None):
        """Main routing function with gradient fallback."""
        pool = self.load_model_pool()

        # Auto-classify if task_type not provided
        if not task_type:
            prompt_lower = user_prompt.lower()
            if any(kw in prompt_lower for kw in ["浏览器", "browser", "点击", "click", "表单", "form"]):
                task_type = "gui_operation"
            elif any(kw in prompt_lower for kw in ["tts", "语音", "音频", "audio", "视频", "video"]):
                task_type = "voice_media"
            elif any(kw in prompt_lower for kw in ["重构", "refactor", "架构", "architecture", "多文件", "oauth", "jwt"]):
                task_type = "complex"
            elif any(kw in prompt_lower for kw in ["总结", "summarize", "翻译", "translate", "简单", "simple"]):
                task_type = "simple"
            else:
                task_type = "medium"

        # Select router with gradient fallback
        router = self.select_router(task_type, pool, test_availability=False)

        if not router:
            # Emergency: use any available model
            available = self.get_available_models(pool)
            if available:
                model_id = list(available.keys())[0]
                router = {
                    "model": model_id,
                    "tier": 99,
                    "cost": "unknown",
                    "config": available[model_id]
                }
            else:
                return {"error": "No available models"}

        return {
            "task_type": task_type,
            "router": router["model"],
            "tier": router["tier"],
            "cost": router["cost"],
            "fallback_chain": [c["model"] for c in self.get_router_chain(task_type, pool)]
        }

def main():
    """Main entry point."""
    router = GradientRouter()

    # Test with a complex task
    test_prompt = "请帮我重构整个项目的认证模块，涉及 15 个文件，包括 OAuth2 流程、JWT 签发验证、数据库迁移和前后端联调"
    result = router.route_task(test_prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
