import re

def add_search_to_3d():
    path = r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'id="searchInput"' in content:
        print("Search already in 3D map")
        return

    # Add search HTML
    search_html = """
        <hr>
        <div style="margin-top: 10px;">
            <input type="text" id="searchInput" placeholder="Search table..." style="padding: 5px; width: 150px; border-radius: 3px; border: 1px solid #ccc;">
            <button onclick="searchNode()" style="padding: 5px; cursor: pointer; border-radius: 3px;">Search</button>
        </div>
    </div>
    """
    content = content.replace('</div>\n    <div id="3d-graph">', search_html + '    <div id="3d-graph">')

    # Add search JS
    search_js = """
        function searchNode() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            if (!query) return;
            const nodes = Graph.graphData().nodes;
            const found = nodes.find(n => n.id.toLowerCase().includes(query) || (n.name && n.name.toLowerCase().includes(query)));
            if (found) {
                // Focus on node
                const distance = 100;
                const distRatio = 1 + distance/Math.hypot(found.x, found.y, found.z);
                Graph.cameraPosition(
                    { x: found.x * distRatio, y: found.y * distRatio, z: found.z * distRatio },
                    found,
                    3000
                );
            } else {
                alert("Table not found!");
            }
        }
    </script>
    """
    content = content.replace('</script>\n</body>', search_js + '</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated 3D map")

def add_search_to_2d():
    path = r'C:\Users\User\.gemini\antigravity\brain\672f7d1e-7d0b-441e-be38-f3f10ade7c45\database_map_2d.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'id="searchInput"' in content:
        print("Search already in 2D map")
        return

    # Add search HTML
    search_html = """
        <hr>
        <div style="margin-top: 10px;">
            <input type="text" id="searchInput" placeholder="Search table..." style="padding: 5px; width: 150px; border-radius: 3px; border: 1px solid #ccc; color: black;">
            <button onclick="searchNode()" style="padding: 5px; cursor: pointer; border-radius: 3px; color: black;">Search</button>
        </div>
    </div>
    """
    content = content.replace('</div>\n    <div id="mynetwork">', search_html + '    <div id="mynetwork">')

    # Add search JS
    search_js = """
        function searchNode() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            if (!query) return;
            const allNodes = nodes.get();
            const found = allNodes.find(n => n.id.toLowerCase().includes(query) || (n.label && n.label.toLowerCase().includes(query)));
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
                alert("Table not found!");
            }
        }
    </script>
    """
    content = content.replace('</script>\n</body>', search_js + '</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated 2D map")

add_search_to_3d()
add_search_to_2d()
