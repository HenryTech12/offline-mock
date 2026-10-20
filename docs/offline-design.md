# Offline design

The service worker precaches the Vite application shell and uses navigation fallback for cached routes. Question packs, active answers, results, and preferences live in IndexedDB through `idb`. Practice reads the local pack and never requests the API while answering. A failed import or download does not delete an existing pack. Packs are versioned and local records are replaced atomically by key.

Progress sync is intentionally not enabled in this MVP. This avoids silently uploading anonymous student data. A future sync boundary should use explicit consent, idempotency keys, a retry queue, and deterministic conflict handling.
