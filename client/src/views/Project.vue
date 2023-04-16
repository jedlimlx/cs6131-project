<template>
    <v-container fill-height>
        <v-row class="pb-10 pt-10">
            <div class="text-h3 pr-6">Project</div>
            <v-btn color="primary" icon="mdi-plus" @click="editedTitle = ''; newProject = true; editTitleDialog=true"></v-btn>
        </v-row>

        <div class="text-h5 pr-6" v-if="projects.length === 0">No Projects Created. Create one now!</div>

        <v-row v-if="projects.length > 0">
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

            <v-btn color="black" icon="mdi-pencil" @click="editedTitle = projects[selectedItem].name; newProject = false; editTitleDialog=true" variant="text" v-if="lead"></v-btn>
            <v-btn color="black" icon="mdi-trash-can" @click="deleteProject()" variant="text" v-if="lead"></v-btn>
            <v-btn color="black" icon="mdi-bullhorn" @click="announcementDialog=true" variant="text"></v-btn>
        </v-row>

        <v-row class="pt-10" v-if="projects.length > 0">
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

                <v-timeline class="pa-5" density="comfortable">
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
                            :lead="lead"
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
                            {{ new Date(Date.parse(publisher.deadline)).toLocaleString() }}
                        </template>
                        <v-card
                            :text="new Date(publisher.deadline) > new Date ? Math.ceil(((new Date(publisher.deadline)).getTime() - (new Date()).getTime()) / (1000 * 24 * 3600)) + ' days left' : 'Deadline over'"
                            width="250"
                            class="text-wrap"
                        >
                            <template v-slot:title>
                                <v-card-title class="text-wrap">
                                    {{ publisher.pname }}
                                </v-card-title>
                            </template>
                            <template v-slot:subtitle>
                                <v-card-subtitle class="text-wrap">
                                    {{ publisher.website }}
                                </v-card-subtitle>
                            </template>
                            <v-card-actions>
                                <v-btn @click="publisher = []; updatePublisher()" color="primary">Remove Goal</v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon="mdi-link" :href="publisher.website" target="_blank"></v-btn>
                            </v-card-actions>
                        </v-card>
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
                            width="250"
                            class="text-wrap"
                        >
                            <template v-slot:title>
                                <v-card-title class="text-wrap">
                                    {{ publisher.pname }}
                                </v-card-title>
                            </template>
                            <template v-slot:subtitle>
                                <v-card-subtitle class="text-wrap">
                                    {{ publisher.website }}
                                </v-card-subtitle>
                            </template>
                            <v-card-actions>
                                <v-btn @click="publisher = []; updatePublisher()" color="primary">Remove Goal</v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon="mdi-link" :href="publisher.website" target="_blank"></v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-timeline-item>

                    <v-timeline-item
                        v-if="publisher.length === 0"
                        dot-color="black"
                        icon="mdi-book"
                    >
                        <template v-slot:opposite>
                            Add a publication goal?
                        </template>
                        <v-card
                            title="Add a Publisher"
                            width="250"
                            class="text-wrap"
                        >
                            <v-combobox
                                v-model="selectedPublisher"
                                label="Publisher"
                                color="primary"
                                item-title="pname"
                                item-value="pname"
                                :items="journals"
                                class="pa-5"
                            ></v-combobox>
                            <v-card-actions>
                                <v-btn
                                    @click="publisher = selectedPublisher; updatePublisher()"
                                    color="primary"
                                >Confirm</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-timeline-item>
                </v-timeline>
            </v-virtual-scroll>

            <v-spacer></v-spacer>

            <v-col class="align-right justify-end justify-content-end fill-width">
                <v-row class="align-right justify-end">
                    <v-col cols="6">
                         <v-card
                            class="align-right justify-end mr-4"
                            width="320"
                            min-height="300"
                            title="LOGS"
                        >
                            <template v-slot:append>
                                <v-btn
                                    variant="text"
                                    icon="mdi-notebook"
                                    @click="logbookOpen = true; editing = false"
                                ></v-btn>
                                <v-btn
                                    variant="text"
                                    icon=""
                                    @click="logs.unshift(
                                        {
                                            'pid': projects[selectedItem].pid,
                                            'lnumber': logs.length > 0 ? Math.max.apply(Math, logs.map(x => x.lnumber))+1 : 0,
                                            'uid': userStore.uid,
                                            'firstname': userStore.firstname,
                                            'title': 'Untitled Log',
                                            'date': new Date(),
                                            'text': ''
                                        }
                                    ); shownLogs.unshift(logs[0]); logbookPage = 1; text = 'Write your log here.'; title = 'Untitled Log'; addLog(); logbookOpen = true; editing = true"
                                >+</v-btn>
                            </template>

                            <v-list density="compact">
                                <v-text-field
                                    v-model="logSearchTerm"
                                    label="Search"
                                    class="pr-5 pl-5"
                                    variant="outlined"
                                    color="primary"
                                    @update:modelValue="shownLogs = logs.filter(x => x.title.toLowerCase().includes(logSearchTerm.toLowerCase()))"
                                ></v-text-field>

                                <v-list-item>
                                    <v-list-item-subtitle>{{ shownLogs.length + " logs found" }}</v-list-item-subtitle>
                                </v-list-item>

                                <v-list-item
                                    v-for="(item, i) in shownLogs"
                                    :key="i"
                                    :value="item"
                                    active-color="primary"
                                    @click="logbookPage=logs.map(x => x.lnumber).indexOf(item.lnumber)+1; logbookOpen=true; editing = false"
                                >
                                    <template v-slot:append>
                                        <v-chip
                                            :color="colour(item.uid)"
                                        >
                                            {{ item.firstname }}
                                        </v-chip>
                                    </template>
                                    <v-list-item-title v-text="item.title"></v-list-item-title>
                                    <v-list-item-subtitle v-text="new Date(Date.parse(item.date)).toLocaleString()"></v-list-item-subtitle>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-col>

                    <v-col cols="6">
                        <v-card
                            class="align-right justify-right fill-height"
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
                                    <v-list density="compact">
                                        <v-list-subheader v-if="suggestedMembers.length > 0">SUGGESTIONS</v-list-subheader>
                                        <v-list-item
                                            v-for="(item2, i) in suggestedMembers"
                                            :key="i"
                                            :value="item2"
                                            :title="item2.username"
                                            @click="addMember(item2.uid); menu2 = false"
                                        ></v-list-item>
                                        <v-divider v-if="suggestedMembers.length > 0"></v-divider>
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
                                                    :disabled="!lead"
                                                >
                                                    {{ item.role }}
                                                </v-btn>

                                                <v-btn
                                                    icon="mdi-trash-can"
                                                    elevation="0"
                                                    @click="deleteMember(item.uid)"
                                                    v-if="lead"
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

                    <v-col cols="12">
                        <v-card
                            class="align-right justify-end justify-content-end"
                            width="660"
                            min-height="300"
                            title="REFERENCES"
                            style="margin-top:25px"
                        >
                            <template v-slot:append>
                                <v-btn
                                    variant="text"
                                    icon=""
                                    @click="$refs.refDialog.show = true"
                                >+</v-btn>
                            </template>
                            <v-list density="compact">
                                <v-text-field
                                    v-model="referencesSearchTerm"
                                    label="Search"
                                    class="pr-5 pl-5"
                                    variant="outlined"
                                    color="primary"
                                    @update:modelValue="shownReferences = references.filter(x => x.title.toLowerCase().includes(referencesSearchTerm.toLowerCase()))"
                                ></v-text-field>

                                <v-list-item>
                                    <v-list-item-subtitle>
                                        {{ shownReferences.length + " references " + (referencesSearchTerm === '' ? 'cited' : 'found') }}
                                    </v-list-item-subtitle>
                                </v-list-item>

                                <v-list-item
                                    v-for="(item, i) in shownReferences"
                                    :key="i"
                                    :value="item"
                                    active-color="primary"
                                >
                                    <Reference
                                        :read="false"
                                        :can-delete="true"
                                        :reference="item"
                                        :selected="false"
                                        @delete="deleteReference(item)"
                                    ></Reference>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-col>
                </v-row>
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
                                <v-card-subtitle class="pt-3">{{ new Date(Date.parse(item.time)).toLocaleString() }}</v-card-subtitle>
                                <v-btn
                                    icon="mdi-pencil" color="transparent" elevation="0" size="small"
                                    @click="announcementIndex = index; text = item.announcement; announcementCreationDialog = true"
                                >
                                    <v-icon color="primary"></v-icon>
                                </v-btn>
                                <v-btn
                                    icon="mdi-trash-can" color="transparent" elevation="0" size="small"
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
                        @click="announcementIndex = -1; text = ''; announcementCreationDialog = true"
                        v-if="lead"
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

        <v-dialog
            v-model="logbookOpen"
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
                        @click="logbookOpen = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>Virtual Logbook</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                            @click="editLog(logbookPage-1); editing=!editing"
                            v-if="logs.length > 0 && userStore.uid === logs[logbookPage-1].uid"
                        >
                            <v-icon :icon="editing ? 'mdi-content-save' : 'mdi-pencil'" color="white"></v-icon>
                        </v-btn>
                        <v-btn @click="deleteLog(logbookPage-1)">
                            <v-icon icon="mdi-trash-can" color="white" v-if="logs.length > 0"></v-icon>
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>

                <v-window
                    :model-value="logbookPage-1"
                    :show-arrows="false"
                >
                    <v-window-item
                        v-for="(log, index) in logs"
                        :key="index"
                    >
                        <v-card style="font-family: 'Montserrat'">
                            <template v-slot:append>
                                <v-chip :color="colour(log.uid)">
                                    {{ log.firstname }}
                                </v-chip>
                            </template>
                            <template v-slot:title>
                                <v-card-title
                                    v-if="!editing"
                                >{{ log.title }}</v-card-title>
                                <v-text-field
                                    v-model="title"
                                    variant="outlined"
                                    color="primary"
                                    label="Title"
                                    v-if="editing"
                                    class="mt-5"
                                ></v-text-field>
                            </template>
                            <v-card-subtitle>{{ new Date(Date.parse(log.date)).toLocaleString() }}</v-card-subtitle>

                            <MdEditor
                                previewOnly
                                class="ma-5"
                                v-model="log.text"
                                language="en-US"
                                v-if="!editing"
                                style="max-width: 97%; height: 345px !important;"
                            ></MdEditor>

                            <MdEditor
                                class="ma-5"
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
                                v-if="editing"
                                style="max-width: 97%; max-height: 290px !important;"
                            ></MdEditor>
                        </v-card>
                    </v-window-item>
                </v-window>
                <v-pagination
                    :length="logs.length"
                    v-model="logbookPage"
                    class="align-bottom justify-bottom"
                    @click="editLog(logbookPage); editing = false"
                    v-if="logs.length > 0"
                ></v-pagination>
                <v-card-title v-if="logs.length <= 0">
                    No logs here yet!
                </v-card-title>
            </v-card>
        </v-dialog>

        <v-row justify="center">
            <v-dialog
                v-model="editTitleDialog"
                persistent
                max-width="900"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        {{ newProject ? 'New Project' : 'Edit Title' }}
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="editedTitle"
                            label="Enter Title"
                            variant="outlined"
                            color="primary"
                        ></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="editTitleDialog = false">
                            Cancel
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="editTitleDialog = false; (newProject ? createProject() : editTitle())">
                            Confirm
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>

        <ReferenceDialog
            ref="refDialog"
            @addReference="addReference"
        ></ReferenceDialog>
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
import Reference from "@/components/Reference.vue";
import ReferenceDialog from "@/components/ReferenceDialog.vue";
import {storeToRefs} from "pinia";

