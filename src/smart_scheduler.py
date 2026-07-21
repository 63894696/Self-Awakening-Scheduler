#!/usr/bin/env python3
"""
Smart Resource Scheduler
Routes tasks to optimal model based on quality, cost, availability, and resource limits.
"""

import json
import os
from datetime import datetime

class SmartScheduler:
    """Smart scheduler for model selection."""

    def __init__(self, resource_profiles_path=None, usage_log_path=None):
        self.resource_profiles_path = resource_profiles_path or os.path.expanduser("~/.cc-switch/resource_profiles.json")
        self.usage_log_path = usage_log_path or os.path.expanduser("~/.cc-switch/model_usage_log.json")

    def load_json(self, path):
        """Load JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_json(self, path, data):
        """Save JSON file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_usage_stats(self):
        """Get model usage statistics."""
        log = self.load_json(self.usage_log_path)
        today = datetime.now().strftime("%Y-%m-%d")

        if "daily_usage" not in log:
            log["daily_usage"] = {}
        if today not in log["daily_usage"]:
            log["daily_usage"][today] = {}

        return log

    def update_usage_stats(self, model_id, tokens_used):
        """Update model usage statistics."""
        log = self.get_usage_stats()
        today = datetime.now().strftime("%Y-%m-%d")

        if model_id not in log["daily_usage"][today]:
            log["daily_usage"][today][model_id] = {"calls": 0, "tokens": 0}

        log["daily_usage"][today][model_id]["calls"] += 1
        log["daily_usage"][today][model_id]["tokens"] += tokens_used

        self.save_json(self.usage_log_path, log)

    def check_quota(self, model_id, profile):
        """Check if model has quota available."""
        usage = self.get_usage_stats()
        today = datetime.now().strftime("%Y-%m-%d")

        daily_usage = usage.get("daily_usage", {}).get(today, {}).get(model_id, {"calls": 0, "tokens": 0})

        # Check rate limit (if known)
        rate_limit = profile.get("rate_limit")
        if rate_limit and rate_limit != "unknown":
            # Simplified check - in production, track per-minute usage
            pass

        # Check daily quota (if known)
        daily_quota = profile.get("daily_quota")
        if daily_quota and daily_quota != "unknown":
            if "limit" in daily_quota.lower():
                monthly_calls = sum(
                    day.get(model_id, {}).get("calls", 0)
                    for day in usage.get("daily_usage", {}).values()
                )
                if monthly_calls > 100:  # Arbitrary limit
                    return False, "monthly_limit_exceeded"

        return True, "ok"

    def score_model(self, model_id, profile, task_type, usage_stats):
        """Score a model for a given task type."""
        base_score = profile.get("quality_score", 5)

        # Task type matching
        strengths = profile.get("strengths", [])
        task_match = {
            "simple": ["simple", "fast", "small-model"],
            "medium": ["code", "general-purpose"],
            "complex": ["long-context", "reasoning", "large-model"],
            "gui_operation": ["routing", "general-purpose"],
            "voice_media": ["tts", "video", "image"]
        }

        match_bonus = 0
        for strength in strengths:
            if strength in task_match.get(task_type, []):
                match_bonus += 2

        # Cost penalty
        cost = profile.get("cost", "unknown")
        cost_penalty = {"free": 0, "monthly": 1, "payg": 3}.get(cost, 2)

        # Availability bonus
        status = profile.get("status", "unknown")
        availability_bonus = 3 if status == "available" else -5

        # Usage penalty (avoid overused models)
        today = datetime.now().strftime("%Y-%m-%d")
        daily_usage = usage_stats.get("daily_usage", {}).get(today, {}).get(model_id, {"calls": 0})
        usage_penalty = min(daily_usage["calls"] // 10, 3)  # Cap at 3

        total_score = base_score + match_bonus - cost_penalty + availability_bonus - usage_penalty

        return total_score, {
            "base": base_score,
            "match": match_bonus,
            "cost": -cost_penalty,
            "availability": availability_bonus,
            "usage": -usage_penalty
        }

    def select_optimal_model(self, task_type, user_prompt=""):
        """Select optimal model for a task."""
        profiles = self.load_json(self.resource_profiles_path)
        usage_stats = self.get_usage_stats()

        # Get all available models
        candidates = []
        for platform, platform_data in profiles.get("resource_profiles", {}).items():
            models = platform_data.get("models", {})
            for model_id, profile in models.items():
                # Check quota
                has_quota, quota_reason = self.check_quota(model_id, profile)
                if not has_quota:
                    continue

                # Score model
                score, breakdown = self.score_model(model_id, profile, task_type, usage_stats)

                candidates.append({
                    "model_id": model_id,
                    "platform": platform,
                    "score": score,
                    "breakdown": breakdown,
                    "profile": profile
                })

        # Sort by score (descending)
        candidates.sort(key=lambda x: x["score"], reverse=True)

        if not candidates:
            return {"error": "No available models with quota"}

        best = candidates[0]

        return {
            "task_type": task_type,
            "selected_model": best["model_id"],
            "platform": best["platform"],
            "score": best["score"],
            "breakdown": best["breakdown"],
            "alternatives": [c["model_id"] for c in candidates[1:4]],  # Top 3 alternatives
            "usage_stats": usage_stats.get("daily_usage", {}).get(datetime.now().strftime("%Y-%m-%d"), {})
        }

# Convenience function for backward compatibility
def select_optimal_model(task_type, user_prompt=""):
    """Select optimal model for a task."""
    scheduler = SmartScheduler()
    return scheduler.select_optimal_model(task_type, user_prompt)

def update_usage_stats(model_id, tokens_used):
    """Update model usage statistics."""
    scheduler = SmartScheduler()
    scheduler.update_usage_stats(model_id, tokens_used)
