import argparse
import importlib
import importlib.resources
import json
import os

from rdflib import OWL, RDF, BNode, Graph, Namespace, URIRef

from .transformation import compoundUnitValidation


class UnsupportedExpression(Exception):
    pass


class Converter_sirp2dsi:
    def __init__(self) -> None:
        self.define_syntax_components()

    def convert(self, sirp_unit_graph: Graph, use_per=False):
        top_node = self.get_top_level_node(sirp_unit_graph)
        unit_elements = [self.construct_unit_element(unit_node=top_node)]

        any_changes = True
        while any_changes:
            unit_elements, any_changes = self.break_down_unit(
                sirp_unit_graph, unit_elements
            )

        unit_elements = self.sort_unit_elements(unit_elements)
        dsi_string = self.convert_to_dsi_string(unit_elements, use_per=use_per)

        return dsi_string

    def load_turtle(self, turtle_path):
        # prepare empty graph
        g = Graph()
        g.bind("si", self.SI)
        g.bind("prefixes", self.PREFIXES)
        g.bind("units", self.UNITS)

        # load example
        g.parse(turtle_path, format="ttl")
        # owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

        return g

    def get_top_level_node(self, g):
        result = list(g.query(self.top_node_query))

        if len(result) != 1:
            raise UnsupportedExpression("Unclear top level node. Aborting.")

        top_node = result[0][0]
        return top_node

    def construct_unit_element(
        self, prefix=None, multiplier=1.0, unit_node=None, exponent=1.0
    ):
        return (prefix, multiplier, unit_node, exponent)

    def break_down_unit(self, g, unit_elements):
        updated_elements = []
        any_changes = False

        for element in unit_elements:
            prefix, multiplier, unit_node, exponent = element

            # assume fully resolved element if given as URI
            if isinstance(unit_node, URIRef):
                updated_elements.append(element)

            # try to resolve "anonymous" node
            elif isinstance(unit_node, BNode):
                sameAs_check = list(g.triples((unit_node, OWL.sameAs, None)))
                type_check = list(g.triples((unit_node, RDF.type, None)))

                # case A: unit referenced by sameAs-relation
                if len(sameAs_check) == 1:
                    new_element = (prefix, multiplier, sameAs_check[0][2], exponent)
                    updated_elements.append(new_element)
                    any_changes = True
                    continue

                # case B: specific unit type is used
                elif len(type_check) > 0:
                    # identify most specific type
                    found_types = [row[2] for row in type_check]
                    node_type = None
                    for uc in self.unit_concepts:
                        if uc in found_types:
                            node_type = uc
                            break

                    # cases based on type
                    if node_type == self.SI.UnitProduct:
                        terms = list(
                            g.triples_choices(
                                (
                                    unit_node,
                                    [
                                        self.SI.hasUnitTerm,
                                        self.SI.hasLeftUnitTerm,
                                        self.SI.hasRightUnitTerm,
                                    ],
                                    None,
                                )
                            )
                        )

                        for term in terms:
                            new_element = (prefix, multiplier, term[2], exponent)
                            updated_elements.append(new_element)
                            any_changes = True

                    elif node_type == self.SI.UnitPower:
                        numeric_exponent = list(
                            g.triples((unit_node, self.SI.hasNumericExponent, None))
                        )[0][2].value
                        unit_base = list(
                            g.triples((unit_node, self.SI.hasUnitBase, None))
                        )[0][2]

                        new_element = (
                            prefix,
                            multiplier,
                            unit_base,
                            exponent * numeric_exponent,
                        )
                        updated_elements.append(new_element)
                        any_changes = True

                    elif node_type == self.SI.PrefixedUnit:
                        prefix_value = list(
                            g.triples((unit_node, self.SI.hasPrefix, None))
                        )[0][2]
                        non_prefixed_unit = list(
                            g.triples((unit_node, self.SI.hasNonPrefixedUnit, None))
                        )[0][2]

                        if prefix is None:
                            new_element = (
                                prefix_value,
                                multiplier,
                                non_prefixed_unit,
                                exponent,
                            )
                            updated_elements.append(new_element)
                            any_changes = True
                        else:
                            raise UnsupportedExpression(
                                "Cannot add two prefixes to a unit."
                            )

                    elif node_type == self.SI.UnitMultiple:
                        numeric_factor = list(
                            g.triples((unit_node, self.SI.hasNumericFactor, None))
                        )[0][2].value
                        unit_term = list(
                            g.triples((unit_node, self.SI.hasUnitTerm, None))
                        )[0][2]

                        new_element = (
                            prefix_value,
                            multiplier * numeric_factor,
                            unit_term,
                            exponent,
                        )
                        updated_elements.append(new_element)
                        any_changes = True

                    elif node_type == self.SI.MeasurementUnit:
                        raise UnsupportedExpression(
                            "Generic node type cannot be handled."
                        )

                    else:
                        raise UnsupportedExpression(
                            f"Unknown type of node: <{node_type}>."
                        )

                else:
                    raise UnsupportedExpression(
                        "Blank node is neither defined by sameAs nor of recognized type."
                    )

        return updated_elements, any_changes

    def sort_unit_elements(self, elements):
        # sort elements by exponent
        sorted_elements = sorted(elements, key=lambda x: x[3], reverse=True)
        return sorted_elements

    def convert_to_dsi_string(self, elements, use_per=False):
        dsi_string = ""
        previous_exponent = -1.0
        exponent_factor = 1.0

        for element in elements:
            prefix, multiplier, unit_node, exponent = element

            # insert \per if wanted
            if previous_exponent > 0.0 and exponent < 0.0:
                dsi_string += "\\per"
                exponent_factor = -1.0

            # insert prefix, if given
            if prefix is not None:
                prefix_uri = str(prefix)
                if prefix_uri in self.dsi_prefixes.keys():
                    dsi_string += f"\\{self.dsi_prefixes[prefix_uri]}"
                else:
                    raise Warning(f"Unsupported: prefix {prefix.n3()}")

            # warn about use of unit multiples
            if multiplier != 1.0:
                raise Warning(
                    f"Unsupported: UnitMultiple ({multiplier} times {unit_node.n3()})"
                )

            # insert unit
            unit_node_uri = str(unit_node)
            if unit_node_uri in self.dsi_units.keys():
                dsi_string += f"\\{self.dsi_units[unit_node_uri]}"
            else:
                raise Warning(f"Unsupported unit {unit_node.n3()}")

            # insert exponent, if given (+ take care of \per)
            eff_exponent = exponent * exponent_factor
            if eff_exponent != 1.0:
                if eff_exponent % 1 == 0.0:
                    eff_exponent = int(eff_exponent)
                dsi_string += f"\\tothe{{{eff_exponent}}}"

            if use_per:
                previous_exponent = exponent

        return dsi_string

    def define_syntax_components(self):
        cache = importlib.resources.files(__package__) / "cache" / "sirp_cache.json"
        with open(cache, "r", encoding="UTF-8") as f:
            sirp_cache = json.load(f)

        # SIRP/DSI vocabulary, use to look up valid entries
        self.dsi_units = {val["url"]: key for key, val in sirp_cache["units"].items()}
        self.dsi_prefixes = {
            val["url"]: key for key, val in sirp_cache["prefixes"].items()
        }

        self.SI = Namespace("http://si-digital-framework.org/SI#")
        self.PREFIXES = Namespace("http://si-digital-framework.org/SI/prefixes/")
        self.UNITS = Namespace("http://si-digital-framework.org/SI/units/")

        # define unit subclasses, ordered by decreasing specificity
        self.unit_concepts = [
            self.SI.UnitProduct,
            self.SI.UnitPower,
            self.SI.PrefixedUnit,
            self.SI.UnitMultiple,
            self.SI.MeasurementUnit,
        ]  # necessary to avoid reasoning for every example...

        # SPARQL query to find origin/top node
        self.top_node_query = """
        SELECT DISTINCT ?s
        WHERE 
        {
            # look for nodes, that are of specific kind and do not appear as objects
            {
                VALUES ?value
                {
                si:MeasurementUnit
                si:UnitProduct
                si:UnitPower
                si:PrefixedUnit
                }
                ?s a ?value . 
                MINUS { ?o ?p ?s }
            }
            UNION
            # alternatively: check for same-as-relation
            {
                ?s owl:sameAs ?o
            }
        }
        """


