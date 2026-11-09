import ast
import operator


# =========================================
# Supported Mathematical Operations
# =========================================

BINARY_OPERATORS = {

    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod

}


UNARY_OPERATORS = {

    ast.UAdd: operator.pos,
    ast.USub: operator.neg

}


# =========================================
# Supported Comparison Operations
# =========================================

COMPARISON_OPERATORS = {

    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne

}


# =========================================
# Evaluate Numeric Expression
# =========================================

def evaluate_expression(expression, variables):

    tree = ast.parse(
        expression,
        mode="eval"
    )

    result = evaluate_node(
        tree.body,
        variables
    )

    if isinstance(result, bool) or not isinstance(result, (int, float)):

        raise ValueError(
            "Expression must produce a numeric result."
        )

    return float(result)


# =========================================
# Evaluate Boolean Condition
# =========================================

def evaluate_condition(expression, variables):

    tree = ast.parse(
        expression,
        mode="eval"
    )

    result = evaluate_node(
        tree.body,
        variables
    )

    if not isinstance(result, bool):

        raise ValueError(
            "Guard expression must produce True or False."
        )

    return result


# =========================================
# AST Node Evaluator
# =========================================

def evaluate_node(node, variables):

    # Numeric and Boolean constants
    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float, bool)):

            return node.value

        raise ValueError(
            "Only numeric and Boolean constants are allowed."
        )

    # Variable names
    elif isinstance(node, ast.Name):

        if node.id not in variables:

            if node.id == "True":
                return True

            if node.id == "False":
                return False

            raise ValueError(
                f"Unknown variable: {node.id}"
            )

        value = variables[node.id]

        if isinstance(value, bool) or not isinstance(value, (int, float)):

            raise ValueError(
                f"Variable '{node.id}' must contain a numeric value."
            )

        return value

    # Binary operations: +, -, *, /, **, %
    elif isinstance(node, ast.BinOp):

        operator_type = type(node.op)

        if operator_type not in BINARY_OPERATORS:

            raise ValueError(
                "Unsupported mathematical operation."
            )

        left = evaluate_node(
            node.left,
            variables
        )

        right = evaluate_node(
            node.right,
            variables
        )

        if (
            isinstance(left, bool)
            or not isinstance(left, (int, float))
            or isinstance(right, bool)
            or not isinstance(right, (int, float))
        ):

            raise ValueError(
                "Mathematical operations require numeric operands."
            )

        return BINARY_OPERATORS[operator_type](
            left,
            right
        )

    # Unary operations: +x, -x, not x
    elif isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.Not):

            value = evaluate_node(
                node.operand,
                variables
            )

            if not isinstance(value, bool):

                raise ValueError(
                    "NOT operation requires a Boolean value."
                )

            return not value

        operator_type = type(node.op)

        if operator_type not in UNARY_OPERATORS:

            raise ValueError(
                "Unsupported unary operation."
            )

        value = evaluate_node(
            node.operand,
            variables
        )

        if isinstance(value, bool) or not isinstance(value, (int, float)):

            raise ValueError(
                "Unary mathematical operations require numeric values."
            )

        return UNARY_OPERATORS[operator_type](
            value
        )

    # Comparison operations: >, <, >=, <=, ==, !=
    elif isinstance(node, ast.Compare):

        left = evaluate_node(
            node.left,
            variables
        )

        for operator_node, comparator in zip(
            node.ops,
            node.comparators
        ):

            right = evaluate_node(
                comparator,
                variables
            )

            operator_type = type(operator_node)

            if operator_type not in COMPARISON_OPERATORS:

                raise ValueError(
                    "Unsupported comparison operation."
                )

            if (
                isinstance(left, bool)
                or not isinstance(left, (int, float))
                or isinstance(right, bool)
                or not isinstance(right, (int, float))
            ):

                raise ValueError(
                    "Comparisons require numeric operands."
                )

            result = COMPARISON_OPERATORS[operator_type](
                left,
                right
            )

            if not result:
                return False

            left = right

        return True

    # Logical operations: AND, OR
    elif isinstance(node, ast.BoolOp):

        if isinstance(node.op, ast.And):

            for value_node in node.values:

                value = evaluate_node(
                    value_node,
                    variables
                )

                if not isinstance(value, bool):

                    raise ValueError(
                        "AND operation requires Boolean values."
                    )

                if not value:
                    return False

            return True

        elif isinstance(node.op, ast.Or):

            for value_node in node.values:

                value = evaluate_node(
                    value_node,
                    variables
                )

                if not isinstance(value, bool):

                    raise ValueError(
                        "OR operation requires Boolean values."
                    )

                if value:
                    return True

            return False

        raise ValueError(
            "Unsupported logical operation."
        )

    else:

        raise ValueError(
            f"Unsupported expression element: {type(node).__name__}"
        )