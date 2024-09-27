<script setup>
import { router } from "@/router";
import { request } from "@/assets/request.js";

const submit = async (event) => {
  event.preventDefault();
  const url = "http://localhost:5000/users/" + event.submitter.id;

  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;

  try {
    let response = await request(url, "POST", { username, password });
    // TODO popup with successfully logged in or registered
    sessionStorage.setItem("token", response.token);
    router.push("/game"); // TODO should this push if registred successfully? if so, create a token in backend!
  } catch (error) {
    console.log(error);
    // TODO this is only if the server is unreachable and cannot be caught in handle response!
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
