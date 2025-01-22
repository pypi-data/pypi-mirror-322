from abc import ABC, abstractmethod
from enum import Enum
from os import PathLike
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Tuple, TypeVar, Union

import networkx as nx

from golem.core.dag.graph_node import GraphNode
from golem.visualisation.graph_viz import GraphVisualizer, NodeColorType

NodeType = TypeVar('NodeType', bound=GraphNode, covariant=False, contravariant=False)


class ReconnectType(Enum):
    """Defines allowed kinds of removals in Graph. Used by mutations."""
    none = 'none'  # do not reconnect predecessors
    single = 'single'  # reconnect a predecessor only if it's single
    all = 'all'  # reconnect all predecessors to all successors


class Graph(ABC):
    """Defines abstract graph interface that's required by graph optimisation process.
    """

    @abstractmethod
    def add_node(self, node: GraphNode):
        """Adds new node to the graph together with its parent nodes.

        Args:
            node: graph nodes
        """
        raise NotImplementedError()

    @abstractmethod
    def update_node(self, old_node: GraphNode, new_node: GraphNode):
        """Replaces ``old_node`` node with ``new_node``

        Args:
            old_node: node to be replaced
            new_node: node to be placed instead
        """
        raise NotImplementedError()

    @abstractmethod
    def update_subtree(self, old_subtree: GraphNode, new_subtree: GraphNode):
        """Changes ``old_subtree`` subtree to ``new_subtree``

        Args:
            old_subtree: node and its subtree to be removed
            new_subtree: node and its subtree to be placed instead
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_node(self, node: GraphNode, reconnect: ReconnectType = ReconnectType.single):
        """Removes ``node`` from the graph.
        If ``node`` has only one child, then connects all of the ``node`` parents to it.

        Args:
            node: node of the graph to be deleted
            reconnect: defines how to treat left edges between parents and children
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_subtree(self, subtree: GraphNode):
        """Deletes given node with all its parents.
        Deletes all edges from removed nodes to remaining graph nodes

        Args:
            subtree: node to be deleted with all of its parents
                and their connections amongst the remaining graph nodes
        """
        raise NotImplementedError()

    @abstractmethod
    def node_children(self, node: GraphNode) -> Sequence[Optional[GraphNode]]:
        """Returns all children of the ``node``

        Args:
            node: for getting children from

        Returns: children of the ``node``
        """
        raise NotImplementedError()

    @abstractmethod
    def connect_nodes(self, node_parent: GraphNode, node_child: GraphNode):
        """Adds edge between ``parent`` and ``child``

        Args:
            node_parent: acts like parent in graph connection relations
            node_child:  acts like child in graph connection relations
        """
        raise NotImplementedError()

    @abstractmethod
    def disconnect_nodes(self, node_parent: GraphNode, node_child: GraphNode,
                         clean_up_leftovers: bool = False):
        """Removes an edge between two nodes

        Args:
            node_parent: where the removing edge comes out
            node_child: where the removing edge enters
            clean_up_leftovers: whether to remove the remaining invalid vertices with edges or not
        """
        raise NotImplementedError()

    @abstractmethod
    def get_edges(self) -> Sequence[Tuple[GraphNode, GraphNode]]:
        """Gets all available edges in this graph

        Returns:
            pairs of parent_node -> child_node
        """
        raise NotImplementedError()

    def get_nodes_by_name(self, name: str) -> List[GraphNode]:
        """Returns list of nodes with the required ``name``

        Args:
            name: name to filter by

        Returns:
            list: relevant nodes (empty if there are no such nodes)
        """

        appropriate_nodes = filter(lambda x: x.name == name, self.nodes)

        return list(appropriate_nodes)

    def get_node_by_uid(self, uid: str) -> Optional[GraphNode]:
        """Returns node with the required ``uid``

        Args:
            uid: uid of node to filter by

        Returns:
            Optional[Node]: relevant node (None if there is no such node)
        """

        appropriate_nodes = list(filter(lambda x: x.uid == uid, self.nodes))

        return appropriate_nodes[0] if appropriate_nodes else None

    @abstractmethod
    def __eq__(self, other_graph: 'Graph') -> bool:
        """Compares this graph with the ``other_graph``

        Args:
            other_graph: another graph

        Returns:
            is it equal to ``other_graph`` in terms of the graphs
        """
        raise NotImplementedError()

    def root_nodes(self) -> Sequence[GraphNode]:
        raise NotImplementedError()

    @property
    def root_node(self) -> Union[GraphNode, Sequence[GraphNode]]:
        """Gets the final layer node(s) of the graph

        Returns:
            the final layer node(s)
        """
        roots = self.root_nodes()
        if len(roots) == 1:
            return roots[0]
        return roots

    @property
    @abstractmethod
    def nodes(self) -> List[GraphNode]:
        """Return list of all graph nodes

        Returns:
            graph nodes
        """
        raise NotImplementedError()

    @nodes.setter
    @abstractmethod
    def nodes(self, new_nodes: List[GraphNode]):
        raise NotImplementedError()

    @property
    @abstractmethod
    def depth(self) -> int:
        """Gets this graph depth from its sink-node to its source-node

        Returns:
            length of a path from the root node to the farthest primary node
        """
        raise NotImplementedError()

    @property
    def length(self) -> int:
        """Return size of the graph (number of nodes)

        Returns:
            graph size
        """

        return len(self.nodes)

    def show(self, save_path: Optional[Union[PathLike, str]] = None, engine: Optional[str] = None,
             node_color: Optional[NodeColorType] = None, dpi: Optional[int] = None,
             node_size_scale: Optional[float] = None, font_size_scale: Optional[float] = None,
             edge_curvature_scale: Optional[float] = None,
             title: Optional[str] = None,
             node_names_placement: Optional[Literal['auto', 'nodes', 'legend', 'none']] = None,
             nodes_labels: Dict[int, str] = None, edges_labels: Dict[int, str] = None,
             nodes_layout_function: Optional[Callable[[nx.DiGraph], Dict[Any, Tuple[float, float]]]] = None):
        """Visualizes graph or saves its picture to the specified ``path``

        Args:
            save_path: optional, save location of the graph visualization image.
            engine: engine to visualize the graph. Possible values: 'matplotlib', 'pyvis', 'graphviz'.
            node_color: color of nodes to use.
            node_size_scale: use to make node size bigger or lesser. Supported only for the engine 'matplotlib'.
            font_size_scale: use to make font size bigger or lesser. Supported only for the engine 'matplotlib'.
            edge_curvature_scale: use to make edges more or less curved. Supported only for the engine 'matplotlib'.
            dpi: DPI of the output image. Not supported for the engine 'pyvis'.
            title: title for plot
            node_names_placement: variant of node names displaying. Defaults to ``auto``.

                Possible options:

                    - ``auto`` -> empirical rule by node size

                    - ``nodes`` -> place node names on top of the nodes

                    - ``legend`` -> place node names at the legend

                    - ``none`` -> do not show node names

            nodes_labels: labels to display near nodes
            edges_labels: labels to display near edges
            nodes_layout_function: any of `Networkx layout functions \
                <https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout>`_ .
        """
        GraphVisualizer(graph=self) \
            .visualise(save_path=save_path, engine=engine, node_color=node_color, dpi=dpi,
                       node_size_scale=node_size_scale, font_size_scale=font_size_scale,
                       edge_curvature_scale=edge_curvature_scale, node_names_placement=node_names_placement,
                       title=title, nodes_layout_function=nodes_layout_function,
                       nodes_labels=nodes_labels, edges_labels=edges_labels)

    @property
    def graph_description(self) -> Dict:
        """Return summary characteristics of the graph

        Returns:
            dict: containing information about the graph
        """
        return {
            'depth': self.depth,
            'length': self.length,
            'nodes': self.nodes,
        }

    @property
    def descriptive_id(self) -> str:
        """Returns human-readable identifier of the graph.

        Returns:
            str: text description of the content in the node and its parameters
        """
        if self.root_nodes:
            return self.root_node.descriptive_id
        else:
            return sorted(self.nodes, key=lambda x: x.uid)[0].descriptive_id

    def __str__(self):
        return str(self.graph_description)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.length
