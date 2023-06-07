from dm_parser import Assigment, BinaryOperation, Identifier, Number


class NodeVisitor:
    """
    Base class for the visitor pattern. It provdes a generic `visit` method that
    dynamically dispatches to specific visit methods based on the node visited.
    Each method is named as `visit_<NodeType>` to match the type of the node.
    """

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        raise NotImplementedError(
            f"Visit method not implemented for {type(node).__name__}"
        )


class ASTVisitor(NodeVisitor):
    def visit_Program(self, node):
        results = []
        for statement in node.statements:
            result = self.visit(statement)
            results.append(result)

        return results

    def vist_Assignment(self, node):
        identifier = self.visit(node.identifier)
        expression = self.visit(node.expression)
        return Assigment(identifier, expression)

    def visit_Identifier(self, node):
        return Identifier(node.name)

    def visit_Number(self, node):
        return Number(node.value)

    def visit_BinaryOperation(self, node):
        left = self.visit(node.left)
        right = self.visit(node.rigth)
        return BinaryOperation(left, node.operator, right)
