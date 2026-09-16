import re

def update_ui_3d():
    path = r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the legend content (inside overlay, excluding the search part we added)
    # The original had <h2>BTF ERP 3D Database Map</h2> ...
    
    # We will just completely replace the style, overlay and script
    new_style = """
    <style>
        body { margin: 0; padding: 0; background-color: #111; color: white; font-family: sans-serif; overflow: hidden; } 
        #3d-graph { width: 100vw; height: 100vh; }
        
        /* New UI Elements */
        #searchContainer {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100;
            display: flex;
            align-items: center;
            background: #fff;
            border-radius: 24px;
            padding: 5px 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        #searchInput {
            border: none;
            outline: none;
            padding: 8px;
            font-size: 16px;
            width: 300px;
            color: black;
            background: transparent;
        }
        #searchBtn {
            border: none;
            background: transparent;
            cursor: pointer;
            color: #333;
            font-weight: bold;
            font-size: 16px;
            padding: 5px;
        }
        #searchBtn:hover { color: #000; }
        
        #menuBtn {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 100;
            cursor: pointer;
            background: rgba(0,0,0,0.8);
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        #sidebar {
            position: absolute;
            top: 0;
            left: -350px;
            width: 300px;
            height: 100vh;
            background: rgba(0,0,0,0.9);
            padding: 20px;
            padding-top: 70px;
            z-index: 99;
            transition: left 0.3s ease;
            box-sizing: border-box;
            overflow-y: auto;
            border-right: 1px solid #333;
        }
        
        .legend-item { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; } 
        .color-box { width: 15px; height: 15px; border-radius: 3px; }
    </style>
    """
    
    new_html = """
<body>
    <div id="searchContainer">
        <input type="text" id="searchInput" placeholder="Search table name (e.g. sm_good_xidmet)">
        <button id="searchBtn" onclick="searchNode()">Search</button>
    </div>

    <button id="menuBtn">☰ Legend & Info</button>

    <div id="sidebar">
        <h2>BTF ERP 3D Map</h2>
        <div class="legend-item"><div class="color-box" style="background: #27AE60;"></div> Green: Dashboard Active</div>
        <div class="legend-item"><div class="color-box" style="background: #2980B9;"></div> Blue: System Active</div>
        <div class="legend-item"><div class="color-box" style="background: #E74C3C;"></div> Red: Inactive / Old</div>
        <hr style="border-color:#444">
        <div class="legend-item">📅 <b>White Ring:</b> Date-Verified Table</div>
        <div class="legend-item">🗂️ <b>No Ring:</b> Static Dictionary Table</div>
        <br>
        <small><i>Scroll to zoom.<br>Left click & drag to rotate.<br>Right click & drag to pan.</i></small>
    </div>

    <div id="3d-graph"></div>
    """
    
    # Replace from <style> to <div id="3d-graph">
    content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)
    content = re.sub(r'<body>.*?<div id="3d-graph"></div>', new_html, content, flags=re.DOTALL)
    
    # Update script to include the new search logic and sidebar toggle
    new_script = """
    <script>
        const sidebar = document.getElementById('sidebar');
        const menuBtn = document.getElementById('menuBtn');
        menuBtn.addEventListener('click', (e) => {
            sidebar.style.left = sidebar.style.left === '0px' ? '-350px' : '0px';
            e.stopPropagation();
        });
        document.body.addEventListener('click', (e) => {
            if(sidebar.style.left === '0px' && !sidebar.contains(e.target) && e.target !== menuBtn) {
                sidebar.style.left = '-350px';
            }
        });

        function searchNode() {
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            if (!query) return;
            const nodes = Graph.graphData().nodes;
            
            // Try exact match first
            let found = nodes.find(n => n.id.toLowerCase() === query);
            if (!found) {
                // Try partial match
                found = nodes.find(n => n.id.toLowerCase().includes(query) || (n.name && n.name.toLowerCase().includes(query)));
            }
            
            if (found) {
                if (found.x === undefined || found.y === undefined) {
                    alert("Graph is still calculating layout, please try again in a few seconds.");
                    return;
                }
                const distance = 100;
                const distRatio = 1 + distance/Math.hypot(found.x, found.y, found.z);
                Graph.cameraPosition(
                    { x: found.x * distRatio, y: found.y * distRatio, z: found.z * distRatio },
                    found,
                    2000
                );
            } else {
                alert("Table not found: " + query);
            }
        }
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchNode();
            }
        });
    </script>
</body>
    """
    
    # Find where the old script ends and replace search logic
    content = re.sub(r'function searchNode\(\) \{.*?</script>\s*</body>', new_script, content, flags=re.DOTALL)
    
    # If the old script didn't have searchNode yet (in case regex failed), we just append it before </body>
    if 'function searchNode()' not in content:
        content = content.replace('</body>', new_script)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("3D Map UI updated")

