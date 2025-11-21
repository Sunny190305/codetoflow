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

def parse_c_cpp_code(code):
    nodes = []
    edges = []
    
    # Normalize code: remove comments and extra whitespace
    # Simple comment removal (not perfect but works for snippets)
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    
    last_id = None
    parent_stack = [] # Stack to track scope (simplified)
    
    # Regex patterns
    # Function definition: type name(args) {
    func_pattern = re.compile(r'^\w+\s+(\w+)\s*\(.*\)\s*\{?$')
    # Control structures
    if_pattern = re.compile(r'^if\s*\((.*)\)\s*\{?$')
    else_pattern = re.compile(r'^else\s*\{?$')
    else_if_pattern = re.compile(r'^else\s+if\s*\((.*)\)\s*\{?$')
    while_pattern = re.compile(r'^while\s*\((.*)\)\s*\{?$')
    for_pattern = re.compile(r'^for\s*\((.*)\)\s*\{?$')
    
    # Simple line-by-line processing (heuristic)
    # This is a "flat" parser that detects structures but doesn't perfectly handle nesting 
    # without a full parser. It connects sequential statements.
    
    for line in lines:
        node_id = None
        
        if match := func_pattern.match(line):
            if "if" not in line and "while" not in line and "for" not in line: # Avoid false positives
                node_id = add_node(nodes, "function", f"Function: {match.group(1)}")
        
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
            # Regular statement
            node_id = add_node(nodes, "process", line)
            
        # If we created a node, connect it to the previous one
        if node_id:
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            last_id = node_id
            
    return {"nodes": nodes, "edges": edges}
