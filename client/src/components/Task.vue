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
                @click:close="removeAssigned(item.pid)"
            >
                {{ item.firstname }}
            </v-chip>

            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-chip
                        color="primary"
                        class="ma-2"
                        v-bind="props"
                    >+
                    </v-chip>
                </template>
                <v-list>
                    <v-list-item
                        v-for="(item, index) in members.filter(x => !assigned.map(y => y.uid).includes(x.uid))"
                        :key="index"
                        :value="index"
                    >
                        <v-list-item-title
                            @click="addAssigned(item.uid)"
                        >{{ item.firstname }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-row>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn color="red">
                Delete
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary">
                Edit
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="js">
import {SERVER} from "@/main"
import drs from "deterministic-random-sequence"

export default {
    components: {},
    props: ["task", "members"],
    emits: [],
    data() {
        return {
            assigned: []
        }
    },
    methods: {
        async f(pid, tnumber) {
            // @ts-ignore
            this.assigned = await (await
                    fetch(SERVER + "/assigned/pid=" + pid + "&tnumber=" + tnumber)
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
            await fetch(SERVER +
                "/task_completed/pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber +
                "&completed=" + (0 + !this.task.completed)
            )
        },
        async addAssigned(uid) {
            this.f(this.task.pid, this.task.tnumber)
            await fetch(SERVER +
                "/add_assigned/uid=" + uid +
                "&pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber
            )
        },
        async removeAssigned(uid) {
            this.f(this.task.pid, this.task.tnumber)
            await fetch(SERVER +
                "/remove_assigned/uid=" + uid +
                "&pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber
            )
        }
    },
    created() {
        // @ts-ignore
        this.f(this.task.pid, this.task.tnumber)
    }
}
</script>
