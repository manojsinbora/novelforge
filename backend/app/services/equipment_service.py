"""
NovelForge AI — Equipment & Artifact Engine
Phase 3: Rarity Tiers, Durability, Evolution, and Provenance Tracking
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    Equipment, EquipmentRarity, EquipmentSlot, EquipmentOwnershipRecord
)

RARITY_MULTIPLIER = {
    EquipmentRarity.COMMON: 1.0,
    EquipmentRarity.UNCOMMON: 1.5,
    EquipmentRarity.RARE: 2.5,
    EquipmentRarity.EPIC: 4.5,
    EquipmentRarity.LEGENDARY: 8.0,
    EquipmentRarity.MYTHIC: 15.0,
    EquipmentRarity.TRANSCENDENT: 30.0,
}


class EquipmentService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def create_equipment(
        self,
        story_id: str,
        name: str,
        rarity: EquipmentRarity,
        slot: EquipmentSlot,
        owner_id: Optional[str] = None,
        attributes: Optional[Dict[str, float]] = None,
        passive_effects: Optional[List[str]] = None,
        active_skills: Optional[List[str]] = None,
        spirit_resonance: float = 0.0,
        chapter_created: int = 1,
    ) -> Equipment:
        base_attrs = attributes or {}
        mult = RARITY_MULTIPLIER.get(rarity, 1.0)
        scaled_attrs = {k: round(v * mult, 1) for k, v in base_attrs.items()}

        item = Equipment(
            id=str(uuid.uuid4()),
            story_id=story_id,
            name=name,
            rarity=rarity,
            slot=slot,
            current_owner_id=owner_id,
            current_durability=100.0,
            max_durability=100.0,
            is_bound=False,
            attributes=scaled_attrs,
            passive_effects=passive_effects or [],
            active_skills=active_skills or [],
            spirit_resonance=spirit_resonance,
            evolution_tier=1,
            is_destroyed=False,
            chapter_created=chapter_created,
        )
        saved = self.power_repo.create_equipment(item)

        # Log initial acquisition in provenance history
        if owner_id:
            rec = EquipmentOwnershipRecord(
                id=str(uuid.uuid4()),
                equipment_id=saved.id,
                previous_owner_id=None,
                new_owner_id=owner_id,
                chapter_transferred=chapter_created,
                transfer_reason="ORIGINAL_FORGE_OR_ACQUISITION",
            )
            with self.power_repo.conn:
                self.power_repo.conn.execute("""
                    INSERT INTO equipment_history (
                        id, equipment_id, previous_owner_id, new_owner_id, chapter_transferred, transfer_reason, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    rec.id, rec.equipment_id, rec.previous_owner_id, rec.new_owner_id,
                    rec.chapter_transferred, rec.transfer_reason, rec.timestamp
                ))
        return saved

    def transfer_ownership(
        self,
        equipment_id: str,
        new_owner_id: Optional[str],
        chapter_number: int,
        reason: str = "LOOTED"
    ) -> EquipmentOwnershipRecord:
        return self.power_repo.transfer_equipment(
            equipment_id=equipment_id,
            new_owner_id=new_owner_id,
            chapter_number=chapter_number,
            reason=reason
        )

    def destroy_equipment(self, equipment_id: str, chapter_number: int) -> Equipment:
        return self.power_repo.destroy_equipment(equipment_id=equipment_id, chapter_number=chapter_number)

    def apply_durability_loss(
        self,
        equipment_id: str,
        loss_amount: float,
        chapter_number: int
    ) -> Equipment:
        eq = self.power_repo.get_equipment(equipment_id)
        if not eq:
            raise ValueError(f"Equipment {equipment_id} not found")
        eq.current_durability = max(0.0, round(eq.current_durability - loss_amount, 1))
        if eq.current_durability == 0.0:
            return self.destroy_equipment(equipment_id, chapter_number)
        return self.power_repo.create_equipment(eq)

    def repair_equipment(self, equipment_id: str, amount: float = 100.0) -> Equipment:
        eq = self.power_repo.get_equipment(equipment_id)
        if not eq:
            raise ValueError(f"Equipment {equipment_id} not found")
        if eq.is_destroyed:
            raise ValueError(f"Cannot repair destroyed equipment {equipment_id}")
        eq.current_durability = min(eq.max_durability, eq.current_durability + amount)
        return self.power_repo.create_equipment(eq)

    def evolve_equipment(
        self,
        equipment_id: str,
        new_rarity: EquipmentRarity,
        additional_attributes: Dict[str, float]
    ) -> Equipment:
        eq = self.power_repo.get_equipment(equipment_id)
        if not eq:
            raise ValueError(f"Equipment {equipment_id} not found")
        eq.rarity = new_rarity
        eq.evolution_tier += 1
        for k, v in additional_attributes.items():
            eq.attributes[k] = round(eq.attributes.get(k, 0.0) + v, 1)
        eq.spirit_resonance = min(1.0, eq.spirit_resonance + 0.2)
        return self.power_repo.create_equipment(eq)
