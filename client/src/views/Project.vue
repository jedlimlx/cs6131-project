<template>
    <v-container fluid>
        <v-menu>
            <template v-slot:activator="{ props }">
                <v-btn
                    color="primary"
                    dark
                    v-bind="props"
                >
                    {{ items[selectedItem].text }}
                </v-btn>
            </template>

            <v-list>
                <v-list-item
                    v-for="(item, index) in items"
                    :key="selectedItem"
                    active-color="primary"
                >
                    <template v-slot:prepend>
                        <v-icon :icon="item.icon"></v-icon>
                    </template>
                    <v-list-item-title @click="selectedItem=index">{{ item.text }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
        <v-list>
            <v-list-subheader>REFERENCES</v-list-subheader>

            <v-text-field
                label="Search"
                prepend-icon="mdi-magnify"
            ></v-text-field>

            <v-list-item
                v-for="(ref, index) in items[selectedItem].references"
                :key="selectedRef"
                :value="ref"
                active-color="primary"
                rounded
            >
            <v-list-item-title v-text="ref" @click="selectedRef=index"></v-list-item-title>
            </v-list-item>
        </v-list>
    </v-container>
</template>

<script lang="ts" setup>
import { ref, Ref } from 'vue'

const selectedItem: Ref = ref(0)
const selectedRef: Ref = ref(0)
const items: Ref = ref([
    {
        text: 'Attention Is All You Need',
        icon: 'mdi-human-male-board',
        references: [
            "Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural " +
            "Information Processing Systems, (NIPS), 2016.",
            "Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv " +
            "preprint arXiv:1608.05859, 2016."
        ]
    },
    {
        text: 'An Image Is Worth 16x16 Words',
        icon: 'mdi-tooltip-image',
        references: [
            "Lucas Beyer, Olivier J. Henaff, Alexander Kolesnikov, Xiaohua Zhai, and A ´ aron van den Oord. " +
            "Are we done with imagenet? arXiv, 2020",
            "Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep " +
            "bidirectional transformers for language understanding. In NAACL, 2019.",
            "Han Hu, Zheng Zhang, Zhenda Xie, and Stephen Lin. Local relation networks for image recognition. " +
            "In ICCV, 2019."
        ]
    },
    {
        text: 'DeiT III: Revenge of the ViT',
        icon: 'mdi-emoticon-angry',
        references: [
            "El-Nouby, A., Izacard, G., Touvron, H., Laptev, I., Jegou, H., Grave, E.: Are large-scale datasets necessary for self-supervised pre-training? arXiv preprint arXiv:2112.10740 (2021)",
            "Huang, G., Sun, Y., Liu, Z., Sedra, D., Weinberger, K.Q.: Deep networks with stochastic depth. In: European Conference on Computer Vision (2016)"
        ]
    },
])
</script>
