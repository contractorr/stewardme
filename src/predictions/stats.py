"""Compute prediction accuracy stats."""

from .store import PredictionStore


class PredictionStats:
    @staticmethod
    def compute(store: PredictionStore) -> dict:
        """Compute stats from store — delegates to store.get_stats()."""
        return store.get_stats()
