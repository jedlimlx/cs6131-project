<template>
    <v-app>
        <v-navigation-drawer v-model="drawerShown" temporary app>
            <v-list dense nav>
                <v-list-item>
                    <h2>Welcome, {{ firstname }} {{ lastname }}!</h2>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item v-for="item in routes" :to="item.path" @click="drawerShown = false"
                             style="text-decoration: none; color: inherit;" :key="item.name">
                    <template v-slot:prepend>
                        <v-icon :icon="item.icon"></v-icon>
                    </template>
                    <v-list-item-title v-text="item.name"></v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon @click="drawerShown = (loggedIn && !drawerShown); alertShown = !loggedIn"></v-app-bar-nav-icon>
            <v-toolbar-title>
                Organisation is all you need!
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn elevation=0 color="white" padding="4" @click="loggingIn = true" v-if="!loggedIn">
                Login
            </v-btn>
            <v-btn elevation=0 color="white" padding="4" @click="creatingNewAccount = true" v-if="!loggedIn">
                New Account
            </v-btn>
            <v-btn elevation=0 color="white" padding="4" @click="loggedIn = false" v-if="loggedIn">
                Logout
            </v-btn>
        </v-app-bar>

        <v-main>
            <router-view />
        </v-main>

        <v-row justify="center">
            <v-dialog
                v-model="loggingIn"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        Login
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="username"
                            label="Enter Username"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>
                        <v-text-field
                            v-model="password"
                            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show1 ? 'text' : 'password'"
                            @click:append="show1 = !show1"
                            label="Enter Password"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="loggingIn = false; clear()">
                            Cancel
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="loggingIn = false; loggedIn = true; login()">
                            Login
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>

        <v-row justify="center">
            <v-dialog
                v-model="creatingNewAccount"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        New Account
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="username"
                            label="Enter Username"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>

                        <v-text-field
                            v-model="password"
                            :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show2 ? 'text' : 'password'"
                            @click:append="show2 = !show2"
                            label="Enter Password"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>

                        <v-text-field
                            :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show3 ? 'text' : 'password'"
                            @click:append="show3 = !show3"
                            label="Enter Password Again"
                            variant="outlined"
                            color="primary"
                            :rules="[
                                v => password === v || '2 passwords must match'
                            ]"
                        ></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="creatingNewAccount = false; clear()">
                            Cancel
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="creatingNewAccount = false; loggedIn = true; login()">
                            Create Account
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>

        <v-row justify="center">
            <v-dialog
                v-model="alertShown"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        Error
                    </v-card-title>
                    <v-card-text>
                        You need to login to access this part of the website!
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="alertShown = false">
                            Ok
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>

        <v-row justify="center">
            <v-dialog
                v-model="loginError"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        Error
                    </v-card-title>
                    <v-card-text>
                        Either your username or password is wrong!
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="loginError = false">
                            Ok
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-app>
</template>

<script lang="ts" setup>
import { createApp, ref, Ref } from 'vue'
import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import Home from "@/views/Home.vue"
import Project from "@/views/Project.vue"
import Feedback from "@/views/Feedback.vue"

import { useUserStore } from "@/store/app"
import { storeToRefs } from "pinia"

const vuetify = createVuetify({
    components,
    directives,
})

const userStore = useUserStore()
const { loggedIn, username, firstname, lastname, uid, email } = storeToRefs(userStore)

const drawerShown: Ref<boolean> = ref(false)

const loggingIn: Ref<boolean> = ref(false)
const creatingNewAccount: Ref<boolean> = ref(false)

const alertShown: Ref<boolean> = ref(false)

const show1: Ref<boolean> = ref(false)
const show2: Ref<boolean> = ref(false)
const show3: Ref<boolean> = ref(false)

const password: Ref<string> = ref("")

const loginError: Ref<boolean> = ref(false)

const routes = [
    {
        name: "Home",
        path: "/",
        icon: "mdi-file-table-box",
        component: Home,
    },
    {
        name: "Projects",
        path: "/projects",
        icon: "mdi-test-tube",
        component: Project,
    },
    {
        name: "Give Feedback",
        path: "/feedback",
        icon: "mdi-message-alert",
        component: Feedback,
    }
]

const clear = function() {
    username.value = ""
    password.value = ""
    show1.value = false
    show2.value = false
    show3.value = false
}

const login = async function() {
    let success = await userStore.login(username.value, password.value)
    if (success) {
        // do something
        // redirect to dashboard or something
        console.log(username)
        console.log(firstname+"")
    } else {
        loginError.value = true
    }
}
</script>
