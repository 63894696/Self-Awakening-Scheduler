#!/usr/bin/env python3
"""
Platform Discovery
Automatically discovers and tests models from multiple platforms.
"""

import json
import os
from platform_config import PlatformConfig

class PlatformDiscovery:
    """Discover models from multiple platforms."""

    def __init__(self):
        self.platforms = PlatformConfig.get_all_platforms()

    def test_all_platforms(self):
        """Test all platforms for availability."""
        results = {}

        for platform_name, platform_config in self.platforms.items():
            print(f"\n=== Testing {platform_config['name']} ===")

            # Get API key from environment
            key_env = f"{platform_name.upper()}_API_KEY"
            api_key = os.environ.get(key_env, "")

            if not api_key:
                print(f"❌ No API key found for {platform_name} (set {key_env})")
                results[platform_name] = {"available": False, "reason": "no api key"}
                continue

            # Test platform
            result = PlatformConfig.test_platform_availability(platform_name, api_key)
            results[platform_name] = result

            if result["available"]:
                print(f"✅ {platform_name} available (model: {result['model']})")
            else:
                print(f"❌ {platform_name} unavailable: {result['reason']}")

        return results

    def discover_all_models(self):
        """Discover models from all available platforms."""
        all_models = {}

        for platform_name, platform_config in self.platforms.items():
            print(f"\n=== Discovering models from {platform_config['name']} ===")

            # Get API key from environment
            key_env = f"{platform_name.upper()}_API_KEY"
            api_key = os.environ.get(key_env, "")

            if not api_key:
                print(f"❌ No API key found for {platform_name}")
                continue

            # Discover models
            models = PlatformConfig.discover_models(platform_name, api_key)
            all_models[platform_name] = models

            print(f"Found {len(models)} models:")
            for model in models[:5]:  # Show first 5
                print(f"  - {model['id']} (context: {model['context_window']})")

            if len(models) > 5:
                print(f"  ... and {len(models) - 5} more")

        return all_models

    def create_model_pool_entry(self, platform_name, model_config):
        """Create a model pool entry for a discovered model."""
        platform = self.platforms[platform_name]

        return {
            "provider": platform["name"],
            "base_url": platform["base_url"],
            "key_env": f"{platform_name.upper()}_API_KEY",
            "payment_type": "payasyougo",
            "context_window": model_config["context_window"],
            "strengths": model_config["strengths"],
            "cost_per_mtok": model_config["cost_per_mtok"],
            "notes": f"{platform['name']} model: {model_config['id']}"
        }

def main():
    """Main entry point."""
    discovery = PlatformDiscovery()

    # Test all platforms
    print("=== Platform Availability Test ===")
    availability = discovery.test_all_platforms()

    # Discover models from available platforms
    print("\n=== Model Discovery ===")
    available_platforms = [p for p, r in availability.items() if r.get("available")]

    if available_platforms:
        print(f"Available platforms: {', '.join(available_platforms)}")
        models = discovery.discover_all_models()

        # Create model pool entries
        print("\n=== Model Pool Entries ===")
        model_pool = {}
        for platform_name, platform_models in models.items():
            for model in platform_models:
                model_id = f"{platform_name}-{model['id']}"
                model_pool[model_id] = discovery.create_model_pool_entry(platform_name, model)
                print(f"  {model_id}: {model['id']}")

        # Save to file
        output_path = os.path.expanduser("~/.cc-switch/discovered_models.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(model_pool, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Discovered {len(model_pool)} models, saved to {output_path}")
    else:
        print("No platforms available. Please set API keys for the platforms you want to use.")

if __name__ == "__main__":
    main()
