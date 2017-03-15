template = '''
HTTP/1.1 204 HAHAHAHA
Content-Type: text/event-stream
'''.strip() + '\n\n'

def main(request, response):
  response.writer.write('invalid')
  response.writer.write(template)
