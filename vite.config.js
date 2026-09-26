import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  publicDir: 'public',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    rollupOptions: {
      external: ['three', 'three/examples/jsm/controls/OrbitControls.js'],
      output: {
        paths: {
          'three': 'https://esm.sh/three@0.160.0',
          'three/examples/jsm/controls/OrbitControls.js': 'https://esm.sh/three@0.160.0/examples/jsm/controls/OrbitControls.js'
        }
      }
    }
  },
  server: {
    port: 3000,
    open: false
  }
});
