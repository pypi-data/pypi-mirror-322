import io

import pytest
from rdflib import Graph

from sirp_dsi_converter.conversion import sirp_to_dsi, dsi_to_sirp
#from sirp_dsi_converter.experimental import dsi_to_sirp

examples = [
    "\\second",
    "\\micro\\second",
    "\\second\\tothe{-1}",
    "\\metre\\per\\second",
    "\\metre\\second\\tothe{-1}",
    "\\metre\\per\\second\\tothe{2}",
    "\\metre\\second\\tothe{-2}",
    "\\degreecelsius\\ampere\\volt",
    "\\kilo\\metre\\tothe{2}\\per\\hour\\milli\\newton\\tothe{3.5}\\degreecelsius",
]

@pytest.mark.parametrize("dsi_unit", examples)
def test_examples(dsi_unit):

    # convert one way
    g, pid = dsi_to_sirp(dsi_unit)
    assert isinstance(g, Graph)
    assert isinstance(pid, str)
    
    # show result
    f = io.BytesIO()
    g.serialize(f, format="ttl")
    f.seek(0)
    ttl = f.read().decode()
    print(ttl)

    # convert back
    dsi_string_returned = sirp_to_dsi(graph=g)

    print(dsi_unit)
    print(dsi_string_returned)
    assert isinstance(dsi_string_returned, str)
