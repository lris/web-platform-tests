import io
import json
import os

import html5lib
import pytest
from selenium import webdriver

from wptserver import WPTServer

_ENC = 'utf8'
_HERE = os.path.dirname(os.path.abspath(__file__))
_WPT_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
_HARNESS = os.path.join(_HERE, 'harness.html')

def pytest_collect_file(path, parent):
    if path.ext.lower() == '.html':
        return HTMLItem(str(path), parent)

def pytest_configure(config):
    config.driver = webdriver.Firefox()
    config.server = WPTServer(_WPT_ROOT)
    config.server.start()
    config.add_cleanup(lambda: config.server.stop())
    config.add_cleanup(lambda: config.driver.quit())

class HTMLItem(pytest.Item, pytest.Collector):
    def __init__(self, filename, parent):
        self.filename = filename
        with io.open(filename, encoding=_ENC) as f:
            markup = f.read()

        parsed = html5lib.parse(markup, namespaceHTMLElements=False)
        name = None
        self.expected = None

        for element in parsed.getiterator():
            if not name and element.tag == 'title':
                name = element.text
                continue
            if element.attrib.get('id') == 'expected':
                self.expected = element.text
                continue

        super(HTMLItem, self).__init__(name, parent)

    def repr_failure(self, excinfo):
        return pytest.Collector.repr_failure(self, excinfo)

    def runtest(self):
        driver = self.session.config.driver
        server = self.session.config.server

        driver.get(server.url(_HARNESS))

        if self.expected is None:
            raise Exception('Expected value not declared')
        expected = json.loads(self.expected)

        actual = driver.execute_async_script('runTest("%s", "foo", arguments[0])' % server.url(str(self.filename)))

        actual["status"] = self._scrub_stack(actual["status"])
        actual["tests"] = map(self._scrub_stack, actual["tests"])

        assert actual == expected

    @staticmethod
    def _scrub_stack(obj):
        copy = dict(obj)

        assert "stack" in obj

        if obj["stack"] is not None:
            copy["stack"] = "(implementation-defined)"

        return copy
