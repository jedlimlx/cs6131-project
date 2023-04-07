<template>
    <v-container fill-height>
        <v-row class="pb-10 pt-10">
            <div class="text-h3 pr-6">Project</div>
            <v-btn color="primary" icon="mdi-plus" @click=""></v-btn>
        </v-row>

        <v-row>
            <v-menu v-if="projects.length > 0">
                <template v-slot:activator="{ props }">
                    <v-btn
                        color="primary"
                        dark
                        v-bind="props"
                    >
                        {{ projects[selectedItem].name }}
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item
                        v-for="(item, index) in projects"
                        :key="selectedItem"
                        active-color="primary"
                    >
                        <v-list-item-title @click="selectedItem=index; loadProjectData()">{{ item.name }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <v-btn color="black" icon="mdi-bullhorn" @click="announcementDialog=true" variant="text"></v-btn>
        </v-row>

        <v-row class="pt-10">
            <v-virtual-scroll height="500">
                <v-row style="margin-left:10px">
                    <div class="text-h4 centre">Timeline</div>
                    <v-progress-circular
                        :rotate="360"
                        :size="50"
                        :width="5"
                        v-model="progress"
                        color="primary"
                        style="margin-left:15px"
                        v-if="projects[selectedItem]"
                    >
                        {{ progress.toFixed() + '%' }}
                    </v-progress-circular>

                    <v-btn
                        color="primary"
                        icon="mdi-plus"
                        @click="text=''; title=''; date=new Date(); taskIndex=-1; dialog=true"
                        style="margin-left:15px"
                    ></v-btn>
                </v-row>

                <v-timeline class="pa-5">
                    <v-timeline-item
                        v-for="(item, index) in tasks"
                        :dot-color="item.completed ? 'green' : (new Date() < new Date(item.deadline) ? 'orange-darken-1' : 'red')"
                        :icon="item.completed ? 'mdi-progress-check' : (new Date() < new Date(item.deadline) ?
                        'mdi-progress-helper' : 'mdi-progress-alert')"
                    >
                        <template v-slot:opposite>
                            {{ item.deadline }}
                        </template>
                        <Task
                            :task="item"
                            :members="members"
                            @showDialog="text = tasks[index].description; title = tasks[index].title; date = new Date(tasks[index].deadline); taskIndex=index; dialog = true"
                            @completenessChanged="recomputeProgress(item.tnumber)"
                            @delete="deleteTask(index)"
                        ></Task>
                    </v-timeline-item>

                    <v-timeline-item
                        v-if="publisher && publisher.type === 1"
                        :dot-color="new Date() < new Date(publisher.deadline) ? 'orange-darken-1' : 'red'"
                        icon="mdi-book"
                    >
                        <template v-slot:opposite>
                            {{ publisher.deadline }}
                        </template>
                        <v-card
                            :title="publisher.pname"
                            :subtitle="publisher.website"
                            :text="new Date(publisher.deadline) > new Date ? Math.ceil(((new Date(publisher.deadline)).getTime() - (new Date()).getTime()) / (1000 * 24 * 3600)) + ' days left' : 'Deadline over'"
                            width="250"
                            :href="publisher.website"
                            class="text-wrap"
                        ></v-card>
                    </v-timeline-item>

                    <v-timeline-item
                        v-if="publisher && publisher.type === 0"
                        dot-color="black"
                        icon="mdi-book"
                    >
                        <template v-slot:opposite>
                            No deadline :)
                        </template>
                        <v-card
                            :title="publisher.pname"
                            :subtitle="publisher.website"
                            width="250"
                            :href="publisher.website"
                            class="text-wrap"
                        ></v-card>
                    </v-timeline-item>
                </v-timeline>
            </v-virtual-scroll>

            <v-spacer></v-spacer>

            <v-col>
                <v-card
                    class="align-right justify-end"
                    width="320"
                    min-height="300"
                    title="LOGS"
                    style="margin-bottom:25px"
                >
                    <template v-slot:append>
                        <v-btn
                            variant="text"
                            icon=""
                        >+</v-btn>
                    </template>
                </v-card>

                <v-card
                    class="align-right justify-right"
                    width="320"
                    min-height="300"
                    title="MEMBERS"
                >
                    <template v-slot:append>
                        <v-menu
                            width="300"
                            v-model="menu2"
                            :close-on-content-click="false"
                        >
                            <template v-slot:activator="{ props }">
                                <v-btn
                                    variant="text"
                                    icon=""
                                    v-bind="props"
                                >+</v-btn>
                            </template>
                            <v-list>
                                <v-text-field
                                    v-model="possibleUsername"
                                    class="pa-5 rounded-pill"
                                    color="primary"
                                    label="Username"
                                    prepend-icon="mdi-account"
                                    variant="outlined"
                                    @update:modelValue="getPossibleMembers()"
                                ></v-text-field>
                                <v-list-item
                                    v-for="(item2, i) in possibleMembers"
                                    :key="i"
                                    :value="item2"
                                    :title="item2.username"
                                    @click="addMember(item2.uid); menu2 = false"
                                ></v-list-item>
                            </v-list>
                        </v-menu>
                    </template>

                    <v-list density="compact">
                        <v-list-item
                            v-for="(item, i) in members"
                            :key="i"
                            :value="item"
                            active-color="primary"
                        >
                            <template v-slot:prepend>
                                <v-icon icon="mdi-account-circle" :color="colour(item.uid)"></v-icon>
                            </template>

                            <v-list-item-title v-text="item.firstname"></v-list-item-title>

                            <template v-slot:append>
                                <v-menu>
                                    <template v-slot:activator="{ props: menu }">
                                        <v-btn
                                            color="primary"
                                            variant="text"
                                            v-bind="menu"
                                            :disabled="members[members.map(x => x.uid).findIndex(x => x ===userStore.uid)].role === 'member'"
                                        >
                                            {{ item.role }}
                                        </v-btn>

                                        <v-btn
                                            icon="mdi-trash-can"
                                            elevation="0"
                                            @click="deleteMember(item.uid)"
                                            v-if="members[members.map(x => x.uid).findIndex(x => x ===userStore.uid)].role === 'lead'"
                                        >
                                            <v-icon color="red"></v-icon>
                                        </v-btn>
                                    </template>

                                    <v-list>
                                        <v-list-item
                                            v-for="(item2, i) in ['Member', 'Lead']"
                                            :key="i"
                                            :value="item2"
                                            :title="item2"
                                            @click="item.role=item2.toLowerCase()"
                                        ></v-list-item>
                                    </v-list>
                                </v-menu>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>
        </v-row>

        <v-dialog
            v-model="errorDialog"
            persistent
            max-width="290"
        >
            <v-card>
                <v-card-title class="text-h5">
                    Error
                </v-card-title>
                <v-card-text>
                    {{ error }}
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="errorDialog = false">
                        Ok
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog
            v-model="announcementDialog"
            persistent
            width="365"
        >
            <v-card>
                <v-card-title class="text-h5">
                    Announcements
                </v-card-title>
                <v-virtual-scroll max-height="300">
                    <v-list
                        v-for="(item, index) in announcements"
                        :key="item.time"
                        class="pr-5 pl-5"
                        v-if="announcements.length > 0"
                        width="355"
                    >
                        <v-card>
                            <v-row class="pa-2">
                                <v-card-subtitle class="pt-3">{{ item.time }}</v-card-subtitle>
                                <v-btn
                                    icon="mdi-pencil" color="transparent" elevation="0" size="small"
                                    v-if="members[members.map(x => x.uid).findIndex(x => x ===userStore.uid)].role === 'lead'"
                                    @click="announcementIndex = index; text = item.announcement; announcementCreationDialog = true"
                                >
                                    <v-icon color="primary"></v-icon>
                                </v-btn>
                                <v-btn
                                    icon="mdi-trash-can" color="transparent" elevation="0" size="small"
                                    v-if="members[members.map(x => x.uid).findIndex(x => x ===userStore.uid)].role === 'lead'"
                                    @click="deleteAnnouncement(index)"
                                >
                                    <v-icon color="red"></v-icon>
                                </v-btn>
                            </v-row>
                            <VMarkdownView
                                mode="light"
                                :content="item.announcement"
                                style="padding:5px; margin:5px; font-family: 'Montserrat'; font-size:13px"
                            ></VMarkdownView>
                        </v-card>
                    </v-list>
                </v-virtual-scroll>
                <v-card-text v-if="announcements.length === 0">No announcements made yet!</v-card-text>
                <v-card-actions>
                    <v-btn color="primary" text @click="announcementDialog = false">
                        Close
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        text
                        @click="announcementIndex = -1; announcementCreationDialog = true"
                        v-if="members[members.map(x => x.uid).findIndex(x => x ===userStore.uid)].role === 'lead'"
                    >New</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog
            v-model="dialog"
            fullscreen
            :scrim="false"
            transition="dialog-bottom-transition"
        >
            <v-card>
                <v-toolbar
                    dark
                    color="primary"
                >
                    <v-btn
                        icon
                        dark
                        @click="dialog = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ taskIndex === -1 ? 'New Task' : 'Edit Task' }}</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                            variant="text"
                            @click="dialog = false; editTask(taskIndex)"
                        >
                            Save
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-col>
                    <v-row cols="12">
                        <v-text-field
                            v-model="title"
                            label="Enter Title"
                            variant="outlined"
                            color="primary"
                            class="pa-5"
                            width="100"
                        ></v-text-field>
                        <Datepicker v-model="date" style="padding: 30px 10px 10px;width: 400px"/>
                    </v-row>

                    <MdEditor
                        v-model="text"
                        language="en-US"
                        :toolbars="[
                            'bold',
                            'underline',
                            'italic',
                            '-',
                            'title',
                            'strikeThrough',
                            'sub',
                            'sup',
                            'quote',
                            'unorderedList',
                            'orderedList',
                            'task',
                            '-',
                            'codeRow',
                            'code',
                            'link',
                            'image',
                            'table',
                            'mermaid',
                            'katex',
                            '-',
                            'revoke',
                            'next',
                            '=',
                            'pageFullscreen',
                            'fullscreen',
                            'preview',
                        ]"
                    ></MdEditor>
                </v-col>
            </v-card>
        </v-dialog>

        <v-dialog
            v-model="announcementCreationDialog"
            fullscreen
            :scrim="false"
            transition="dialog-bottom-transition"
        >
            <v-card>
                <v-toolbar
                    dark
                    color="primary"
                >
                    <v-btn
                        icon
                        dark
                        @click="announcementCreationDialog = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ announcementIndex === -1 ? 'New Announcement' : 'Edit Announcement' }}</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                            variant="text"
                            @click="announcementCreationDialog = false; editAnnouncement(announcementIndex)"
                        >
                            Create
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <MdEditor
                    v-model="text"
                    language="en-US"
                    :toolbars="[
                        'bold',
                        'underline',
                        'italic',
                        '-',
                        'title',
                        'strikeThrough',
                        'sub',
                        'sup',
                        'quote',
                        'unorderedList',
                        'orderedList',
                        'task',
                        '-',
                        'codeRow',
                        'code',
                        'link',
                        'image',
                        'table',
                        'mermaid',
                        'katex',
                        '-',
                        'revoke',
                        'next',
                        '=',
                        'pageFullscreen',
                        'fullscreen',
                        'preview',
                    ]"
                    class="fill-height"
                ></MdEditor>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script lang="ts" setup>
