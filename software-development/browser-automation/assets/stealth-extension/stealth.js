// Override automation flags before page scripts run
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// Override chrome.runtime to hide extension
if (window.chrome && window.chrome.runtime) {
  const originalGetManifest = window.chrome.runtime.getManifest;
  window.chrome.runtime.getManifest = function() {
    const manifest = originalGetManifest.call(this);
    return manifest;
  };
}

// Override permissions query to hide automation
if (navigator.permissions) {
  const origQuery = navigator.permissions.query;
  navigator.permissions.query = (desc) => {
    if (desc.name === 'clipboard-read' || desc.name === 'clipboard-write') {
      return Promise.resolve({ state: 'granted', onchange: null });
    }
    return origQuery.call(navigator.permissions, desc);
  };
}

// Patch plugins array length
Object.defineProperty(navigator, 'plugins', {
  get: () => {
    const arr = [1, 2, 3, 4, 5];
    arr.item = (i) => arr[i];
    arr.namedItem = () => null;
    arr.refresh = () => {};
    return arr;
  }
});

// Patch languages
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-US', 'en']
});
