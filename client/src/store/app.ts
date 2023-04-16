// Utilities
import { defineStore } from 'pinia'
import { SERVER } from "@/main"
import { useLocalStorage } from "@vueuse/core"

export const useUserStore = defineStore('user', {
    state: () => ({
        //@ts-ignore
        loggedIn: useLocalStorage("loggedIn", false),
        //@ts-ignore
        username: useLocalStorage("username", ""),
        //@ts-ignore
        firstname: useLocalStorage("firstname", ""),
        //@ts-ignore
        lastname: useLocalStorage("lastname", ""),
        //@ts-ignore
        uid: useLocalStorage("uid", -1),
        //@ts-ignore
        email: useLocalStorage("email", ""),
        //@ts-ignore
        creatingNewAccount: false,
        selectedItem: useLocalStorage("index", 0)
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
            }

            return this.loggedIn
        },
        logout() {
            // Edit local storage
            localStorage.removeItem("loggedIn")
            localStorage.removeItem("username")
            localStorage.removeItem("firstname")
            localStorage.removeItem("lastname")
            localStorage.removeItem("uid")
            localStorage.removeItem("email")

            // Reset to original variables
            this.loggedIn = false
            this.username = ""
            this.firstname = ""
            this.lastname = ""
            this.uid = -1
            this.email = ""
        }
    }
})
