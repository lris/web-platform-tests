import pytest

from support.asserts import assert_error, assert_success, assert_dialog_handled, assert_same_element
from support.fixtures import create_dialog
from support.inline import inline

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

def find(session, start_node, using, value):
    """Locate an element according to the heuristic defined by WebDriver's
    "find" algorithm. Use of this function allows tests to assert the
    implementation of WebDriver commands without also enforcing conformance
    with the underlying DOM specification."""
    pass

def strategy_css_selector(session, start_node, value):
    return session.execute_script(
                         "return arguments[0].querySelectorAll(arguments[1]);",
                         args=[start_node, value])

def strategy_link_text(session, start_node, value):
    elements = session.execute_script("return arguments[0].querySelectorAll('a');",
                             args=[start_node])
    result = []

    # TODO: Research injecting `bot.js`
    # https://github.com/SeleniumHQ/selenium/blob/1721e627e3b5ab90a06e82df1b088a33a8d11c20/javascript/atoms/bot.js
    for element in elements:
        rendered_text = session.execute_script("")
