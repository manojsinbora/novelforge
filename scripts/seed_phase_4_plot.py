"""
NovelForge AI — Phase 4 Seed Script
Populates canonical Plot Architecture for 'Echoes of the Fallen Heaven'.
"""
import os
import json
from novelforge.database.plot_repository import PlotRepository
from novelforge.backend.app.services.plot_thread_service import PlotThreadService
from novelforge.backend.app.services.character_arc_service import CharacterArcService
from novelforge.backend.app.services.mystery_promise_service import MysteryPromiseService
from novelforge.backend.app.services.foreshadowing_twist_service import ForeshadowingTwistService
from novelforge.backend.app.services.arc_chapter_planning_service import ArcChapterPlanningService
from novelforge.schemas.plot_models import (
    PlotThreadType, ThreadStatus, ArcType, GoalType, GoalStatus,
    ConflictType, MysteryStatus, PromiseStatus, ForeshadowingType,
    ForeshadowingQuality, PlanConfidence
)

def run_seed():
    db_path = 'novelforge/database/novelforge.sqlite3'
    repo = PlotRepository(db_path)
    plot_svc = PlotThreadService(repo)
    arc_svc = CharacterArcService(repo)
    mp_svc = MysteryPromiseService(repo)
    ft_svc = ForeshadowingTwistService(repo)
    plan_svc = ArcChapterPlanningService(repo)

    story_id = 'echoes-of-fallen-heaven-001'
    print(f'Seeding Phase 4 Plot Architecture for story: {story_id}...')

    main_plot = plot_svc.initialize_main_plot(
        story_id=story_id,
        premise='A regressed peak cultivator returns to his youth to prevent the cataclysmic fall of the Fallen Heaven Sect, only to discover that the sect destruction was engineered from within by the very celestial laws he once revered.',
        central_conflict='Lin Chen vs. The Inevitable Collapse engineered by traitorous sect elders and Blood Raven conspirators',
        protagonist_goal='Reconstruct the Nine Heavenly Pillars and root out the nine Traitor Disciples before Year 3.',
        ultimate_antagonistic_force='The Primordial Sovereign and Blood Raven Patriarch Yan',
        central_stakes='The complete annihilation of the Southern Continent and eternal soul-binding under Blood Raven tyranny.',
        thematic_question='Can Lin Chen alter predestined doom without sacrificing his humanity?',
        desired_ending='Fallen Heaven Sect re-established as the supreme righteous pillar of the continent.'
    )

    plot_svc.add_turning_point(story_id, 'Awakening in Outer Peak Infirmary', 'Lin Chen regresses 300 years back into his 16-year-old body.', 1, 1, 1)
    plot_svc.add_turning_point(story_id, 'Shattering the Blood Raven Spies', 'Lin Chen exposes the subterranean fissure trade route.', 1, 1, 10)
    plot_svc.add_turning_point(story_id, 'Securing the Fallen Star Core', 'Lin Chen secures the ancestral core before Elder Han can embezzle it.', 1, 2, 30)

    t_main = plot_svc.create_thread(
        story_id=story_id,
        name='Rebuild Fallen Heaven Heritage',
        thread_type=PlotThreadType.MAIN_PLOT,
        description='Primary story spine to restore the 9 Heavenly Pillars.',
        importance=10.0,
        priority=1,
        started_chapter=1,
        target_resolution_chapter=500
    )

    t_linxia = plot_svc.create_thread(
        story_id=story_id,
        name='Lin Xia Sovereign Vessel Awakening',
        thread_type=PlotThreadType.CHARACTER_PLOT,
        description='Purify Lin Xia meridians before her sovereign physique detonates.',
        importance=9.0,
        priority=1,
        started_chapter=3,
        target_resolution_chapter=45
    )

    t_bloodraven = plot_svc.create_thread(
        story_id=story_id,
        name='Blood Raven Infiltration & Fissure War',
        thread_type=PlotThreadType.WAR,
        description='Repel Ghost Envoy Mo and uncover sect moles.',
        importance=8.5,
        priority=2,
        started_chapter=5,
        target_resolution_chapter=25
    )

    t_songclan = plot_svc.create_thread(
        story_id=story_id,
        name='Song Clan Resource Monopoly Spar',
        thread_type=PlotThreadType.REVENGE,
        description='Dismantle Song Yu pill monopoly in the sparring ring.',
        importance=6.0,
        priority=3,
        started_chapter=2,
        target_resolution_chapter=12
    )
    plot_svc.update_thread_status(t_songclan.id, ThreadStatus.RESOLVED, actual_resolution_chapter=12)

    arc_chen = arc_svc.create_character_arc(
        character_id='char-001',
        story_id=story_id,
        arc_type=ArcType.POSITIVE_TRANSFORMATION,
        initial_state='Paranoid, solitary regressor trusting no one.',
        internal_problem='Deep trauma from seeing all loved ones butchered.',
        want='Absolute solitary power to crush all threats single-handedly.',
        need='To build reliable alliances and protect companions with love rather than fear.',
        pressure='Impending Blood Raven invasion countdown.',
        transformation='From ruthless survivor to benevolent sect patriarch.',
        final_state='Transcendent leader with unwavering loyalty from the Nine Peaks.'
    )
    m1 = arc_svc.add_arc_milestone(arc_chen.id, 1, 'Refuses companionship in outer infirmary', 'Lin Chen pushes others away.', 'char-001', status='COMPLETED')

    arc_xia = arc_svc.create_character_arc(
        character_id='char-002',
        story_id=story_id,
        arc_type=ArcType.MATURITY,
        initial_state='Sickly, timid sister believing herself a burden.',
        internal_problem='Inferiority complex and fear of holding Lin Chen back.',
        want='To fade away quietly without causing trouble.',
        need='To embrace her supreme sovereign constitution.',
        pressure='Meridian collapse pain.',
        transformation='From frail invalid to fierce sovereign empress.',
        final_state='Sovereign of the Celestial Flame.'
    )
    arc_svc.add_arc_milestone(arc_xia.id, 3, 'Witnesses Lin Chen coughing blood', 'Vows to become strong.', 'char-002', status='COMPLETED')

    g1 = arc_svc.create_goal(
        character_id='char-001',
        story_id=story_id,
        description='Harvest Frost-Jade Blossom for Lin Xia',
        goal_type=GoalType.SURVIVAL,
        motivation='Save sister from meridian detonation',
        deadline_chapter=10
    )
    arc_svc.update_goal_progress(g1.id, progress=1.0, status=GoalStatus.COMPLETED)

    myst_fall = mp_svc.create_mystery(
        story_id=story_id,
        title='Fall of the Fallen Heaven Sect',
        question='Why did the invincible 9th Peak shatter in a single night 300 years ago?',
        hidden_truth='The Sect Patriarch deliberately deactivated the protective formation to seal an outer god entering through his own consciousness.',
        reveal_plan='Discovered through ancestral tablets in Peak 9 ruins'
    )
    mp_svc.add_clue(
        mystery_id=myst_fall.id,
        clue_text='Scorched basalt with inward-facing blast marks at the Mountain Gate.',
        chapter_introduced=4
    )
    mp_svc.add_clue(
        mystery_id=myst_fall.id,
        clue_text='Elder Han ledger records zero defensive talismans requisitioned during the siege night.',
        chapter_introduced=8
    )

    myst_traitor = mp_svc.create_mystery(
        story_id=story_id,
        title='Identity of the Sect Traitor',
        question='Who provided the Blood Raven vanguard with the mountain array bypass talisman?',
        hidden_truth='Elder Han traded the formation token in exchange for a Tier 3 Life-Extension Pill from Patriarch Yan.',
        reveal_plan='Exposed during outer disciplinary tribunal'
    )
    mp_svc.add_clue(
        mystery_id=myst_traitor.id,
        clue_text='A crimson silk thread soaked in Ghost Cinnabar recovered from the formation relay.',
        chapter_introduced=6
    )

    p1 = mp_svc.create_promise(
        story_id=story_id,
        description='Lin Chen vows to cure Lin Xia meridians completely',
        promise_type='CHARACTER_VOW',
        introduced_chapter=3,
        importance='CORE',
        expected_payoff_window=25
    )
    mp_svc.advance_promise(p1.id, PromiseStatus.DEVELOPING)

    p2 = mp_svc.create_promise(
        story_id=story_id,
        description='Confrontation with Song Clan Patriarch',
        promise_type='REVENGE_PAYOFF',
        introduced_chapter=4,
        importance='HIGH',
        expected_payoff_window=10
    )

    seed1 = ft_svc.plant_seed(
        story_id=story_id,
        seed_text='Elder Han habitually scratches the left sleeve of his robe when discussing sect pill allocations.',
        foreshadowing_type=ForeshadowingType.BEHAVIORAL,
        target_event='Elder Han Thrall Exposure',
        target_reveal='Elder Han is enslaved by the Soul-Slaving Gu worm',
        chapter_introduced=2,
        clue_strength=0.5,
        payoff_window_end=18
    )

    twist1 = ft_svc.create_twist(
        story_id=story_id,
        title='Elder Han Thrall Exposure',
        setup='Elder Han suspected of betraying sect for pills',
        hidden_truth='Elder Han is mind-controlled by Blood Raven Patriarch Gu worm',
        reveal_text='Han reveals the writhed parasite behind his ear',
        expected_reader_belief='Elder Han is a traitorous coward',
        actual_truth='Elder Han was resisting mental domination to protect disciple ledgers',
        reveal_chapter=18,
        foreshadowing_ids=[seed1.id]
    )

    arc1 = plan_svc.create_arc_plan(
        saga_id='saga-001',
        story_id=story_id,
        arc_name='Outer Peak Awakening Arc',
        sequence_order=1,
        start_chapter=1,
        end_chapter=25,
        arc_objective='Establish an untouchable footing in the Outer Sect and cure Lin Xia.',
        central_conflict='Lin Chen vs Outer Disciplinary Hall and Blood Raven vanguard',
        primary_characters=['char-001', 'char-002', 'char-003']
    )

    ch1 = plan_svc.create_chapter_plan(
        arc_id=arc1.id,
        chapter_number=1,
        title='The Soul Remembers Heaven',
        chapter_objective='Establish Lin Chen regression baseline and protect sister.',
        main_conflict='Lin Chen vs Temporal Disorientation and Infirmary Enforcers'
    )

    plan_svc.create_scene_plan(
        chapter_id=ch1.id,
        sequence_order=1,
        title='Infirmary Awakening',
        purpose='Verify temporal regression and confirm Lin Xia safety.',
        location_id='loc-outer-infirmary',
        characters_present=['char-001', 'char-002'],
        entry_state={'char-001': 'Confused, weak', 'char-002': 'Feverish'},
        exit_state={'char-001': 'Resolute, cultivating', 'char-002': 'Resting'}
    )

    export_dir = 'novelforge/stories/echoes_of_the_fallen_heaven/plot'
    os.makedirs(export_dir, exist_ok=True)
    with open(f'{export_dir}/main_plot.json', 'w', encoding='utf-8') as f:
        json.dump(main_plot.to_dict(), f, indent=2)
    with open(f'{export_dir}/character_arcs.json', 'w', encoding='utf-8') as f:
        json.dump([arc_chen.to_dict(), arc_xia.to_dict()], f, indent=2)
    with open(f'{export_dir}/mysteries.json', 'w', encoding='utf-8') as f:
        json.dump([myst_fall.to_dict(), myst_traitor.to_dict()], f, indent=2)
    with open(f'{export_dir}/promises.json', 'w', encoding='utf-8') as f:
        json.dump([p1.to_dict(), p2.to_dict()], f, indent=2)

    print('Phase 4 Plot Architecture Seeding Complete! Exported to novelforge/stories/echoes_of_the_fallen_heaven/plot/')

if __name__ == '__main__':
    run_seed()
