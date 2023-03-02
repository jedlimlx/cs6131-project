<template>
    <v-card
        :href="'https://doi.org/' + reference.doi"
    >
        <v-card-title>{{ reference.title }}</v-card-title>
        <v-card-subtitle>{{ reference.authors.join(", ") }}</v-card-subtitle>
        <v-card-text v-if="reference.type === 0">Published in {{ reference.pname }} on {{ reference.date }}</v-card-text>
        <v-card-text v-if="reference.type === 1">Published at {{ reference.pname }} {{ reference.year }}</v-card-text>
        <v-card-text v-if="reference.type === 2">ISBN {{ reference.isbn }}</v-card-text>
    </v-card>
</template>

<script lang="ts">
export default {
    props: [ "reference" ]
}
</script>
