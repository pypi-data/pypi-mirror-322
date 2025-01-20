import pandas as pd
from pandas import DataFrame
from pydantic_extra_types.color import Color

from neo4j_viz.pandas import from_dfs


def test_from_df() -> None:
    nodes = DataFrame(
        {
            "id": [0, 1],
            "caption": ["A", "B"],
            "size": [1337, 42],
            "color": "#FF0000",
        }
    )
    relationships = DataFrame(
        {
            "source": [0, 1],
            "target": [1, 0],
            "caption": ["REL", "REL2"],
        }
    )
    VG = from_dfs(nodes, relationships, node_radius_min_max=(42, 1337))

    assert len(VG.nodes) == 2

    assert VG.nodes[0].id == 0
    assert VG.nodes[0].caption == "A"
    assert VG.nodes[0].size == 1337
    assert VG.nodes[0].color == Color("#ff0000")

    assert VG.nodes[1].id == 1
    assert VG.nodes[1].caption == "B"
    assert VG.nodes[1].size == 42
    assert VG.nodes[0].color == Color("#ff0000")

    assert len(VG.relationships) == 2

    assert VG.relationships[0].source == 0
    assert VG.relationships[0].target == 1
    assert VG.relationships[0].caption == "REL"

    assert VG.relationships[1].source == 1
    assert VG.relationships[1].target == 0
    assert VG.relationships[1].caption == "REL2"


def test_node_scaling() -> None:
    from neo4j_viz.pandas import _scale_node_size

    sizes = pd.Series([0, 2, 3, 4, 10])
    min_size = 3
    max_size = 6

    scaled_sizes = _scale_node_size(sizes, min_size, max_size)

    assert scaled_sizes.equals(pd.Series([3.0, 3.6, 3.9, 4.2, 6.0]))


def test_node_scaling_constant() -> None:
    from neo4j_viz.pandas import _scale_node_size

    sizes = pd.Series([2, 2, 2, 2, 2])
    min_size = 3
    max_size = 6

    scaled_sizes = _scale_node_size(sizes, min_size, max_size)

    assert scaled_sizes.equals(pd.Series([min_size + (max_size - min_size) / 2.0] * len(sizes)))
