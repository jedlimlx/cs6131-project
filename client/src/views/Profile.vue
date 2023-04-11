<template>
    <v-container fill-height>
        <v-card width="600" class="mt-10">
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
            <v-divider></v-divider>
            <v-card-title>Your Progress</v-card-title>
            <v-card-text>{{ numUndoneTasks }} tasks outstanding, {{ numOverdueTasks }} overdue</v-card-text>
            <v-card-text>{{ numUnreadReferences }} unread references</v-card-text>
            <v-divider></v-divider>
            <v-list density="compact">
                <v-list-subheader>PROJECTS</v-list-subheader>
                <v-list-item
                    v-for="(item, i) in projects"
                    :key="i"
                    :value="item"
                >
                    <v-list-item>{{ item.name }}</v-list-item>

                    <template v-slot:append>
                        <v-progress-circular
                            :rotate="360"
                            :size="50"
                            :width="5"
                            :model-value="item.progress * 100"
                            color="primary"
                            style="margin-left:15px"
                        >
                            {{ (item.progress * 100).toFixed() + '%' }}
                        </v-progress-circular>
                    </template>
                </v-list-item>
            </v-list>
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
import {onMounted, Ref, ref} from "vue"
import { SERVER } from "@/main"
const userStore = useUserStore()

const editing: Ref<boolean> = ref(false)

const password: Ref<string> = ref("")
const newPassword: Ref<string> = ref("")
const changingPassword: Ref<boolean> = ref(false)

const show1: Ref<boolean> = ref(false)
const show2: Ref<boolean> = ref(false)

const projects: Ref = ref()

const numUndoneTasks: Ref<number> = ref(0)
const numOverdueTasks: Ref<number> = ref(0)
const numUnreadReferences: Ref<number> = ref(0)

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

const loadStats = async function() {
    projects.value = await (await fetch(SERVER + "/projects/uid=" + userStore.uid + "&order=1")).json()

    let lst = await (await fetch(SERVER + "/num_tasks/uid=" + userStore.uid)).json()
    numUndoneTasks.value = lst[0]
    numOverdueTasks.value = lst[1]
    numUnreadReferences.value = (await (await fetch(SERVER + "/num_unread_references/uid=" + userStore.uid)).json())[0]
}

onMounted(() => {
    loadStats()
})
</script>
