import { createRouter, createWebHistory } from 'vue-router';
import Course from '../views/Course.vue';
import CourseDetail from '../views/CourseDetail.vue';
import Login from '../views/Login.vue';

const routes = [
  { path: '/', component: Course },
  { path: '/courses/:id', component: CourseDetail, props: true },
  { path: '/login', component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  if (to.path !== '/login' && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;