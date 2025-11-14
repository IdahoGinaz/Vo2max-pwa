const CACHE = 'vo2-fit-v1';
const FILES = ['/', 'index.html', 'manifest.json'];

self.addEventListener('install', evt => {
  evt.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)));
  self.skipWaiting();
});

self.addEventListener('activate', evt => {
  evt.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', evt => {
  evt.respondWith(
    caches.match(evt.request).then(r => r || fetch(evt.request))
  );
});
