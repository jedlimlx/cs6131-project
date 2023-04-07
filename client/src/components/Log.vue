<template>
    <v-card
        width="250"
        :title="log.title"
    >
        <v-card-subtitle>
            {{ log.date }}
        </v-card-subtitle>

        <v-card-text>
            {{ log.text }}
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
            <v-btn>Edit</v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
import { SERVER } from "@/main";

export default {
    components: { },
    props: [ "log" ],
    emits: [ ],
    data() {
        return {
        }
    },
    methods: {
    }
}
</script>
