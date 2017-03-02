import time

def main(request, response):
  response.add_required_headers = False

  response_body_raw = "data: data\n\n"
  response_headers_raw = (
            'Content-Type: text/event-stream\n' +
            'Content-Length: %s' % len(response_body_raw))
  response_proto = 'HTTP/1.1'
  response_status = '204'
  response_status_text = 'OK' # this can be random

  # sending all this stuff
  payload = '%s %s %s\n' % (response_proto, response_status, response_status_text)
  payload += response_headers_raw + '\n'
  payload += '\n' # to separate headers from body
  payload += response_body_raw

  split_at = int(request.GET.first("split_at", "0")) % len(payload)
  print 'split_at = %s' % split_at
  print '[%s]' % payload[:split_at]
  response.writer.write(payload[:split_at])
  time.sleep(0.4)
  response.writer.write(payload[split_at:])
  #status = (request.GET.first("status", "404"), "HAHAHAHA")
  #status = int(request.GET.first("status", "404"))
  #headers = [("Content-Type", "text/event-stream")]
  #return status, headers, "data: data\n\n"
