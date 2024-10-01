"""A work-in-progress mapping from XSD types to Hypothesis strategies."""

import re

from hypothesis import strategies as st
from hypothesis.provisional import urls
from hypothesis.strategies._internal.strategies import SearchStrategy
from rdflib import URIRef, XSD


# _fill = lambda x: str(x).zfill(2)
# _base_date_time: SearchStrategy = st.datetimes(timezones=timezones())


def get_xsd_type_strategies(
    text_strategy: SearchStrategy[str] = st.text(),
) -> dict[URIRef, SearchStrategy]:
    """Return a mapping of the most important XSD types to Hypothesis strategies."""
    xsd_type_strategy_mapping: dict[URIRef, SearchStrategy] = {
        XSD.string: text_strategy,
        XSD.token: text_strategy.map(lambda s: re.sub(r"\s{2,}", " ", s.strip())),
        XSD.anyURI: urls(),
        XSD.boolean: st.sampled_from(["true", "false"]),
        XSD.integer: st.integers(),
        XSD.int: st.integers().filter(lambda n: -2147483648 <= n <= 2147483647),
        XSD.decimal: st.decimals(allow_nan=False, allow_infinity=None),
        XSD.negativeInteger: st.integers(max_value=-1),
        XSD.nonNegativeInteger: st.integers(min_value=0),
        XSD.nonPositiveInteger: st.integers(max_value=0),
        XSD.positiveInteger: st.integers(min_value=1),
        # XSD.dateTime: _base_date_time.map(lambda dt: dt.isoformat()),
        # XSD.time: _base_date_time.map(lambda dt: str(dt.time())),
        # XSD.date: _base_date_time.map(lambda dt: str(dt.date())),
        # XSD.gDay: _base_date_time.map(lambda dt: f"---{_fill(dt.day)}"),
        # XSD.gMonth: _base_date_time.map(lambda dt: f"--{_fill(dt.month)}"),
        # XSD.gYear: _base_date_time.map(lambda dt: str(dt.year)),
        # XSD.gMonthDay: _base_date_time.map(
        #     lambda dt: f"--{_fill(dt.month)}-{_fill(dt.day)}"
        # ),
        # XSD.gYearMonth: _base_date_time.map(lambda dt: f"{dt.year}-{dt.month}"),
        # language
    }

    return xsd_type_strategy_mapping
