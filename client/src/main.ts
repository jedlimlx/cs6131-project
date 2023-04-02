/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')

// Create the pinia store
import { createPinia } from "pinia"
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

const pinia = createPinia()

pinia.use(piniaPluginPersistedState)

// Use Mavon Editor
import mavonEditor from "mavon-editor";
import "mavon-editor/dist/css/index.css";

app.use(mavonEditor)

export const SERVER = "http://localhost:5000"
