import pytest

from support.asserts import assert_dialog_handled, assert_error, assert_success
from support.fixtures import create_dialog
from support.inline import inline

# TODO(ato): Test for http:// and https:// protocols.
# We need to expose a fixture for accessing
# documents served by wptserve in order to test this.

# 1. If the current top-level browsing context is no longer open, return error
#    with error code no such window.
def test_from_closed_context(session, create_window):
    new_window = create_window()
    session.window_handle = new_window
    session.close()

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {})

    assert_error(result, "no such window")

# [...]
# 2. Handle any user prompts and return its value if it is an error.
# [...]
# In order to handle any user prompts a remote end must take the following
# steps:
# 2. Run the substeps of the first matching user prompt handler:
#
#    [...]
#    - dismiss state
#      1. Dismiss the current user prompt.
#    [...]
#
# 3. Return success.
def test_handle_prompt_dismiss(new_session):
    _, session = new_session({"alwaysMatch": {"unhandledPromptBehavior": "dismiss"}})
    session.url = inline("")

    create_dialog(session)("alert", text="dismiss #1", result_var="dismiss1")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("first")})

    assert_success(result, None)
    assert_dialog_handled(session, "dismiss #1")
    assert session.execute_script("return window.dismiss1;") == None

    create_dialog(session)("confirm", text="dismiss #2", result_var="dismiss2")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("second")})

    assert_success(result, None)
    assert_dialog_handled(session, "dismiss #2")
    assert session.execute_script("return window.dismiss1;") == None

    create_dialog(session)("prompt", text="dismiss #3", result_var="dismiss3")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("third")})

    assert_success(result, None)
    assert_dialog_handled(session, "dismiss #3")
    assert session.execute_script("return window.dismiss3;") == None

# [...]
# 2. Handle any user prompts and return its value if it is an error.
# [...]
# In order to handle any user prompts a remote end must take the following
# steps:
# 2. Run the substeps of the first matching user prompt handler:
#
#    [...]
#    - accept state
#      1. Accept the current user prompt.
#    [...]
#
# 3. Return success.
def test_handle_prompt_accept(new_session):
    _, session = new_session({"alwaysMatch": {"unhandledPromptBehavior": "accept"}})
    session.url = inline("")
    create_dialog(session)("alert", text="accept #1", result_var="accept1")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("first")})

    assert_success(result, None)
    assert_dialog_handled(session, "accept #1")
    assert session.execute_script("return accept1;") == None

    create_dialog(session)("confirm", text="accept #2", result_var="accept2")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("second")})

    assert_success(result, None)
    assert_dialog_handled(session, "accept #2")
    assert session.execute_script("return accept2;"), True

    create_dialog(session)("prompt", text="accept #3", result_var="accept3")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": inline("third")})


    assert_success(result, None)
    assert_dialog_handled(session, "accept #3")
    assert session.execute_script("return accept3;") == ""

# [...]
# 2. Handle any user prompts and return its value if it is an error.
# [...]
# In order to handle any user prompts a remote end must take the following
# steps:
# 2. Run the substeps of the first matching user prompt handler:
#
#    [...]
#    - missing value default state
#    - not in the table of simple dialogs
#      1. Dismiss the current user prompt.
#      2. Return error with error code unexpected alert open.
def test_handle_prompt_missing_value(session, create_dialog):
    session.url = inline("")
    create_dialog("alert", text="dismiss #1", result_var="dismiss1")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id)

    assert_error(result, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #1")
    assert session.execute_script("return accept1;") == None

    create_dialog("confirm", text="dismiss #2", result_var="dismiss2")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id)

    assert_error(result, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #2")
    assert session.execute_script("return dismiss2;") == False

    create_dialog("prompt", text="dismiss #3", result_var="dismiss3")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id)

    assert_error(result, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #3")
    assert session.execute_script("return dismiss3;") == None

# > [...]
# > 4. Let url be the result of getting the property url from the parameters
# >    argument.
# >
# > 5. If url is not an absolute URL or is not an absolute URL with fragment or
# >    not a local scheme, return error with error code invalid argument.
@pytest.mark.parametrize("value", [
  {},
  {"URL": "http://127.0.0.1"},
  {"Url": "http://127.0.0.1"},
  {" url": "http://127.0.0.1"},
  {"url ": "http://127.0.0.1"},
  {"url": None},
  {"url": 2},
  {"url": True},
  {"url": "foo"},
])
def test_set_malformed_url(session, value):
    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    value)

    assert_error(result, "invalid argument")

# > 8. Navigate the current top-level browsing context to url.
# > [...]
# > 10. Set the current browsing context to the current top-level browsing
#       context.
@pytest.mark.parametrize("initial_suffix, destination_suffix", [
    ("", "?query"),
    ("?query", ""),
    ("?query1", "?query2"),
    ("", "#fragment"),
    ("#fragment", ""),
    ("#fragment1", "#fragment2"),
    ("", ""),
])
def test_from_nested_context(session, create_frame, url, initial_suffix,
                             destination_suffix):
    session.url = url("/webdriver/support/blank.html" + initial_suffix)

    session.switch_frame(create_frame())
    assert session.execute_script("return window !== window.top;")

    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": url(destination_suffix)})

    assert session.execute_script("return window === window.top")
