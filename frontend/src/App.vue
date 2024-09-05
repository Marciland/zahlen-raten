<script setup></script>

<template>
  <div class="app-container">
    <header>
      <h1 class="title">Zahlen Raten</h1>
    </header>

    <main>
      <router-view />
    </main>

    <footer></footer>
  </div>
</template>

<style>
.title {
  display: block;
  text-decoration: underline;
  text-align: center;
  font-size: 50px;
  font-family: t;
  font-weight: 1000;
  margin: 0 auto;
  padding-top: 20px;
  padding-bottom: 20px;
}
.app-container {
  background-image: url("https://cdn.pixabay.com/photo/2023/01/10/03/57/digits-7708860_1280.jpg");
  background-size: cover;
  width: 100vw;
  height: 100vh;
}
</style>
