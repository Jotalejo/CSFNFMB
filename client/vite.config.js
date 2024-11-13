import { defineConfig, preprocessCSS } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'
import {config} from 'dotenv';

config();

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 8002,
    host: '127.0.0.1',
    watch: {
      usePolling: true
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  define: {
    'process.env': process.env
  }
});


