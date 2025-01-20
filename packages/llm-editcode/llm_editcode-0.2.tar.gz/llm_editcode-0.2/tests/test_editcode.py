import pytest
from llm_editcode import find_sublist_index, extract, apply, Edit

@pytest.mark.parametrize("input_str, expected_edits", [
    (
        "<SEARCH>\na\n</SEARCH>\n<REPLACE>\nb\n</REPLACE>\n",
        [Edit(search="a", replace="b")]
    ),
    (
        "<SEARCH>\nx\n</SEARCH>\n<REPLACE>\ny\n</REPLACE>\n",
        [Edit(search="x", replace="y")]
    ),
    (
        "\n".join([
            "<SEARCH>"
            "print(\"hello\")",
            "</SEARCH>",
            "<REPLACE>",
            "print(\"hello\", end=\"\")",
            "</REPLACE>"
        ]),
        [
            Edit(search="print(\"hello\")", replace="print(\"hello\", end=\"\")")
        ]
    )
])
def test_extract(input_str, expected_edits):
    result = extract(input_str)
    assert len(result) == len(expected_edits)
    for res, exp in zip(result, expected_edits):
        assert res.search == exp.search
        assert res.replace == exp.replace

@pytest.mark.parametrize("input_text, edits, expected_output", [
    (
        "a",
        [Edit(search="a", replace="b")],
        "b"
    ),
    (
        "1\na\na",
        [Edit(search="a\na", replace="b\nb")],
        "1\nb\nb"
    ),
    (
        "a\n",
        [],
        "a\n"
    ),
    (
        "foo\nbar\nbaz\n",
        [Edit(search="bar", replace="qux")],
        "foo\nqux\nbaz\n"
    ),
    (
        "\nprint(\"hello\")\n",
        [Edit(search="print(\"hello\")", replace="print(\"hello\", end=\"\")")],
        "\nprint(\"hello\", end=\"\")\n"
    )
])
def test_apply(input_text, edits, expected_output):
    result = apply(input_text, edits)
    assert result == expected_output

@pytest.mark.parametrize("lines, search_lines, expected_index", [
    (["a"], ["a"], 0),
    (["b", "b", "c", "c"], ["c", "c"], 2),
    (["b", "b", "c", "c"], ["a", "a"], -1),
    (["b", "b", "c", "c"], ["b", "b"], 0),
])
def test_find_sublist_index(lines, search_lines, expected_index):
    result = find_sublist_index(lines, search_lines)
    assert result == expected_index
