#!/usr/bin/env python3
"""
Unit tests for SmartScheduler
"""

import unittest
import json
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_scheduler import SmartScheduler

class TestSmartScheduler(unittest.TestCase):
    """Test SmartScheduler functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.scheduler = SmartScheduler()

    def test_load_json(self):
        """Test loading JSON files."""
        # Test with non-existent file
        result = self.scheduler.load_json("/nonexistent/file.json")
        self.assertEqual(result, {})

    def test_save_json(self):
        """Test saving JSON files."""
        test_data = {"test": "data"}
        test_path = os.path.join(os.path.dirname(__file__), "test_output.json")

        self.scheduler.save_json(test_path, test_data)
        self.assertTrue(os.path.exists(test_path))

        # Clean up
        os.remove(test_path)

    def test_get_usage_stats(self):
        """Test getting usage statistics."""
        stats = self.scheduler.get_usage_stats()
        self.assertIn("daily_usage", stats)

    def test_update_usage_stats(self):
        """Test updating usage statistics."""
        self.scheduler.update_usage_stats("test-model", 100)
        stats = self.scheduler.get_usage_stats()
        today = datetime.now().strftime("%Y-%m-%d")

        self.assertIn(today, stats["daily_usage"])
        self.assertIn("test-model", stats["daily_usage"][today])

    def test_check_quota(self):
        """Test quota checking."""
        profile = {"rate_limit": "unknown", "daily_quota": "unknown"}
        has_quota, reason = self.scheduler.check_quota("test-model", profile)
        self.assertTrue(has_quota)
        self.assertEqual(reason, "ok")

    def test_score_model(self):
        """Test model scoring."""
        profile = {
            "quality_score": 7,
            "strengths": ["code", "reasoning"],
            "cost": "free",
            "status": "available"
        }
        usage_stats = {"daily_usage": {}}

        score, breakdown = self.scheduler.score_model("test-model", profile, "complex", usage_stats)

        self.assertGreater(score, 0)
        self.assertIn("base", breakdown)
        self.assertIn("match", breakdown)
        self.assertIn("cost", breakdown)
        self.assertIn("availability", breakdown)
        self.assertIn("usage", breakdown)

    def test_select_optimal_model(self):
        """Test optimal model selection."""
        result = self.scheduler.select_optimal_model("complex", "test task")

        # Should return a result (may be error if no models available)
        self.assertIsInstance(result, dict)

    def test_classify_task(self):
        """Test task classification."""
        # Test simple task
        task_type = self.scheduler.classify_task("Summarize this article")
        self.assertEqual(task_type, "simple")

        # Test complex task
        task_type = self.scheduler.classify_task("Refactor 15 files with OAuth2")
        self.assertEqual(task_type, "complex")

        # Test GUI task
        task_type = self.scheduler.classify_task("Open browser and click button")
        self.assertEqual(task_type, "gui_operation")

        # Test voice media task
        task_type = self.scheduler.classify_task("Generate TTS for audiobook")
        self.assertEqual(task_type, "voice_media")

class TestGradientRouter(unittest.TestCase):
    """Test GradientRouter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from gradient_router import GradientRouter
        self.router = GradientRouter()

    def test_load_model_pool(self):
        """Test loading model pool."""
        pool = self.router.load_model_pool()
        self.assertIsInstance(pool, dict)

    def test_get_available_models(self):
        """Test getting available models."""
        pool = {"models": {"test-model": {"_unavailable": False}}}
        available = self.router.get_available_models(pool)
        self.assertIn("test-model", available)

    def test_get_router_chain(self):
        """Test getting router chain."""
        pool = {"routing_rules": {"complex": {"preferred_router": "test-model"}}}
        chain = self.router.get_router_chain("complex", pool)
        self.assertIsInstance(chain, list)

class TestModelPoolUpdater(unittest.TestCase):
    """Test ModelPoolUpdater functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from model_pool_updater import ModelPoolUpdater
        self.updater = ModelPoolUpdater()

    def test_load_model_pool(self):
        """Test loading model pool."""
        pool = self.updater.load_model_pool()
        self.assertIsInstance(pool, dict)

    def test_check_model_availability(self):
        """Test model availability checking."""
        config = {"base_url": "", "key_env": ""}
        result = self.updater.check_model_availability("test-model", config)
        self.assertFalse(result["available"])
        self.assertEqual(result["reason"], "missing config")

class TestUsageMonitor(unittest.TestCase):
    """Test UsageMonitor functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from usage_monitor import UsageMonitor
        self.monitor = UsageMonitor()

    def test_analyze_usage(self):
        """Test usage analysis."""
        analysis = self.monitor.analyze_usage()
        # Should return error if no data
        self.assertIn("error", analysis)

if __name__ == "__main__":
    unittest.main()
