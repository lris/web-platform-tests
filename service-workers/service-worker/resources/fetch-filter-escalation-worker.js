self.addEventListener('fetch', function(event) {
    if (!/proxy$/.test(event.request.url)) {
      return;
    }

    event.respondWith(fetch('fetch-access-control.py'));
  });
