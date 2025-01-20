from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from tc_analyzer_lib.metrics.heatmaps.analytics_hourly import AnalyticsHourly
from tc_analyzer_lib.utils.mongo import MongoSingleton


class TestHeatmapsAnalyticsBaseNoFilter(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.platform_id = "3456789"
        self.raw_data_model = AnalyticsHourly(self.platform_id)
        self.mongo_client = MongoSingleton.get_instance(
            skip_singleton=True
        ).get_client()
        self.mongo_client[self.platform_id].drop_collection("rawmemberactivities")

    async def test_get_hourly_analytics_single_date(self):
        sample_raw_data = [
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            }
        ]
        self.mongo_client[self.platform_id]["rawmemberactivities"].insert_many(
            sample_raw_data
        )
        hourly_analytics = await self.raw_data_model.get_hourly_analytics(
            day=datetime(2023, 1, 1).date(),
            activity="interactions",
            user_ids=[9000],
        )

        # mentioning 2 people at hour 0
        expected_analytics = [
            2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.assertIsInstance(hourly_analytics, dict)
        self.assertEqual(len(hourly_analytics[9000]), 24)
        self.assertEqual(hourly_analytics[9000], expected_analytics)

    async def test_get_hourly_analytics_multiple_date(self):
        sample_raw_data = [
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
            {
                "author_id": 9001,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
        ]
        self.mongo_client[self.platform_id]["rawmemberactivities"].insert_many(
            sample_raw_data
        )
        hourly_analytics = await self.raw_data_model.get_hourly_analytics(
            day=datetime(2023, 1, 1).date(),
            activity="interactions",
            user_ids=[9000],
        )

        expected_analytics = [
            2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.assertIsInstance(hourly_analytics, dict)
        self.assertEqual(len(hourly_analytics[9000]), 24)
        self.assertEqual(hourly_analytics[9000], expected_analytics)

    async def test_get_hourly_analytics_multiple_date_multiple_authors(self):
        sample_raw_data = [
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
            {
                "author_id": 9001,
                "date": datetime(2023, 1, 2),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
        ]
        self.mongo_client[self.platform_id]["rawmemberactivities"].insert_many(
            sample_raw_data
        )
        hourly_analytics = await self.raw_data_model.get_hourly_analytics(
            day=datetime(2023, 1, 1).date(),
            activity="interactions",
            user_ids=[9000],
        )

        expected_analytics = [
            4,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.assertIsInstance(hourly_analytics, dict)
        self.assertEqual(len(hourly_analytics[9000]), 24)
        self.assertEqual(hourly_analytics[9000], expected_analytics)

    async def test_get_hourly_analytics_multiple_date_multiple_data(self):
        sample_raw_data = [
            {
                "author_id": 9001,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
            {
                "author_id": 9001,
                "date": datetime(2023, 1, 2),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
            {
                "author_id": 9001,
                "date": datetime(2023, 1, 2),
                "source_id": "10000",
                "metadata": {"thread_id": 7000, "channel_id": 2000},
                "actions": [{"name": "message", "type": "receiver"}],
                "interactions": [
                    {
                        "name": "mention",
                        "users_engaged_id": [9003, 9002],
                        "type": "emitter",
                    }
                ],
            },
        ]
        self.mongo_client[self.platform_id]["rawmemberactivities"].insert_many(
            sample_raw_data
        )
        hourly_analytics = await self.raw_data_model.get_hourly_analytics(
            day=datetime(2023, 1, 2).date(),
            activity="interactions",
            user_ids=[9001],
        )

        expected_analytics = [
            4,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.assertIsInstance(hourly_analytics, dict)
        self.assertEqual(len(hourly_analytics[9001]), 24)
        self.assertEqual(hourly_analytics[9001], expected_analytics)
