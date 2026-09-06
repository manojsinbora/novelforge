"""
NovelForge AI — Story File Synchronization Service
Phase 2: Bidirectional Sync between DB and stories/{story_id}/
Supports PyYAML when available with standard-library fallback.
"""
from __future__ import annotations
import os
import json
from typing import Dict, Any, Optional
from novelforge.database.narrative_repository import NarrativeRepository

# Optional PyYAML import with clean standard-library fallback
try:
    import yaml
    def dump_structured_data(data: Any, stream) -> None:
        yaml.dump(data, stream, sort_keys=False)
except ImportError:
    def dump_structured_data(data: Any, stream) -> None:
        json.dump(data, stream, indent=2)


class StorySyncService:
    def __init__(self, repository: NarrativeRepository, base_stories_dir: str = "novelforge/stories"):
        self.repo = repository
        self.base_stories_dir = base_stories_dir

    def export_story_to_filesystem(self, story_id: str, folder_name: Optional[str] = None) -> str:
        story = self.repo.get_story(story_id)
        if not story:
            raise ValueError(f"Story {story_id} not found in database.")

        dir_name = folder_name or story.title.lower().replace(" ", "_").replace("'", "")
        target_dir = os.path.join(self.base_stories_dir, dir_name)

        # Create directory layout
        for sub in ["bible", "characters", "world", "timeline", "chapters", "memory"]:
            os.makedirs(os.path.join(target_dir, sub), exist_ok=True)

        # 1. Export Story & Bible
        bible = self.repo.get_story_bible(story_id) or {}
        story_meta = story.to_dict()

        with open(os.path.join(target_dir, "bible", "story.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data(story_meta, f)

        premise_data = bible.get("premise", {})
        premise_md = f"# {story.title} — Premise\n\n"
        premise_md += f"**Elevator Pitch:** {premise_data.get('elevator_pitch', '')}\n\n"
        premise_md += f"**Core Premise:** {premise_data.get('core_premise', '')}\n\n"
        premise_md += f"**Central Conflict:** {premise_data.get('central_conflict', '')}\n\n"
        premise_md += f"**Protagonist Objective:** {premise_data.get('protagonist_objective', '')}\n\n"
        premise_md += f"**Primary Antagonist:** {premise_data.get('primary_antagonist', '')}\n"

        with open(os.path.join(target_dir, "bible", "premise.md"), "w", encoding="utf-8") as f:
            f.write(premise_md)

        with open(os.path.join(target_dir, "bible", "themes.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data(bible.get("themes", {}), f)

        with open(os.path.join(target_dir, "bible", "rules.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data({
                "narrative_rules": bible.get("narrative_rules", {}),
                "world_rules": bible.get("world_rules", {})
            }, f)

        # 2. Export Characters
        characters = self.repo.get_characters(story_id)
        for idx, char in enumerate(characters, start=1):
            c_filename = f"character_{idx:03d}_{char['name'].lower().replace(' ', '_')}.yaml"
            with open(os.path.join(target_dir, "characters", c_filename), "w", encoding="utf-8") as f:
                dump_structured_data(char, f)

        # 3. Export World
        locations = self.repo.get_locations(story_id)
        factions = self.repo.get_factions(story_id)
        with open(os.path.join(target_dir, "world", "locations.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data(locations, f)
        with open(os.path.join(target_dir, "world", "factions.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data(factions, f)

        # 4. Export Timeline
        events = self.repo.get_events(story_id)
        with open(os.path.join(target_dir, "timeline", "events.yaml"), "w", encoding="utf-8") as f:
            dump_structured_data(events, f)

        # 5. Export Chapters
        chapters = self.repo.get_chapters(story_id)
        for ch in chapters:
            ch_num = ch["chapter_number"]
            ch_filename = f"{ch_num:04d}.md"
            ch_content = f"# Chapter {ch_num}: {ch['title']}\n\n"
            ch_content += f"**Summary:** {ch.get('summary', '')}\n\n"
            ch_content += f"**Word Count:** {ch.get('word_count', 0)}\n\n"
            ch_content += f"**Status:** {ch.get('canon_status', 'DRAFT')}\n"
            with open(os.path.join(target_dir, "chapters", ch_filename), "w", encoding="utf-8") as f:
                f.write(ch_content)

            mem = self.repo.get_chapter_memory(story_id, ch_num)
            if mem:
                with open(os.path.join(target_dir, "memory", f"chapter_{ch_num:04d}.yaml"), "w", encoding="utf-8") as f:
                    dump_structured_data(mem, f)

        return target_dir
