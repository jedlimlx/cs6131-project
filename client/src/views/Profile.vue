<template>
    <v-container fill-height>
        <v-card width="500">
            <v-card-title v-if="!editing">{{ userStore.firstname }} {{ userStore.lastname }}</v-card-title>
            <v-row class="pa-6" v-if="editing">
                <v-text-field
                    label="First Name"
                    variant="outlined"
                    color="primary"
                    v-model="userStore.firstname"
                    v-if="editing"
                    class="pr-3"
                ></v-text-field>
                <v-text-field
                    label="Last Name"
                    variant="outlined"
                    color="primary"
                    v-model="userStore.lastname"
                    class="pl-3"
                ></v-text-field>
            </v-row>
            <v-card-subtitle v-if="!editing">{{ userStore.username }}#{{ userStore.uid }}</v-card-subtitle>
            <v-card-text v-if="!editing">Email: {{ userStore.email }}</v-card-text>
            <v-text-field
                label="Email"
                variant="outlined"
                color="primary"
                v-model="userStore.email"
                v-if="editing"
                class="pr-3 pl-3"
            ></v-text-field>
            <v-card-actions>
                <v-btn color="primary" v-if="!editing" @click="editing=!editing">Edit</v-btn>
                <v-btn color="primary" v-if="editing" @click="editing=!editing; updateDatabase()">Save</v-btn>
                <v-btn color="red" v-if="editing" @click="editing=!editing">Cancel</v-btn>
                <v-btn color="primary">Change Password</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app";
import { Ref, ref } from "vue";
import { SERVER } from "@/main";
const userStore = useUserStore();

const editing: Ref<boolean> = ref(false);

const updateDatabase = function() {
    fetch(
        SERVER+
        "/update_user/username="+userStore.username+
        "&firstname="+userStore.firstname+
        "&lastname="+userStore.lastname+
        "&email="+userStore.email
    )
}
</script>
