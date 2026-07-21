#!/usr/bin/env python3
"""
Usage Monitor
Analyzes model usage patterns and provides optimization suggestions.
"""

import json
import os
from datetime import datetime
from collections import defaultdict

class UsageMonitor:
    """Monitor and analyze model usage."""

    def __init__(self, usage_log_path=None, model_pool_path=None):
        self.usage_log_path = usage_log_path or os.path.expanduser("~/.cc-switch/model_usage_log.json")
        self.model_pool_path = model_pool_path or os.path.expanduser("~/.cc-switch/model_pool.json")

    def load_json(self, path):
        """Load JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def analyze_usage(self):
        """Analyze model usage patterns."""
        log = self.load_json(self.usage_log_path)
        pool = self.load_json(self.model_pool_path)

        if not log.get("daily_usage"):
            return {"error": "No usage data available"}

        daily_usage = log["daily_usage"]

        # Aggregate statistics
        total_calls = defaultdict(int)
        total_tokens = defaultdict(int)
        daily_calls = defaultdict(lambda: defaultdict(int))

        for date, models in daily_usage.items():
            for model_id, stats in models.items():
                total_calls[model_id] += stats.get("calls", 0)
                total_tokens[model_id] += stats.get("tokens", 0)
                daily_calls[date][model_id] = stats.get("calls", 0)

        # Calculate trends
        dates = sorted(daily_usage.keys())
        recent_dates = dates[-7:] if len(dates) >= 7 else dates

        recent_usage = defaultdict(int)
        for date in recent_dates:
            for model_id, calls in daily_calls[date].items():
                recent_usage[model_id] += calls

        # Cost analysis
        cost_analysis = {}
        for model_id, calls in total_calls.items():
            model_info = pool.get("models", {}).get(model_id, {})
            cost_type = model_info.get("payment_type", "unknown")

            if cost_type == "free":
                cost = 0
            elif cost_type == "subscription":
                cost = "monthly_fee"
            elif cost_type == "payasyougo":
                tokens = total_tokens[model_id]
                cost = f"${tokens * 0.00003:.4f}"  # Rough estimate
            else:
                cost = "unknown"

            cost_analysis[model_id] = {
                "calls": calls,
                "tokens": total_tokens[model_id],
                "cost_type": cost_type,
                "estimated_cost": cost
            }

        # Optimization suggestions
        suggestions = []

        # Find underutilized models
        underutilized = []
        for model_id, info in pool.get("models", {}).items():
            if not info.get("_unavailable", False):
                calls = total_calls.get(model_id, 0)
                if calls == 0:
                    underutilized.append(model_id)

        if underutilized:
            suggestions.append({
                "type": "underutilized_models",
                "message": f"Consider using these free/available models: {', '.join(underutilized[:5])}",
                "models": underutilized[:5]
            })

        # Find overused models
        overused = []
        for model_id, calls in total_calls.items():
            if calls > 100:  # Arbitrary threshold
                overused.append(model_id)

        if overused:
            suggestions.append({
                "type": "overused_models",
                "message": f"Consider reducing usage of these models: {', '.join(overused[:5])}",
                "models": overused[:5]
            })

        # Cost optimization
        paid_models = [m for m, a in cost_analysis.items() if a["cost_type"] in ["payasyougo", "subscription"]]
        if paid_models:
            suggestions.append({
                "type": "cost_optimization",
                "message": f"Consider using free alternatives for: {', '.join(paid_models[:3])}",
                "models": paid_models[:3]
            })

        return {
            "total_calls": dict(total_calls),
            "total_tokens": dict(total_tokens),
            "recent_usage": dict(recent_usage),
            "cost_analysis": cost_analysis,
            "suggestions": suggestions,
            "summary": {
                "total_models_used": len(total_calls),
                "total_calls": sum(total_calls.values()),
                "total_tokens": sum(total_tokens.values()),
                "date_range": f"{dates[0]} to {dates[-1]}" if dates else "N/A"
            }
        }

    def print_report(self, analysis):
        """Print usage analysis report."""
        if "error" in analysis:
            print(f"Error: {analysis['error']}")
            return

        print("=" * 60)
        print("Model Usage Analysis Report")
        print("=" * 60)
        print()

        # Summary
        summary = analysis["summary"]
        print(f"Date Range: {summary['date_range']}")
        print(f"Total Models Used: {summary['total_models_used']}")
        print(f"Total Calls: {summary['total_calls']}")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print()

        # Top models by calls
        print("Top Models by Calls:")
        sorted_calls = sorted(analysis["total_calls"].items(), key=lambda x: x[1], reverse=True)
        for i, (model_id, calls) in enumerate(sorted_calls[:5], 1):
            tokens = analysis["total_tokens"][model_id]
            print(f"  {i}. {model_id}: {calls} calls, {tokens:,} tokens")
        print()

        # Cost analysis
        print("Cost Analysis:")
        for model_id, data in sorted(analysis["cost_analysis"].items(), key=lambda x: x[1]["calls"], reverse=True)[:5]:
            print(f"  {model_id}:")
            print(f"    Calls: {data['calls']}")
            print(f"    Tokens: {data['tokens']:,}")
            print(f"    Cost Type: {data['cost_type']}")
            print(f"    Estimated Cost: {data['estimated_cost']}")
        print()

        # Recent usage trend
        print("Recent Usage (Last 7 Days):")
        sorted_recent = sorted(analysis["recent_usage"].items(), key=lambda x: x[1], reverse=True)
        for i, (model_id, calls) in enumerate(sorted_recent[:5], 1):
            print(f"  {i}. {model_id}: {calls} calls")
        print()

        # Suggestions
        if analysis["suggestions"]:
            print("Optimization Suggestions:")
            for suggestion in analysis["suggestions"]:
                print(f"  • {suggestion['message']}")
            print()

        print("=" * 60)

def main():
    """Main entry point."""
    monitor = UsageMonitor()
    analysis = monitor.analyze_usage()
    monitor.print_report(analysis)

if __name__ == "__main__":
    main()
