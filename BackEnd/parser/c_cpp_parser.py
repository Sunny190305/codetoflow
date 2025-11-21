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
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    
    # Regex patterns
    func_pattern = re.compile(r'^\w+\s+(\w+)\s*\(.*\)\s*\{?$')
    if_pattern = re.compile(r'^if\s*\((.*)\)\s*\{?$')
    else_pattern = re.compile(r'^else\s*\{?$')
    else_if_pattern = re.compile(r'^else\s+if\s*\((.*)\)\s*\{?$')
    while_pattern = re.compile(r'^while\s*\((.*)\)\s*\{?$')
    for_pattern = re.compile(r'^for\s*\((.*)\)\s*\{?$')
    
    last_id = None
    decision_stack = []  # Stack to track if/else blocks
    
    i = 0
    while i < len(lines):
        line = lines[i]
        node_id = None
        
        if match := func_pattern.match(line):
            if "if" not in line and "while" not in line and "for" not in line:
                node_id = add_node(nodes, "function", f"Function: {match.group(1)}")
        
        elif match := if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"If: {match.group(1)}")
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            decision_stack.append({"if_node": node_id, "last_then": None, "last_else": None})
            last_id = None  # Reset to handle then branch
            i += 1
            continue
            
        elif match := else_if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"Else If: {match.group(1)}")
            if decision_stack:
                parent = decision_stack[-1]["if_node"]
                edges.append({"from": parent, "to": node_id})
            decision_stack.append({"if_node": node_id, "last_then": None, "last_else": None})
            last_id = None
            i += 1
            continue
            
        elif else_pattern.match(line):
            node_id = add_node(nodes, "process", "Else")
            if decision_stack:
                parent = decision_stack[-1]["if_node"]
                edges.append({"from": parent, "to": node_id})
                decision_stack[-1]["last_else"] = node_id
            last_id = node_id
            i += 1
            continue
            
        elif match := while_pattern.match(line):
            node_id = add_node(nodes, "loop", f"While: {match.group(1)}")
            
        elif match := for_pattern.match(line):
            node_id = add_node(nodes, "loop", f"For: {match.group(1)}")
            
        elif line.endswith(';') and '}' not in line and '{' not in line:
            node_id = add_node(nodes, "process", line)
        
        elif line == '}':
            if decision_stack:
                decision_stack.pop()
            i += 1
            continue
            
        # Connect nodes
        if node_id:
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            elif decision_stack and decision_stack[-1]["last_then"] is None:
                # First statement in then branch
                parent = decision_stack[-1]["if_node"]
                edges.append({"from": parent, "to": node_id})
                decision_stack[-1]["last_then"] = node_id
            last_id = node_id
            
        i += 1
            
    return {"nodes": nodes, "edges": edges}
