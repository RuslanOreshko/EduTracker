import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/loginView.vue";
import DashboardView from "../views/DashboardView.vue";
import AppLayout from "../layouts/AppLayout.vue";

import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/login",
    component: LoginView,
  },
  {
    path: "/",
    component: AppLayout,
    children: [
      { path: "", redirect: "/dashboard" },
      { path: "dashboard", component: DashboardView },
      {
        path: "stats/average-lessons",
        component: () => import("../views/stats/AverageLessonsView.vue"),
      },
      {
        path: "stats/peak-load",
        component: () => import("../views/stats/PeakLoadView.vue"),
      },
      {
        path: "stats/compare",
        component: () => import("../views/stats/CompareTeachersView.vue"),
      },
      {
        path: "stats/teachers",
        component: () => import("../views/stats/TeachersStatsView.vue"),
      },
      {
        path: "stats/top-teachers",
        component: () => import("../views/stats/TopTeachersView.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (!auth.isReady) {
    await auth.init();
  }

  const isPublic = to.path === "/login";
  if (!isPublic && !auth.isAuthenticated) {
    return "/login";
  }

  if (isPublic && auth.isAuthenticated) {
    return "/dashboard";
  }
});

export default router;
