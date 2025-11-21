import ast
import uuid

def add_node(nodes, node_type, label):
    node = {
        "id": str(uuid.uuid4()),
        "type": node_type,
        "label": label
    }
    nodes.append(node)
    return node["id"]

def parse_ast(node, nodes, edges, parent_id=None):
    # sourcery skip: low-code-quality, remove-redundant-if
    """
    Recursive AST visitor that:
    - Adds nodes for if, for, while, function
    - Adds edges from parent to current
    """
    if isinstance(node, ast.Module):
        # Process body
        last_id = None
        for stmt in node.body:
            child_id = parse_ast(stmt, nodes, edges, parent_id)
            if last_id and child_id:
                edges.append({"from": last_id, "to": child_id})
            elif parent_id and child_id:
                edges.append({"from": parent_id, "to": child_id})
            last_id = child_id
        return last_id

    elif isinstance(node, ast.FunctionDef):
        node_id = add_node(nodes, "function", f"Function: {node.name}")
        last_id = None
        for stmt in node.body:
            child_id = parse_ast(stmt, nodes, edges, node_id)
            if last_id and child_id:
                edges.append({"from": last_id, "to": child_id})
            last_id = child_id
        return node_id

    elif isinstance(node, ast.If):
        node_id = add_node(nodes, "decision", f"If: {ast.unparse(node.test)}")
        # Then branch
        last_then = None
        for stmt in node.body:
            child_id = parse_ast(stmt, nodes, edges, node_id)
            if last_then and child_id:
                edges.append({"from": last_then, "to": child_id})
            last_then = child_id
        # Else branch
        if node.orelse:
            else_id = add_node(nodes, "process", "Else")
            edges.append({"from": node_id, "to": else_id})
            last_else = None
            for stmt in node.orelse:
                child_id = parse_ast(stmt, nodes, edges, else_id)
                if last_else and child_id:
                    edges.append({"from": last_else, "to": child_id})
                last_else = child_id
        return node_id

    elif isinstance(node, (ast.For, ast.While)):
        loop_type = "For loop" if isinstance(node, ast.For) else "While loop"
        # For better label: show iterator for For, condition for While
        if isinstance(node, ast.For):
            target = ast.unparse(node.target)
            iter_ = ast.unparse(node.iter)
            label = f"For: {target} in {iter_}"
        else:
            label = f"While: {ast.unparse(node.test)}"

        node_id = add_node(nodes, "loop", label)

        last_id = None
        for stmt in node.body:
            child_id = parse_ast(stmt, nodes, edges, node_id)
            if last_id and child_id:
                edges.append({"from": last_id, "to": child_id})
            last_id = child_id

        return node_id

    elif isinstance(node, ast.Expr):
        # Expression statements (e.g., function calls)
        expr_code = ast.unparse(node)
        node_id = add_node(nodes, "process", f"Expr: {expr_code}")
        if parent_id:
            edges.append({"from": parent_id, "to": node_id})
        return node_id

    elif isinstance(node, ast.Assign):
        assign_code = ast.unparse(node)
        node_id = add_node(nodes, "process", f"Assign: {assign_code}")
        if parent_id:
            edges.append({"from": parent_id, "to": node_id})
        return node_id

    else:
        # For other node types, just add a generic process node
        try:
            code = ast.unparse(node)
        except Exception:
            code = str(type(node))
        node_id = add_node(nodes, "process", code[:30] + ("..." if len(code) > 30 else ""))
        if parent_id:
            edges.append({"from": parent_id, "to": node_id})
        return node_id

def parse_python_code(source_code):
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"error": f"Syntax error in source code: {str(e)}"}

    nodes = []
    edges = []
    parse_ast(tree, nodes, edges)
    return {"nodes": nodes, "edges": edges}
