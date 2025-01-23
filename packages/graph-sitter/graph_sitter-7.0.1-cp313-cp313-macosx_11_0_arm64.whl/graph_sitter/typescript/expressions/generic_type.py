from typing import TYPE_CHECKING, Self, TypeVar

from tree_sitter import Node as TSNode

from graph_sitter.core.expressions.generic_type import GenericType
from graph_sitter.core.symbol_groups.collection import Collection
from graph_sitter.core.symbol_groups.dict import Dict
from graph_sitter.writer_decorators import ts_apidoc

if TYPE_CHECKING:
    pass
Parent = TypeVar("Parent")


@ts_apidoc
class TSGenericType(GenericType["TSType", Parent]):
    """Generic type

    Examples:
        `Array<Type>`
    """

    def _get_name_node(self) -> TSNode:
        return self.child_by_field_name("name").ts_node

    def _get_parameters(self) -> Collection[Self, Self] | Dict[Self, Self] | None:
        type_parameter = self.child_by_field_types("type_arguments").ts_node
        types = [self._parse_type(child) for child in type_parameter.named_children]
        return Collection(node=type_parameter, file_node_id=self.file_node_id, G=self.G, parent=self, children=types)
