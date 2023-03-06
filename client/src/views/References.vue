<template>
    <v-container fill-height>
        <v-row class="pb-10">
            <div class="text-h3 pr-6">References</div>
            <v-btn color="primary" icon="mdi-book-plus" @click="addingReference = true"></v-btn>
        </v-row>

        <v-text-field
            v-model="searchTerm"
            label="Search"
            prepend-icon="mdi-magnify"
            @change="search(searchTerm)"
        ></v-text-field>

        <v-list
            v-for="item in references"
            :key="item.title"
            :title="item.title"
            subtitle="..."
        >
            <Reference :reference="item"></Reference>
        </v-list>

        <v-row justify="center">
            <v-dialog
                v-model="addingReference"
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
                                    v-model="keyword2"
                                    class="pa-5"
                                    color="primary"
                                    label="Search our database"
                                    prepend-icon="mdi-magnify"
                                    variant="outlined"
                                    @change="searchServer(keyword2)"
                                ></v-text-field>

                                <v-list
                                    v-for="item in references2"
                                    :key="item.title"
                                    :title="item.title"
                                    class="pr-5 pl-5"
                                >
                                    <Reference :reference="item" class="pa-2"></Reference>
                                </v-list>
                            </v-window-item>
                        </v-window>
                    </v-virtual-scroll>

                    <v-card-actions>
                        <v-btn color="red" text @click="addingReference = false">
                            Cancel
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="addingReference = false">
                            Add
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app";
import { defineComponent, onMounted, ref, Ref } from "vue";
import { SERVER } from "@/main";
import Reference from "@/components/Reference.vue";

defineComponent({
    components: {Reference}
})

const userStore = useUserStore()

const tab: Ref<number> = ref(1)

const searchTerm: Ref<string> = ref("")

const allReferences: Ref<Array<object>> = ref([])
const references: Ref<Array<object>> = ref([])
const references2: Ref<Array<object>> = ref([])

const addingReference: Ref<boolean> = ref(false)

const doi: Ref<string> = ref("")
const keyword2: Ref<string> = ref("")

const loadReference = async function () {
    let data = await (await fetch(SERVER + "/references/uid=" + userStore.uid)).json()
    allReferences.value = data
    references.value = JSON.parse(JSON.stringify(data))
}

const search = function (keyword: string) {
    references.value = []
    for (const item of allReferences.value) {
        if (item.title.toLowerCase().includes(keyword.toLowerCase())) {
            references.value.push(item)
        }
    }
}

const searchServer = async function (keyword: string) {
    references2.value = await (await fetch(SERVER + "/search_reference/q=" + keyword)).json()
}


onMounted(() => {
    loadReference()
})
</script>
