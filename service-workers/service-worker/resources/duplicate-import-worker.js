importScripts('/resources/testharness.js');

let version = null;
importScripts('get-version.py');
// Once imported, the stored script should be loaded for subsequent importScripts.
const expected_version = version;

version = null;
importScripts('get-version.py');
assert_equals(expected_version, version, 'second import');

version = null;
importScripts('get-version.py', 'get-version.py', 'get-version.py');
assert_equals(expected_version, version, 'multiple imports');
