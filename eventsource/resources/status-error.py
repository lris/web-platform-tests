import time
body = 'This should not be'
template = '''
HTTP/1.1 200 HAHAHAHA
Content-Type: text/event-stream
Content-Length: %s

'''.lstrip() % (len(body))

def main(request, response):
  #request_id_1 = request.GET.first('request_id_1')
  print response.writer._handler
  return ''
  if request.GET.first('foo', '0') == '1':
      request.server.stash.put(token, 'something')
      return ''
  response.writer.write(template)
  response.writer.flush()

  while request.server.stash.take(token) == None:
      time.sleep(1)
      pass
  response.writer.write(body)
  response.writer.flush()
