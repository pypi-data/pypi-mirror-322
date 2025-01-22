import pytest


@pytest.mark.parametrize(
    "string,lemma",
    [
        ("verborum", "uerbum"),
        ("uerborum", "uerbum"),
    ],
)
def test_la_lemmatizer_lookup_assigns(la_nlp, string, lemma):
    tokens = la_nlp(string)
    assert tokens[0].lemma_ == lemma