def update_ui_2d():
    path = r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map_2d.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_style = """
    <style type="text/css">
        body { font-family: sans-serif; margin: 0; padding: 0; background-color: #1a1a1a; color: #fff; overflow: hidden; }
        #mynetwork { width: 100vw; height: 100vh; }
        
        /* New UI Elements */
        #searchContainer {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100;
            display: flex;
            align-items: center;
            background: #fff;
            border-radius: 24px;
            padding: 5px 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        #searchInput {
            border: none;
            outline: none;
            padding: 8px;
            font-size: 16px;
            width: 300px;
            color: black;
            background: transparent;
        }
        #searchBtn {
            border: none;
            background: transparent;
            cursor: pointer;
            color: #333;
            font-weight: bold;
            font-size: 16px;
            padding: 5px;
        }
        #searchBtn:hover { color: #000; }
        
        #menuBtn {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 100;
            cursor: pointer;
            background: rgba(0,0,0,0.8);
            color: white;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        #sidebar {
            position: absolute;
            top: 0;
            left: -350px;
            width: 300px;
            height: 100vh;
            background: rgba(0,0,0,0.9);
            padding: 20px;
            padding-top: 70px;
            z-index: 99;
            transition: left 0.3s ease;
            box-sizing: border-box;
            overflow-y: auto;
            border-right: 1px solid #333;
        }
        
        .legend-item { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
        .color-box { width: 15px; height: 15px; border-radius: 3px; }
        .line-box { width: 25px; height: 3px; }
    </style>
    """
    
    new_html = """
<body>
    <div id="searchContainer">
        <input type="text" id="searchInput" placeholder="Search table name (e.g. sm_good_xidmet)">
        <button id="searchBtn" onclick="searchNode()">Search</button>
    </div>

    <button id="menuBtn">☰ Legend & Info</button>

    <div id="sidebar">
        <h2>BTF ERP 2D Map</h2>
        <p><strong>Visibility:</strong> 100% of the Database (385/386 tables)</p>
        <hr style="border-color:#444">
        <div class="legend-item"><div class="color-box" style="background: #27AE60;"></div> Green: Dashboard Active</div>
        <div class="legend-item"><div class="color-box" style="background: #2980B9;"></div> Blue: System Active</div>
        <div class="legend-item"><div class="color-box" style="background: #E74C3C;"></div> Red: Inactive / Empty / Old</div>
        <div class="legend-item"><div class="color-box" style="background: #F39C12;"></div> Orange: Modules</div>
        <div class="legend-item"><div class="color-box" style="background: #8E44AD;"></div> Purple: Root DB</div>
        <hr style="border-color:#444">
        <div class="legend-item"><div class="line-box" style="background: #F1C40F;"></div> Golden Line: Main Tree Branch</div>
        <div class="legend-item"><div class="line-box" style="background: #BDC3C7;"></div> Silver Line: Foreign Key Link</div>
        <br>
        <small><i>Scroll to zoom.<br>Click & drag to pan.</i></small>
    </div>

    <div id="mynetwork"></div>
    """
    
    content = re.sub(r'<style type="text/css">.*?</style>', new_style, content, flags=re.DOTALL)
    content = re.sub(r'<body>.*?<div id="mynetwork"></div>', new_html, content, flags=re.DOTALL)
    
    new_script = """
        const sidebar = document.getElementById('sidebar');
        const menuBtn = document.getElementById('menuBtn');
        menuBtn.addEventListener('click', (e) => {
            sidebar.style.left = sidebar.style.left === '0px' ? '-350px' : '0px';
            e.stopPropagation();
        });
        document.body.addEventListener('click', (e) => {
            if(sidebar.style.left === '0px' && !sidebar.contains(e.target) && e.target !== menuBtn) {
                sidebar.style.left = '-350px';
            }
        });

        function searchNode() {
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            if (!query) return;
            const allNodes = nodes.get();
            
            let found = allNodes.find(n => n.id.toLowerCase() === query);
            if (!found) {
                found = allNodes.find(n => n.id.toLowerCase().includes(query) || (n.label && n.label.toLowerCase().includes(query)));
            }
            
            if (found) {
                network.selectNodes([found.id]);
                network.focus(found.id, {
                    scale: 1.5,
                    animation: {
                        duration: 1000,
                        easingFunction: "easeInOutQuad"
                    }
                });
            } else {
                alert("Table not found: " + query);
            }
        }
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchNode();
            }
        });
    </script>
</body>
    """
    
    content = re.sub(r'function searchNode\(\) \{.*?</script>\s*</body>', new_script, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("2D Map UI updated")

update_ui_3d()
update_ui_2d()
