<script setup>
import { router } from "@/router";

const submit = async (event) => {
  event.preventDefault();
  const url = "http://localhost:5000/" + event.submitter.id;
  let token;

  const username = document.getElementById("userName").value;
  const password = document.getElementById("password").value;
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    signal: AbortSignal.timeout(2000),
    body: JSON.stringify({ username, password }),
  };
  // TODO handle errors properly
  try {
    const response = await fetch(url, requestOptions);
    if (response.status != 200) {
      console.log(response.status);
      return;
    }
    const body = await response.json();
    token = body.token;
  } catch (error) {
    console.log(error);
    return;
  }
  // TODO popup with successfully logged in or registered
  sessionStorage.setItem("token", token);
  router.push("/game");
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