const userStore = useUserStore()

const { selectedItem } = storeToRefs(userStore)
const projects: Ref = ref([])
const tasks: Ref = ref([])
const publisher: Ref = ref([])
const members: Ref = ref([])

const possibleUsername: Ref = ref([])
const possibleMembers: Ref = ref([])
const suggestedMembers: Ref = ref([])

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
const shownLogs: Ref = ref([])

const announcements: Ref = ref([])
const announcementDialog: Ref = ref(false)
const announcementCreationDialog: Ref = ref(false)
const announcementIndex: Ref = ref(-1)

const logbookOpen: Ref = ref(false)
const logbookPage: Ref = ref(1)
const logSearchTerm: Ref = ref("")

const journals: Ref = ref([])
const selectedPublisher: Ref = ref([])

const editing: Ref = ref(false)

const lead: Ref = ref(false)

const references: Ref = ref([])
const shownReferences: Ref = ref([])

const refDialog = ref(null)
const referencesSearchTerm = ref("")

const editTitleDialog = ref(false)
const editedTitle = ref("")
const newProject = ref(false)

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
    projects.value = await (await fetch(SERVER + "/projects/uid=" + userStore.uid + "&order=0")).json()
    selectedItem.value = Math.min(selectedItem.value, projects.value.length - 1)

    if (projects.value.length > 0) {
        progress.value = projects.value[selectedItem.value].progress * 100
        if (projects.value[selectedItem.value].pname != null) {
            publisher.value = await (await fetch(
                SERVER + "/publisher/pname=" + projects.value[selectedItem.value].pname
            )).json()
        } else {
            publisher.value = []
        }

        tasks.value = await (await fetch(SERVER + "/tasks/pid=" + projects.value[selectedItem.value].pid)).json()
        members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
        logs.value = await (await fetch(SERVER + "/logs/pid=" + projects.value[selectedItem.value].pid)).json()
        //@ts-ignore
        shownLogs.value = logs.value.map(x => x)

        announcements.value = await (await fetch(SERVER + "/announcements/pid=" + projects.value[selectedItem.value].pid)).json()
        references.value = await (await fetch(SERVER + "/references/pid=" + projects.value[selectedItem.value].pid)).json()
        //@ts-ignore
        shownReferences.value = references.value.map(x => x)

        journals.value = await (await fetch(SERVER + "/publishers")).json()
        suggestedMembers.value = await (await fetch(SERVER + '/suggested_members/uid='+userStore.uid)).json()
        suggestedMembers.value = suggestedMembers.value.filter(x => !members.value.map(x => x.uid).includes(x.uid))

        lead.value = members.value[members.value.map(x => x.uid).indexOf(userStore.uid)].role === "lead"
    }
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

    //@ts-ignore
    shownLogs.value = logs.value.map(x => x)

    announcements.value = await (await fetch(SERVER + "/announcements/pid=" + projects.value[selectedItem.value].pid)).json()
    references.value = await (await fetch(SERVER + "/references/pid=" + projects.value[selectedItem.value].pid)).json()

    //@ts-ignore
    shownReferences.value = references.value.map(x => x)

    lead.value = members.value[members.value.map(x => x.uid).indexOf(userStore.uid)].role === "lead"
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
    tasks.value.splice(index, 1)
    recomputeProgress(-1)
}

