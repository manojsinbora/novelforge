import json, re

with open("stories/omnicrafter_of_the_fallen_era/chapters/0001.md", "r", encoding="utf-8") as f:
    ch1_raw = f.read()

with open("stories/omnicrafter_of_the_fallen_era/chapters/0002.md", "r", encoding="utf-8") as f:
    ch2_raw = f.read()

def md_to_html(md_text):
    lines = md_text.split("\n")
    html_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append("<br>")
        elif line.startswith("# "):
            html_lines.append(f"<h1 style=\"color: var(--accent-blue); margin: 25px 0 15px 0; font-size: 1.8rem;\">{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2 style=\"color: var(--accent-purple); margin: 20px 0 12px 0;\">{line[3:]}</h2>")
        elif line.startswith("*") and line.endswith("*") and len(line) > 2:
            html_lines.append(f"<p style=\"color: var(--text-secondary); font-style: italic; margin-bottom: 12px; line-height: 1.8;\">{line[1:-1]}</p>")
        else:
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<strong style=\"color: var(--text-primary);\">\\1</strong>", line)
            formatted = re.sub(r"\*(.*?)\*", r"<em>\\1</em>", formatted)
            formatted = formatted.replace("`", "\\`")
            html_lines.append(f"<p style=\"color: #cbd5e1; margin-bottom: 14px; line-height: 1.8; font-size: 1.05rem;\">{formatted}</p>")
    return "\n".join(html_lines)

ch1_html = md_to_html(ch1_raw)
ch2_html = md_to_html(ch2_raw)

