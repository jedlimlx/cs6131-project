// Utilities
import { createPinia, defineStore } from 'pinia'
import { ref } from "vue";
import { SERVER } from "@/main";

export const useUserStore = defineStore('user', {
    state: () => ({
        loggedIn: false,
        username: "",
        firstname: "",
        lastname: "",
        uid: -1,
        email: "",
        creatingNewAccount: false
    }),
    actions: {
        async login(username: string, password: string): Promise<boolean> {
            let data = await (await fetch(SERVER+"/login/username="+username+"&password="+password)).json()
            if (data.status == 0) {
                this.loggedIn = false
            } else {
                this.loggedIn = true
                this.username = username
                this.firstname = data.firstname
                this.lastname = data.lastname
                this.email = data.email
                this.uid = data.uid
                console.log(data)
            }

            return this.loggedIn
        },
    },
    persist: true
})
