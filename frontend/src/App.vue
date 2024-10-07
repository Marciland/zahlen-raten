<script setup>
import * as bootstrap from "bootstrap";
import { getPayload } from "@/assets/validation";
import { ref, provide } from "vue";
import { router } from "@/router";

const token = sessionStorage.getItem("token");
const isLoggedIn = ref(false);
const payload = getPayload(token);
isLoggedIn.value = payload.user !== undefined;
const user = ref(payload.user);
provide("isLoggedIn", isLoggedIn);
provide("user", user);

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
        style="min-height: 40px"
      >
        <div class="container-fluid">
          <ul class="navbar-nav ms-auto">
            <li v-if="isLoggedIn" class="nav-item">
              <button
                @click="logout"
                class="nav-link"
                style="cursor: pointer; color: white"
              >
                Logout
              </button>
            </li>
            <li class="nav-item">
              <a class="nav-link" style="cursor: pointer; color: white">{{
                user
              }}</a>
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
