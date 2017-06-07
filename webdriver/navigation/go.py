from support.asserts import assert_error

# TODO(ato): Test for http:// and https:// protocols.
# We need to expose a fixture for accessing
# documents served by wptserve in order to test this.

def test_set_malformed_url(session):
    result = session.transport.send("POST",
                                    "session/%s/url" % session.session_id,
                                    {"url": "foo"})

    assert_error(result, "invalid argument")
