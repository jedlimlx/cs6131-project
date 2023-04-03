<template>
    <v-container class="hero fill-height fill-width align-center" fluid>
        <v-virtual-scroll>
            <v-row class="fill-width" style="margin-top: 50px; margin-bottom:50px">
                <v-col class="fill-width centre" fluid>
                    <div class="text-h2 font-weight-bold text-white" style="margin-left:30px">
                        An Online Logbook for Your Research.
                    </div>

                    <br>

                    <div v-if="userStore.loggedIn" class="text-h3 text-white" style="margin-left:30px">
                        Welcome, {{ userStore.firstname }} {{ userStore.lastname }}!
                    </div>

                    <br>

                    <v-row  style="margin-left:30px">
                        <v-img max-width="30" aspect-ratio="1" src="public/icon.png"></v-img>
                        <div class="text-h5 text-white" style="margin-left:10px">
                            Organised. Collaborative. Productive.
                        </div>
                    </v-row>

                    <br>

                    <v-btn
                        v-if="!userStore.loggedIn"
                        color="primary"
                        style="margin-left:30px"
                        @click="userStore.creatingNewAccount = true"
                    >
                        Get Started
                    </v-btn>
                </v-col>
            </v-row>

            <v-timeline>
                <v-timeline-item class="item">
                    <v-card
                        :width="300"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word text-h1"
                        text="Set deadlines and assign people to do work!"
                        title="Organise tasks"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                    ></v-card>
                </v-timeline-item>

                <v-timeline-item class="item">
                    <v-card
                        :width="300"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word text-h1"
                        text="A central place for everyone to store their experimental logs and keep track of each other's progress"
                        title="Write experimental logs"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                    ></v-card>
                </v-timeline-item>

                <v-timeline-item class="item">
                    <v-card
                        :width="300"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word text-h1"
                        text="Keep track of all your references - the ones you need to read, the ones you have read, etc."
                        title="Keep track of references"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                    ></v-card>
                </v-timeline-item>
            </v-timeline>
        </v-virtual-scroll>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app"
const userStore = useUserStore()
</script>

<style scoped>
.hero {
    background: url('public/picture.jpg') no-repeat center center fixed !important;
    background-size: cover;
}

.item {
    margin: 3000px
}
</style>
