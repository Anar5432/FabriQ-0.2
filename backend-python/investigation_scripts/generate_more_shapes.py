import os

OUT_DIR = r"C:\Users\User\.gemini\antigravity\brain\d5a8764c-f5a4-4448-830a-dc20e1f7f25f"

def get_svg_wrapper(content, width=850, height=600):
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:sans-serif; border: 1px solid #eee;">
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3498db" />
        </marker>
        <style>
            .part {{ fill: #fdfbf7; stroke: #555; stroke-width: 2; }}
            .mdf {{ fill: #d3b89b; stroke: #8b7355; stroke-width: 2; }}
            .wood {{ fill: #e6dac3; stroke: #8b7355; stroke-width: 2; }}
            .label {{ font-size: 14px; font-weight: bold; fill: #2c3e50; }}
            .title {{ font-size: 22px; font-weight: bold; fill: #2c3e50; }}
            .desc {{ font-size: 14px; fill: #7f8c8d; }}
            .highlight {{ fill: #fff5f5; stroke: #e74c3c; stroke-width: 2; stroke-dasharray: 4,4; }}
        </style>
    </defs>
    {content}
</svg>'''

# -----------------
# OBJECT 4: MAIN BED FRAME
# -----------------
obj4 = '''
    <text x="30" y="40" class="title">Shape 4: Main Bed Frame (Ana Karyola Kasası)</text>
    <text x="30" y="65" class="desc">Combining the large side rails, headboard, footboard, back guard, and mattress base.</text>

    <!-- Individual Parts -->
    <!-- Headboard -->
    <rect x="50" y="90" width="30" height="110" rx="5" class="part" />
    <text x="35" y="145" class="label" transform="rotate(-90 35,145)">[H1] Headboard</text>

    <!-- Footboard -->
    <rect x="120" y="90" width="30" height="110" rx="5" class="part" />
    <text x="105" y="145" class="label" transform="rotate(-90 105,145)">[H2] Footboard</text>

    <!-- Side Rails -->
    <rect x="50" y="240" width="160" height="20" class="part" />
    <text x="60" y="230" class="label">[L1] & [L2] Side Rails</text>
    <rect x="50" y="270" width="160" height="20" class="part" />

    <!-- Back Guard -->
    <path d="M 50 320 Q 90 300 130 320 T 210 320 L 210 350 L 50 350 Z" class="part" />
    <text x="50" y="375" class="label">[L3] Wavy Back Guard</text>

    <!-- Base Board -->
    <rect x="50" y="410" width="160" height="40" class="part" fill="#f0f0f0" />
    <text x="50" y="475" class="label">[L4] Mattress Base</text>

    <!-- Arrow -->
    <path d="M 280 250 L 380 250" stroke="#3498db" stroke-width="4" fill="none" marker-end="url(#arrow)" />

    <!-- Assembled Object -->
    <g transform="translate(420, 150)">
        
        <!-- Back Rail L2 -->
        <rect x="20" y="120" width="300" height="20" class="part" fill="#f4f4f4" />
        
        <!-- Wavy Back Guard L3 -->
        <path d="M 20 50 Q 100 -20 180 50 T 320 50 L 320 120 L 20 120 Z" class="part" fill="#fcfcfc" />
        <text x="120" y="55" class="label" fill="#777">[L3]</text>

        <!-- Base L4 -->
        <rect x="20" y="140" width="300" height="30" class="part" fill="#f0f0f0" />
        <text x="130" y="160" class="label" fill="#777">[L4]</text>

        <!-- Headboard H1 -->
        <rect x="0" y="0" width="30" height="200" rx="10" class="part" />
        <text x="-15" y="100" class="label" transform="rotate(-90 -15,100)">[H1]</text>

        <!-- Footboard H2 -->
        <rect x="310" y="0" width="30" height="200" rx="10" class="part" />
        <text x="350" y="100" class="label" transform="rotate(-90 350,100)">[H2]</text>

        <!-- Front Rail L1 -->
        <rect x="20" y="170" width="300" height="30" class="part" />
        <text x="150" y="190" class="label">[L1]</text>

        <text x="0" y="250" class="title">Completed Shape 4: Main Bed Frame</text>
    </g>
'''
with open(os.path.join(OUT_DIR, "shape4.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj4))


# -----------------
# OBJECT 5: FINAL ASSEMBLY (All Shapes Combined)
# -----------------
obj5 = '''
    <text x="30" y="40" class="title">Shape 5: Final Bed Structure (Tamamlanmış Beşik)</text>
    <text x="30" y="65" class="desc">Combining the 4 completed sub-assemblies into the final piece of furniture.</text>

    <!-- Individual Parts (The Shapes) -->
    
    <!-- Shape 4: Frame -->
    <rect x="40" y="90" width="160" height="60" class="part" />
    <text x="50" y="130" class="label">Shape 4: Main Frame</text>

    <!-- Shape 2: Dresser -->
    <rect x="40" y="170" width="80" height="80" class="highlight" />
    <text x="50" y="215" class="label">Shape 2: Dresser</text>

    <!-- Shape 1: Drawers x3 -->
    <rect x="150" y="170" width="60" height="15" class="part" />
    <rect x="150" y="190" width="60" height="15" class="part" />
    <rect x="150" y="210" width="60" height="15" class="part" />
    <text x="145" y="245" class="label">Shape 1: Drawers(x3)</text>
    
    <!-- Shape 3: Basket -->
    <rect x="40" y="270" width="120" height="70" class="part" />
    <line x1="50" y1="280" x2="50" y2="330" stroke="#ccc" stroke-width="2"/>
    <line x1="70" y1="280" x2="70" y2="330" stroke="#ccc" stroke-width="2"/>
    <line x1="90" y1="280" x2="90" y2="330" stroke="#ccc" stroke-width="2"/>
    <text x="50" y="365" class="label">Shape 3: Baby Basket</text>

    <!-- Swing Links -->
    <rect x="190" y="280" width="10" height="40" rx="5" class="part" fill="#ccc" />
    <text x="175" y="335" class="label">[S-Links]</text>

    <!-- Arrow -->
    <path d="M 280 200 L 380 200" stroke="#3498db" stroke-width="4" fill="none" marker-end="url(#arrow)" />

    <!-- Assembled Object -->
    <g transform="translate(420, 100)">
        
        <!-- Shape 4 (Frame) Background -->
        <rect x="20" y="120" width="300" height="20" class="part" fill="#f4f4f4" />
        <path d="M 20 50 Q 100 -20 180 50 T 320 50 L 320 120 L 20 120 Z" class="part" fill="#fcfcfc" />
        <rect x="20" y="140" width="300" height="30" class="part" fill="#f0f0f0" />
        <rect x="0" y="0" width="30" height="200" rx="10" class="part" />
        <rect x="310" y="0" width="30" height="200" rx="10" class="part" />
        
        <!-- Shape 2 (Dresser) Placed -->
        <rect x="190" y="70" width="120" height="100" class="highlight" />
        <text x="210" y="60" class="label" fill="#e74c3c">Shape 2</text>

        <!-- Shape 1 (Drawers) Placed -->
        <rect x="200" y="80" width="100" height="20" class="part" />
        <rect x="200" y="110" width="100" height="20" class="part" />
        <rect x="200" y="140" width="100" height="20" class="part" />
        <circle cx="250" cy="90" r="2" fill="#555" />
        <circle cx="250" cy="120" r="2" fill="#555" />
        <circle cx="250" cy="150" r="2" fill="#555" />

        <!-- Shape 3 (Basket) Placed -->
        <rect x="50" y="70" width="120" height="80" class="part" />
        <!-- Slats for Basket -->
        <rect x="60" y="80" width="8" height="60" fill="#fff" stroke="#ccc"/>
        <rect x="80" y="80" width="8" height="60" fill="#fff" stroke="#ccc"/>
        <rect x="100" y="80" width="8" height="60" fill="#fff" stroke="#ccc"/>
        <rect x="120" y="80" width="8" height="60" fill="#fff" stroke="#ccc"/>
        <rect x="140" y="80" width="8" height="60" fill="#fff" stroke="#ccc"/>
        <text x="70" y="60" class="label" fill="#2c3e50">Shape 3</text>

        <!-- Swing Links S-Links -->
        <rect x="35" y="80" width="10" height="30" rx="3" fill="#999" />
        <rect x="175" y="80" width="10" height="30" rx="3" fill="#999" />

        <!-- Shape 4 Front Rail -->
        <rect x="20" y="170" width="300" height="30" class="part" />

        <text x="30" y="250" class="title">Completed Shape 5: Full Bed</text>
    </g>
'''
with open(os.path.join(OUT_DIR, "shape4.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj4))

with open(os.path.join(OUT_DIR, "shape5.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj5))

print("More SVGs created successfully!")
