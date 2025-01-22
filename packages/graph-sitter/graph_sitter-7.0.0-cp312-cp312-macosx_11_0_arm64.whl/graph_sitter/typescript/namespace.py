from __future__ import annotations

from typing import TYPE_CHECKING

from tree_sitter import Node as TSNode

from graph_sitter.codebase.codebase_graph import CodebaseGraph
from graph_sitter.core.autocommit import commiter
from graph_sitter.core.dataclasses.usage import UsageKind
from graph_sitter.core.interfaces.has_name import HasName
from graph_sitter.core.node_id_factory import NodeId
from graph_sitter.core.statements.statement import Statement
from graph_sitter.core.statements.symbol_statement import SymbolStatement
from graph_sitter.core.symbol import Symbol
from graph_sitter.enums import SymbolType
from graph_sitter.extensions.utils import cached_property
from graph_sitter.typescript.class_definition import TSClass
from graph_sitter.typescript.enum_definition import TSEnum
from graph_sitter.typescript.function import TSFunction
from graph_sitter.typescript.interface import TSInterface
from graph_sitter.typescript.interfaces.has_block import TSHasBlock
from graph_sitter.typescript.symbol import TSSymbol
from graph_sitter.typescript.type_alias import TSTypeAlias
from graph_sitter.writer_decorators import noapidoc, ts_apidoc

if TYPE_CHECKING:
    from graph_sitter.typescript.detached_symbols.code_block import TSCodeBlock


@ts_apidoc
class TSNamespace(TSSymbol, TSHasBlock, HasName):
    """Representation of a namespace module in TypeScript"""

    symbol_type = SymbolType.Namespace
    code_block: TSCodeBlock

    def __init__(self, ts_node: TSNode, file_id: NodeId, G: CodebaseGraph, parent: Statement, namespace_node: TSNode | None = None) -> None:
        ts_node = namespace_node or ts_node
        name_node = ts_node.child_by_field_name("name")
        super().__init__(ts_node, file_id, G, parent, name_node=name_node)

    @noapidoc
    @commiter
    def _compute_dependencies(self, usage_type: UsageKind | None = None, dest: HasName | None = None) -> None:
        """Computes dependencies for the namespace by analyzing its code block.

        Args:
            usage_type: Optional UsageKind specifying how the dependencies are used
            dest: Optional HasName destination for the dependencies
        """
        # Use self as destination if none provided
        dest = dest or self.self_dest

        # Compute dependencies from the namespace's code block
        self.code_block._compute_dependencies(usage_type, dest)

    @cached_property
    def symbols(self) -> list[Symbol]:
        """Returns all symbols defined within this namespace, including nested ones."""
        all_symbols = []
        for stmt in self.code_block.statements:
            # Handle export statements
            if stmt.ts_node_type == "export_statement":
                for export in stmt.exports:
                    all_symbols.append(export.declared_symbol)
            # Handle direct symbols
            elif isinstance(stmt, SymbolStatement):
                all_symbols.append(stmt)
        return all_symbols

    def get_symbol(self, name: str, recursive: bool = True) -> Symbol | None:
        """Get a symbol by name from this namespace.

        Args:
            name: Name of the symbol to find
            recursive: If True, also search in nested namespaces

        Returns:
            Symbol | None: The found symbol, or None if not found
        """
        # First check direct symbols in this namespace
        for symbol in self.symbols:
            if hasattr(symbol, "name") and symbol.name == name:
                return symbol

            # If recursive and this is a namespace, check its symbols
            if recursive and isinstance(symbol, TSNamespace):
                nested_symbol = symbol.get_symbol(name, recursive=True)
                return nested_symbol

        return None

    @cached_property
    def functions(self) -> list[TSFunction]:
        """Get all functions defined in this namespace.

        Returns:
            List of Function objects in this namespace
        """
        return [symbol for symbol in self.symbols if isinstance(symbol, TSFunction)]

    def get_function(self, name: str, recursive: bool = True, use_full_name: bool = False) -> TSFunction | None:
        """Get a function by name from this namespace.

        Args:
            name: Name of the function to find (can be fully qualified like 'Outer.Inner.func')
            recursive: If True, also search in nested namespaces
            use_full_name: If True, match against the full qualified name

        Returns:
            TSFunction | None: The found function, or None if not found
        """
        if use_full_name and "." in name:
            namespace_path, func_name = name.rsplit(".", 1)
            target_ns = self.get_namespace(namespace_path)
            return target_ns.get_function(func_name, recursive=False) if target_ns else None

        symbol = self.get_symbol(name, recursive=recursive)
        return symbol if isinstance(symbol, TSFunction) else None

    @cached_property
    def classes(self) -> list[TSClass]:
        """Get all classes defined in this namespace.

        Returns:
            List of Class objects in this namespace
        """
        return [symbol for symbol in self.symbols if isinstance(symbol, TSClass)]

    def get_class(self, name: str, recursive: bool = True) -> TSClass | None:
        """Get a class by name from this namespace.

        Args:
            name: Name of the class to find
            recursive: If True, also search in nested namespaces
        """
        symbol = self.get_symbol(name, recursive=recursive)
        return symbol if isinstance(symbol, TSClass) else None

    def get_interface(self, name: str, recursive: bool = True) -> TSInterface | None:
        """Get an interface by name from this namespace.

        Args:
            name: Name of the interface to find
            recursive: If True, also search in nested namespaces
        """
        symbol = self.get_symbol(name, recursive=recursive)
        return symbol if isinstance(symbol, TSInterface) else None

    def get_type(self, name: str, recursive: bool = True) -> TSTypeAlias | None:
        """Get a type alias by name from this namespace.

        Args:
            name: Name of the type to find
            recursive: If True, also search in nested namespaces
        """
        symbol = self.get_symbol(name, recursive=recursive)
        return symbol if isinstance(symbol, TSTypeAlias) else None

    def get_enum(self, name: str, recursive: bool = True) -> TSEnum | None:
        """Get an enum by name from this namespace.

        Args:
            name: Name of the enum to find
            recursive: If True, also search in nested namespaces
        """
        symbol = self.get_symbol(name, recursive=recursive)
        return symbol if isinstance(symbol, TSEnum) else None

    def get_namespace(self, name: str, recursive: bool = True) -> TSNamespace | None:
        """Get a namespace by name from this namespace.

        Args:
            name: Name of the namespace to find
            recursive: If True, also search in nested namespaces

        Returns:
            TSNamespace | None: The found namespace, or None if not found
        """
        # First check direct symbols in this namespace
        for symbol in self.symbols:
            if isinstance(symbol, TSNamespace) and symbol.name == name:
                return symbol

            # If recursive and this is a namespace, check its symbols
            if recursive and isinstance(symbol, TSNamespace):
                nested_namespace = symbol.get_namespace(name, recursive=True)
                return nested_namespace

        return None

    def get_nested_namespaces(self) -> list[TSNamespace]:
        """Get all nested namespaces within this namespace.

        Returns:
            list[TSNamespace]: List of all nested namespace objects
        """
        nested = []
        for symbol in self.symbols:
            if isinstance(symbol, TSNamespace):
                nested.append(symbol)
                nested.extend(symbol.get_nested_namespaces())
        return nested
