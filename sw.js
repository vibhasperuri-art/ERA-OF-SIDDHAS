const CACHE_NAME = 'era-of-siddhas-v1';
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
  './admin.html',
  './js/api.js',
  './sacred_city.png',
  './flying_manuscript.png',
  './ancient_weapons.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then(networkResponse => {
        if (networkResponse.status === 200 && event.request.method === 'GET') {
          const cacheCopy = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, cacheCopy);
          });
        }
        return networkResponse;
      }).catch(() => {
        if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
          return caches.match('./index.html');
        }
      });
    })
  );
});
