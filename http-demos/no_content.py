import time

response_text = '''HTTP/1.1 204 No Content
Content-Type: application/javascript
%s
'''

def main(request, response):
    length = int(request.GET.first('length'))
    if length > 0:
        payload = response_text % ('Content-Length: %s\n' % length)
    else:
        payload = response_text % ''

    response.writer.write(payload)
    response.writer.flush()
