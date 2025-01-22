from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from tc_analyzer_lib.metrics.heatmaps.analytics_hourly import AnalyticsHourly
from tc_analyzer_lib.utils.mongo import MongoSingleton


class TestHeatmapsAnalyticsBaseWithFilter(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.platform_id = "3456789"
        self.raw_data_model = AnalyticsHourly(self.platform_id, testing=True)
        self.mongo_client = MongoSingleton.get_instance(
            skip_singleton=True
        ).get_client()
        self.mongo_client[self.platform_id].drop_collection("rawmemberactivities")

    def tearDown(self) -> None:
        # cleanup
        self.mongo_client.drop_database(self.platform_id)

    async def test_get_hourly_analytics_single_date(self):
        sample_raw_data = [
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"threadId": 7000, "channelId": 2000},
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
            filters={"interactions.name": "mention"},
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

    async def test_get_hourly_analytics_single_date_irrelevant_filter(self):
        """
        test the hourly analytics with a filter that all data will be skipped
        """
        sample_raw_data = [
            {
                "author_id": 9000,
                "date": datetime(2023, 1, 1),
                "source_id": "10000",
                "metadata": {"threadId": 7000, "channelId": 2000},
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
            filters={"interactions.name": "reply"},
            user_ids=[9000],
        )

        self.assertIsInstance(hourly_analytics, dict)
        self.assertEqual(hourly_analytics, {})
