<template>
    <v-container fill-height>
        <v-card width="500" class="mt-10">
            <v-card-title v-if="!editing">{{ userStore.firstname }} {{ userStore.lastname }}</v-card-title>
            <v-row class="pa-6" v-if="editing">
                <v-text-field
                    label="First Name"
                    variant="outlined"
                    color="primary"
                    v-model="userStore.firstname"
                    v-if="editing"
                    class="pr-3"
                ></v-text-field>
                <v-text-field
                    label="Last Name"
                    variant="outlined"
                    color="primary"
                    v-model="userStore.lastname"
                    class="pl-3"
                ></v-text-field>
            </v-row>
            <v-card-subtitle v-if="!editing">{{ userStore.username }}#{{ userStore.uid }}</v-card-subtitle>
            <v-card-text v-if="!editing">Email: {{ userStore.email }}</v-card-text>
            <v-text-field
                label="Email"
                variant="outlined"
                color="primary"
                v-model="userStore.email"
                v-if="editing"
                class="pr-3 pl-3"
            ></v-text-field>
            <v-card-actions>
                <v-btn color="primary" v-if="!editing" @click="editing=!editing">Edit</v-btn>
                <v-btn color="primary" v-if="editing" @click="editing=!editing; updateDatabase()">Save</v-btn>
                <v-btn color="red" v-if="editing" @click="editing=!editing">Cancel</v-btn>
                <v-btn color="primary" @click="changingPassword=true">Change Password</v-btn>
            </v-card-actions>
        </v-card>

        <v-row justify="center">
            <v-dialog
                v-model="changingPassword"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        Change Password
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="password"
                            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show1 ? 'text' : 'password'"
                            @click:append="show1 = !show1"
                            label="Enter Old Password"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>

                        <v-text-field
                            v-model="newPassword"
                            :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show2 ? 'text' : 'password'"
                            @click:append="show2 = !show2"
                            label="Enter New Password"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="changingPassword = false">
                            Cancel
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="changingPassword = false; changePassword()">
                            Change Password
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app"
import { Ref, ref } from "vue"
import { SERVER } from "@/main"
const userStore = useUserStore()

const editing: Ref<boolean> = ref(false)

const password: Ref<string> = ref("")
const newPassword: Ref<string> = ref("")
const changingPassword: Ref<boolean> = ref(false)

const show1: Ref<boolean> = ref(false)
const show2: Ref<boolean> = ref(false)

const updateDatabase = function() {
    fetch(
        SERVER+
        "/update_user/uid="+userStore.uid+
        "&firstname="+userStore.firstname+
        "&lastname="+userStore.lastname+
        "&email="+userStore.email
    )
}

const changePassword = function() {
    fetch(
        SERVER+
        "/change_password/uid="+userStore.uid+
        "&password="+password.value+
        "&new_password="+newPassword.value
    )
}
</script>
