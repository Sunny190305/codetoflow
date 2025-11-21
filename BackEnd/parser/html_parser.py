try:
    from bs4 import BeautifulSoup
except ImportError:
    # Simple fallback parser that treats the whole HTML as a single node
    class BeautifulSoup:
        def __init__(self, html, parser):
            self.html = html
        @property
        def body(self):
            return self
        @property
        def children(self):
            return []
        def __iter__(self):
            return iter([])
import uuid

def add_node(nodes, node_type, label):
    node = {
        "id": str(uuid.uuid4()),
        "type": node_type,
        "label": label
    }
    nodes.append(node)
    return node["id"]

def parse_html_recursive(element, nodes, edges, parent_id=None):
    if element.name:
        label = f"<{element.name}>"
        if element.get('id'):
            label += f" #{element['id']}"
        elif element.get('class'):
            label += f" .{'.'.join(element['class'])}"
            
        node_id = add_node(nodes, "process", label)
        
        if parent_id:
            edges.append({"from": parent_id, "to": node_id})
            
        for child in element.children:
            if child.name: # Ignore text nodes for now to keep it clean
                parse_html_recursive(child, nodes, edges, node_id)

def parse_html_code(code):
    nodes = []
    edges = []
    
    try:
        soup = BeautifulSoup(code, 'html.parser')
        
        # Start from body if exists, else just the top elements
        root = soup.body if soup.body else soup
        
        for child in root.children:
            if child.name:
                parse_html_recursive(child, nodes, edges)
                
    except Exception as e:
        return {"error": f"Error parsing HTML: {str(e)}"}
        
    return {"nodes": nodes, "edges": edges}