const editTask = async function(index: number) {
    if (title.value.length === 0 || text.value.length === 0) {
        errorDialog.value = true
        error.value = "Title or text are empty"
        return
    }

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
        recomputeProgress(-1)
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
    if (text.value.length === 0) {
        errorDialog.value = true
        error.value = "Text is empty"
        return
    }

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

const addLog = async function() {
    if (title.value.length === 0 || text.value.length === 0) {
        errorDialog.value = true
        error.value = "Title or text are empty"
        return
    }

    logs.value[0].title = title.value
    logs.value[0].text = text.value

    let b64log = btoa(text.value)
    await fetch(
        SERVER + "/add_log/pid="+projects.value[selectedItem.value].pid+"&uid="+userStore.uid+
        "&title="+title.value+"&text="+b64log
    )
}

const editLog = async function(index: number) {
    if (editing.value) {
        if (title.value.length === 0 || text.value.length === 0) {
            errorDialog.value = true
            error.value = "Title or text are empty"
            return
        }

        logs.value[index].title = title.value
        logs.value[index].text = text.value

        let b64log = btoa(text.value)
        await fetch(
            SERVER + "/edit_log/pid="+projects.value[selectedItem.value].pid+"&lnumber="+logs.value[index].lnumber+
            "&title="+title.value+"&text="+b64log
        )
    } else {
        title.value = logs.value[index].title
        text.value = logs.value[index].text
    }
}

const deleteLog = async function(index: number) {
    if (logs.value.length === 1)
        logbookOpen.value = false

    await fetch(
        SERVER + "/delete_log/pid="+projects.value[selectedItem.value].pid+"&lnumber="+logs.value[index].lnumber
    )
    logs.value.splice(index, 1)
    logSearchTerm.value = ""
    // ts-ignore
    shownLogs.value = logs.value.map(x => x)

    logbookPage.value = Math.min(logbookPage.value,logs.value.length)
}

const updatePublisher = async function() {
    if (publisher.value.length == 0) {
        await fetch(
            SERVER + "/update_publisher/pname=NULL&pid="+projects.value[selectedItem.value].pid
        )
    } else {
        await fetch(
            SERVER + "/update_publisher/pname="+publisher.value.pname+"&pid="+projects.value[selectedItem.value].pid
        )
    }
}

const addReference = async function() {
    // @ts-ignore
    let data = await (await fetch(SERVER + "/add_reference/doi=\""+refDialog.value.doi.replaceAll("/", "$2F")+
        "\"&pid="+projects.value[selectedItem.value].pid)).json()
    if (data.status == 0) {
        if (data.error.includes("Duplicate")) {
            error.value = "This reference is already in the database."
        } else {
            error.value = data.error
        }

        errorDialog.value = true
    }

    // Reload the references
    references.value = await (await fetch(SERVER + "/references/pid=" + projects.value[selectedItem.value].pid)).json()
    //@ts-ignore
    shownReferences.value = references.value.map(x => x)
}

const deleteReference = async function(item: object) {
    //@ts-ignore
    await fetch(SERVER + "/delete_reference/doi=\""+item.doi.replaceAll("/", "$2F")+"&pid="+projects.value[selectedItem.value].pid)
    //@ts-ignore
    references.value = references.value.filter(i => i !== item)
    //@ts-ignore
    shownReferences.value = references.value.map(x => x)
}

const editTitle = async function() {
    if (editedTitle.value.length === 0) {
        editedTitle.value = true
        error.value = "Title is empty"
        return
    }

    projects.value[selectedItem.value].name = editedTitle.value
    await fetch(SERVER + "/edit_title/pid="+projects.value[selectedItem.value].pid+"&title="+editedTitle.value)
}

const createProject = async function() {
    if (editedTitle.value.length === 0) {
        editedTitle.value = true
        error.value = "Title is empty"
        return
    }

    projects.value.push(await (await fetch(SERVER + "/new_project/title="+editedTitle.value+"&uid="+userStore.uid)).json())
    selectedItem.value = projects.value.length - 1
    if (projects.value.length === 1) {
        loadEverything()
    }
}

const deleteProject = async function() {
    await fetch(SERVER + "/delete_project/pid="+projects.value[selectedItem.value].pid)
    projects.value.splice(selectedItem.value, 1)
    selectedItem.value = Math.min(selectedItem.value, projects.value.length-1)
}

const print = function(x: any) { console.log(x) }

onMounted(() => {
    loadEverything()
    return { refDialog }
})
</script>
