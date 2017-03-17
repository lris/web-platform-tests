importScripts('./service-worker-recorder.js');

self.addEventListener('fetch', function(event) {
    setTimeout(function() {
        try {
          event.respondWith(new Response());
          ServiceWorkerRecorder.worker.save('FAIL: did not throw');
        } catch (error) {
          if (error.name == 'InvalidStateError') {
            ServiceWorkerRecorder.worker.save('PASS');
          } else {
            ServiceWorkerRecorder.worker.save(
              'FAIL: Unexpected exception: ' + error
            );
          }
        }
      }, 0);
  });
