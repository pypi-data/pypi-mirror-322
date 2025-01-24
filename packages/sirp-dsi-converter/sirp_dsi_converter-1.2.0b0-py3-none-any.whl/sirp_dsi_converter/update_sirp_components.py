import datetime
import json
import os

import owlrl
import rdflib
from rdflib import RDF

if True: # handle proxy
    os.environ['http_proxy'] = 'http://webproxy.bs.ptb.de:8080'
    os.environ['https_proxy'] = os.environ['http_proxy']

# see https://si-digital-framework.org/SI

# output structure
output_file_path = "sirp_dsi_converter/cache/sirp_cache.json"
sirp_cache = {
    "last_update": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "prefixes": {},
    "units": {},
}

SI = rdflib.Namespace("http://si-digital-framework.org/SI#")
PREFIXES = rdflib.Namespace("http://si-digital-framework.org/SI/prefixes/")
UNITS = rdflib.Namespace("http://si-digital-framework.org/SI/units/")


# download and extract turtle files:
base_url = "https://raw.githubusercontent.com/TheBIPM/SI_Digital_Framework/refs/heads/main/SI_Reference_Point/TTL/si.ttl"
prefixes_url = "https://raw.githubusercontent.com/TheBIPM/SI_Digital_Framework/refs/heads/main/SI_Reference_Point/TTL/prefixes.ttl"
units_url = "https://raw.githubusercontent.com/TheBIPM/SI_Digital_Framework/refs/heads/main/SI_Reference_Point/TTL/units.ttl"

# prefixes
g = rdflib.Graph()
g.parse(location=prefixes_url, format="ttl")
g.bind("si", SI)
g.bind("prefixes", PREFIXES)
for s, p, o in g.triples((None, RDF.type, SI.SIPrefix)):
    s_name = s.split("/")[-1]
    symbol = ""
    for ss, pp, oo in g.triples((s, SI.hasSymbol, None)):
        symbol = oo.toPython()
    sirp_cache["prefixes"][s_name] = {"url": s.toPython(), "symbol": symbol}

# units
g_units = rdflib.Graph()
g_units.parse(location=base_url, format="ttl")
g_units.parse(location=units_url, format="ttl")
owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g_units)
g_units.bind("units", UNITS)
g_units.bind("si", SI)

for s, p, o in g_units.triples((None, RDF.type, SI.MeasurementUnit)):
    if s.startswith(UNITS):
        s_name = s.split("/")[-1]
        symbol = ""
        for ss, pp, oo in g_units.triples((s, SI.hasSymbol, None)):
            symbol = oo.toPython()
        sirp_cache["units"][s_name.lower()] = {"url": s.toPython(), "symbol": symbol}

# save output
output_dir = os.path.split(output_file_path)[0]
os.makedirs(output_dir, exist_ok=True)
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(sirp_cache, f, indent=1, ensure_ascii=False)
print(f"\nOutput written to <{output_file_path}>.\n")
