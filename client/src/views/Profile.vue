<template>
    <v-container fill-height>
        <v-row class="pa-10" cols="12">
            <v-col cols="6">
                <v-card width="500" class="mt-5">
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
                            active-color="primary"
                            @click="userStore.selectedItem = projects2.map(x => x.pid).indexOf(item.pid); $router.push('/projects')"
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
            </v-col>
            <v-col cols="6">
                <v-row style="margin-top:30px">
                    <div class="text-h4 centre">Outstanding Tasks</div>
                </v-row>

                <v-timeline class="pa-5 pl-0" density="comfortable">
                    <v-timeline-item
                        v-for="(item, index) in tasks"
                        :dot-color="item.completed ? 'green' : (new Date() < new Date(item.deadline) ? 'orange-darken-1' : 'red')"
                        :icon="item.completed ? 'mdi-progress-check' : (new Date() < new Date(item.deadline) ?
                        'mdi-progress-helper' : 'mdi-progress-alert')"
                    >
                        <template v-slot:opposite>
                            {{ new Date(Date.parse(item.deadline)).toLocaleString() }}
                        </template>
                        <Task
                            :task="item"
                            :members="members"
                            :lead="false"
                            :profile="true"
                            @jump="userStore.selectedItem = projects2.map(x => x.pid).indexOf(item.pid); $router.push('/projects')"
                        ></Task>
                    </v-timeline-item>
                </v-timeline>
            </v-col>
        </v-row>

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
import Task from "@/components/Task.vue";
const userStore = useUserStore()

const editing: Ref<boolean> = ref(false)

const password: Ref<string> = ref("")
const newPassword: Ref<string> = ref("")
const changingPassword: Ref<boolean> = ref(false)

const show1: Ref<boolean> = ref(false)
const show2: Ref<boolean> = ref(false)

const projects: Ref = ref([])
const projects2: Ref = ref([])

const tasks: Ref = ref([])
const members: Ref = ref([])

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
    projects2.value = await (await fetch(SERVER + "/projects/uid=" + userStore.uid + "&order=0")).json()

    let lst = await (await fetch(SERVER + "/num_tasks/uid=" + userStore.uid)).json()
    numUndoneTasks.value = lst[0]
    numOverdueTasks.value = lst[1]
    numUnreadReferences.value = (await (await fetch(SERVER + "/num_unread_references/uid=" + userStore.uid)).json())[0]
}

const loadOutstandingTasks = async function() {
    tasks.value = await (await fetch(SERVER + "/get_outstanding_tasks/uid=" + userStore.uid)).json()
    members.value = await (await fetch(SERVER + "/all_possible_members")).json()
}

onMounted(() => {
    loadStats()
    loadOutstandingTasks()
})
</script>
