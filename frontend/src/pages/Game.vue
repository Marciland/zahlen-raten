<script setup>
import { router } from "@/router";

const submit = async (event) => {
  event.preventDefault();
  const guess = document.getElementById("inputGuess").value;
  const gameId = sessionStorage.getItem("gameId");
  const token = sessionStorage.getItem("token");

  const requestOptions = {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    signal: AbortSignal.timeout(2000),
    body: JSON.stringify({ gameId, guess }),
  };

  try {
    const response = await fetch("http://localhost:5000/guess", requestOptions);

    if (response.ok) {
      let json = await response.json();
      alert(json.detail);
      if (!sessionStorage.getItem("gameId")) {
        sessionStorage.setItem("gameId", json.gameId);
      }
      // TODO wenn game finished, lösche game id aus session storage
    } else {
      if (response.status === 401) {
        sessionStorage.removeItem("token");
        router.push("/");
        return;
      }
    }
  } catch (error) {
    console.log(error);
    alert("Error");
  }

  // TODO if not game id in session storage then save game id in session storage from header
  // ToDo: Alerts ersetzen wegen schelchter screen reader Kompatibilität
};
</script>

<template>
  <div class="displayBox">
    <h1 class="title">Zahlen Raten</h1>
    <form class="gameForm" :onSubmit="submit" method="post">
      <label for="Eingabefeld">Zahl von 0 - 100</label>
      <input
        type="number"
        id="inputGuess"
        name="Eingabefeld"
        pattern="[0-9]*"
        inputmode="numeric"
        min="0"
        max="100"
        required
      />
      <button id="guess" type="submit">RATEN!</button>
    </form>
  </div>
</template>

<style scoped>
.gameForm {
  display: flex;
  flex-direction: column;
}

.gameForm input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

.gameForm button {
  width: 100%;
  padding: 10px;
  cursor: pointer;
  margin-bottom: 15px;
}
</style>
