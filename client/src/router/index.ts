// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/Default.vue'),
        children: [
            {
                path: '/profile',
                name: 'Profile',
                component: () => import('@/views/Profile.vue'),
            },
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
                path: '/',
                name: 'Home',
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
