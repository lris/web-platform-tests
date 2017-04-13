response_text = '''HTTP/1.1 200 OK
Content-Type: application/javascript
Content-Length: 1

0'''

def main(request, response):
    payload = ''
    count = int(request.GET.first('count'))

    if count > 0:
        payload = 'x' * count

    payload += response_text

    response.writer.write(payload)
    response.writer.flush()
