"""
NovelForge AI — Timeline & Spatial Travel Service
Validates chronological event order and flags impossible travel anomalies.
"""
from __future__ import annotations
import math
from typing import Dict, Any, List, Optional, Tuple
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.schemas.narrative_models import StoryEventEntity, StoryEventType


class TimelineService:
    def __init__(self, repository: NarrativeRepository):
        self.repo = repository

    def calculate_location_distance(
        self,
        loc1: Dict[str, Any],
        loc2: Dict[str, Any]
    ) -> float:
        """Euclidean coordinate distance between two locations (in kilometers/li)."""
        c1 = loc1.get("coordinates", {"x": 0.0, "y": 0.0})
        c2 = loc2.get("coordinates", {"x": 0.0, "y": 0.0})
        dx = c1.get("x", 0.0) - c2.get("x", 0.0)
        dy = c1.get("y", 0.0) - c2.get("y", 0.0)
        return math.sqrt(dx * dx + dy * dy)

    def validate_travel_continuity(
        self,
        story_id: str,
        character_id: str,
        character_name: str,
        from_location_id: str,
        to_location_id: str,
        start_day: int,
        arrival_day: int,
        standard_travel_speed_km_per_day: float = 40.0
    ) -> Dict[str, Any]:
        """
        Detects whether travel between two locations is physically possible in the allotted story days.
        """
        locations = {loc["id"]: loc for loc in self.repo.get_locations(story_id)}
        loc_from = locations.get(from_location_id)
        loc_to = locations.get(to_location_id)

        if not loc_from or not loc_to:
            return {"is_valid": True, "reason": "Unknown location coordinates, bypass check."}

        distance_km = self.calculate_location_distance(loc_from, loc_to)
        days_passed = max(0, arrival_day - start_day)
        required_days = distance_km / max(1.0, standard_travel_speed_km_per_day)

        if days_passed < required_days:
            return {
                "is_valid": False,
                "error_type": "CONTINUITY_ERROR_IMPOSSIBLE_TRAVEL",
                "character": character_name,
                "from_location": loc_from["name"],
                "to_location": loc_to["name"],
                "distance_km": round(distance_km, 2),
                "days_passed": days_passed,
                "required_days": round(required_days, 1),
                "error_message": (
                    f"Continuity Error: Character '{character_name}' moved from '{loc_from['name']}' "
                    f"to '{loc_to['name']}' ({distance_km:.1f} km) in {days_passed} days, but journey "
                    f"requires at least {required_days:.1f} days!"
                )
            }

        return {
            "is_valid": True,
            "distance_km": round(distance_km, 2),
            "days_passed": days_passed,
            "required_days": round(required_days, 1)
        }

    def check_character_presence_anomaly(
        self,
        story_id: str,
        character_name: str,
        story_day: int,
        active_chapter: int
    ) -> Optional[str]:
        """
        Checks if a character is recorded participating in incompatible locations on the same story day.
        """
        events = self.repo.get_events(story_id)
        day_events = [
            e for e in events
            if e["story_day"] == story_day and character_name in e.get("participants", [])
        ]
        locations = {e["location_name"] for e in day_events if e.get("location_name")}
        if len(locations) > 1:
            return (
                f"Spatial Anomaly: Character '{character_name}' is recorded participating in "
                f"multiple distant locations on Story Day {story_day}: {list(locations)}."
            )
        return None
