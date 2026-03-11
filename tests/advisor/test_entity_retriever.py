from unittest.mock import Mock

from advisor.entity_retriever import EntityRetriever


def test_entity_retriever_escapes_xml_like_attributes():
    entity_store = Mock()
    entity_store.get_relationships.return_value = [
        {
            "source_id": 1,
            "target_name": 'Widget "Co" <Beta>',
            "type": 'COMPETES&WITH',
            "evidence": 'Quote "here" & <there>',
        }
    ]
    entity_store.get_entity_items.return_value = [
        {
            "source": 'rss&feed',
            "title": 'Launch "update"',
            "summary": "Summary with <xml> & quotes",
        }
    ]
    retriever = EntityRetriever(entity_store)

    rendered = retriever.retrieve(
        [{"id": 1, "name": 'Acme "Corp" <AI>', "type": "Company&Lab", "item_count": 3}],
        "Acme",
    )

    assert 'name=\'Acme "Corp" &lt;AI&gt;\'' in rendered
    assert 'type="Company&amp;Lab"' in rendered
    assert 'target=\'Widget "Co" &lt;Beta&gt;\'' in rendered
    assert 'evidence=\'Quote "here" &amp; &lt;there&gt;\'' in rendered
    assert 'source="rss&amp;feed"' in rendered
    assert 'summary="Summary with &lt;xml&gt; &amp; quotes"' in rendered
