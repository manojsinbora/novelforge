"""
NovelForge AI — Seed Data Script for 'Echoes of the Fallen Heaven'
Populates 10+ characters, 5+ factions, 10+ locations, 10+ events, 10+ equipment, secrets, relationships, and 3 arcs.
"""
from __future__ import annotations
import uuid
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.backend.app.services.sync_service import StorySyncService
from novelforge.schemas.narrative_models import (
    StoryModel, StoryBible, StoryPremise, StoryThemes, StoryTone,
    NarrativeRules, WorldRules, Saga, Arc, Chapter, CharacterEntity,
    CharacterCultivationProfile, CharacterVoiceProfile, CharacterRelationship,
    RelationshipType, KnowledgeFactEntity, FactKnowledgeEntry, KnowledgeState,
    WorldLocation, LocationType, FactionEntity, StoryEventEntity, StoryEventType,
    CanonStatus, EntityStatus
)

STORY_ID = "echoes-of-fallen-heaven-001"


def seed_echoes_story(repo: NarrativeRepository) -> str:
    # 1. Story Entity
    story = StoryModel(
        id=STORY_ID,
        title="Echoes of the Fallen Heaven",
        working_title="Regression of the Starlit Core",
        premise=(
            "A regressed grandmaster returns to his 16-year-old self as a disgraced outer disciple "
            "on the eve of the cataclysmic awakening of Earth's subterranean primordial veins."
        ),
        genre="Cultivation",
        subgenres=["Regression", "Mystery", "Sect Intrigue"],
        target_audience="Serialized Web Novel Readers",
        tone="Dark, analytical, with deadpan humor and high-tension pacing",
        themes=["Fate vs Calculation", "Cost of Immortality", "The Burden of Regressed Foresight"],
        narrative_style="Third Person Limited",
        target_chapter_count=500,
        target_chapter_word_count=2000,
        planned_ending="Lin Chen seals the Planar Incursion by synthesizing the Sovereign Matrix.",
        current_saga=1,
        current_arc=1,
        current_chapter=1,
        status=EntityStatus.ACTIVE
    )
    repo.create_story(story)

    # 2. Story Bible
    bible = StoryBible(
        story_id=STORY_ID,
        premise=StoryPremise(
            core_premise="Regressed grandmaster Lin Chen navigates sect politics and subterranean monster incursions.",
            elevator_pitch="Return of the Mount Hua Sect meets The Legendary Mechanic in a grimdark cultivation apocalypse.",
            central_conflict="Verdant Cloud Sect vs Blood Raven Warlords vs Subterranean Primordial Leviathans.",
            protagonist_objective="Protect his sister Lin Xia, purge corrupt sect elders, and seal the ancient planar veins.",
            primary_antagonist="Patriarch Yan of the Blood Raven Sect & The Shadow Sovereign.",
            ultimate_stakes="The complete collapse of the human mortal realm into a feral chimera feeding ground."
        ),
        themes=StoryThemes(
            major_themes=["Merit vs Bloodline Aristocracy", "The Epistemic Isolation of Secrets"],
            minor_themes=["Fraternal Loyalty", "The Irony of Coincidental Glory"],
            moral_questions=["Is it justified to sacrifice an enemy sect to protect a planar seal?"],
            recurring_motifs=["Constellations", "Cracked Jade", "High-Carbon Scalpels"]
        ),
        tone=StoryTone(darkness=0.6, humor=0.4, seriousness=0.7, violence_level=0.7),
        narrative_rules=NarrativeRules(
            pov_rules="Third Person Limited (Lin Chen POV primary)",
            dialogue_preferences="Brisk, razor-sharp, dry humor contrast"
        ),
        world_rules=WorldRules(
            magic_rules={"energy_type": "Primordial Miasma and Earthly Spiritual Qi"},
            cultivation_rules={"tiers": "Novice -> Intermediate -> Master -> Grandmaster -> Great Grandmaster -> Sovereign -> Transcendent"},
            physics_exceptions=["Subterranean orichalcum blocks miasma expansion"]
        )
    )
    repo.set_story_bible(bible)

    # 3. Sagas & 3 Arcs
    saga1 = Saga(
        id="saga-01", story_id=STORY_ID, sequence_order=1,
        name="Saga I: The Crucible of Rebirth",
        description="Lin Chen's reawakening and rise through the Outer Peak to the Sect Grand Tournament."
    )
    repo.add_saga(saga1)

    arcs_data = [
        ("arc-01", 1, "Arc 1: The Outer Peak Crucible", 1, 30, "Surviving resource trials and awakening the Astral Compass."),
        ("arc-02", 2, "Arc 2: The Blood Raven Incursion", 31, 70, "Defending the northern perimeter from beast-wave raiders."),
        ("arc-03", 3, "Arc 3: The Subterranean Vault Awakening", 71, 120, "Infiltrating the ancient Starlit Sovereign ruins.")
    ]
    for aid, seq, aname, start_c, end_c, summary in arcs_data:
        repo.add_arc(Arc(
            id=aid, story_id=STORY_ID, saga_id="saga-01", sequence_order=seq,
            name=aname, start_chapter=start_c, end_chapter=end_c, summary=summary
        ))

    # 4. Chapters 1 to 5
    for cnum in range(1, 6):
        repo.add_chapter(Chapter(
            id=f"ch-{cnum:03d}", story_id=STORY_ID, arc_id="arc-01",
            chapter_number=cnum, title=f"Chapter {cnum} of the Starlit Core",
            summary=f"Events of chapter {cnum}", word_count=1850,
            canon_status=CanonStatus.CANON
        ))

    # 5. 11 Detailed Characters
    chars = [
        ("char-001", "Lin Chen", 16, "Novice", "Peak", 1, "Protagonist / Regressed Scholar", "Outer Disciple Peak"),
        ("char-002", "Lin Xia", 13, "Mortal", "None", 0, "Sister / Latent Sovereign Vessel", "Outer Infirmary"),
        ("char-003", "Elder Han", 140, "Intermediate", "Late", 2, "Corrupt Disciplinary Elder", "Discipline Hall"),
        ("char-004", "Song Yu", 18, "Novice", "Late", 1, "Arrogant Rival Disciple", "Martial Ring"),
        ("char-005", "Grand Elder Gu", 480, "Grandmaster", "Peak", 4, "Sect Grandmaster", "Grand Cloud Hall"),
        ("char-006", "Jiang Meng", 26, "Intermediate", "Middle", 2, "Enigmatic Alchemist", "Spirit Herb Pavilion"),
        ("char-007", "Patriarch Yan", 320, "Grandmaster", "Early", 4, "Blood Raven Antagonist", "Blood Raven Fortress"),
        ("char-008", "Xiao Feng", 22, "Novice", "Middle", 1, "Rogue Informant", "Cloud Peak Market"),
        ("char-009", "Bai Yue", 19, "Intermediate", "Early", 2, "Sword Genius Senior Sister", "Sword Cleansing Pond"),
        ("char-010", "Ghost Envoy Mo", 45, "Master", "Early", 3, "Shadow Court Infiltrator", "Shadow Valley"),
        ("char-011", "Barnaby the Camp Rat", 1, "Mortal", "None", 0, "Comedic Lucky Rat", "Outer Peak Kitchen")
    ]
    for cid, name, age, realm, sub_realm, rank, role, loc in chars:
        repo.add_character(CharacterEntity(
            id=cid, story_id=STORY_ID, name=name, age=age,
            cultivation=CharacterCultivationProfile(realm=realm, sub_realm=sub_realm, rank_level=rank),
            current_location_name=loc,
            character_arc=role,
            canon_status=CanonStatus.CANON
        ))

    # 6. 5 Factions
    factions_data = [
        ("fac-01", "Verdant Cloud Sect", "Sect", "Declining Righteous Sword Sect", "fac-02"),
        ("fac-02", "Blood Raven Sect", "Warlord Cult", "Ruthless blood vitality cultivators", "fac-01"),
        ("fac-03", "The Shadow Court", "Syndicate", "Underground information and assassination guild", "None"),
        ("fac-04", "Song Aristocratic Clan", "Clan", "Corrupt merchant-cultivator family inside the sect", "fac-01"),
        ("fac-05", "The Starlit Remnant", "Ancient Faction", "Pre-collapse civilization sealed beneath Earth", "None")
    ]
    for fid, fname, ftype, desc, rival in factions_data:
        repo.add_faction(FactionEntity(
            id=fid, story_id=STORY_ID, name=fname, faction_type=ftype,
            description=desc, rival_faction_ids=[rival] if rival != "None" else []
        ))

    # 7. 11 Hierarchical Locations
    locations_data = [
        ("loc-01", "Great Azure Planar World", LocationType.WORLD, None, 0.0, 0.0),
        ("loc-02", "Eastern Mist Continent", LocationType.CONTINENT, "loc-01", 100.0, 100.0),
        ("loc-03", "Tiannan Country", LocationType.COUNTRY, "loc-02", 150.0, 150.0),
        ("loc-04", "Verdant Cloud Sect", LocationType.SECT, "loc-03", 200.0, 200.0),
        ("loc-05", "Outer Disciple Peak", LocationType.LANDMARK, "loc-04", 205.0, 205.0),
        ("loc-06", "Discipline Hall", LocationType.BUILDING, "loc-04", 210.0, 210.0),
        ("loc-07", "Spirit Herb Pavilion", LocationType.BUILDING, "loc-04", 215.0, 215.0),
        ("loc-08", "Sword Cleansing Pond", LocationType.LANDMARK, "loc-04", 220.0, 220.0),
        ("loc-09", "The Subterranean Star Vault", LocationType.ROOM, "loc-05", 206.0, 206.0),
        ("loc-10", "Cloud Peak Market", LocationType.CITY, "loc-03", 260.0, 260.0),
        ("loc-11", "Blood Raven Fortress", LocationType.BUILDING, "loc-03", 600.0, 600.0) # 400km away!
    ]
    for lid, lname, ltype, parent, x, y in locations_data:
        repo.add_location(WorldLocation(
            id=lid, story_id=STORY_ID, name=lname, type=ltype,
            parent_location_id=parent, coordinates={"x": x, "y": y}
        ))

    # 8. 10 Timeline Events (Distinguishing real-world time, story_day, story_year, and chapter)
    events_data = [
        ("ev-01", 1, 1, 1, 1, "loc-05", "Outer Disciple Peak", ["Lin Chen"], StoryEventType.DISCOVERY, "Lin Chen returns to his 16-year-old body during morning chores."),
        ("ev-02", 1, 2, 1, 1, "loc-09", "Subterranean Star Vault", ["Lin Chen"], StoryEventType.ITEM_ACQUIRED, "Unearths the dormant Astral Compass beneath the quarry."),
        ("ev-03", 2, 1, 2, 1, "loc-05", "Outer Disciple Peak", ["Lin Chen", "Song Yu"], StoryEventType.BATTLE, "Song Yu attempts to extort Lin Chen; Lin Chen uses weak-point strike to disarm him."),
        ("ev-04", 2, 2, 2, 1, "loc-06", "Discipline Hall", ["Lin Chen", "Elder Han"], StoryEventType.MEETING, "Elder Han interrogates Lin Chen regarding Song Yu's broken arm."),
        ("ev-05", 3, 1, 3, 1, "loc-07", "Spirit Herb Pavilion", ["Lin Chen", "Jiang Meng"], StoryEventType.DISCOVERY, "Lin Chen barters for Silver Needle Grass to synthesize Eleanor's tonic."),
        ("ev-06", 3, 2, 3, 1, "loc-05", "Outer Disciple Peak", ["Lin Chen", "Barnaby the Camp Rat"], StoryEventType.REVELATION, "Barnaby knocks over a tea kettle, extinguishing a fire set by an assassin."),
        ("ev-07", 4, 1, 4, 1, "loc-08", "Sword Cleansing Pond", ["Lin Chen", "Bai Yue"], StoryEventType.MEETING, "Bai Yue notices Lin Chen's refined sword intent and shields him from Elder Han."),
        ("ev-08", 4, 2, 5, 1, "loc-05", "Outer Disciple Peak", ["Lin Chen"], StoryEventType.BREAKTHROUGH, "Lin Chen breaks through from Novice Early to Novice Middle using Astral breathing."),
        ("ev-09", 5, 1, 6, 1, "loc-10", "Cloud Peak Market", ["Lin Chen", "Xiao Feng"], StoryEventType.DISCOVERY, "Xiao Feng warns of Blood Raven scouts infiltrating the lower valley."),
        ("ev-10", 5, 2, 7, 1, "loc-11", "Blood Raven Fortress", ["Patriarch Yan", "Ghost Envoy Mo"], StoryEventType.POLITICAL_CHANGE, "Blood Raven council votes to launch a coordinated assault on Verdant Cloud Sect.")
    ]
    for eid, ch, sc, s_day, s_yr, lid, lname, parts, etype, desc in events_data:
        repo.add_event(StoryEventEntity(
            id=eid, story_id=STORY_ID, chapter_number=ch, scene_number=sc,
            story_day=s_day, story_year=s_yr, location_id=lid,
            location_name=lname, participants=parts, event_type=etype,
            description=desc
        ))

    # 9. Knowledge Facts & Secrets (Epistemic Matrix)
    # Secret 1: Elder Han is a traitor working for Blood Raven Sect
    fact1 = KnowledgeFactEntity(
        id="fact-001", story_id=STORY_ID, fact_key="elder_han_is_traitor",
        description="Elder Han has secretly pledged allegiance to Blood Raven Sect.",
        author_knowledge=True, reader_knowledge=False,
        planned_reveal_chapter=25,
        character_knowledge_map={
            "char-003": FactKnowledgeEntry("char-003", "Elder Han", KnowledgeState.KNOWN_TRUE, 1, 1, "He took the blood oath"),
            "char-007": FactKnowledgeEntry("char-007", "Patriarch Yan", KnowledgeState.KNOWN_TRUE, 1, 1, "Accepted the oath"),
            "char-001": FactKnowledgeEntry("char-001", "Lin Chen", KnowledgeState.KNOWN_TRUE, 1, 1, "Knows from previous regression timeline"),
            "char-009": FactKnowledgeEntry("char-009", "Bai Yue", KnowledgeState.UNKNOWN, None, None, "Does not know")
        }
    )
    repo.add_knowledge_fact(fact1)

    # Secret 2: The Starlit Sovereign Empire was not destroyed by demons, but by the Nine Great Sages
    fact2 = KnowledgeFactEntity(
        id="fact-002", story_id=STORY_ID, fact_key="fall_of_starlit_empire_betrayal",
        description="The Starlit Empire was betrayed by the orthodox sects who coveted their cosmic core.",
        author_knowledge=True, reader_knowledge=False,
        planned_reveal_chapter=95,
        character_knowledge_map={
            "char-001": FactKnowledgeEntry("char-001", "Lin Chen", KnowledgeState.SUSPECTED, 1, 1, "Suspects from partial regression memories"),
            "char-005": FactKnowledgeEntry("char-005", "Grand Elder Gu", KnowledgeState.KNOWN_TRUE, 1, 1, "Inherited secret scroll")
        }
    )
    repo.add_knowledge_fact(fact2)

    # 10. Character Relationships
    relationships = [
        ("char-001", "char-002", RelationshipType.FAMILY, 1.0, 1.0, 0.0, "Brother and sister; absolute mutual devotion."),
        ("char-001", "char-003", RelationshipType.ENEMY, 0.8, -1.0, 0.9, "Lin Chen knows Han is a traitor; Han views Lin Chen as an annoying cockroach."),
        ("char-001", "char-004", RelationshipType.RIVAL, 0.6, -0.5, 0.7, "Outer sect competitor humiliated by Lin Chen."),
        ("char-001", "char-009", RelationshipType.ALLY, 0.7, 0.8, 0.0, "Bai Yue respects Lin Chen's sword insight; mutual alliance.")
    ]
    for s_id, t_id, r_type, strg, trst, host, notes in relationships:
        repo.set_relationship(CharacterRelationship(
            story_id=STORY_ID, source_character_id=s_id, target_character_id=t_id,
            relationship_type=r_type, strength=strg, trust=trst, hostility=host,
            beginning_chapter=1, current_chapter=5, notes=notes
        ))

    # 11. Sync & Export to Filesystem
    sync = StorySyncService(repo)
    export_path = sync.export_story_to_filesystem(STORY_ID, folder_name="echoes_of_the_fallen_heaven")
    return export_path


if __name__ == "__main__":
    repo = NarrativeRepository("sqlite:///novelforge/database/novelforge.sqlite3")
    export_dir = seed_echoes_story(repo)
    print(f"Successfully seeded 'Echoes of the Fallen Heaven' and exported to: {export_dir}")
