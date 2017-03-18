importScripts('./recorder.js');

self.addEventListener('fetch', function(event) {
    setTimeout(function() {
        try {
          event.respondWith(new Response());
          recorder.save('FAIL: did not throw');
        } catch (error) {
          if (error.name == 'InvalidStateError') {
            recorder.save('PASS');
          } else {
            recorder.save('FAIL: Unexpected exception: ' + error);
          }
        }
      }, 0);
  });
