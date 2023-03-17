<template>
<v-row justify="center">
    <v-dialog
        v-model="show"
        max-width="800"
        persistent
    >
        <v-card class="ma-5">
            <v-card-title class="text-h5">
                Add Reference
            </v-card-title>

            <v-virtual-scroll>
                <v-tabs
                    v-model="tab"
                    align-tabs="center"
                    color="primary"
                >
                    <v-tab value="one">DOI / Link</v-tab>
                    <v-tab value="two">Search</v-tab>
                </v-tabs>

                <v-window v-model="tab">
                    <v-window-item value="one">
                        <v-card-text>Supports ArXiv, Nature and AIP Journals</v-card-text>

                        <v-text-field
                            v-model="doi"
                            class="pa-5"
                            color="primary"
                            label="Enter DOI / Link"
                            prepend-icon="mdi-link"
                            variant="outlined"
                        ></v-text-field>
                    </v-window-item>

                    <v-window-item value="two">
                        <v-text-field
                            v-model="keyword"
                            class="pa-5"
                            color="primary"
                            label="Search our database"
                            prepend-icon="mdi-magnify"
                            variant="outlined"
                            @change="references = f(keyword)"
                        ></v-text-field>

                        <v-list
                            v-for="item in references"
                            :key="item.title"
                            :title="item.title"
                            class="pr-5 pl-5"
                        >
                            <Reference
                                :reference="item"
                                :selected="item.selected"
                                :canDelete="false"
                                :read="false"
                                @toggle="item.selected = !item.selected"
                                class="pa-2"
                            ></Reference>
                        </v-list>
                    </v-window-item>
                </v-window>
            </v-virtual-scroll>

            <v-card-actions>
                <v-btn color="red" text @click="show = false">
                    Cancel
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="show = false; addReference()">
                    Add
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</v-row>
</template>

<script lang="js">
import { SERVER } from "@/main";
import Reference from "@/components/Reference.vue";

export default {
    components: { Reference },
    props: [ ],
    emits: [ "addReference" ],
    data() {
        return {
            show: false,
            tab: "",
            doi: "",
            keyword: "",
            references: []
        }
    },
    methods: {
        async f(keyword) {
            this.references = await (await fetch(SERVER + "/search_reference/q=" + keyword)).json()
            for (const item of this.references) {
                item.selected = false
            }
        },
        addReference() {
            if (this.tab === "one") {
                this.$emit("addReference")
            } else {
                for (const item of this.references) {
                    if (item.selected) {
                        this.doi = item.doi
                        this.$emit("addReference")
                    }
                }

                this.doi = ""
            }
        }
    }
}


</script>

<style scoped>

</style>
