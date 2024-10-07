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

router.beforeEach(async (to, _from, next) => {
  if (!["/", "/game", "/highscore"].includes(to.path)) {
    return next("/"); // TODO 404 page?
  }
  const privateRoutes = ["/game", "/highscore"];

  if (
    to.path === "/" &&
    (await tokenIsValid(sessionStorage.getItem("token")))
  ) {
    // gehe zu game, wenn user zu login mit gültigem token will
    return next("/game");
  }
  if (privateRoutes.includes(to.path)) {
    // wenn private und nicht gültig, gehe zu index
    let token = sessionStorage.getItem("token");
    if (await tokenIsValid(token)) {
      return next();
    } else {
      sessionStorage.removeItem("token");
      return next("/");
    }
    // TODO alert
  }
  next();
});
