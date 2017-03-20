body = 'console.log(1);'
template = '''
HTTP/1.1 204 HAHAHAHA
Content-Type: applicatiThis should not beon/javascript
Content-Length: %s

%s'''.lstrip() % (len(body), body)

def main(request, response):
  response.writer.write(template)
  response.writer.flush()

