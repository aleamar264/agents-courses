from abc import abstractmethod
from llama_index.core.schema import NodeWithScore
from llama_index.core import QueryBundle


class DuplicateRemoverNodePostProcessor:

    @abstractmethod
    def postprocess_nodes(
        self, nodes: list[NodeWithScore], query_bundle: QueryBundle | None
    )-> list[NodeWithScore]:
        unique_hashes = set()
        unique_nodes = []

        for node in nodes:
            node_hash = node.node.hash
            if node_hash not in unique_hashes:
                unique_hashes.add(node_hash)
                unique_nodes.append(node)
        return unique_nodes



