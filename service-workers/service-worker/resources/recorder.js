'use strict';
(function() {
  var dbName = 'recorder.js';
  var start = new Date().getTime();
  var impls = { client: {}, worker: {} };

  function connect() {
    return new Promise(function(resolve, reject) {
        var request = indexedDB.open(dbName);
        request.onerror = reject;
        request.onblocked  = function() {
          reject(new Error('recorder.js: database is blocked'));
        };
        request.onupgradeneeded = function(event) {
          var db = event.target.result;
          event.target.result
            .createObjectStore('events', { keyPath: 'timeStamp' });
        };
        request.onsuccess = function(event) {
          resolve(event.target.result);
        };
      });
  }

  function clientSend(worker, topic, value) {
    return new Promise(function(resolve, reject) {
        function onMessage(event) {
          resolve(event.data);
        }
        var channel = new MessageChannel();
        var data = {port: channel.port2, topic: topic, value: value};
        channel.port1.onmessage = onMessage;
        worker.postMessage(data, [channel.port2]);
      });
  }

  function onMessage(event) {
    var topic = event.data && event.data.topic;
    var operation = null;

    if (topic === 'recorder.js:clear') {
      operation = impls.worker.clear;
    } else if (topic === 'recorder.js:save') {
      operation = impls.worker.save;
    } else if (topic === 'recorder.js:read') {
      operation = impls.worker.read;
    }

    if (operation) {
      event.waitUntil(operation().then(function(result) {
          event.data.port.postMessage(result);
        }));
    }
  }

  impls.worker.clear = function() {
    var timeStamp = start + performance.now();

    return connect().then(function(db) {
        var transaction = db.transaction(['events'], 'readwrite');
        var close = db.close.bind(db, db);
        var old = IDBKeyRange.upperBound(timeStamp);
        var del = new Promise(function(resolve, reject) {
            var request = transaction.objectStore('events').delete(old);
            request.onsuccess = function() { resolve(); };
            request.onerror = function() { reject(request.error); };
          });

        del.then(close, close);

        return del;
      });
  };
  impls.client.clear = function(worker) {
    return clientSend(worker, 'recorder.js:clear');
  };

  impls.worker.save = function(value) {
    var timeStamp = start + performance.now();

    return connect().then(function(db) {
        var transaction = db.transaction(['events'], 'readwrite');
        var close = db.close.bind(db);
        var put = new Promise(function(resolve, reject) {
            transaction.objectStore('events').put({
                timeStamp: timeStamp,
                value: value
              });
            transaction.onerror = reject;
            transaction.oncomplete = resolve;
          });

        put.then(close, close);

        return put;
      });
  };
  impls.client.save = function(worker, value) {
    return clientSend(worker, 'recorder.js:save', value);
  };

  impls.worker.read = function() {
    return connect().then(function(db) {
        var txn = db.transaction(['events']);
        var request = txn.objectStore('events').openCursor();
        var close = db.close.bind(db);
        var readAll = new Promise(function(resolve, reject) {
            var results = [];
            txn.onerror = request.onerror = reject;

            request.onsuccess = function(event) {
              var cursor = event.target.result;
              if (cursor) {
                results.push(cursor.value);
                cursor.continue();
                return;
              }
              results.sort(function(a, b) {
                  return a.timeStamp - b.timeStamp;
                });
              resolve(results.map(function(result) { return result.value; }));
            };
          });

        readAll.then(close, close);

        return readAll;
      });
  };
  impls.client.read = function(worker) {
    return clientSend(worker, 'recorder.js:read');
  };

  if ('ServiceWorkerGlobalScope' in self &&
    self instanceof ServiceWorkerGlobalScope) {
    self.recorder = impls.worker;
    self.addEventListener('message', onMessage);
  } else {
    self.recorder = impls.client;
  }
}());
