"""A work-in-progress mapping from XSD types to Hypothesis strategies."""

import re

from hypothesis import strategies as st
from hypothesis.provisional import urls
from hypothesis.strategies._internal.strategies import SearchStrategy
from rdflib import URIRef, XSD


def get_xsd_type_strategies(
    text_strategy: SearchStrategy[str] = st.text(),
) -> dict[URIRef, SearchStrategy]:
    """Return a mapping of XSD types to Hypothesis strategies."""
    xsd_type_strategy_mapping: dict[URIRef, SearchStrategy] = {
        XSD.string: text_strategy,
        XSD.token: text_strategy.map(lambda s: re.sub(r"\s{2,}", " ", s.strip())),
        XSD.anyURI: urls(),
        XSD.boolean: st.sampled_from(["true", "false", 1, 0]),
        XSD.boolean: st.sampled_from(["true", "false"]),
        XSD.integer: st.integers(),
        XSD.int: st.integers().filter(lambda n: -2147483648 <= n <= 2147483647),
        XSD.decimal: st.decimals(allow_nan=False),
        # double vs. float might need numpy based strategy
        XSD.double: st.floats(allow_nan=False),
        XSD.float: st.floats(allow_nan=False),
        XSD.short: st.integers().filter(lambda n: -32768 <= n <= 32767),
        XSD.long: st.integers().filter(
            lambda n: -9223372036854775808 <= n <= 9223372036854775807
        ),
        XSD.negativeInteger: st.integers(max_value=-1),
        XSD.nonNegativeInteger: st.integers(min_value=0),
        XSD.nonPositiveInteger: st.integers(max_value=0),
        XSD.positiveInteger: st.integers(min_value=1),
    }

    return xsd_type_strategy_mapping
