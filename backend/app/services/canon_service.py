"""
NovelForge AI — Canon Protection & Permission Service
Enforces permission tiers and handles proposed change workflows.
"""
from __future__ import annotations
from typing import Dict, Any, Optional, List
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.schemas.narrative_models import ProposedChange, PermissionLevel, ProposalStatus


class CanonService:
    def __init__(self, repository: NarrativeRepository):
        self.repo = repository

    def mutate_canon_directly(
        self,
        story_id: str,
        entity_type: str,
        entity_id: str,
        field_name: str,
        new_value: Any,
        actor: str,
        permission_level: PermissionLevel,
        reason: str = "Direct update"
    ) -> bool:
        """
        Directly mutates canonical data. Strictly blocked for READ_ONLY_AGENT and PROPOSAL_AGENT.
        """
        if permission_level in [PermissionLevel.READ_ONLY_AGENT, PermissionLevel.PROPOSAL_AGENT]:
            raise PermissionError(
                f"Unauthorized: Agent '{actor}' with permission '{permission_level.value}' "
                f"cannot directly mutate CANON information. Submit a proposal instead."
            )
        # Canon editors or System may apply changes directly through repository
        return True

    def submit_proposed_change(
        self,
        story_id: str,
        agent: str,
        model: str,
        permission_level: PermissionLevel,
        entity_type: str,
        entity_id: str,
        field_name: str,
        previous_value: Any,
        proposed_value: Any,
        reason: str
    ) -> ProposedChange:
        proposal = ProposedChange(
            story_id=story_id,
            agent=agent,
            model=model,
            permission_level=permission_level,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            previous_value=previous_value,
            proposed_value=proposed_value,
            reason=reason,
            status=ProposalStatus.PENDING
        )
        return self.repo.submit_proposal(proposal)

    def review_proposal(
        self,
        proposal_id: str,
        approver: str,
        permission_level: PermissionLevel,
        decision: str # "APPROVE" or "REJECT"
    ) -> bool:
        if decision == "APPROVE":
            return self.repo.approve_proposal(proposal_id, approver, permission_level)
        else:
            with self.repo.get_session() as session:
                from novelforge.database.models import ProposedChangeRecord
                prop = session.query(ProposedChangeRecord).filter(ProposedChangeRecord.id == proposal_id).first()
                if prop:
                    prop.status = "REJECTED"
                    prop.approved_by = approver
                    session.commit()
                    return True
        return False
