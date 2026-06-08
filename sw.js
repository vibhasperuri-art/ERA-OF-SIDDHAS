const CACHE_NAME = 'era-of-siddhas-v5';
const ASSETS = [
  './',
  './index.html',
  './pillar_hub.html',
  './course_hub.html',
  './wisdom_hub.html',
  './sangha.html',
  './vicara_sannidhi.html',
  './chanting.html',
  './begin-journey.html',
  './interactive_lesson.html',
  './about.html',
  './glossary.html',
  './admin.html',
  './js/api.js',
  './js/translations.js',
  './sacred_city.png',
  './flying_manuscript.png',
  './ancient_weapons.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    Promise.all([
      self.clients.claim(),
      caches.keys().then(keys => {
        return Promise.all(
          keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
        );
      })
    ])
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const isHtml = event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html');
  const isLocal = event.request.url.startsWith(self.location.origin);

  if (isHtml && isLocal) {
    event.respondWith(
      fetch(event.request)
        .then(networkResponse => {
          if (networkResponse.status === 200) {
            const cacheCopy = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, cacheCopy);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) return cachedResponse;
            return caches.match('./index.html');
          });
        })
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then(networkResponse => {
        if (networkResponse.status === 200) {
          const cacheCopy = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, cacheCopy);
          });
        }
        return networkResponse;
      });
    })
  );
});