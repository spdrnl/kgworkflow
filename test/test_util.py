from util import reason, get_kb, sparql_df, get_sparql, sparql_ask


def test_get_kb():
    g = get_kb("util-test")
    assert len(g) > 0


def test_reason_hermit():
    result = reason(get_kb("util-test"))
    assert len(result) > 0


def test_sparql_df():
    query = get_sparql("s-p-o")
    result = sparql_df(query, get_kb("util-test"))
    assert len(result) > 0


def test_sparql_ask():
    kb = get_kb("util-test")
    query = get_sparql("ask")
    result = sparql_ask(sparql=query, graph=kb)
    assert result == True


if __name__ == '__main__':
    pass
