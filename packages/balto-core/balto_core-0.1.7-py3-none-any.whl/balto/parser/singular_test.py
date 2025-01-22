from balto.contracts.graph.nodes import SingularTestNode
from balto.node_types import NodeType
from balto.parser.base import SimpleSQLParser
from balto.parser.search import FileBlock
from balto.utils import get_pseudo_test_path


class SingularTestParser(SimpleSQLParser[SingularTestNode]):
    def parse_from_dict(self, dct, validate=True) -> SingularTestNode:
        if validate:
            SingularTestNode.validate(dct)
        return SingularTestNode.from_dict(dct)

    @property
    def resource_type(self) -> NodeType:
        return NodeType.Test

    @classmethod
    def get_compiled_path(cls, block: FileBlock):
        return get_pseudo_test_path(block.name, block.path.relative_path)
