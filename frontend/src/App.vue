<script setup>
import * as bootstrap from "bootstrap";
import { getPayload } from "@/assets/validation";
import { ref, provide } from "vue";
import { router } from "@/router";
import { RouterLink } from "vue-router";

const token = sessionStorage.getItem("token");
const isLoggedIn = ref(false);
const payload = getPayload(token);
const user = ref(payload.user);
const yourTries = ref("");

isLoggedIn.value = payload.user !== undefined;

provide("isLoggedIn", isLoggedIn);
provide("user", user);
provide("yourTries", yourTries);

const logout = () => {
  sessionStorage.removeItem("token");
  sessionStorage.removeItem("gameId");
  const token = sessionStorage.getItem("token");
  const payload = getPayload(token);
  isLoggedIn.value = payload.user !== undefined;
  user.value = "";
  router.push("/");
};
</script>

<template>
  <div class="app-container">
    <header>
      <nav
        class="navbar navbar-expand-sm bg-dark justify-content-end"
        style="min-height: 50px; padding: 0px"
      >
        <div class="container-fluid" v-if="isLoggedIn">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink to="/game" class="nav-link" style="color: white"
                >Spiel</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/highscore" class="nav-link" style="color: white"
                >Highscores</RouterLink
              >
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <button
                @click="logout"
                class="nav-link"
                style="cursor: pointer; color: white"
              >
                Logout
              </button>
            </li>
            <li class="nav-item nav-link" style="cursor: pointer; color: white">
              {{ user }}
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <main>
      <router-view />
    </main>

    <footer></footer>
  </div>
</template>

<style>
@import "@/assets/main.css";
</style>
