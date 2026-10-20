import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [react(), VitePWA({ registerType: 'autoUpdate', includeAssets: ['favicon.svg'], manifest: { name: 'OfflineMock', short_name: 'OfflineMock', description: 'Practice anywhere, understand every mistake.', theme_color: '#103c3b', background_color: '#f7f3ea', display: 'standalone', start_url: '/' }, workbox: { navigateFallback: '/index.html' } })],
  server: { port: 5173 }
});
