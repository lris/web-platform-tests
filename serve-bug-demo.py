import time

template_200 = '''
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: %s

%s
'''.strip()

def main(request, response):
  body = '<body style="background: green;">Expected document</body>'
  response.writer.write(template_200 % (len(body), body))
  response.writer.flush()
  time.sleep(1)
  body = '<body style="background: red;">Unexpected document</body>'
  response.writer.write(template_200 % (len(body), body))
