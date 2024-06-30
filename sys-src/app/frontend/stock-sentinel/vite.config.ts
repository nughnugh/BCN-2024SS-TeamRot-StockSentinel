import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import dotenv from 'dotenv';

dotenv.config({path: '../../../.env'});

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: true,
		port: 8080
	},
	define: {
		__API_ADDRESS__: `"http://${process.env.BACKEND_HOST || "localhost"}:3000"`,
	}
});