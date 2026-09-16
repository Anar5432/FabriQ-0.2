import os

OUT_DIR = r"C:\Users\User\.gemini\antigravity\brain\d5a8764c-f5a4-4448-830a-dc20e1f7f25f"

def get_svg_wrapper(content, width=800, height=400):
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:sans-serif;">
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#e74c3c" />
        </marker>
        <style>
            .wood {{ fill: #fdfbf7; stroke: #555; stroke-width: 2; }}
            .highlight {{ stroke: #e74c3c; stroke-width: 3; stroke-dasharray: 4,4; fill: #fff5f5; }}
            .text-label {{ font-size: 16px; font-weight: bold; fill: #333; }}
            .text-desc {{ font-size: 14px; fill: #555; }}
            .hardware {{ fill: #ccc; stroke: #666; stroke-width: 1.5; }}
        </style>
    </defs>
    {content}
</svg>'''

# -----------------
# STEP 1: Main Bed
# -----------------
step1_content = '''
    <!-- Main Base -->
    <rect x="150" y="250" width="400" height="40" class="wood" />
    <text x="270" y="275" class="text-label">[L1] Front Side Rail</text>
    
    <rect x="170" y="200" width="400" height="15" class="wood" fill="#f0f0f0" />
    <text x="320" y="212" class="text-desc">[L2] Back Rail</text>

    <!-- Headboard (Left) -->
    <rect x="130" y="100" width="40" height="200" rx="10" class="wood" />
    <text x="135" y="180" class="text-label" transform="rotate(-90 135,180)">[H1] Headboard</text>

    <!-- Footboard (Right) -->
    <rect x="530" y="100" width="40" height="200" rx="10" class="wood" />
    <text x="535" y="200" class="text-label" transform="rotate(-90 535,200)">[H2] Footboard</text>

    <!-- Base Board -->
    <rect x="170" y="230" width="360" height="20" class="wood" fill="#e6e6e6" />
    <text x="280" y="245" class="text-label">[L4] Mattress Base Board</text>

    <!-- Arrows & Info -->
    <path d="M 100 150 Q 150 100 200 150" stroke="#e74c3c" stroke-width="2" fill="none" marker-end="url(#arrow)" />
    <text x="50" y="80" class="text-label" fill="#e74c3c">Step 1: Assemble the Outer Bed Frame</text>
'''
with open(os.path.join(OUT_DIR, "step1.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(step1_content))


# -----------------
# STEP 2: Dresser
# -----------------
step2_content = '''
    <!-- Main Bed Context -->
    <rect x="150" y="250" width="400" height="40" class="wood" opacity="0.3" />
    <rect x="130" y="100" width="40" height="200" rx="10" class="wood" opacity="0.3" />
    <rect x="530" y="100" width="40" height="200" rx="10" class="wood" />
    <text x="535" y="200" class="text-label" transform="rotate(-90 535,200)">[H2] Footboard</text>

    <!-- Dresser Box -->
    <rect x="380" y="120" width="150" height="130" class="highlight" />
    <text x="400" y="145" class="text-label">[D-Panels]</text>
    <text x="400" y="165" class="text-desc">Dresser Unit</text>

    <!-- Drawers -->
    <rect x="390" y="175" width="130" height="20" class="wood" />
    <text x="420" y="190" class="text-desc">[D1] Drawer</text>
    <rect x="390" y="200" width="130" height="20" class="wood" />
    <text x="420" y="215" class="text-desc">[D2] Drawer</text>
    <rect x="390" y="225" width="130" height="20" class="wood" />
    <text x="420" y="240" class="text-desc">[D3] Drawer</text>
    
    <!-- Arrows -->
    <path d="M 450 80 L 450 110" stroke="#e74c3c" stroke-width="3" fill="none" marker-end="url(#arrow)" />
    <text x="50" y="80" class="text-label" fill="#e74c3c">Step 2: Build the Dresser & Place Against Footboard</text>
'''
with open(os.path.join(OUT_DIR, "step2.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(step2_content))

# -----------------
# STEP 3: Crib Basket
# -----------------
step3_content = '''
    <!-- Context -->
    <rect x="150" y="250" width="400" height="40" class="wood" opacity="0.3" />
    <rect x="130" y="100" width="40" height="200" rx="10" class="wood" />
    <text x="135" y="180" class="text-label" transform="rotate(-90 135,180)">[H1] Headboard</text>
    <rect x="380" y="120" width="150" height="130" class="wood" opacity="0.4"/>
    <text x="400" y="145" class="text-desc">Dresser Unit</text>
    
    <!-- Crib Basket -->
    <rect x="190" y="120" width="170" height="110" class="highlight" />
    <text x="210" y="170" class="text-label">[C2] & [H3]</text>
    <text x="200" y="190" class="text-desc">Crib Basket Frame</text>
    
    <!-- Swing Links -->
    <rect x="155" y="140" width="20" height="60" rx="10" class="hardware" />
    <circle cx="165" cy="150" r="3" fill="white"/>
    <circle cx="165" cy="190" r="3" fill="white"/>
    <text x="110" y="130" class="text-label" fill="#e74c3c">[S-Links]</text>

    <rect x="375" y="140" width="20" height="60" rx="10" class="hardware" />
    <circle cx="385" cy="150" r="3" fill="white"/>
    <circle cx="385" cy="190" r="3" fill="white"/>
    <text x="360" y="130" class="text-label" fill="#e74c3c">[S-Links]</text>

    <!-- Arrow -->
    <path d="M 270 70 L 270 110" stroke="#e74c3c" stroke-width="3" fill="none" marker-end="url(#arrow)" />
    <text x="50" y="80" class="text-label" fill="#e74c3c">Step 3: Hang the Crib Basket onto the Swing Links</text>
'''
with open(os.path.join(OUT_DIR, "step3.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(step3_content))

# -----------------
# STEP 4: Drop Side & Final
# -----------------
step4_content = '''
    <!-- Complete Bed -->
    <rect x="150" y="250" width="400" height="40" class="wood" />
    <rect x="130" y="100" width="40" height="200" rx="10" class="wood" />
    <rect x="530" y="100" width="40" height="200" rx="10" class="wood" />
    
    <rect x="380" y="120" width="150" height="130" class="wood" />
    <rect x="390" y="175" width="130" height="20" class="wood" />
    <rect x="390" y="200" width="130" height="20" class="wood" />
    <rect x="390" y="225" width="130" height="20" class="wood" />
    
    <!-- Crib Basket -->
    <rect x="190" y="120" width="170" height="110" class="wood" />
    
    <!-- Drop Side Rail (Slatted) -->
    <rect x="190" y="130" width="170" height="90" class="highlight" />
    <!-- Slats -->
    <rect x="200" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="220" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="240" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="260" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="280" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="300" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="320" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>
    <rect x="340" y="135" width="10" height="80" fill="#fff" stroke="#ccc"/>

    <text x="210" y="180" class="text-label" fill="#e74c3c" style="background:#fff">[C1] Drop-Side Rail</text>

    <!-- Metal Rod -->
    <line x1="180" y1="120" x2="180" y2="230" stroke="#777" stroke-width="4" />
    <text x="110" y="235" class="text-label" fill="#e74c3c">[M-Rod]</text>
    <line x1="370" y1="120" x2="370" y2="230" stroke="#777" stroke-width="4" />

    <text x="50" y="80" class="text-label" fill="#e74c3c">Step 4: Insert Guide Rods & Attach Drop-Side Rail</text>
    <text x="220" y="330" class="text-label" font-size="20">Final Assembled Büyüyen Beşik</text>
'''
with open(os.path.join(OUT_DIR, "step4.svg"), "w", encoding="utf-8") as f:
    f.write(get_svg_wrapper(step4_content))

print("SVGs created successfully!")
