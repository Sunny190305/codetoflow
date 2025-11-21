import re
import uuid

def add_node(nodes, node_type, label):
    node = {
        "id": str(uuid.uuid4()),
        "type": node_type,
        "label": label
    }
    nodes.append(node)
    return node["id"]

def parse_java_code(code):
    nodes = []
    edges = []
    
    # Normalize code
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    
    last_id = None
    
    # Regex patterns
    # Method definition: public static void main(String[] args) {
    # Simplified: access_mod return_type name(args) {
    method_pattern = re.compile(r'^(?:public|private|protected|static|\s)*[\w<>]+\s+(\w+)\s*\(.*\)\s*\{?$')
    
    if_pattern = re.compile(r'^if\s*\((.*)\)\s*\{?$')
    else_pattern = re.compile(r'^else\s*\{?$')
    else_if_pattern = re.compile(r'^else\s+if\s*\((.*)\)\s*\{?$')
    while_pattern = re.compile(r'^while\s*\((.*)\)\s*\{?$')
    for_pattern = re.compile(r'^for\s*\((.*)\)\s*\{?$')
    
    for line in lines:
        node_id = None
        
        # Check for class definition (ignore for flow, but maybe good to note)
        if line.startswith("class "):
            continue

        if match := method_pattern.match(line):
            if "if" not in line and "while" not in line and "for" not in line and "new" not in line:
                node_id = add_node(nodes, "function", f"Method: {match.group(1)}")
        
        elif match := if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"If: {match.group(1)}")
            
        elif match := else_if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"Else If: {match.group(1)}")
            
        elif else_pattern.match(line):
            node_id = add_node(nodes, "process", "Else")
            
        elif match := while_pattern.match(line):
            node_id = add_node(nodes, "loop", f"While: {match.group(1)}")
            
        elif match := for_pattern.match(line):
            node_id = add_node(nodes, "loop", f"For: {match.group(1)}")
            
        elif line.endswith(';') and '}' not in line and '{' not in line:
            node_id = add_node(nodes, "process", line)
            
        if node_id:
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            last_id = node_id
            
    return {"nodes": nodes, "edges": edges}
