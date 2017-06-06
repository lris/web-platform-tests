import pytest

from webdriver.error import InvalidSelectorException

from support.asserts import assert_error, assert_success, assert_dialog_handled, assert_same_element
from support.inline import inline
from support.find import find

# > 1. If the current browsing context is no longer open, return error with
# >    error code no such window.
#def test_closed_context(session, create_window):
#    session.url = inline("<body></body>")
#    new_window = create_window()
#    session.window_handle = new_window
#    session.close()
#
#    result = session.transport.send("POST",
#                                    "session/%s/element" % session.session_id)
#
#    assert_error(result, "no such window")

# TODO: Enable this test pending acceptance of the following spec patch:
# https://github.com/w3c/webdriver/pull/935
#def test_document_element_null(session):
#    session.execute_script("document.documentElement.remove();")
#
#    result = session.transport.send("POST",
#                                    "session/%s/element" % session.session_id)
#
#    assert_error(result, "no such element")

# > [...]
# > 3. Let location strategy be the result of getting a property called
#      "using".
# > 4. If location strategy is not present as a keyword in the table of
#      location strategies, return error with error code invalid argument. If
#      location strategy is not present as a keyword in the table of location
#      strategies, return error with error code invalid argument.
def test_using_missing(session):
    result = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"value":"anything"})

    assert_error(result, "invalid argument")

@pytest.mark.parametrize("using,value", [
    (None, "*"),
    ("cssselector", "*"),
    ("css-selector", "*"),
    ("css_selector", "*"),
    ("CSS selector", "*"),
    (" css selector", "*"),
    ("css selector ", "*"),
    ("css", "*"),
    ("CSS", "*"),
    ("linktext", "a"),
    ("link-text", "a"),
    ("link_text", "a"),
    ("Link text", "a"),
    (" link text", "a"),
    ("link text ", "a"),
    ("link", "a"),
    ("Link", "a"),
    ("partiallinktext", "a"),
    ("partial-link-text", "a"),
    ("partial_link_text", "a"),
    ("Partial link text", "a"),
    (" partial link text", "a"),
    ("partial link text ", "a"),
    ("partial", "a"),
    ("Partial", "a"),
    ("tagname", "a"),
    ("tag-name", "a"),
    ("tag_name", "a"),
    ("Tag name", "a"),
    (" tag name", "a"),
    ("tag name ", "a"),
    ("tag", "a"),
    ("Tag", "a"),
    (" xpath", "a"),
    ("xpath ", "a"),
    ("Xpath", "a"),
    ("XPATH", "a")
])
def test_using_invalid(session, using, value):
    result = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"using":using,"value":value})

    assert_error(result, "invalid argument")

# > [...]
# > 5. Let selector be the result of getting a property called "value".
# > 6. If selector is undefined, return error with error code invalid argument.
def test_value_missing(session):
    result = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"using":"css selector"})

    assert_error(result, "invalid argument")

    result = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"using":"css selector","value":None})

    assert_error(result, "invalid argument")

@pytest.mark.parametrize("using,value", [
    ("css selector", "*"),
    ("css selector", "span"),
    ("css selector", ".two"),
    ("css selector", ".not-found"),
    ("css selector", "invalid selector >"),
    ("tag name", "*"),
    ("tag name", "span"),
    ("tag name", "div"),
    ("tag name", "notfound"),
    #("link text", "an anchor"),
    #("link text", "not found"),
    #("partial link text", "an anchor"),
    #("partial link text", "anchor"),
    #("partial link text", "not found"),
    ("xpath", "//*"),
    ("xpath", "//span"),
    ("xpath", "//*[contains(@class, 'two')]"),
    ("xpath", "//not-found"),
    ("xpath", "invalid selector"),
    ("xpath", "//span/text()"), # TextNode matched and returned
    ("xpath", "//span | //span/text()"), # TextNode matched but not returned
])
def test_locator(session, using, value):
    session.url = inline("""
        <span class="two">a span</span>
        <div class="two">a div</div>
        <div>another div</div>
        <a>an anchor</a>
        <a>another anchor</a>
        <a>a third anchor</a>
    """)
    start_node = session.execute_script("return document.documentElement")
    expected = find(session, start_node, using, value)
    actual = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"using":using,"value":value})

    if isinstance(expected, InvalidSelectorException):
        assert_error(actual, "invalid selector")
    elif len(expected) == 0:
        assert_error(actual, "no such element")
    else:
        assert actual.status == 200
        assert "value" in actual.body
        assert_same_element(session, actual.body["value"], expected[0])

#def test_xpath(session):
#    session.url = inline("""
#    textNode
#    <div>
#      textNode
#      <span>First</span>
#    </div>
#    <span>Second</span>
#    """)
#    result = session.transport.send("POST",
#                                    "session/%s/element" % session.session_id,
#                                    {"using":"xpath","value":"//span"})
#    start_node = session.execute_script("return document.documentElement")
#
#    assert_xpath_result(session, start_node, "//span", result)
#
#def test_xpath_invalid_selector_syntax(session):
#    session.url = inline("<span>text</span>")
#    result = session.transport.send("POST",
#                                    "session/%s/element" % session.session_id,
#                                    {"using":"xpath","value":"this is invalid"})
#    start_node = session.execute_script("return document.documentElement")
#
#    assert_xpath_result(session, start_node, "this is invalid", result)
#
#def test_xpath_invalid_selector_text_node(session):
#    session.url = inline("<span>a text node</span>")
#    result = session.transport.send("POST",
#                                    "session/%s/element" % session.session_id,
#                                    {"using":"xpath","value":"//span/text()"})
#    start_node = session.execute_script("return document.documentElement")
#
#    assert_xpath_result(session, start_node, "//span/text()", result)
#
#    assert result.status == 200
#    assert "value" in result.body
#    assert_same_element(session, result.body["value"], script_result[0])
