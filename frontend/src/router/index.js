import { createRouter, createWebHistory } from "vue-router";
import { Login, Game, Rankings } from "@/pages";
import { tokenIsValid } from "@/assets/validation";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Login },
    { path: "/game", component: Game },
    { path: "/highscore", component: Rankings },
  ],
});

router.beforeEach((to, _from) => {
  const privateRoutes = ["/game", "/highscore"];

  if (to.path === "/" && sessionStorage.getItem("token")) {
    router.push("/game");
  }

  if (privateRoutes.includes(to.path)) {
    let token = sessionStorage.getItem("token");
    if (tokenIsValid(token)) {
      return true;
    }

    sessionStorage.removeItem("token");
    router.push("/");
    // TODO alert
  }
});