import { onMounted, ref, Ref } from 'vue'
import { SERVER } from "@/main"
import { useUserStore } from "@/store/app"
import { colour } from "@/colour"

import MdEditor from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

import Task from "@/components/Task.vue"
import Log from "@/components/Log.vue"

import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'

const userStore = useUserStore()

const selectedItem: Ref = ref(0)
const projects: Ref = ref([])
const tasks: Ref = ref([])
const publisher: Ref = ref([])
const members: Ref = ref([])

const possibleUsername: Ref = ref([])
const possibleMembers: Ref = ref([])

const menu2: Ref = ref(false)

const error: Ref = ref("You cannot remove yourself from the project!")
const errorDialog: Ref = ref(false)

const dialog: Ref = ref(false)

const taskIndex: Ref = ref(-1)
const text: Ref = ref("")
const title: Ref = ref("")

const date: Ref<Date> = ref(new Date())

const progress: Ref = ref(0)

const logs: Ref = ref([])

const announcements: Ref = ref([])
const announcementDialog: Ref = ref(false)
const announcementCreationDialog: Ref = ref(false)

const announcementIndex: Ref = ref(-1)

const recomputeProgress = function(tnumber: number) {
    let count = 0
    let length = 0
    for (let item of tasks.value) {
        if (!item.completed && item.tnumber === tnumber) count++
        else if (item.completed && item.tnumber !== tnumber) count++
        length++
    }

    progress.value = count / length * 100
}

