# Question 2: Expression Evaluator

# ---------------- TOKEN CLASS ----------------
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"[{self.type}:{self.value}]"


# ---------------- NODE CLASS ----------------
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# ---------------- TOKENIZER ----------------
def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(Token("NUM", num))
            continue

        if ch in "+-*/":
            tokens.append(Token("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(Token("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(Token("RPAREN", ch))
            i += 1
            continue

        raise ValueError("Invalid character")

    tokens.append(Token("END", ""))
    return tokens


# ---------------- PARSER ----------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, type_=None, value=None):
        token = self.current()

        if type_ and token.type != type_:
            raise ValueError("Unexpected token")
        if value and token.value != value:
            raise ValueError("Unexpected token")

        self.pos += 1
        return token

    # expression → term ((+|-) term)*
    def parse_expression(self):
        node = self.parse_term()

        while self.current().type == "OP" and self.current().value in "+-":
            op = self.eat("OP").value
            right = self.parse_term()
            node = Node(op, node, right)

        return node

    # term → unary ((*|/) unary)*
    def parse_term(self):
        node = self.parse_unary()

        while self.current().type == "OP" and self.current().value in "*/":
            op = self.eat("OP").value
            right = self.parse_unary()
            node = Node(op, node, right)

        return node

    # unary → - unary | primary
    def parse_unary(self):
        if self.current().type == "OP" and self.current().value == "-":
            self.eat("OP", "-")
            return Node("neg", self.parse_unary())

        return self.parse_primary()
