import glob
import importlib
import json
import re

from rdflib import OWL, RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef

from sirp_dsi_converter.conversion import Converter_sirp2dsi


class DSIGeneralSyntaxError(Exception):
    pass


class DSIUnknownTokenError(Exception):
    pass


class UnsupportedExpression(Exception):
    pass


class DSIAvoidIfPossible(UserWarning):
    pass


class Converter_dsi2sirp:
    def __init__(self) -> None:
        self.define_syntax_components()

        # very basic pattern check
        self.pattern_basic = re.compile("(\\\\[^\\\\]+)")

        # detailed pattern
        p1 = f"({self.PREFIXES})?"
        p2 = f"({self.UNITS})"
        p3 = "(\\\\tothe\{[-\.\d]+\})?"
        p4 = "|(\\\\per)"
        p = p1 + p2 + p3 + p4
        self.pattern_dsi = re.compile(p)

        # exponent extraction
        self.exponent_pattern = re.compile("\\\\tothe\{([-\.\d]+)\}")
        self.prefix_pattern = re.compile("\\\\([^\\\\]+)")
        self.unit_pattern = re.compile("\\\\([^\\\\]+)")

    def convert(self, dsi_unit: str):
        raw_result = self.parse(dsi_unit)
        parsed_unit = self.convert_raw_parsed_tuples(raw_result)
        graph = self.convert_to_RDF(parsed_unit)
        pid = self.convert_to_PID(parsed_unit)

        return graph, pid

    def parse(self, input: str):
        # check against basic syntax
        result = re.findall(self.pattern_basic, input)
        rejoined_result = "".join(result)
        basic_syntax_success = rejoined_result == input

        if not basic_syntax_success:
            message = f"""
            Basic syntax check 'did not' succeed:
            input:    {input}
            rejoined: {rejoined_result}
            """
            raise DSIGeneralSyntaxError(message)

        # check against detailed syntax
        result = re.findall(self.pattern_dsi, input)
        rejoined_result = "".join(["".join(tupl) for tupl in result])
        parsing_success = rejoined_result == input

        if not parsing_success:
            message = f"""
            Parsing did not succeed:
            input:    {input}
            rejoined: {rejoined_result}
            """
            raise DSIUnknownTokenError(message)
        else:
            print("Found the following groups (prefix, unit, exponent, per):")
            for tupl in result:
                print(tupl)

        # check for edge/corner cases
        advanced_checks_success = True
        if parsing_success:
            pass
            # advanced checks, like:
            # - \kilogram not no \kilo\gram (DSIAvoidIfPossible)
            # - degreeCelsius/degreecelsius (DSIAvoidIfPossible)
            # - correct/integer exponents (UnsupportedExpression)
            # - units to be used without exponents (UnsupportedExpression)
            # - reject multiple \per (UnsupportedExpression)

        return result

    def convert_raw_parsed_tuples(self, raw_result):
        # adjust tuples
        parsed_input = []
        exponent_factor = 1.0
        for tupl in raw_result:
            tupl_adjusted = []

            # handle prefix (optional)
            prefix = re.findall(self.prefix_pattern, tupl[0])
            if prefix:
                tupl_adjusted.append(prefix[0])
            else:
                tupl_adjusted.append(None)

            # handle unit (always present)
            unit = re.findall(self.unit_pattern, tupl[1])
            if unit:
                tupl_adjusted.append(unit[0])
            else:
                tupl_adjusted.append(None)

            # handle exponent (optional)
            exponent = re.findall(self.exponent_pattern, tupl[2])
            if exponent:
                exp = float(exponent[0]) * exponent_factor
            else:
                exp = exp = 1.0 * exponent_factor

            if exp != 1.0:
                tupl_adjusted.append(exp)
            else:
                tupl_adjusted.append(None)

            # handle \per
            if tupl[3] == "\\per":
                exponent_factor = -1.0
            else:
                parsed_input.append(tupl_adjusted)

        return parsed_input

    def convert_to_RDF(self, unit_list):
        # define namespaces
        SI = Namespace("http://si-digital-framework.org/SI#")
        UNITS = Namespace("http://si-digital-framework.org/SI/units/")
        PREFIXES = Namespace("http://si-digital-framework.org/SI/prefixes/")

        # init graph
        g = Graph()
        g.bind("si", SI)
        g.bind("units", UNITS)
        g.bind("prefixes", PREFIXES)
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        g.bind("rdfs", RDFS)
        g.bind("xsd", XSD)

        # output is a UnitProduct if multiple units are combined
        unit = BNode()
        if len(unit_list) > 1:
            g.add((unit, RDF.type, SI.UnitProduct))

        # iterate over input
        for item in unit_list:
            if len(unit_list) == 1:
                term = unit
            else:
                term = BNode()

            # case 1: "pure" SI unit
            is_pure_unit = False
            if (item[0] is None) and (item[2] is None):
                term = UNITS[item[1]]
                is_pure_unit = True

            # case 2: "pure" PrefixedUnit
            elif (item[0] is not None) and (item[2] is None):
                g.add((term, RDF.type, SI.PrefixedUnit))
                g.add((term, SI.hasPrefix, PREFIXES[item[0]]))
                g.add((term, SI.hasNonPrefixedUnit, UNITS[item[1]]))

            # case 3: "pure" UnitPower
            elif (item[0] is None) and (item[2] is not None):
                g.add((term, RDF.type, SI.UnitPower))
                g.add((term, SI.hasUnitBase, UNITS[item[1]]))
                g.add(
                    (term, SI.hasNumericExponent, Literal(item[2], datatype=XSD.float))
                )

            # case 4: UnitPower of PrefixedUnit
            elif (item[0] is not None) and (item[2] is not None):
                prefixed_term = BNode()
                g.add((prefixed_term, RDF.type, SI.PrefixedUnit))
                g.add((prefixed_term, SI.hasPrefix, PREFIXES[item[0]]))
                g.add((prefixed_term, SI.hasNonPrefixedUnit, UNITS[item[1]]))

                g.add((term, RDF.type, SI.UnitPower))
                g.add((term, SI.hasUnitBase, prefixed_term))
                g.add(
                    (term, SI.hasNumericExponent, Literal(item[2], datatype=XSD.float))
                )

            else:
                raise RuntimeError("Should not happen.")

            # output is either a generic MeasurementUnit or a UnitProduct
            if len(unit_list) == 1:
                if is_pure_unit:
                    g.add((unit, OWL.sameAs, term))
            else:
                g.add((unit, SI.hasUnitTerm, term))

        return g

    def convert_to_PID(self, unit_list):
        base_url = "https://si-digital-framework.org/SI/units/"

        components = []
        for item in unit_list:
            short = ""

            # prefix optional
            if item[0] is not None:
                short += self.sirp_prefixes[item[0]]["symbol"]

            # unit mandatory
            short += self.sirp_units[item[1]]["symbol"]

            # exponent optional
            if item[2] is not None and item[2] != 1.0:
                short += str(int(item[2]))
            components.append(short)

        # multiply the components together
        pid = base_url + ".".join(components)

        return pid

    def define_syntax_components(self):
        cache = importlib.resources.files(__package__) / "cache" / "sirp_cache.json"
        with open(cache, "r", encoding="UTF-8") as f:
            sirp_cache = json.load(f)
        
        # SIRP vocabulary, use to generate regex-word-list
        self.sirp_units = sirp_cache["units"]
        self.UNITS = "|".join(
            ["\\\\" + s for s in sorted(self.sirp_units.keys(), key=len, reverse=True)]
        )

        # SIRP vocabulary, use to generate regex-word-list
        self.sirp_prefixes = sirp_cache["prefixes"]
        self.PREFIXES = "|".join(
            [
                "\\\\" + s
                for s in sorted(self.sirp_prefixes.keys(), key=len, reverse=True)
            ]
        )


def dsi_to_sirp(dsi_string: str):
    c = Converter_dsi2sirp()
    g, pid = c.convert(dsi_string)
    #return g, pid
    return g

if __name__ == "__main__":
    c1 = Converter_dsi2sirp()

    units_for_testing = [
        "\\second",
        "\\micro\\second",
        "\\second\\tothe{-1}",
        "\\metre\\per\\second",
        "\\metre\\per\\second\\tothe{2}",
        "\\degreeCelsius\\ampere\\volt",
        "\\kilo\\metre\\tothe{2}\\per\\hour\\milli\\newton\\tothe{3.5}\\degreeCelsius",
    ]

    for i, dsi_unit in enumerate(units_for_testing):
        print("=" * 20)
        g, pid = c1.convert(dsi_unit)
        g.serialize(destination=f"test_{i}.ttl")
        print(pid)

    c2 = Converter_sirp2dsi()
    example_paths = glob.glob("test_*.ttl")
    for ep in example_paths:
        print("=" * 20)
        g = c2.load_turtle(ep)
        dsi_string = c2.convert(g, use_per=True)
        print(f"{ep}: {dsi_string}")
