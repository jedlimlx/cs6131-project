// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/Default.vue'),
        children: [
            {
                path: '/projects',
                name: 'Projects',
                component: () => import('@/views/Project.vue'),
            },
            {
                path: '/feedback',
                name: 'Feedback',
                component: () => import('@/views/Feedback.vue'),
            },
            {
                path: '/:username',
                name: 'Home',
                component: () => import('@/views/Home.vue'),
            },
            {
                path: '/',
                name: 'Not the same',
                component: () => import('@/views/Home.vue'),
            }
        ],
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
