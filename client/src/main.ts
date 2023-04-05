/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp, watch } from 'vue'

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

export const SERVER = "http://localhost:5000"
