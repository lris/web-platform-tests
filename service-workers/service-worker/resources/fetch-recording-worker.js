importScripts('./recorder.js');

self.addEventListener('fetch', function(event) {
    recorder.save(event.request.url);
  });
