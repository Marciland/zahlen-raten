<script setup>
import { router } from "@/router";
import { request } from "@/assets/request.js";
import { inject } from "vue";
import { getPayload } from "@/assets/validation";

const isLoggedIn = inject("isLoggedIn");
const user = inject("user");

const submit = async (event) => {
  event.preventDefault();
  const url = "http://localhost:5000/users/" + event.submitter.id;

  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;

  try {
    let response = await request(url, "POST", { username, password });
    var alertBox = document.getElementById("customAlert");
    alertBox.style.display = "block";
    setTimeout(function () {
      alertBox.style.display = "none";
    }, 5000);
    sessionStorage.setItem("token", response.token);

    const payload = getPayload(response.token);
    isLoggedIn.value = payload.user !== undefined;
    user.value = payload.user;
    router.push("/game");
  } catch (error) {
    console.log(error);
  }
};
</script>

<template>
  <div class="displayBox">
    <h1 class="title">Zahlen Raten</h1>
    <form class="loginForm" :onSubmit="submit" method="post">
      <input id="userName" type="text" placeholder="Username" />
      <input id="password" type="password" placeholder="Password" />
      <button id="login" type="submit">Login</button>
      <button id="register" type="submit">Register</button>
    </form>
    <div id="customAlert">Registrierung war erfolgreich!</div>
  </div>
</template>

<style scoped>
.loginForm {
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.loginForm input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

.loginForm button {
  width: 100%;
  padding: 10px;
  cursor: pointer;
  margin-bottom: 15px;
}
</style>
