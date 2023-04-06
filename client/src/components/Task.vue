<template>
    <v-card
        width="250"
        :color="task.completed ? 'green-lighten-5' : (new Date() < new Date(task.deadline) ? 'orange-lighten-5' : 'red-lighten-5')"
        :title="task.title"
        class="text-wrap"
    >
        <template v-slot:append>
            <v-checkbox
                color="green"
                v-model="task.completed"
                @click="updateCompleted(); $emit('completenessChanged')"
            ></v-checkbox>
        </template>

        <VMarkdownView
            mode="light"
            :content="task.description"
            style="padding:5px; margin:10px; font-family: 'Montserrat'; font-size:13px; background: #E8F5E9"
            v-if="task.completed"
        ></VMarkdownView>

        <VMarkdownView
            mode="light"
            :content="task.description"
            style="padding:5px; margin:10px; font-family: 'Montserrat'; font-size:13px; background: #FFEBEE"
            v-if="!task.completed && new Date() > new Date(task.deadline)"
        ></VMarkdownView>

        <VMarkdownView
            mode="light"
            :content="task.description"
            style="padding:5px; margin:10px; font-family: 'Montserrat'; font-size:13px; background: #FFF3E0"
            v-if="!task.completed && new Date() < new Date(task.deadline)"
        ></VMarkdownView>

        <v-divider></v-divider>
        <v-row class="pa-4">
            <v-chip
                v-for="(item, index) in members"
                v-model="assigned[index]"
                :key="index"
                :value="index"
                :color="colourUid(item.uid)"
                class="ma-2"
                closable
                @click:close="removeAssigned(members[index].uid)"
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
                        v-for="(item, index) in members.map((e,i) => !assigned[i] ? e : undefined).filter(x => x)"
                        :key="index"
                        :value="index"
                    >
                        <v-list-item-title @click="addAssigned(item.uid)">
                            {{ item.firstname }}
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-row>
        <v-divider></v-divider>
        <v-card-actions>
            <v-btn color="red" @click="$emit('delete')">
                Delete
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="$emit('showDialog')">
                Edit
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="js">
import { SERVER } from "@/main"
import { colour } from "@/colour"

import { VMarkdownView } from 'vue3-markdown'
import 'vue3-markdown/dist/style.css'

export default {
    components: { VMarkdownView },
    props: ["task", "members"],
    emits: ["showDialog", "completenessChanged", "delete"],
    data() {
        return {
            assigned: []
        }
    },
    methods: {
        colourUid(uid) {
            return colour(uid)
        },
        async f(pid, tnumber) {
            // @ts-ignore
            let assigned = (await (
                await fetch(SERVER + "/assigned/pid=" + pid + "&tnumber=" + tnumber)
            ).json()).map(x => x.uid)

            this.assigned = []
            for (let i = 0; i < this.members.length; i++) {
                if (assigned.includes(this.members[i].uid)) this.assigned.push(true)
                else this.assigned.push(false)
            }
        },
        async updateCompleted() {
            await fetch(SERVER +
                "/task_completed/pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber +
                "&completed=" + (0 + !this.task.completed)
            )
        },
        async addAssigned(uid) {
            for (let i = 0; i < this.members.length; i++) {
                if (this.members[i].uid === uid) {
                    this.assigned[i] = true
                    break
                }
            }
            await fetch(SERVER +
                "/add_assigned/uid=" + uid +
                "&pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber
            )
        },
        async removeAssigned(uid) {
            for (let i = 0; i < this.members.length; i++) {
                if (this.members[i].uid === uid) {
                    this.assigned[i] = false
                    break
                }
            }
            await fetch(SERVER +
                "/remove_assigned/uid=" + uid +
                "&pid=" + this.task.pid +
                "&tnumber=" + this.task.tnumber
            )
        }
    },
    updated() {
        // @ts-ignore
        this.f(this.task.pid, this.task.tnumber)
    }
}
</script>
