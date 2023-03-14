<template>
    <v-container fill-height>
        <v-row class="pb-10">
            <div class="text-h3 pr-6">References</div>
            <v-btn color="primary" icon="mdi-book-plus" @click="//@ts-ignore
            $refs.refDialog.show = true"></v-btn>
        </v-row>

        <v-text-field
            v-model="searchTerm"
            label="Search"
            prepend-icon="mdi-magnify"
            @change="search(searchTerm)"
        ></v-text-field>

        <v-list
            v-for="item in references"
            :key="//@ts-ignore
                    item.title"
            :title="//@ts-ignore
                    item.title"
            subtitle="..."
        >
            <Reference
                :reference="item"
                :selected="item.selected"
                @toggle="item.selected = !item.selected"
            ></Reference>
        </v-list>

        <v-row justify="center">
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

onMounted(() => {
    return { refDialog }
})

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
}

const search = function (keyword: string) {
    references.value = []
    for (const item of allReferences.value) {
        // @ts-ignore
        if (item.title.toLowerCase().includes(keyword.toLowerCase())) {
            references.value.push(item)
        }
    }

    for (const item of references.value) {
        // @ts-ignore
        item.selected = false
    }
}

onMounted(() => {
    loadReference()
})
</script>
