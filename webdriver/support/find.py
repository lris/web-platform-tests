from webdriver.error import (InvalidSelectorException, JavascriptErrorException)

# > CSS Selectors
# >
# > To find a web element with the CSS Selector strategy the following steps
# > need to be completed:
# >
# > 1. Let elements be the result of calling querySelectorAll with selector
# >    with the context object equal to the start node.
# > 2. Return elements.
def find_using_css_selector(session, start_node, value):
    script = "return arguments[0].querySelectorAll(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])

# > Link Text
# >
# > To find a web element with the Link Text strategy the following steps need
# > to be completed:
# >
# > 1. Let elements be the result of calling querySelectorAll, with argument a
# >    elements, with the context object equal to the start node.
# > 2. Let result be an empty NodeList.
# > 3. For each element in elements:
# >    1. Let rendered text be the value that would be returned via a call to
# >       Get Element Text for element.
# >    2. Let trimmed text be the result of removing all whitespace from the
# >       start and end of the string rendered text.
# >    3. If trimmed text equals selector, append element to result.
# > 4. Return result.
def find_using_link_text(session, start_node, value):
    # elements = session.execute_script("return arguments[0].querySelectorAll('a');",
    #                          args=[start_node])
    # result = []

    # # TODO: Research injecting `bot.js`
    # # https://github.com/SeleniumHQ/selenium/blob/1721e627e3b5ab90a06e82df1b088a33a8d11c20/javascript/atoms/bot.js
    # for element in elements:
    #     rendered_text = session.execute_script("")
    raise NotImplementedError()

# > Partial Link Text
# >
# > The Partial link text strategy is very similar to the Link Text strategy,
# > but rather than matching the entire string, only a substring needs to
# > match. That is, return all a elements with rendered text that contains the
# > selector expression.
# >
# > To find a web element with the Partial Link Text strategy the following
# > steps need to be completed:
# >
# > 1. Let elements be the result of calling querySelectorAll, with argument a
# >    elements, with the context object equal to the start node.
# > 2. Let result be an empty NodeList.
# > 3. For each element in elements:
# >    1. Let rendered text be the value that would be returned via a call to
# >       Get Element Text for element.
# >    2. If rendered text contains selector, append element to result.
# > 4. Return result.
def find_using_partial_link_text(session, start_node, value):
    raise NotImplementedError()

# > Tag Name
# >
# > To find a web element with the Tag Name strategy return the result of
# > calling getElementsByTagName with the argument selector, with the context
# > object equal to the start node.
def find_using_tag_name(session, start_node, value):
    script = "return arguments[0].getElementsByTagName(arguments[1]);"
    return session.execute_script(script, args=[start_node, value])

# > XPath
# >
# > To find a web element with the XPath Selector strategy the following steps
# > need to be completed:
# >
# > 1. Let evaluateResult be the result of calling evaluate, with arguments
# >    selector, start node, null, ORDERED_NODE_SNAPSHOT_TYPE, and null.
# >    Note: A snapshot is used to promote operation atomicity.
# > 2. Let index be 0.
# > 3. Let length be the result of getting the property "snapshotLength" from
# >    evaluateResult.
# > 4. Let result be an empty NodeList.
# > 5. Repeat, while index is less than length:
# >    1. Let node be the result of calling snapshotItem with argument index,
# >       with the context object equal to evaluateResult.
# >    2. If node is not an element return an error with error code invalid
# >       selector.
# >    3. Append node to result.
# >    4. Increment index by 1.
# > 6. Return result.
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
