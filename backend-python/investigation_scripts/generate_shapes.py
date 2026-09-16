import os

OUT_DIR = r"C:\Users\User\.gemini\antigravity\brain\d5a8764c-f5a4-4448-830a-dc20e1f7f25f"

def get_svg_wrapper(content, width=800, height=600):
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
            .line {{ stroke: #3498db; stroke-width: 2; stroke-dasharray: 5,5; }}
        </style>
    </defs>
    {content}
</svg>'''

# -----------------
# OBJECT 1: DRAWER
# -----------------
obj1 = '''
    <text x="30" y="40" class="title">Object 1: Drawer Assembly (Çekmece)</text>
    <text x="30" y="65" class="desc">Combining front, sides, back, and bottom into one unit.</text>

    <!-- Individual Parts -->
    <rect x="50" y="100" width="180" height="40" class="part" />
    <line x1="50" y1="120" x2="230" y2="120" stroke="#ccc" stroke-width="2" /> <!-- Groove -->
    <circle cx="100" cy="110" r="3" fill="#555" />
    <circle cx="180" cy="110" r="3" fill="#555" />
    <text x="90" y="155" class="label">[D-Front] Front Panel</text>

    <rect x="50" y="180" width="120" height="30" class="wood" />
    <text x="55" y="225" class="label">[D-Left] Side Wood</text>

    <rect x="200" y="180" width="120" height="30" class="wood" />
    <text x="205" y="225" class="label">[D-Right] Side Wood</text>

    <rect x="50" y="250" width="160" height="30" class="wood" />
    <text x="60" y="295" class="label">[D-Back] Back Wood</text>

    <rect x="50" y="320" width="170" height="110" class="mdf" />
    <text x="60" y="450" class="label">[D-Base] MDF Bottom</text>

    <!-- Arrow -->
    <path d="M 350 250 L 450 250" stroke="#3498db" stroke-width="4" fill="none" marker-end="url(#arrow)" />

    <!-- Assembled Object -->
    <g transform="translate(480, 150)">
        <!-- Back -->
        <rect x="30" y="30" width="160" height="30" class="wood" />
        <!-- Bottom MDF -->
        <rect x="30" y="60" width="160" height="80" class="mdf" />
        <!-- Sides -->
        <rect x="10" y="30" width="20" height="110" class="wood" />
        <rect x="190" y="30" width="20" height="110" class="wood" />
        <!-- Front -->
        <rect x="0" y="140" width="220" height="50" class="part" />
        <line x1="0" y1="165" x2="220" y2="165" stroke="#ccc" stroke-width="2" />
        <circle cx="80" cy="155" r="3" fill="#555" />
        <circle cx="140" cy="155" r="3" fill="#555" />
        
        <text x="20" y="215" class="label">Completed Shape 1: The Drawer</text>
    </g>
'''
with open(os.path.join(OUT_DIR, "shape1.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj1))


# -----------------
# OBJECT 2: DRESSER UNIT
# -----------------
obj2 = '''
    <text x="30" y="40" class="title">Object 2: Dresser Box (Komodin)</text>
    <text x="30" y="65" class="desc">Combining top, bottom, sides, and back panel.</text>

    <!-- Individual Parts -->
    <!-- Top -->
    <rect x="50" y="100" width="160" height="20" class="part" />
    <text x="60" y="135" class="label">[K-Top] Top Panel</text>

    <!-- Bottom -->
    <rect x="50" y="160" width="160" height="20" class="part" />
    <text x="60" y="195" class="label">[K-Bot] Bottom Panel</text>

    <!-- Left Side -->
    <rect x="50" y="220" width="60" height="140" class="part" />
    <line x1="60" y1="240" x2="100" y2="240" stroke="#ccc" stroke-width="2" />
    <line x1="60" y1="280" x2="100" y2="280" stroke="#ccc" stroke-width="2" />
    <text x="40" y="380" class="label">[K-Left] Left Side</text>

    <!-- Right Side -->
    <rect x="150" y="220" width="60" height="140" class="part" />
    <text x="140" y="380" class="label">[K-Right] Right Side</text>
    
    <!-- MDF Back -->
    <rect x="50" y="410" width="160" height="140" class="mdf" />
    <text x="60" y="570" class="label">[K-Back] MDF Back</text>

    <!-- Arrow -->
    <path d="M 330 280 L 410 280" stroke="#3498db" stroke-width="4" fill="none" marker-end="url(#arrow)" />

    <!-- Assembled Object -->
    <g transform="translate(450, 150)">
        <!-- Back -->
        <rect x="20" y="20" width="160" height="180" class="mdf" />
        <text x="60" y="110" class="label" fill="#777">[K-Back]</text>
        
        <!-- Left -->
        <rect x="0" y="20" width="20" height="180" class="part" />
        <text x="-40" y="110" class="label" fill="#555">[K-Left]</text>
        
        <!-- Right -->
        <rect x="180" y="20" width="20" height="180" class="part" />
        <text x="210" y="110" class="label" fill="#555">[K-Right]</text>

        <!-- Top -->
        <rect x="0" y="0" width="200" height="20" class="part" />
        <text x="60" y="-10" class="label" fill="#555">[K-Top]</text>

        <!-- Bottom -->
        <rect x="0" y="200" width="200" height="20" class="part" />
        <text x="60" y="235" class="label" fill="#555">[K-Bot]</text>
        
        <text x="-10" y="270" class="title">Completed Shape 2: Dresser Box</text>
    </g>
'''
with open(os.path.join(OUT_DIR, "shape2.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj2))

# -----------------
# OBJECT 3: BABY BASKET
# -----------------
obj3 = '''
    <text x="30" y="40" class="title">Object 3: Swinging Baby Basket (Beşik Sepeti)</text>
    <text x="30" y="65" class="desc">Combining slatted rails, divider wall, and base into a 4-sided basket.</text>

    <!-- Individual Parts -->
    <!-- Divider/Side -->
    <rect x="50" y="100" width="80" height="120" rx="10" class="part" />
    <text x="45" y="240" class="label">[H3] Side Divider</text>

    <!-- Base -->
    <rect x="160" y="100" width="160" height="20" class="part" />
    <text x="170" y="135" class="label">[B-Base] Basket Base</text>
    
    <!-- Back Slotted Panel -->
    <rect x="50" y="270" width="130" height="100" class="part" />
    <!-- slots -->
    <rect x="65" y="280" width="10" height="80" fill="#fff" stroke="#ccc" />
    <rect x="85" y="280" width="10" height="80" fill="#fff" stroke="#ccc" />
    <rect x="105" y="280" width="10" height="80" fill="#fff" stroke="#ccc" />
    <rect x="125" y="280" width="10" height="80" fill="#fff" stroke="#ccc" />
    <text x="50" y="390" class="label">[C2] Slotted Back Rail</text>

    <!-- Front Slatted Drop-Side -->
    <rect x="220" y="270" width="160" height="100" class="part" />
    <rect x="235" y="280" width="8" height="80" fill="#fff" stroke="#ccc" />
    <rect x="255" y="280" width="8" height="80" fill="#fff" stroke="#ccc" />
    <rect x="275" y="280" width="8" height="80" fill="#fff" stroke="#ccc" />
    <rect x="295" y="280" width="8" height="80" fill="#fff" stroke="#ccc" />
    <rect x="315" y="280" width="8" height="80" fill="#fff" stroke="#ccc" />
    <!-- Cutout -->
    <path d="M 280 270 Q 300 290 320 270" fill="#fff" stroke="#ccc" stroke-width="2" />
    <text x="220" y="390" class="label">[C1] Drop-Side Front Rail</text>

    <!-- Arrow -->
    <path d="M 390 200 L 460 200" stroke="#3498db" stroke-width="4" fill="none" marker-end="url(#arrow)" />

    <!-- Assembled Object (Top-Down Isometric-ish layout) -->
    <g transform="translate(480, 100)">
        
        <!-- Base -->
        <rect x="30" y="160" width="190" height="20" class="part" />
        <text x="80" y="175" class="label" fill="#777">[B-Base]</text>
        
        <!-- Back Slotted -->
        <rect x="30" y="40" width="190" height="120" class="part" fill="#fdfbf7" />
        <rect x="50" y="50" width="15" height="100" fill="#fff" stroke="#ccc" />
        <rect x="80" y="50" width="15" height="100" fill="#fff" stroke="#ccc" />
        <rect x="110" y="50" width="15" height="100" fill="#fff" stroke="#ccc" />
        <rect x="140" y="50" width="15" height="100" fill="#fff" stroke="#ccc" />
        <text x="80" y="25" class="label">[C2] Back</text>
        
        <!-- Left Side Divider -->
        <rect x="0" y="20" width="30" height="160" rx="10" class="part" />
        <text x="-40" y="90" class="label">[H3]</text>
        
        <!-- Front Drop-Side (Slightly lowered/transparent to show inside) -->
        <rect x="30" y="90" width="190" height="90" class="part" opacity="0.85" />
        <rect x="50" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <rect x="75" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <rect x="100" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <rect x="125" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <rect x="150" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <rect x="175" y="100" width="10" height="70" fill="#fff" stroke="#ccc" />
        <path d="M 105 90 Q 125 110 145 90" fill="none" stroke="#ccc" stroke-width="2" />
        
        <text x="60" y="210" class="label">[C1] Front</text>

        <text x="0" y="260" class="title">Completed Shape 3: Baby Basket</text>
    </g>
'''
with open(os.path.join(OUT_DIR, "shape3.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(obj3))

print("Shape SVGs created successfully!")
