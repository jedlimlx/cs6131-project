<template>
    <v-card
        @click="$emit('toggle')"
        :color="selected ? 'primary' : 'white'"
        :title="reference.title"
    >
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
                :href="'https://doi.org/'+reference.doi"
                icon="mdi-link"
                elevation="0"
                color="transparent"
                @click="$emit('toggle')"
            ></v-btn>
        </template>
        <v-card-subtitle>{{ reference.authors.join(", ") }}</v-card-subtitle>
        <v-card-text v-if="reference.type === 0">Published in {{ reference.pname }} on {{ reference.date }}</v-card-text>
        <v-card-text v-if="reference.type === 1">Published at {{ reference.pname }} {{ reference.year }}</v-card-text>
        <v-card-text v-if="reference.type === 2">ISBN {{ reference.isbn }}</v-card-text>
    </v-card>
</template>

<script lang="ts">
export default {
    props: [ "reference", "selected", "read", "canDelete" ],
    emits: [ "toggle" ]
}
</script>