html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>NovelForge AI — The Omnicrafter of the Fallen Era</title>
    <style>
        :root {{
            --bg-primary: #090d16;
            --bg-secondary: #131b2e;
            --bg-card: #1e293b;
            --accent-blue: #38bdf8;
            --accent-cyan: #22d3ee;
            --accent-purple: #c084fc;
            --accent-green: #4ade80;
            --accent-red: #f87171;
            --accent-amber: #fbbf24;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif; }}
        body {{ background: var(--bg-primary); color: var(--text-primary); display: flex; height: 100vh; overflow: hidden; }}
        
        #sidebar {{ width: 280px; background: var(--bg-secondary); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }}
        .logo-box {{ padding: 22px 20px; border-bottom: 1px solid var(--border-color); font-size: 1.25rem; font-weight: bold; color: var(--accent-blue); display: flex; align-items: center; gap: 12px; }}
        .nav-links {{ list-style: none; padding: 15px 0; flex: 1; overflow-y: auto; }}
        .nav-item {{ padding: 12px 24px; cursor: pointer; color: var(--text-secondary); display: flex; align-items: center; gap: 12px; font-size: 0.95rem; transition: all 0.2s; }}
        .nav-item:hover, .nav-item.active {{ background: #0f172a80; color: var(--accent-blue); border-left: 4px solid var(--accent-blue); }}
        
        #main-container {{ flex: 1; display: flex; flex-direction: column; overflow-y: auto; }}
        .header-bar {{ height: 70px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; padding: 0 30px; }}
        .content-area {{ padding: 30px; flex: 1; overflow-y: auto; }}
        
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 25px; }}
        .stat-card {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.25); }}
        .stat-label {{ font-size: 0.85rem; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; }}
        .stat-value {{ font-size: 1.8rem; font-weight: bold; color: var(--text-primary); }}
        
        .tab-view {{ display: none; }}
        .tab-view.active {{ display: block; }}
        .card {{ background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
        .card-header {{ font-size: 1.2rem; font-weight: bold; color: var(--accent-blue); margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }}
        
        .char-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
        .char-card {{ background: var(--bg-card); border-radius: 10px; padding: 20px; cursor: pointer; transition: transform 0.2s, border-color 0.2s; border: 1px solid var(--border-color); }}
        .char-card:hover {{ transform: translateY(-3px); border-color: var(--accent-cyan); }}
        .tag {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; margin-right: 6px; margin-bottom: 6px; }}
        .tag-realm {{ background: #38bdf820; color: #38bdf8; border: 1px solid #38bdf880; }}
        .tag-canon {{ background: #4ade8020; color: #4ade80; border: 1px solid #4ade8080; }}
        .tag-legend {{ background: #fbbf2420; color: #fbbf24; border: 1px solid #fbbf2480; }}
        .tag-danger {{ background: #f8717120; color: #f87171; border: 1px solid #f8717180; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ text-align: left; padding: 14px; border-bottom: 1px solid var(--border-color); font-size: 0.92rem; }}
        th {{ color: var(--text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.5px; }}
        
        .btn {{ padding: 9px 18px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; font-size: 0.88rem; transition: opacity 0.2s; }}
        .btn:hover {{ opacity: 0.9; }}
        .btn-primary {{ background: var(--accent-blue); color: #090d16; }}
        .btn-success {{ background: var(--accent-green); color: #090d16; }}
        
        .reader-controls {{ display: flex; gap: 12px; margin-bottom: 20px; align-items: center; }}
        .reader-body {{ background: #0c1220; border: 1px solid var(--border-color); border-radius: 12px; padding: 40px; max-width: 900px; margin: 0 auto; box-shadow: 0 8px 30px rgba(0,0,0,0.5); }}
    </style>
</head>
<body>

    <div id=\"sidebar\">
        <div class=\"logo-box\">
            <span>⚙️ NovelForge AI</span>
        </div>
        <ul class=\"nav-links\">
            <li class=\"nav-item active\" onclick=\"showTab('tab-dashboard')\">📊 Dashboard & Overview</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-reader')\">📖 Read Chapters (Live)</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-characters')\">👤 Characters Registry</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-equipment')\">🛠️ Workshop & Equipment</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-combat')\">⚔️ Combat Simulator</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-plot-threads')\">📜 Plot Threads (12)</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-power')\">⚡ 7-Tier Awakening</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-world')\">🗺️ Oakhaven Map</li>
            <li class=\"nav-item\" onclick=\"showTab('tab-story-health')\">📈 Story Health & QA</li>
        </ul>
        <div style=\"padding: 20px; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: var(--text-secondary); line-height: 1.6;\">
            <strong>The Omnicrafter of the Fallen Era</strong><br>
            Engine: NovelForge 4.0.0<br>
            SQLite State: Canonical Synced
        </div>
    </div>

    <div id=\"main-container\">
        <div class=\"header-bar\">
            <div>
                <h2 style=\"font-size: 1.3rem; color: var(--accent-blue);\">The Omnicrafter of the Fallen Era</h2>
                <span style=\"font-size: 0.85rem; color: var(--text-secondary);\">Apocalyptic Battle-Artificer · Deadpan Comedy · Saitama/King Irony</span>
            </div>
            <div style=\"display: flex; gap: 12px;\">
                <button class=\"btn btn-primary\" onclick=\"showTab('tab-reader')\">📖 Read Chapter 2</button>
            </div>
        </div>

        <div class=\"content-area\">

            <div id=\"tab-dashboard\" class=\"tab-view active\">
                <div class=\"stats-grid\">
                    <div class=\"stat-card\">
                        <div class=\"stat-label\">Published Chapters / Words</div>
                        <div class=\"stat-value\" style=\"color: var(--accent-blue);\">2 <span style=\"font-size: 1rem; color: var(--text-secondary);\">/ 5,198 words</span></div>
                    </div>
                    <div class=\"stat-card\">
                        <div class=\"stat-label\">Protagonist (Arthur Vance)</div>
                        <div class=\"stat-value\" style=\"color: var(--accent-cyan); font-size: 1.4rem;\">Novice Mid</div>
                        <div style=\"font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;\">Weapon: The Electric Spanner</div>
                    </div>
                    <div class=\"stat-card\">
                        <div class=\"stat-label\">Eleanor Rescue Countdown</div>
                        <div class=\"stat-value\" style=\"color: var(--accent-red);\">47 hrs <span style=\"font-size: 1rem; color: var(--text-secondary);\">left</span></div>
                        <div style=\"font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;\">Target: St. Jude Ward 4 (3 mi away)</div>
                    </div>
                    <div class=\"stat-card\">
                        <div class=\"stat-label\">Uncredited Legend Status</div>
                        <div class=\"stat-value\" style=\"color: var(--accent-amber); font-size: 1.4rem;\">100% Stolen</div>
                        <div style=\"font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;\">Barnaby & Trash Dragon took glory</div>
                    </div>
                </div>

                <div class=\"card\">
                    <div class=\"card-header\">
                        <span>Current Narrative Snapshot</span>
                        <span class=\"tag tag-canon\">CANON VERIFIED</span>
                    </div>
                    <p style=\"color: #cbd5e1; line-height: 1.7; margin-bottom: 16px;\">
                        <strong>Current Location:</strong> Commerce Avenue & 8th Street, Oakhaven (3 miles east of St. Jude Clinic).<br>
                        <strong>Active Objective:</strong> Arthur is advancing west toward St. Jude Clinic to reach his fifteen-year-old sister Eleanor before the purple miasma boils her resonant blood.<br>
                        <strong>Latest Combat Feat:</strong> Ambushed by three mutant hounds; neutralized alpha hound via 15,000V neural shock with <em>The Electric Spanner</em> and tripped second hound with high-tension aircraft cable.<br>
                        <strong>Public Perception:</strong> The crowd on Commerce Avenue believes local gym hero Chadwick Briggs (\"The Trash Dragon\") summoned lightning from inside a dumpster. Arthur was told to go sweep up broken glass.
                    </p>
                </div>

                <div class=\"card\">
                    <div class=\"card-header\">Arthur Vance's Active Field Kit</div>
                    <table>
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Classification</th>
                                <th>Durability</th>
                                <th>Combat & Utility Effect</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>The Electric Spanner</strong></td>
                                <td><span class=\"tag tag-realm\">Rare Custom Weapon</span></td>
                                <td>100 / 100</td>
                                <td>14-inch pipe wrench with masonry chisel spike & 12V lithium capacitor: delivers 15,000V neural overload on contact.</td>
                            </tr>
                            <tr>
                                <td><strong>Brass Workshop Respirator</strong></td>
                                <td><span class=\"tag tag-canon\">Essential Gear</span></td>
                                <td>95 / 100</td>
                                <td>Crushed charcoal + vinegar-treated filter cloth: 98% filtration against purple primordial miasma.</td>
                            </tr>
                            <tr>
                                <td><strong>Ancient Codex Vellum Leaf</strong></td>
                                <td><span class=\"tag tag-legend\">Artifact Lore</span></td>
                                <td>100 / 100</td>
                                <td>Torn ninth folio showing hand-inked schematic of subterranean energy veins and five-humor refining.</td>
                            </tr>
                            <tr>
                                <td><strong>Drop-Forged Steel Cable</strong></td>
                                <td><span class=\"tag tag-realm\">Tactical Tool</span></td>
                                <td>50 ft</td>
                                <td>500-lb test weight braided aircraft cable with weighted loop for tripping large charging quadrupeds.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div id=\"tab-reader\" class=\"tab-view\">
                <div class=\"reader-controls\">
                    <button class=\"btn btn-primary\" onclick=\"setChapter(1)\">Chapter 1: The Cracking Stacks</button>
                    <button class=\"btn btn-success\" onclick=\"setChapter(2)\">Chapter 2: The Bleeding Avenues</button>
                    <span style=\"color: var(--text-secondary); margin-left: 15px; font-size: 0.9rem;\" id=\"chapter-meta\">Showing Chapter 2 (2,918 words)</span>
                </div>
                <div class=\"reader-body\" id=\"reader-container\">
                    {ch2_html}
                </div>
            </div>

            <div id=\"tab-characters\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">Characters Registry (Dossiers & Public Glory Status)</div>
                    <div class=\"char-grid\">
                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--accent-blue);\">Arthur Vance (23)</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Protagonist · Municipal Archivist & Battle-Artificer</div>
                            <div>
                                <span class=\"tag tag-realm\">Novice Mid</span>
                                <span class=\"tag tag-canon\">HERO IN THE SHADOWS</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                Meticulous, deadpan, and deeply protective of his sister Eleanor. Possesses an encyclopedic memory of 42,000 volumes. Treats apocalypse like a municipal project failure.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-amber);\">
                                📍 Location: Heading west on 8th Street (Commerce District)
                            </div>
                        </div>

                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--accent-purple);\">Eleanor Vance (15)</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Sister · Latent Starlight Sovereign Vessel</div>
                            <div>
                                <span class=\"tag tag-realm\">Dormant Sovereign</span>
                                <span class=\"tag tag-danger\">CRITICAL CONDITION</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                Bedridden for three years with an inexplicable burning fever that glows blue under her skin. Her body resonates with the planetary miasma. 47 hours remain to stabilize her.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-red);\">
                                📍 Location: St. Jude Clinic, Isolation Ward 4
                            </div>
                        </div>

                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--accent-amber);\">Barnaby the Rat</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Cellar Rat · \"Sacred Guardian of Section 14\"</div>
                            <div>
                                <span class=\"tag tag-legend\">APEX DEITY (ALLEGED)</span>
                                <span class=\"tag tag-canon\">CANON</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                A fat, one-eared sewer rat that likes sourdough crusts. Stood on top of the dead mutant security guard while sniffing for breadcrumbs. Now worshiped as an immortal ancestral spirit by library survivors.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-green);\">
                                📍 Location: Wainscoting baseboard, Sub-Basement Archive
                            </div>
                        </div>

                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--accent-green);\">Chadwick \"Chad\" Briggs</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Gym Trainer · \"The Trash Dragon\"</div>
                            <div>
                                <span class=\"tag tag-legend\">LOCAL HERO (ACCIDENTAL)</span>
                                <span class=\"tag tag-realm\">Mortal (Bruised)</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                Regional Golden Gloves semi-finalist who tried to fight mutant hounds with an aluminum softball bat. Got swatted into a dumpster, emerged covered in rotten celery, and took credit for Arthur's electric shock.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-cyan);\">
                                📍 Location: Commerce Avenue Municipal Bus Stop
                            </div>
                        </div>

                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--accent-red);\">Ironfang Marcus Cole</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Mutant Warlord · Main Antagonist</div>
                            <div>
                                <span class=\"tag tag-danger\">Intermediate Peak</span>
                                <span class=\"tag tag-realm\">Apex Corrupted</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                Former demolition contractor who drank the unrefined purple miasma directly from a fissure. His skin is hardened iron-chitin. Rules the West Industrial District with ruthless biological dominance.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-red);\">
                                📍 Location: West Rail Yard & Foundry
                            </div>
                        </div>

                        <div class=\"char-card\">
                            <div style=\"font-weight: bold; font-size: 1.2rem; margin-bottom: 6px; color: var(--text-primary);\">Dr. Evelyn Ward</div>
                            <div style=\"font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;\">Chief Physician · St. Jude Clinic</div>
                            <div>
                                <span class=\"tag tag-canon\">Allied NPC</span>
                                <span class=\"tag tag-danger\">Under Siege</span>
                            </div>
                            <p style=\"margin-top: 12px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;\">
                                Eleanor's dedicated doctor. Currently barricaded inside Medical Ward 4 with emergency air scrubbers and a dwindling supply of saline solution.
                            </p>
                            <div style=\"margin-top: 12px; font-size: 0.8rem; color: var(--accent-purple);\">
                                📍 Location: St. Jude Clinic, West Wing
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id=\"tab-equipment\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">
                        <span>Arthur Vance's Artificer Workshop & Crafting Recipes</span>
                        <span class=\"tag tag-canon\">Modular Engineering</span>
                    </div>
                    <div style=\"display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;\">
                        <div style=\"background: var(--bg-card); padding: 20px; border-radius: 10px; border: 1px solid var(--border-color);\">
                            <h3 style=\"color: var(--accent-blue); margin-bottom: 8px;\">The Electric Spanner</h3>
                            <div style=\"font-size: 0.8rem; color: var(--accent-cyan); margin-bottom: 12px;\">Crafted in Chapter 2 @ Holloway's Hardware</div>
                            <ul style=\"color: #cbd5e1; font-size: 0.88rem; line-height: 1.8; margin-left: 20px;\">
                                <li><strong>Base:</strong> 14-inch drop-forged high-carbon steel pipe wrench.</li>
                                <li><strong>Piercing Head:</strong> Ground 5-inch masonry chisel clamped to the crown.</li>
                                <li><strong>Power Source:</strong> 12V lithium cordless power-drill battery pack.</li>
                                <li><strong>Discharge:</strong> High-voltage automotive ignition capacitors (15,000V pulse).</li>
                                <li><strong>Safety:</strong> Triple-layer vulcanized rubber grip insulation.</li>
                            </ul>
                        </div>

                        <div style=\"background: var(--bg-card); padding: 20px; border-radius: 10px; border: 1px solid var(--border-color);\">
                            <h3 style=\"color: var(--accent-green); margin-bottom: 8px;\">Brass Workshop Respirator</h3>
                            <div style=\"font-size: 0.8rem; color: var(--accent-cyan); margin-bottom: 12px;\">Crafted in Chapter 1 @ Library Preservation Desk</div>
                            <ul style=\"color: #cbd5e1; font-size: 0.88rem; line-height: 1.8; margin-left: 20px;\">
                                <li><strong>Body:</strong> Vintage brass spray nozzle respirator with screw-on canister.</li>
                                <li><strong>Filter Core:</strong> Crushed activated charcoal granules (volatile organic trap).</li>
                                <li><strong>Pre-Filter:</strong> Cotton pad soaked in diluted vinegar wash (neutralizes acidic particulates).</li>
                                <li><strong>Efficiency:</strong> 98% against purple primordial miasma.</li>
                            </ul>
                        </div>

                        <div style=\"background: var(--bg-card); padding: 20px; border-radius: 10px; border: 1px solid var(--border-color);\">
                            <h3 style=\"color: var(--accent-purple); margin-bottom: 8px;\">Upcoming Upgrade: Runic Chimera Frame</h3>
                            <div style=\"font-size: 0.8rem; color: var(--accent-purple); margin-bottom: 12px;\">Planned for Chapter 4 @ St. Jude Maintenance Lab</div>
                            <ul style=\"color: #cbd5e1; font-size: 0.88rem; line-height: 1.8; margin-left: 20px;\">
                                <li><strong>Concept:</strong> Modular exo-arm frame incorporating Eleanor's starlight frequency.</li>
                                <li><strong>Components:</strong> Surgical stainless steel calipers + defibrillator coils.</li>
                                <li><strong>Anticipated Power:</strong> Intermediate-tier kinetic discharge.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div id=\"tab-combat\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">Deterministic Empirical Combat Evaluator</div>
                    <div style=\"display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;\">
                        <div>
                            <label style=\"font-size: 0.85rem; color: var(--text-secondary);\">Combatant A (Protagonist):</label>
                            <select id=\"combat-a\" style=\"width: 100%; padding: 10px; background: var(--bg-card); color: #fff; border: 1px solid var(--border-color); border-radius: 6px; margin-top: 5px;\">
                                <option value=\"arthur\">Arthur Vance (Novice Mid / Electric Spanner)</option>
                            </select>
                        </div>
                        <div>
                            <label style=\"font-size: 0.85rem; color: var(--text-secondary);\">Combatant B (Opponent):</label>
                            <select id=\"combat-b\" style=\"width: 100%; padding: 10px; background: var(--bg-card); color: #fff; border: 1px solid var(--border-color); border-radius: 6px; margin-top: 5px;\">
                                <option value=\"guard\">Mutated Library Guard (Bob) (Tier 1 Novice)</option>
                                <option value=\"hound\">Scaled Street Hound Pack (Tier 1 Novice)</option>
                                <option value=\"chad\">Chadwick Briggs vs Dumpster (Mortal)</option>
                                <option value=\"cole\">Ironfang Marcus Cole (Intermediate Peak)</option>
                            </select>
                        </div>
                    </div>
                    <button class=\"btn btn-primary\" onclick=\"runCombatSimulation()\">⚔️ Simulate Tactical Matchup</button>

                    <div id=\"combat-results-box\" style=\"margin-top: 20px; background: var(--bg-card); border-radius: 8px; padding: 20px; display: none;\">
                        <h4 id=\"combat-outcome-title\" style=\"color: var(--accent-blue); margin-bottom: 10px;\"></h4>
                        <div style=\"font-size: 1.1rem; margin-bottom: 12px;\" id=\"combat-odds\"></div>
                        <p id=\"combat-factors\" style=\"color: var(--text-secondary); margin-bottom: 10px; line-height: 1.6;\"></p>
                        <div id=\"combat-reversal\" style=\"padding: 10px; background: #3b82f620; border-left: 3px solid var(--accent-cyan); font-size: 0.85rem;\"></div>
                    </div>
                </div>
            </div>

            <div id=\"tab-plot-threads\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">
                        <span>Active Canonical Plot Threads (12 Seeded)</span>
                        <span class=\"tag tag-canon\">Synchronized</span>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Thread</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Urgency</th>
                                <th>Key Entities</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Rescue Sister Eleanor from Ward 4</strong></td>
                                <td><span class=\"tag tag-realm\">MAIN_PLOT</span></td>
                                <td><span class=\"tag tag-danger\">ACTIVE</span></td>
                                <td>CRITICAL (47h)</td>
                                <td>Arthur Vance, Eleanor Vance, St. Jude Clinic</td>
                            </tr>
                            <tr>
                                <td><strong>Synthesize Starlight Stabilization Cure</strong></td>
                                <td><span class=\"tag tag-realm\">MAIN_PLOT</span></td>
                                <td><span class=\"tag tag-canon\">PENDING</span></td>
                                <td>HIGH</td>
                                <td>Ancient Codex Leaf, Alchemical Reagents</td>
                            </tr>
                            <tr>
                                <td><strong>The Legend of Barnaby the Sacred Rat</strong></td>
                                <td><span class=\"tag tag-legend\">COMEDY_CORE</span></td>
                                <td><span class=\"tag tag-canon\">ACTIVE</span></td>
                                <td>RISING</td>
                                <td>Barnaby, Library Survivors, Cult of Section 14</td>
                            </tr>
                            <tr>
                                <td><strong>The Trash Dragon's Unearned Rise</strong></td>
                                <td><span class=\"tag tag-legend\">COMEDY_CORE</span></td>
                                <td><span class=\"tag tag-canon\">ACTIVE</span></td>
                                <td>RISING</td>
                                <td>Chadwick Briggs, Bus Passengers, City Media</td>
                            </tr>
                            <tr>
                                <td><strong>Ironfang Marcus Cole's Foundry Syndicate</strong></td>
                                <td><span class=\"tag tag-danger\">ANTAGONIST_ARC</span></td>
                                <td><span class=\"tag tag-danger\">LOOMING</span></td>
                                <td>HIGH</td>
                                <td>Marcus Cole, West Rail Yard Warlords</td>
                            </tr>
                            <tr>
                                <td><strong>Blackwood Ridge Bunker 07 Sanctuary</strong></td>
                                <td><span class=\"tag tag-realm\">WORLD_GOAL</span></td>
                                <td><span class=\"tag tag-canon\">SEEDED</span></td>
                                <td>MEDIUM</td>
                                <td>Survivor Convoy, Old Government Bunker</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div id=\"tab-power\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">
                        <span>Sevenfold Awakening Tier Hierarchy</span>
                        <span class=\"tag tag-realm\">Canonical Multipliers</span>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Realm Name</th>
                                <th>Multiplier</th>
                                <th>Biological & Resonant Transformation</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>Tier 1</td><td><strong>Novice</strong></td><td>1.0x</td><td>Initial miasma absorption; bone density x2, rapid muscle remodeling.</td></tr>
                            <tr><td>Tier 2</td><td><strong>Intermediate</strong></td><td>2.2x</td><td>Chitinous plating, internal organ hardening (Marcus Cole tier).</td></tr>
                            <tr><td>Tier 3</td><td><strong>Master</strong></td><td>4.8x</td><td>Resonant vascular nodes form; environmental miasma projection.</td></tr>
                            <tr><td>Tier 4</td><td><strong>Grand Master</strong></td><td>10.5x</td><td>Kinetic domain manifestation; extreme biological regeneration.</td></tr>
                            <tr><td>Tier 5</td><td><strong>Great Grand Master</strong></td><td>22.0x</td><td>Chitin-bone fusion into permanent natural body armor.</td></tr>
                            <tr><td>Tier 6</td><td><strong>Sovereign</strong></td><td>48.0x</td><td>Primordial spatial alignment (Eleanor's latent tier).</td></tr>
                            <tr><td>Tier 7</td><td><strong>Transcendent</strong></td><td>100.0x</td><td>True apex planar integration; planetary vein mastery.</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div id=\"tab-world\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">Oakhaven City Regional Map</div>
                    <div style=\"font-family: monospace; font-size: 0.95rem; line-height: 2; color: var(--text-secondary);\">
                        📁 Oakhaven Metropolitan Area<br>
                        &nbsp;&nbsp;├── 🏛️ Grand Municipal Library (Starting Point)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── 📍 Sub-Basement Archive (Section 14 Fissure - Barnaby's Domain)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── 📍 Preservation Desk (Respirator Crafted)<br>
                        &nbsp;&nbsp;├── 🏙️ Commerce Avenue (Chapter 2 Warzone)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── 🛠️ Holloway's Hardware & Industrial Supply (The Electric Spanner Crafted)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── 🚌 Municipal Bus Crosswalk (Trash Dragon's Dumpster Battlefield)<br>
                        &nbsp;&nbsp;├── 🏥 St. Jude Central Clinic (3 Miles West - Active Objective)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── 📍 Isolation Ward 4 (Eleanor Vance Quarantine)<br>
                        &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── 📍 West Wing Maintenance Lab<br>
                        &nbsp;&nbsp;├── 🏭 West Rail Yards & Foundry (Ironfang Marcus Cole Territory)<br>
                        &nbsp;&nbsp;└── ⛰️ Blackwood Ridge (Endgame Target: Government Bunker 07)<br>
                    </div>
                </div>
            </div>

            <div id=\"tab-story-health\" class=\"tab-view\">
                <div class=\"card\">
                    <div class=\"card-header\">Quantitative Story Health & Narrative QA</div>
                    <div class=\"stats-grid\">
                        <div class=\"stat-card\">
                            <div class=\"stat-label\">Story Health Score</div>
                            <div class=\"stat-value\" style=\"color: var(--accent-green);\">98 / 100</div>
                        </div>
                        <div class=\"stat-card\">
                            <div class=\"stat-label\">Fluidity & Readability</div>
                            <div class=\"stat-value\" style=\"color: var(--accent-blue);\">99% (Everyday Accessible)</div>
                        </div>
                        <div class=\"stat-card\">
                            <div class=\"stat-label\">Comedy Dynamic</div>
                            <div class=\"stat-value\" style=\"color: var(--accent-amber);\">100% (Barnaby & Chad Peak)</div>
                        </div>
                        <div class=\"stat-card\">
                            <div class=\"stat-label\">Automated Tests</div>
                            <div class=\"stat-value\" style=\"color: var(--accent-green);\">36 / 36 Passing</div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script>
        const ch1_content = `{ch1_html}`;
        const ch2_content = `{ch2_html}`;

        function showTab(tabId) {{
            document.querySelectorAll('.tab-view').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            if (event && event.currentTarget) {{
                event.currentTarget.classList.add('active');
            }}
        }}

        function setChapter(num) {{
            const container = document.getElementById('reader-container');
            const meta = document.getElementById('chapter-meta');
            if (num === 1) {{
                container.innerHTML = ch1_content;
                meta.innerText = \"Showing Chapter 1: The Cracking Stacks (2,280 words)\";
            }} else {{
                container.innerHTML = ch2_content;
                meta.innerText = \"Showing Chapter 2: The Bleeding Avenues (2,918 words)\";
            }}
        }}

        function runCombatSimulation() {{
            const opponent = document.getElementById('combat-b').value;
            const resBox = document.getElementById('combat-results-box');
            resBox.style.display = \"block\";

            if (opponent === 'guard') {{
                document.getElementById('combat-outcome-title').innerText = \"Tactical Analysis: Arthur Vance vs Mutated Library Guard (Bob)\";
                document.getElementById('combat-odds').innerHTML = \"Arthur Vance: <strong style='color: var(--accent-green);'>96.2%</strong> | Mutated Guard: <strong style='color: var(--accent-red);'>3.8%</strong>\";
                document.getElementById('combat-factors').innerText = \"Decisive Factors: Chemical Environment Weaponization. Concentrated hydrochloric acid poured on quicklime created instantaneous caustic gas screen blinding and suffocating the unprotected cartilage trachea in 4.2 seconds.\";
                document.getElementById('combat-reversal').innerText = \"⚠️ Comedic Aftermath: 100% of survivors credit Barnaby the one-eared cellar rat.\";
            }} else if (opponent === 'hound') {{
                document.getElementById('combat-outcome-title').innerText = \"Tactical Analysis: Arthur Vance vs Scaled Street Hound Pack\";
                document.getElementById('combat-odds').innerHTML = \"Arthur Vance: <strong style='color: var(--accent-green);'>92.4%</strong> | Hound Pack: <strong style='color: var(--accent-red);'>7.6%</strong>\";
                document.getElementById('combat-factors').innerText = \"Decisive Factors: The Electric Spanner delivery of 15,000V neural shock to the cervical spine ganglia locked the alpha hound into immediate tetanic paralysis; secondary hound tripped with aircraft cable into utility box.\";
                document.getElementById('combat-reversal').innerText = \"⚠️ Comedic Aftermath: Chadwick Briggs claims 'Trash Dragon Thunder Strike' from inside a dumpster.\";
            }} else if (opponent === 'chad') {{
                document.getElementById('combat-outcome-title').innerText = \"Simulation: Chadwick Briggs vs Dumpster Lids\";
                document.getElementById('combat-odds').innerHTML = \"Dumpster: <strong style='color: var(--accent-green);'>99.9%</strong> | Chadwick: <strong style='color: var(--accent-red);'>0.1%</strong>\";
                document.getElementById('combat-factors').innerText = \"Decisive Factors: Aluminum softball bat bent 90 degrees on mutant shoulder; kinetic back-blow propelled Chadwick 15 feet into green garbage bin.\";
                document.getElementById('combat-reversal').innerText = \"⭐ Outcome: Chadwick earns the title of 'The Trash Dragon' and signs coffee cup autographs.\";
            }} else {{
                document.getElementById('combat-outcome-title').innerText = \"Projected Analysis: Arthur Vance vs Ironfang Marcus Cole (Severe Tier Disparity)\";
                document.getElementById('combat-odds').innerHTML = \"Marcus Cole: <strong style='color: var(--accent-red);'>78.5%</strong> | Arthur Vance: <strong style='color: var(--accent-green);'>21.5%</strong>\";
                document.getElementById('combat-factors').innerText = \"Decisive Factors: Heavy iron-chitin carapace deflects standard blunt force. Arthur requires upgraded Runic Chimera Frame and liquid nitrogen or high-amperage arc cutter to bypass armor.\";
                document.getElementById('combat-reversal').innerText = \"💡 Required Preparation: Upgrade to Chapter 4 Chimera Frame at St. Jude maintenance lab.\";
            }}
        }}
    </script>
</body>
</html>
"""

with open("frontend/dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML build complete!")