def sirp_to_dsi(graph: Graph = None, path="", use_per=False):
    c = Converter_sirp2dsi()

    if isinstance(graph, Graph):
        dsi_string = c.convert(graph, use_per=use_per)

    elif os.path.exists(path):
        g = c.load_turtle(path)
        dsi_string = c.convert(g, use_per=use_per)

    else:
        raise ImportError("Please provide a graph or valid path.")

    return dsi_string


def dsi_to_sirp(dsi_string: str):
    # instantiate new class for this string
    info = compoundUnitValidation(dsi_string)

    # run validation and conversion
    info.validation()

    # prepare output
    if info.output_sirp_correspondance:
        graph = info.__g__
        pid = info.output_pid
    else:
        graph = Graph()
        pid = ""

    return graph, pid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="convert_sirp_dsi",
        description="Convert D-SI unit string to corresponding SI Reference Point Representation in Turtle",
    )

    parser.add_argument(
        "--dsi-string",
        default="",
        help="unit to convert from DSI to SIRP-TTL",
    )

    parser.add_argument(
        "--sirp-ttl",
        default="",
        help="unit to convert from SIRP-TTL to DSI",
    )

    # parse CLI arguments
    args = parser.parse_args()

    if args.dsi_string:
        g, pid = dsi_to_sirp(args.dsi_string)
        ttl = g.serialize(format="ttl")
        print(ttl)

    if args.sirp_ttl:
        dsi_string = sirp_to_dsi(path = args.sirp_ttl)
        print(dsi_string)