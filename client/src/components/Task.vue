<template>
    <v-card
        width="250"
        :color="task.completed ? 'green-lighten-5' : (new Date() < new Date(task.deadline) ? 'orange-lighten-5' : 'red-lighten-5')"
    >
        <v-card-title class="text-wrap">{{ task.title }}</v-card-title>
        <v-card-text class="text-wrap">{{ task.description }}</v-card-text>
        <v-card-actions>
            <v-btn color="primary">
                Edit
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
import { SERVER } from "@/main";

export default {
    components: { },
    props: [ "task" ],
    emits: [ ],
    data() {
        return {
        }
    },
    methods: {
    }
}
</script>
