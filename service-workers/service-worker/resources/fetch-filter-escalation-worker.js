self.addEventListener('fetch', function(event) {
    if (!/proxy$/.test(event.request.url)) {
      return;
    }

	event.respondWith(new Response('', { headers: { 'x-service-worker': '1' } }));
  });
