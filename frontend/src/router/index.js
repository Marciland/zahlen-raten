import { createRouter, createWebHistory } from "vue-router";
import { Login, Game, Rankings } from "@/pages";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Login },
    { path: "/play", component: Game },
    { path: "/highscore", component: Rankings },
  ],
});
