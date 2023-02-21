<template>
    <v-container fluid>
        <h1 v-if="userStore.loggedIn">
            Welcome, {{ $route.params.username }}!
        </h1>

        <h2>
            Organise your Research Project
        </h2>

        <p>
            You will need to login to begin accessing your stored citations. If you are already logged in, click on the navigator bar
            at the side to begin.
        </p>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app";
const userStore = useUserStore();
</script>
