"""
NovelForge AI — Deterministic Cultivation & Combat Power Evaluator
Answers: 'Can Character A realistically defeat Character B?' based on stored rules.
"""
from __future__ import annotations
from typing import Dict, Any, Tuple
from novelforge.schemas.story_schemas import Character


class CultivationCombatEvaluator:
    # Standard Xianxia & Apocalypse Awakening hierarchy ranking
    REALM_RANK_MAP = {
        # Apocalypse 7-Level Awakening System
        "Novice": 1,
        "Intermediate": 2,
        "Master": 3,
        "Grandmaster": 4,
        "Great Grandmaster": 5,
        "Sovereign": 6,
        "Transcendent": 7,
        # Classical Xianxia Fallback
        "Mortal": 1,
        "Qi Condensation": 2,
        "Foundation Establishment": 3,
        "Core Formation": 4,
        "Nascent Soul": 5,
        "Soul Formation": 6,
        "Void Tribulation": 7,
        "Mahayana": 8,
        "True Immortal": 9
    }

    SUB_REALM_BONUS = {
        "Early": 0.1,
        "Mid": 0.3,
        "Middle": 0.3,
        "Late": 0.5,
        "Peak": 0.8,
        "None": 0.0
    }


    @classmethod
    def calculate_power_index(cls, character: Character) -> float:
        base_realm_rank = cls.REALM_RANK_MAP.get(character.cultivation.realm, 1)
        sub_realm_bonus = cls.SUB_REALM_BONUS.get(character.cultivation.sub_realm, 0.0)
        
        # Exponential scaling between major realms: each major realm is ~5x stronger
        raw_power = (5.0 ** (base_realm_rank - 1)) * (1.0 + sub_realm_bonus)
        
        # Artifact / treasure modifier: each equipped high-grade treasure gives +20%
        item_multiplier = 1.0 + (len(character.equipped_items) * 0.2)
        
        return raw_power * item_multiplier

    @classmethod
    def evaluate_matchup(cls, attacker: Character, defender: Character) -> Dict[str, Any]:
        attacker_power = cls.calculate_power_index(attacker)
        defender_power = cls.calculate_power_index(defender)
        ratio = attacker_power / max(0.0001, defender_power)

        if ratio >= 2.5:
            verdict = "DECISIVE_VICTORY"
            feasibility = "Attacker will easily overpower Defender with minimal risk."
        elif ratio >= 1.2:
            verdict = "ADVANTAGEOUS_WIN"
            feasibility = "Attacker is likely to win through standard martial superiority."
        elif ratio >= 0.8:
            verdict = "CONTESTED_SKILL_MATCHUP"
            feasibility = "Evenly matched. Outcome depends on terrain, tactics, and hidden trump cards."
        elif ratio >= 0.4:
            verdict = "DESPERATE_PYRRHIC_POSSIBILITY"
            feasibility = "Attacker is outmatched; victory requires extreme sacrifice, forbidden pill, or trap."
        else:
            verdict = "IMPOSSIBLE_VICTORY"
            feasibility = "Realm gap is overwhelming. Attacker CANNOT realistically defeat Defender in direct combat."

        return {
            "attacker_name": attacker.name,
            "attacker_power_index": round(attacker_power, 2),
            "defender_name": defender.name,
            "defender_power_index": round(defender_power, 2),
            "power_ratio": round(ratio, 2),
            "verdict": verdict,
            "feasibility": feasibility,
            "boundary_rule": "LLM scene writer must NOT generate a clean solo victory for attacker" if ratio < 0.4 else "Allowed"
        }
