#!/usr/bin/env python3
"""
Model Pool Updater
Automatically discovers new models from OpenRouter and Ollama Cloud, updates availability status.
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime

class ModelPoolUpdater:
    """Updates model pool with discovered models and availability status."""

    def __init__(self, model_pool_path=None):
        self.model_pool_path = model_pool_path or os.path.expanduser("~/.cc-switch/model_pool.json")
        self.backup_path = self.model_pool_path.replace(".json", ".backup.json")

    def load_model_pool(self):
        """Load current model pool."""
        try:
            with open(self.model_pool_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading model pool: {e}")
            return {"models": {}, "routing_rules": {}}

    def save_model_pool(self, pool):
        """Save model pool with backup."""
        # Backup current
        if os.path.exists(self.model_pool_path):
            with open(self.model_pool_path, 'r', encoding='utf-8') as f:
                backup = json.load(f)
            with open(self.backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup, f, indent=2, ensure_ascii=False)

        # Save new
        os.makedirs(os.path.dirname(self.model_pool_path), exist_ok=True)
        with open(self.model_pool_path, 'w', encoding='utf-8') as f:
            json.dump(pool, f, indent=2, ensure_ascii=False)

    def check_model_availability(self, model_id, config):
        """Check if a model is available by testing its endpoint."""
        base_url = config.get("base_url", "")
        key_env = config.get("key_env", "")

        if not base_url or not key_env:
            return {"available": False, "reason": "missing config"}

        api_key = os.environ.get(key_env, "")
        if not api_key:
            return {"available": False, "reason": f"missing env var {key_env}"}

        # Test with a minimal request
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
            return {"available": True, "status": resp.status}
        except urllib.error.HTTPError as e:
            return {"available": False, "reason": f"HTTP {e.code}", "retryable": e.code in [429, 500, 502, 503]}
        except Exception as e:
            return {"available": False, "reason": str(e), "retryable": True}

    def discover_openrouter_models(self):
        """Discover free models from OpenRouter."""
        new_models = {}
        openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")

        if not openrouter_key:
            return new_models

        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {openrouter_key}"}
            )
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read())

            for model in data.get("data", []):
                model_id = model.get("id", "")
                if ":free" in model_id:
                    new_models[f"openrouter-{model_id}"] = {
                        "provider": "OpenRouter",
                        "base_url": "https://openrouter.ai/api/v1",
                        "key_env": "OPENROUTER_API_KEY",
                        "payment_type": "free",
                        "context_window": model.get("context_length", 131072),
                        "strengths": ["free", "varies"],
                        "notes": f"OpenRouter free model: {model_id}"
                    }
        except Exception as e:
            print(f"Error discovering OpenRouter models: {e}")

        return new_models

    def discover_ollama_models(self):
        """Discover cloud models from Ollama."""
        new_models = {}
        ollama_key = os.environ.get("OLLAMA_API_KEY", "")

        if not ollama_key:
            return new_models

        try:
            req = urllib.request.Request(
                "https://ollama.com/v1/models",
                headers={"Authorization": f"Bearer {ollama_key}"}
            )
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read())

            for model in data.get("data", []):
                model_id = model.get("id", "")
                new_models[f"ollama-{model_id}"] = {
                    "provider": "Ollama",
                    "base_url": "https://ollama.com/v1",
                    "key_env": "OLLAMA_API_KEY",
                    "payment_type": "free",
                    "context_window": 131072,
                    "strengths": ["local", "free"],
                    "notes": f"Ollama cloud model: {model_id}"
                }
        except Exception as e:
            print(f"Error discovering Ollama models: {e}")

        return new_models

    def update(self):
        """Main update function."""
        pool = self.load_model_pool()
        if not pool:
            return False

        models = pool.get("models", {})
        updated = False

        # Check existing models
        print("=== Checking existing models ===")
        for model_id, config in list(models.items()):
            result = self.check_model_availability(model_id, config)
            status = "✅" if result["available"] else "❌"
            reason = result.get("reason", "OK")
            print(f"{status} {model_id}: {reason}")

            if not result["available"] and not result.get("retryable", False):
                config["_unavailable"] = True
                config["_last_check"] = datetime.now().isoformat()
                updated = True
            elif result["available"]:
                if "_unavailable" in config:
                    del config["_unavailable"]
                    updated = True

        # Discover new models
        print("\n=== Discovering new models ===")
        openrouter_models = self.discover_openrouter_models()
        ollama_models = self.discover_ollama_models()

        for model_id, config in {**openrouter_models, **ollama_models}.items():
            if model_id not in models:
                print(f"🆕 Found new model: {model_id}")
                models[model_id] = config
                updated = True

        # Update timestamp
        pool["updated"] = datetime.now().isoformat()

        if updated:
            self.save_model_pool(pool)
            print(f"\n✅ Model pool updated: {len(models)} models")
        else:
            print(f"\n⏸️ No changes: {len(models)} models")

        return True

def main():
    """Main entry point."""
    updater = ModelPoolUpdater()
    updater.update()

if __name__ == "__main__":
    main()
