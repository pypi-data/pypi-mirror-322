from typing import TypeVar

from graph_sitter.core.expressions.ternary_expression import TernaryExpression
from graph_sitter.core.interfaces.editable import Editable
from graph_sitter.writer_decorators import py_apidoc

Parent = TypeVar("Parent", bound="Editable")


@py_apidoc
class PyConditionalExpression(TernaryExpression[Parent]):
    """Conditional Expressions (A if condition else B)"""

    def __init__(self, ts_node, file_node_id, G, parent: Parent) -> None:
        super().__init__(ts_node, file_node_id, G, parent=parent)
        self.consequence = self.children[0]
        self.condition = self.children[1]
        self.alternative = self.children[2]
