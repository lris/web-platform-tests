from webdriver.error import (InvalidSelectorException, JavascriptErrorException)

def find_using_css_selector(session, start_node, value):
    script = "return arguments[0].querySelectorAll(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])

def find_using_link_text(session, start_node, value):
    # elements = session.execute_script("return arguments[0].querySelectorAll('a');",
    #                          args=[start_node])
    # result = []

    # # TODO: Research injecting `bot.js`
    # # https://github.com/SeleniumHQ/selenium/blob/1721e627e3b5ab90a06e82df1b088a33a8d11c20/javascript/atoms/bot.js
    # for element in elements:
    #     rendered_text = session.execute_script("")
    raise NotImplementedError()

def find_using_partial_link_text(session, start_node, value):
    raise NotImplementedError()

def find_using_tag_name(session, start_node, value):
    script = "return arguments[0].getElementsByTagName(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])


def find_using_xpath(session, start_node, value):
    script = """
    var evaluateResult = document.evaluate(
      arguments[1], arguments[0], null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
      null);
    var index = 0;
    var length = evaluateResult.snapshotLength;
    var result = [];
    var node;

    while (index < length) {
      node = evaluateResult.snapshotItem(index);

      if (!(node instanceof Element)) {
        return 'non-element result';
      }

      result.push(node);
      index += 1;
    }

    return result;
    """

    script_result = session.execute_script(script, args=[start_node, value])

    if script_result == 'non-element result':
        return InvalidSelectorException()

    return script_result

locators = {
  "css selector": find_using_css_selector,
  "link text": find_using_link_text,
  "partial link text": find_using_partial_link_text,
  "tag name": find_using_tag_name,
  "xpath": find_using_xpath
}

def find(session, start_node, using, value):
    """Locate an element according to the heuristic defined by WebDriver's
    "find" algorithm. Use of this function allows tests to assert the
    implementation of WebDriver commands without also enforcing conformance
    with the underlying DOM specification."""
    try:
        return locators[using](session, start_node, value)
    except JavascriptErrorException as e:
        return InvalidSelectorException()