const loadEverything = async function() {
    projects.value = await (await fetch(SERVER + "/projects/uid=" + userStore.uid)).json()
    progress.value = projects.value[selectedItem.value].progress * 100

    tasks.value = await (await fetch(SERVER + "/tasks/pid=" + projects.value[selectedItem.value].pid)).json()
    members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
    logs.value = await (await fetch(SERVER + "/logs/pid=" + projects.value[selectedItem.value].pid)).json()
    announcements.value = await (await fetch(SERVER + "/announcements/pid=" + projects.value[selectedItem.value].pid)).json()
}

const loadProjectData = async function() {
    await getTasks()
    if (projects.value[selectedItem.value].pname != null) {
        publisher.value = await (await fetch(
            SERVER + "/publisher/pname=" + projects.value[selectedItem.value].pname
        )).json()
    } else {
        publisher.value = []
    }

    progress.value = projects.value[selectedItem.value].progress * 100
}

const getTasks = async function () {
    tasks.value = await (await fetch(SERVER + "/tasks/pid=" + projects.value[selectedItem.value].pid)).json()
    members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
    logs.value = await (await fetch(SERVER + "/logs/pid=" + projects.value[selectedItem.value].pid)).json()
    announcements.value = await (await fetch(SERVER + "/announcements/pid=" + projects.value[selectedItem.value].pid)).json()

    console.log(announcements.value)
}

