import pytest
from Queue import Queue
from threading import Thread
import time

from webdriver.error import InvalidSelectorException, WebDriverException

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

# > [...]
# > 8. Let result be the result of Find with start node, location strategy, and
# >    selector. 
#
# > Find
# >
# > [...]
# > 4. Let elements returned be the result of the relevant element location
# >    strategy call with arguments start node, and selector.
# >
# > [...]
# >
# > 7. Let result be an empty JSON List.
# > 8. For each element in elements returned, append the serialization of
# >    element to result.
# > 9. Return result. 
@pytest.mark.parametrize("using,value", [
    # > [...]
    # > 5. If a DOMException, SyntaxError, XPathException, or other error occurs
    # >    during the execution of the element location strategy, return error
    # >    invalid selector.
    ("css selector", "invalid selector >"),
    ("xpath", "invalid selector"),

    ("css selector", "*"),
    ("css selector", "span"),
    ("css selector", ".two"),
    ("tag name", "*"),
    ("tag name", "span"),
    ("tag name", "div"),
    #("link text", "an anchor"),
    #("partial link text", "an anchor"),
    #("partial link text", "anchor"),
    ("xpath", "//*"),
    ("xpath", "//span"),
    ("xpath", "//*[contains(@class, 'two')]"),
    ("xpath", "//not-found"),
    ("xpath", "//span/text()"), # TextNode matched and returned
    ("xpath", "//span | //span/text()"), # TextNode matched but not returned


    ("css selector", ".not-found"),
    ("tag name", "notfound"),
    #("link text", "not found"),
    #("partial link text", "not found"),
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

# > [...]
# > 8. Let result be the result of Find with start node, location strategy, and
# >    selector. 
#
# > Find
# >
# > [...]
# > 6. If elements returned is empty and the current time is less than end time
# >    return to step 4. Otherwise, continue to the next step.
#
# Note: there is no observable detail that indicates the driver is actively
#       polling for an element. Because of this, it is not possible to
#       deterministically verify that polling is taking place. This test
#       attempts to induce this state by issuing a second "find" command that
#       is not expected to poll. (Presumably, once processing of this second
#       command is complete, the first will be in progress.)
#
#       Due to the nature of the transport layer and WebDriver's processing
#       model, this heuristic is not guaranteed to produce the intended effect;
#       it is possible that the driver has not yet entered the "polling" state
#       following the delay of the second command. In such cases, the test will
#       spuriously pass. As a consequence of unavoidable indeterminacy, this is
#       preferable to intermittent failure.
def test_locator_wait(new_session):
    _, session = new_session({"alwaysMatch": {"timeouts": {"implicit": 10000}}})
    queue = Queue()
    anchors = None

    session.url = inline("<a>anchor</a>")

    try:
        anchors = session.execute_script("return document.getElementsByTagName('a');")
    except WebDriverException:
        pass

    if anchors is None or len(anchors) != 1:
        # WPT disallows skipping tests imperatively, so simply pass the test
        # if the assertions cannot be executed faithfully.
        # TODO: Talk with jgraham about relaxing this restriction
        #pytest.skip("querySelectorAll implementation incomplete")
        return

    def find_new(session, queue):
        result = session.transport.send("POST",
                                        "session/%s/element" % session.session_id,
                                        {"using": "css selector","value": "div"})
        queue.put(result)

    Thread(target=find_new, args=[session, queue]).start()

    result = session.transport.send("POST",
                                    "session/%s/element" % session.session_id,
                                    {"using":"css selector","value": "a"})
    assert result.status == 200
    assert "value" in result.body
    assert_same_element(session, result.body["value"], anchors[0])

    new_div = session.execute_script("""
        var div = document.createElement('div');
        document.body.appendChild(div);
        return div;
        """)

    result = queue.get()

    assert result.status == 200
    assert "value" in result.body
    assert_same_element(session, result.body["value"], new_div)
