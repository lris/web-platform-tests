importScripts('./recorder.js');

self.addEventListener('fetch', function(event) {
    recorder.save('first handler invoked');
    event.respondWith(new Response());
  });

self.addEventListener('fetch', function(event) {
    recorder.save('second handler invoked');
  });
