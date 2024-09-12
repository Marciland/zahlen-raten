<script setup>
import * as bootstrap from "bootstrap";
</script>

<template>
  <div class="app-container">
    <header>
      <nav class="navbar bg-dark">
        <div class="container-fluid">
          <a class="nav-link ms-auto" style="cursor: pointer; color: white"
            >Profile</a
          >
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