const getPossibleMembers = async function() {
    possibleMembers.value = await (await fetch(SERVER + '/possible_members/username=' + possibleUsername.value)).json()
}

const addMember = async function(uid: Number) {
    await fetch(SERVER + "/add_members/pid=" + projects.value[selectedItem.value].pid + "&uid=" + uid + "&role=member")
    members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
}

const deleteMember = async function(uid: Number) {
    // Input Validation
    if (members.value.length > 1 && uid != userStore.uid) {
        await fetch(SERVER + "/remove_members/pid=" + projects.value[selectedItem.value].pid + "&uid=" + uid)
        members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
    } else if (uid == userStore.uid) {  // Cannot delete yourself
        error.value = "You cannot remove yourself from the project!"
        errorDialog.value = true
    }
}

function padTo2Digits(num: number) {
    return num.toString().padStart(2, '0');
}

function formatDate(date: Date) {
    return (
        [
            date.getUTCFullYear(),
            padTo2Digits(date.getUTCMonth() + 1),
            padTo2Digits(date.getUTCDate()),
            ].join('-') +
            ' ' +
        [
            padTo2Digits(date.getUTCHours()),
            padTo2Digits(date.getUTCMinutes()),
            padTo2Digits(date.getUTCSeconds()),
        ].join(':')
    );
}

const deleteTask = async function(index: number) {
    await fetch(SERVER + "/delete_task/pid="+projects.value[selectedItem.value].pid
        +"&tnumber="+tasks.value[index].tnumber)
    delete tasks.value[index]
}

const editTask = async function(index: number) {
    let dateString = formatDate(date.value)
    let b64description = btoa(text.value)
    if (index === -1) {
        await fetch(
            SERVER + "/new_task/pid="+projects.value[selectedItem.value].pid
            + "&deadline="+dateString
            + "&title="+title.value
            + "&description="+b64description
        )
        await getTasks()
    } else {
        await fetch(
            SERVER + "/edit_task_details/pid="+projects.value[selectedItem.value].pid
            + "&tnumber="+tasks.value[index].tnumber
            + "&deadline="+dateString
            + "&title="+title.value
            + "&description="+b64description
        )
        await getTasks()
    }
}

const editAnnouncement = async function(index: number) {
    let b64announcement = btoa(text.value)
    if (index === -1) {
        await fetch(
            SERVER + "/make_announcement/pid="+projects.value[selectedItem.value].pid+
            "&announcement="+b64announcement
        )
        await getTasks()
    } else {
        let timeString = formatDate(new Date(announcements.value[index].time))
        await fetch(
            SERVER + "/edit_announcement/pid="+projects.value[selectedItem.value].pid+
            "&announcement="+b64announcement+"&time="+timeString
        )
        await getTasks()
    }

}

const deleteAnnouncement = async function(index: number) {
    let b64announcement = btoa(announcements.value[index].announcement)
    let timeString = formatDate(new Date(announcements.value[index].time))
    await fetch(
        SERVER + "/delete_announcement/pid="+projects.value[selectedItem.value].pid+
        "&announcement="+b64announcement+"&time="+timeString
    )
    await getTasks()
}

onMounted(() => {
    loadEverything()
})
</script>
