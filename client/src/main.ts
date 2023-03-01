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

import { createPinia } from "pinia"
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

const pinia = createPinia()

pinia.use(piniaPluginPersistedState)

export const SERVER = "http://127.0.0.1:5000"
