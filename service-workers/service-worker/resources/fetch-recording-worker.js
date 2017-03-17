importScripts('./service-worker-recorder.js');

self.addEventListener('fetch', function(event) {
    ServiceWorkerRecorder.worker.save(event.request.url);
  });
