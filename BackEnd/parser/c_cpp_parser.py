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
    
    # Normalize code
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
    switch_pattern = re.compile(r'^switch\s*\((.*)\)\s*\{?$')
    case_pattern = re.compile(r'^case\s+(.*):$')
    default_pattern = re.compile(r'^default\s*:$')
    
    last_id = None
    # Stack to track nested structures
    # Each item: {type: 'if'|'switch', id: node_id, end_nodes: []}
    stack = [] 
    
    i = 0
    while i < len(lines):
        line = lines[i]
        node_id = None
        
        # Function definition
        if match := func_pattern.match(line):
            if "if" not in line and "while" not in line and "for" not in line and "switch" not in line:
                node_id = add_node(nodes, "function", f"Function: {match.group(1)}")
        
        # Switch statement
        elif match := switch_pattern.match(line):
            node_id = add_node(nodes, "decision", f"Switch: {match.group(1)}")
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            stack.append({"type": "switch", "id": node_id, "end_nodes": []})
            last_id = None # Reset last_id so cases connect to switch
            i += 1
            continue

        # Case statement
        elif match := case_pattern.match(line):
            node_id = add_node(nodes, "decision", f"Case: {match.group(1)}")
            if stack and stack[-1]["type"] == "switch":
                edges.append({"from": stack[-1]["id"], "to": node_id})
            last_id = node_id
            i += 1
            continue

        # Default statement
        elif default_pattern.match(line):
            node_id = add_node(nodes, "decision", "Default")
            if stack and stack[-1]["type"] == "switch":
                edges.append({"from": stack[-1]["id"], "to": node_id})
            last_id = node_id
            i += 1
            continue

        # Break statement (end of a case)
        elif line == "break;":
            if stack and stack[-1]["type"] == "switch":
                # Don't create a node for break, just track where the flow goes
                # But since we don't have a "merge" node yet, we'll just stop the flow here for now
                # or we could add a "break" node and link it to the end later
                pass
            last_id = None # Stop flow from break
            i += 1
            continue

        # If statement
        elif match := if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"If: {match.group(1)}")
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            stack.append({"type": "if", "id": node_id, "end_nodes": []})
            last_id = node_id
            i += 1
            continue
            
        # Else If
        elif match := else_if_pattern.match(line):
            node_id = add_node(nodes, "decision", f"Else If: {match.group(1)}")
            # Connect from the parent IF (this is simplified)
            # For proper visualization, else-if should link from the previous decision's "No" branch
            # But with this flat parser, we'll just link it to the flow
            if last_id:
                 edges.append({"from": last_id, "to": node_id})
            last_id = node_id
            i += 1
            continue
            
        # Else
        elif else_pattern.match(line):
            node_id = add_node(nodes, "process", "Else")
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            last_id = node_id
            i += 1
            continue
            
        # Loops
        elif match := while_pattern.match(line):
            node_id = add_node(nodes, "loop", f"While: {match.group(1)}")
        elif match := for_pattern.match(line):
            node_id = add_node(nodes, "loop", f"For: {match.group(1)}")
            
        # Closing brace
        elif line == '}':
            if stack:
                stack.pop()
            i += 1
            continue
            
        # Regular statement
        elif line.endswith(';') and '}' not in line and '{' not in line:
            node_id = add_node(nodes, "process", line)
            
        # Connect nodes
        if node_id:
            if last_id:
                edges.append({"from": last_id, "to": node_id})
            last_id = node_id
            
        i += 1
            
    return {"nodes": nodes, "edges": edges}
