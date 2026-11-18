import asyncio
import unittest
from decimal import Decimal

from starter import recommend_price, sample_fetch_offers


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    def assert_recommendation(self, result, price, decision):
        self.assertEqual(set(result), {"price", "decision", "reason"})
        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal(price))
        self.assertEqual(result["decision"], decision)
        self.assertIsInstance(result["reason"], str)
        self.assertTrue(result["reason"].strip())

    async def test_sample_calculation(self):
        result = await recommend_price(
            sample_fetch_offers, Decimal("4900.00"), Decimal("4500.00")
        )

        self.assert_recommendation(result, "4728.00", "APPLY")

    async def test_timeout_cancels_request_and_keeps_current_price(self):
        cancelled = asyncio.Event()

        async def slow_fetch():
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        result = await recommend_price(
            slow_fetch, Decimal("40.00"), Decimal("50.00"), timeout_s=0.01
        )

        self.assert_recommendation(result, "40.00", "HOLD")
        self.assertTrue(cancelled.is_set())


if __name__ == "__main__":
    unittest.main()
