self.addEventListener('fetch', event => {
    if (!event.request.url.match(/opaque-response$/))
      return;
    event.respondWith(fetch("http://{{host}}:{{ports[http][0]}}/service-workers/resources/simple.txt", {mode: 'no-cors'}));
  });
