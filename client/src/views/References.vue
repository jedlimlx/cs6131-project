<template>
    <v-container fill-height>
        <v-row class="pb-10">
            <div class="text-h3 pr-6">References</div>
            <v-btn color="primary" icon="mdi-book-plus"></v-btn>
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
    </v-container>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/store/app";
import { defineComponent, onMounted, ref, Ref } from "vue";
import { SERVER } from "@/main";
import Reference from "@/components/Reference.vue";

defineComponent({
    components: { Reference }
})

const userStore = useUserStore()

const searchTerm: Ref<string> = ref("")

const allReferences: Ref<Array<object>> = ref([])
const references: Ref<Array<object>> = ref([])

const loadReference = async function() {
    let data = await (await fetch(SERVER + "/references/uid=" + userStore.uid)).json()
    allReferences.value = data
    references.value = JSON.parse(JSON.stringify(data))
}

const search = function(keyword: string) {
    references.value = []
    for (const item of allReferences.value) {
        if (item.title.toLowerCase().includes(keyword.toLowerCase())) {
            references.value.push(item)
        }
    }
}

onMounted(() => {
    loadReference()
})
</script>
