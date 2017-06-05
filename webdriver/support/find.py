def find(session, start_node, using, value):
    """Locate an element according to the heuristic defined by WebDriver's
    "find" algorithm. Use of this function allows tests to assert the
    implementation of WebDriver commands without also enforcing conformance
    with the underlying DOM specification."""
    pass

def find_using_css_selector(session, start_node, value):
    script = "return arguments[0].querySelectorAll(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])


def find_using_css_selector(session, start_node, value):
    script = "return arguments[0].getElementsByTagName(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])
