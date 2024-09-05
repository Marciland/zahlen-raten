<script setup>
import { ref } from "vue";

const isLoggedIn = ref(false);

const login = async (event) => {
  event.preventDefault();
  const url = "http://localhost:5000/login";
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
  sessionStorage.setItem("token", token);
  isLoggedIn.value = true;
};
</script>

<template>
  <div v-if="!isLoggedIn" class="login">
    <form class="loginForm" :onSubmit="login" method="post">
      <input id="userName" type="text" placeholder="Username" />
      <input id="password" type="password" placeholder="Password" />
      <button id="submit" type="submit">Login</button>
      <button id="submit" type="submit">Register</button>
    </form>
  </div>
  <div v-else>Übersicht für eingeloggte hier</div>
</template>

<style>
.login {
  background-color: white;
  outline: auto;
  width: 50%;
  margin-left: auto;
  margin-right: auto;
  padding: 40px 0;
  min-height: 50vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loginForm {
  width: 90%;
  max-width: 400px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

form button {
  width: 100%;
  padding: 10px;
  cursor: pointer;
}
</style>
