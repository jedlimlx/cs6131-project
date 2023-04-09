<template>
    <v-container class="hero fill-height fill-width align-center" fluid>
        <v-col justify="center">
            <v-row class="fill-width" style="margin-top: 50px; margin-bottom:50px" align-content="start">
                <v-col class="fill-width centre" fluid>
                    <div class="text-h2 font-weight-bold text-white" style="margin-left:30px">
                        An Online Logbook for Your Research.
                    </div>

                    <br>

                    <div v-if="userStore.loggedIn" class="text-h3 text-white" style="margin-left:30px">
                        Welcome, {{ userStore.firstname }} {{ userStore.lastname }}!
                    </div>

                    <br>

                    <v-row style="margin-left:30px">
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

            <v-row align-content="center" justify="center" style="background: none">
                <v-tooltip
                    origin="top center"
                    location="top center"
                    style="color: transparent!important"
                    v-model="tooltipShow"
                    no-click-animation
                    scrim="transparent"
                    disable-hover
                    @update:modelValue="tooltipShow=true"
                >
                    <template v-slot:activator="{ props }">
                        <v-btn
                            color="transparent"
                            style="background: none"
                            v-bind="props" elevation="0"
                            class="mb-10 align-center justify-center"
                        ></v-btn>
                    </template>

                    <template v-slot:default>
                        <v-card
                            variant="outlined"
                            class="rounded-pill text-white align-center justify-center mt-15"
                            style="border-width:2px; pointer-events: initial;"
                            width="500px"
                            @click="tooltipShow=true"
                        >
                            <v-tabs
                                v-model="tabValue"
                                color="secondary"
                                align-tabs="center"
                                class="text-white"
                                style="backdrop-filter: blur(10px); background:none"
                            >
                                <v-tab :value="1" @click="scroll('cite')">Cite</v-tab>
                                <v-tab :value="2" @click="scroll('delegate')">Delegate</v-tab>
                                <v-tab :value="3" @click="scroll('log')">Log</v-tab>
                                <v-tab :value="4" @click="scroll('deadlines')">Deadlines</v-tab>
                            </v-tabs>
                        </v-card>
                    </template>
                </v-tooltip>
            </v-row>

            <v-timeline>
                <v-timeline-item class="item">
                    <v-card
                        :width="400"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word mx-auto"
                        text="Keep track of all your references - the ones you need to read, the ones you have read, etc."
                        title="Keep track of references"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                        prepend-icon="mdi-bookshelf"
                        id="cite"
                        @scroll="tabValue=1"
                    >
                        <template v-slot:prepend>
                            <v-icon color="white" size="25"></v-icon>
                        </template>
                    </v-card>
                </v-timeline-item>

                <v-timeline-item class="item">
                    <v-card
                        :width="400"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word mx-auto"
                        text="Set deadlines and assign people to do work!"
                        title="Organise tasks"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                        prepend-icon="mdi-clipboard-list"
                        id="delegate"
                        @scroll="tabValue=2"
                    >
                        <template v-slot:prepend>
                            <v-icon color="white" size="25"></v-icon>
                        </template>
                    </v-card>
                </v-timeline-item>

                <v-timeline-item class="item">
                    <v-card
                        :width="400"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word mx-auto"
                        text="A central place for everyone to store their experimental logs and keep track of each other's progress"
                        title="Write experimental logs"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                        prepend-icon="mdi-beaker"
                        id="log"
                        @scroll="tabValue=3"
                    >
                        <template v-slot:prepend>
                            <v-icon color="white" size="25"></v-icon>
                        </template>
                    </v-card>
                </v-timeline-item>

                <v-timeline-item class="item">
                    <v-card
                        :width="400"
                        height="170"
                        class="text-white spacing-playground pa-5 ma-5 word-break: break-word mx-auto"
                        text="Keep track of your deadlines so you can plan your time wisely and finish your work on time"
                        title="Keep track of deadlines"
                        style="backdrop-filter: blur(10px); background: none"
                        variant="outlined"
                        prepend-icon="mdi-calendar-alert"
                        id="deadlines"
                        @scroll="tabValue=4"
                    >
                        <template v-slot:prepend>
                            <v-icon color="white" size="25"></v-icon>
                        </template>
                    </v-card>
                </v-timeline-item>
            </v-timeline>
        </v-col>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app"
import { Ref, ref } from "vue";
const userStore = useUserStore()

const tooltipShow: Ref = ref(true)

const tabValue: Ref = ref(0)

const scroll = function(id: string) {
    //@ts-ignore
    document.getElementById(id).scrollIntoView({
        behavior: 'smooth'
    })
}
</script>

<style scoped lang="scss">
.hero {
    background: url('public/picture.jpg') no-repeat center center fixed !important;
    background-size: cover;
}

.item {
    margin: 3000px
}
</style>
