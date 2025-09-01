// sw.js - Service Worker
const CACHE_NAME = 'ycrad-v1.0';
const urlsToCache = [
  './',
  './index.html',
  './pygbag.js',
  './main_web.py',
  './player.py',
  './environment.py',
  './ui.py',
  './controls.py',
  './monsters.py',
  './config.py',
  './assets/character/player.png',
  './assets/monsters/slime.png',
  './assets/monsters/rat.png',
  './assets/backgrounds/village.png',
  './assets/backgrounds/forest.png',
  './assets/ui/icons/potion.png',
  './assets/ui/icons/sword.png',
  './assets/ui/icons/shield.png',
  './assets/ui/icons/coin.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});