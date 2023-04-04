<template>
    <v-container fill-height>
        <v-row class="pb-10 pt-10">
            <div class="text-h3 pr-6">References</div>
            <v-btn color="primary" icon="mdi-book-plus" @click="//@ts-ignore
            $refs.refDialog.show = true"></v-btn>
        </v-row>

        <v-text-field
            v-model="searchTerm"
            label="Search"
            prepend-icon="mdi-magnify"
            @change="search()"
        ></v-text-field>

        <v-row rows="12">
            <v-autocomplete
                v-model="journalFilter"
                :items="journals"
                chips
                closable-chips
                color="primary"
                item-title="pname"
                item-value="pname"
                label="Journal"
                multiple
                class="pa-5"
                style="width: 300px"
                :readonly="!useJournals"
                @update:modelValue="search()"
            >
                <template v-slot:append>
                    <v-slide-x-reverse-transition mode="out-in">
                        <v-icon
                            :key="`icon-${useJournals}`"
                            :color="useJournals ? 'green-darken-3' : 'gray'"
                            :icon="useJournals ? 'mdi-filter-check' : 'mdi-filter-off'"
                            @click="useJournals = !useJournals; search()"
                        ></v-icon>
                    </v-slide-x-reverse-transition>
                </template>

                <template v-slot:chip="{ props, item }">
                    <v-chip
                        v-bind="props"
                        :text="item.raw.pname"
                    ></v-chip>
                </template>

                <template v-slot:item="{ props, item }">
                    <v-list-item
                        v-bind="props"
                        :title="item.raw.pname"
                        :subtitle="item.raw.website"
                    ></v-list-item>
                </template>
            </v-autocomplete>

            <v-autocomplete
                :items="['Read', 'Not Read']"
                v-model="readFilter"
                chips
                closable-chips
                color="primary"
                item-title="pname"
                item-value="pname"
                label="Read"
                multiple
                class="pa-5"
                style="width: 300px"
                :readonly="!useReadFilter"
                @update:modelValue="search()"
            >
                <template v-slot:append>
                    <v-slide-x-reverse-transition mode="out-in">
                        <v-icon
                            :key="`icon-${useReadFilter}`"
                            :color="useReadFilter ? 'green-darken-3' : 'gray'"
                            :icon="useReadFilter ? 'mdi-filter-check' : 'mdi-filter-off'"
                            @click="useReadFilter = !useReadFilter; search()"
                        ></v-icon>
                    </v-slide-x-reverse-transition>
                </template>

                <template v-slot:chip="{ props, item }">
                    <v-chip
                        v-bind="props"
                        :prepend-icon="item.raw === 'Read' ? 'mdi-book-check' : 'mdi-book'"
                        :color="item.raw === 'Read' ? 'green' : 'red'"
                        :text="item.raw"
                    ></v-chip>
                </template>

                <template v-slot:item="{ props, item }">
                    <v-list-item
                        v-bind="props"
                        :prepend-icon="item.raw === 'Read' ? 'mdi-book-check' : 'mdi-book'"
                        :color="item.raw === 'Read' ? 'green' : 'red'"
                        :title="item.raw"
                    ></v-list-item>
                </template>
            </v-autocomplete>
        </v-row>

        <v-list
            v-for="item in references"
            :key="//@ts-ignore
                    item.title"
            :title="//@ts-ignore
                    item.title"
            subtitle="..."
        >
            <Reference
                :read="true"
                :can-delete="true"
                :reference="item"
                :selected="item.selected"
                @toggleRead="item.read = !item.read; toggleRead(item)"
                @toggle="item.selected = !item.selected"
                @delete="deleteReference(item)"
            ></Reference>
        </v-list>

        <v-row justify="center" class="pb-10">
            <v-dialog
                v-model="errorDialog"
                persistent
                max-width="290"
            >
                <v-card>
                    <v-card-title class="text-h5">
                        Error
                    </v-card-title>
                    <v-card-text>
                        {{ error }}
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="errorDialog = false">
                            Ok
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>

        <ReferenceDialog
            ref="refDialog"
            @addReference="addReference"
        ></ReferenceDialog>
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app";
import { defineComponent, onMounted, ref, Ref } from "vue";
import { SERVER } from "@/main";
import Reference from "@/components/Reference.vue";
import ReferenceDialog from "@/components/ReferenceDialog.vue";

defineComponent({
    components: { Reference, ReferenceDialog }
})

const userStore = useUserStore()

const searchTerm: Ref<string> = ref("")

const allReferences: Ref<Array<object>> = ref([])
const references: Ref<Array<object>> = ref([])

const refDialog = ref(null)
const errorDialog = ref(false)
const error = ref("")

const journals = ref([])

const useJournals = ref(false)
const useReadFilter = ref(false)

const journalFilter = ref([])
const readFilter = ref([])


const loadReference = async function () {
    let data = await (await fetch(SERVER + "/references/uid=" + userStore.uid)).json()
    allReferences.value = data
    references.value = JSON.parse(JSON.stringify(data))

    for (const item of references.value) {
        // @ts-ignore
        item.selected = false
    }
}

const addReference = async function() {
    // @ts-ignore
    let data = await (await fetch(SERVER + "/add_reference/doi=\""+refDialog.value.doi.replace("/", "$2F")+
        "\"&uid="+userStore.uid+"&read=0")).json()
    if (data.status == 0) {
        error.value = data.error
        errorDialog.value = true
    }

    // Reload the references
    await loadReference()
}

const search = function() {
    references.value = []
    for (const item of allReferences.value) {
        // @ts-ignore
        if (
            item.title.toLowerCase().includes(searchTerm.value.toLowerCase()) &&
            (!useJournals.value || journalFilter.value.includes(item.pname)) &&
            (!useReadFilter || readFilter.value.includes(item.read ? "Read" : "Not Read"))
        ) {
            references.value.push(item)
        }
    }

    for (const item of references.value) {
        // @ts-ignore
        item.selected = false
    }
}

const toggleRead = function(item: object) {
    //@ts-ignore
    fetch(SERVER + "/update_read/doi=\""+item.doi.replace("/", "$2F")+"&uid="+userStore.uid+"&read="+(0+item.read))
}

const deleteReference = function(item: object) {
    //@ts-ignore
    fetch(SERVER + "/delete_reference/doi=\""+item.doi.replace("/", "$2F")+"&uid="+userStore.uid)
    references.value = references.value.filter(i => i !== item)
}

const getJournals = async function() {
    journals.value = await (await fetch(SERVER + "/publishers")).json()
}

onMounted(() => {
    loadReference()
    getJournals()
    return { refDialog }
})
</script>
