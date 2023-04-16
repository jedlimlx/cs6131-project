<template>
    <v-card
        @click="$emit('toggle')"
        :color="selected ? 'primary' : 'white'"
    >
        <template v-slot:prepend v-if="reference.type === 3 && reference.icon !== null && isValidURL(reference.icon)">
            <v-avatar rounded="0">
                <v-img :src="reference.icon"></v-img>
            </v-avatar>
        </template>

        <template v-slot:append>
            <v-btn
                icon="mdi-trash-can"
                v-if="canDelete"
                elevation="0"
                color="transparent"
                @click="$emit('delete'); $emit('toggle')"
            ></v-btn>
            <v-btn
                icon="mdi-asdasd"
                v-if="read"
                elevation="0"
                color="transparent"
                @click="$emit('toggleRead'); $emit('toggle')"
            >
                <v-icon
                    :color="reference.read ? (selected ? 'green-lighten-1' : 'green-darken-1'): (selected ? 'white' : 'black')"
                    :icon="reference.read ? 'mdi-book-check' : 'mdi-book'"
                ></v-icon>
            </v-btn>
            <v-btn
                :href="reference.type === 3 ? reference.doi : 'https://doi.org/'+reference.doi"
                target="_blank"
                icon="mdi-link"
                elevation="0"
                color="transparent"
                @click="$emit('toggle')"
            ></v-btn>
        </template>
        <template v-slot:title>
            <v-card-title class="text-wrap">{{ reference.title }}</v-card-title>
        </template>
        <v-card-subtitle>{{ reference.authors.join(", ") }}</v-card-subtitle>
        <v-card-subtitle v-if="reference.type === 3">{{ reference.doi }}</v-card-subtitle>
        <v-card-text v-if="reference.type === 0">Published in {{ reference.pname }} on {{ new Date(Date.parse(reference.date)).toLocaleString() }}</v-card-text>
        <v-card-text v-if="reference.type === 1">Published at {{ reference.pname }} {{ reference.year }}</v-card-text>
        <v-card-text v-if="reference.type === 2">ISBN {{ reference.isbn }}</v-card-text>
        <v-card-text v-if="reference.type === 3">Accessed on {{ new Date(Date.parse(reference.dateAccessed)).toLocaleString() }}</v-card-text>
    </v-card>
</template>

<script lang="ts">
export default {
    props: [ "reference", "selected", "read", "canDelete", "titlesize" ],
    emits: [ "toggle", "toggleRead", "delete" ],
    methods: {
        isValidURL(urlString: string): boolean {
            try {
                return Boolean(new URL(urlString))
            }  catch(e) {
                return false
            }
        }
    }
}
</script>
