"""Hypothesis strategies for LOD testing."""

from typing import Annotated, cast, get_type_hints
from xml.sax.saxutils import escape

from hypothesis import strategies as st
from hypothesis.strategies._internal.strategies import SearchStrategy
from langcodes.language_lists import CLDR_LANGUAGES as cldr_lang_codes
from lodkit import _Triple, _TripleObject, _TripleSubject
from lodkit.testing_tools.xsd_type_strategy_mapping import get_xsd_type_strategies
from rdflib import BNode, Literal, URIRef
from rdflib.namespace import XSD


class GraphStrategies:
    """Collection of Hypothesis strategies for generating rdflib.Graphs."""


## todo: fix xsd-typed literals
## todo: st.register_type_strategy


class TripleStrategies:
    """Collection of Hypothesis strategies for RDFLib triple testing.

    Note: hypothesis.register_type_strategy adds entries to the global type-to-strategy lookup
    which means that xml_parsable=True/False strategies would overwrite themselves.

    Example:

    from hypothesis import given
    from lodkit import LODStrategies, _Triple
    from typeguard import check_type
    from rdflib import Graph

    tst = TripleStrategies()
    tst_xml = TripleStrategies(xml_parsable=True)

    @given(tst.triples)
    def test_triple_type(triple):
        assert check_type(triple, _Triple)

    @given(tst_xml.triples)
    def test_triple_parse_xml(triple):
        graph: Graph = Graph()
        graph.add(triple)

        serialized: str = graph.serialize(format="xml")
        parsed_graph: Graph = Graph().parse(data=serialized, format="xml")

        assert parsed_graph
    """

    def __init__(self, xml_parsable: bool = False) -> None:
        self._text_strategy: SearchStrategy[str] = (
            self.xml_parsable_text if xml_parsable else st.text()
        )

    @property
    def xml_parsable_text(self) -> SearchStrategy[str]:
        """Strategy for generating XML 1.0 parsable text."""
        # return st.from_regex(r"^[\u0009\u000A\u000D\u0020-\uD7FF\uE000-\uFFFD]*$")
        return st.builds(
            escape,
            (st.from_regex(r"^[\u0009\u000A\u000D\u0020-\uD7FF\uE000-\uFFFD]*$")),
        )

    @property
    def lang_codes(self) -> SearchStrategy[str]:
        """Strategy for CLDR language codes."""
        return st.sampled_from(list(cldr_lang_codes))

    @property
    def triple_uris(self) -> SearchStrategy[URIRef]:
        """Strategy for generating rdflib.URIRefs."""
        return st.builds(
            lambda x: URIRef(f"https://lodkit.testing_tools/{x}"), st.uuids()
        )

    triple_predicates: Annotated[
        SearchStrategy[URIRef],
        "Strategy for generating RDFLib compliant triple predicates. Alias for triple_uris.",
    ] = cast(SearchStrategy[URIRef], triple_uris)

    @property
    def triple_bnodes(self) -> SearchStrategy[BNode]:
        """Strategy for generating rdflib.BNodes."""
        return st.builds(lambda _: BNode(), st.integers())

    @property
    def triple_literals_plain(self) -> SearchStrategy[Literal]:
        """Strategy for generating untagged/untyped rdflib.Literals."""
        return st.builds(lambda x: Literal(x), self._text_strategy)

    @property
    def triple_literals_lang_tagged(self) -> SearchStrategy[Literal]:
        """Strategy for generating language-tagged rdflib.Literals."""
        return st.builds(
            lambda text, lang: Literal(text, lang=lang),
            self._text_strategy,
            self.lang_codes,
        )

    @property
    def triple_literals_xsd_typed(self) -> SearchStrategy[Literal]:
        """Strategy for generating XSD-typed rdflib.Literals."""
        _xsd_strategies: Annotated[list[SearchStrategy], ""] = [
            st.builds(
                lambda value, datatype: Literal(value, datatype=datatype),
                value,
                st.just(datatype),
            )
            for datatype, value in get_xsd_type_strategies(self._text_strategy).items()
        ]

        return st.one_of(_xsd_strategies)

    @property
    def triple_literals(self) -> SearchStrategy[Literal]:
        """Strategy for generating plain/lang-tagged/typed rdflib.Literals."""
        return st.one_of(
            self.triple_literals_plain,
            self.triple_literals_lang_tagged,
            self.triple_literals_xsd_typed,
        )

    @property
    def triple_subjects(self) -> SearchStrategy[_TripleSubject]:
        """Strategy for generating RDFLib compliant triple subjects."""
        return st.one_of(self.triple_uris, self.triple_bnodes)

    @property
    def triple_objects(self) -> SearchStrategy[_TripleObject]:
        """Strategy for generating RDFLib compliant triple objects."""
        return st.one_of(self.triple_uris, self.triple_bnodes, self.triple_literals)

    rdf_terms: Annotated[SearchStrategy[_TripleObject], ""] = cast(
        SearchStrategy[_TripleObject], triple_objects
    )

    @property
    def triples(self) -> SearchStrategy[_Triple]:
        """Strategy for generating RDFLib triples (lodkit._Triple)."""
        return st.tuples(
            self.triple_subjects, self.triple_predicates, self.triple_objects
        )


tst: Annotated[TripleStrategies, "TripleStrategies Singleton."] = TripleStrategies()

tst_xml: Annotated[
    TripleStrategies,
    "TripleStrategies Singleton with XML 1.0 compliant literals.",
] = TripleStrategies(xml_parsable=True)
