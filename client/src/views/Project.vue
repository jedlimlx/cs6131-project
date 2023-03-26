<template>
    <v-container fill-height>
        <v-row class="pb-10">
            <div class="text-h3 pr-6">Project</div>
            <v-btn color="primary" icon="mdi-plus" @click=""></v-btn>
        </v-row>

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

        <v-virtual-scroll height="500">
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
    </v-container>
</template>

<script lang="ts" setup>
import { onMounted, ref, Ref } from 'vue'
import { SERVER } from "@/main"
import { useUserStore } from "@/store/app"
import Task from "@/components/Task.vue";

const userStore = useUserStore()

const selectedItem: Ref = ref(0)
const projects: Ref = ref([])
const tasks: Ref = ref([])
const publisher: Ref = ref([])
const members: Ref = ref([])

const getProjectNames = async function () {
    projects.value = await (await fetch(SERVER + "/projects/uid=" + userStore.uid)).json()
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
}

const getTasks = async function () {
    tasks.value = await (await fetch(SERVER + "/tasks/pid=" + projects.value[selectedItem.value].pid)).json()
    members.value = await (await fetch(SERVER + "/members/pid=" + projects.value[selectedItem.value].pid)).json()
}

onMounted(() => {
    getProjectNames()
})
</script>
