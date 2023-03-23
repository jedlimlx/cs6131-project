<template>
    <v-card
        width="250"
        :color="task.completed ? 'green-lighten-5' : (new Date() < new Date(task.deadline) ? 'orange-lighten-5' : 'red-lighten-5')"
        :title="task.title"
    >
        <template v-slot:append>
            <v-checkbox
                color="green"
                v-model="task.completed"
                @click="updateCompleted()"
            ></v-checkbox>
        </template>
        <v-card-title class="text-wrap"></v-card-title>
        <v-card-text class="text-wrap">{{ task.description }}</v-card-text>
        <v-divider></v-divider>
        <v-row class="pa-4">
            <v-chip
                v-for="(item, index) in assigned"
                :color="colour(item.uid)"
                class="ma-2"
                closable
            >
                {{ item.firstname }}
            </v-chip>

            <v-chip
                color="primary"
                class="ma-2"
            >+</v-chip>
        </v-row>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn color="primary">
                Edit
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="js">
import { SERVER } from "@/main"
import drs from "deterministic-random-sequence"

export default {
    components: { },
    props: [ "task" ],
    emits: [ ],
    data() {
        return {
            assigned: []
        }
    },
    methods: {
        async f(pid, tnumber) {
            // @ts-ignore
            this.assigned = await (await
                fetch(SERVER+"/assigned/pid="+pid+"&tnumber="+tnumber)
            ).json()
        },
        colour(uid) {
            let index = 0
            let rand = drs("hello")
            for (let i = 0; i < uid + 1; i++) {
                index = Math.round(rand() * 1000)
            }

            return ['red', 'blue', 'green', 'purple', 'pink', 'orange',
                'deep-orange', 'indigo', 'deep-purple', 'amber'][index % 10]
        },
        async updateCompleted() {
            await fetch(SERVER+
                "/task_completed/pid="+this.task.pid+
                "&tnumber="+this.task.tnumber+
                "&completed="+(0+this.task.completed)
            )
        }
    },
    mounted() {
        // @ts-ignore
        this.f(this.task.pid, this.task.tnumber)
    }
}
</script>
