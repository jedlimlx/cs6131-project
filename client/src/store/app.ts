// Utilities
import { createPinia, defineStore } from 'pinia'
import { ref } from "vue";

export const useUserStore = defineStore('user', {
    state: () => ({
        loggedIn: ref(false),
        username: ref("")
    }),
    actions: {
        login(username: string) {
            this.loggedIn = true;
            this.username = username;
            console.log(username);
            console.log(this.username);
        },
    },
    persist: true
})
