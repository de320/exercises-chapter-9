

class Expression:
    def __init__(self, operands):
        self.operands = operands

    def __add__(self, other):
        return Add((self, self._to_expression(other)))

    def __sub__(self, other):
        return Sub((self, self._to_expression(other)))

    def __mul__(self, other):
        return Mul((self, self._to_expression(other)))

    def __truediv__(self, other):
        return Div((self, self._to_expression(other)))

    def __pow__(self, other):
        return Pow((self, self._to_expression(other)))

    def _to_expression(self, other):
        return other if isinstance(other, Expression) else Number(other)


class Operator(Expression):
    precedence = None
    symbol = None

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        op_str = []
        for operand in self.operands:
            if (
                isinstance(operand, Operator) and
                operand.precedence < self.precedence
            ):
                op_str.append(f'({operand})')
            else:
                op_str.append(str(operand))
        return f" {self.symbol} ".join(op_str)


class Add(Operator):
    precedence = 1
    symbol = '+'


class Sub(Operator):
    precedence = 1
    symbol = '-'


class Mul(Operator):
    precedence = 2
    symbol = '*'


class Div(Operator):
    precedence = 2
    symbol = '/'


class Pow(Operator):
    precedence = 3
    symbol = '^'


class Terminal(Expression):
    precedence = 10  # Higher than any operator

    def __init__(self, value):
        super().__init__(())
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Number(Terminal):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Number value must be an integer or float")
        super().__init__(value)


class Symbol(Terminal):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Symbol value must be a string")
        super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """Visit an Expression in postorder applying a function to every node."""
    stack = [(expr, False)]
    results = {}

    while stack:
        node, visited = stack.pop()

        if visited:
            # Apply the function to the node with results of its operands
            results[node] = fn(node, *(results[c] for c in node.operands),
                               **kwargs)
        else:
            # Mark the node as visited and push back onto the stack
            stack.append((node, True))
            # Push children (operands) onto the stack if not already processed
            for child in node.operands:
                if child not in results:
                    stack.append((child, False))

    return results[expr]
