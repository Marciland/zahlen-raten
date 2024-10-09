<script setup>
import { inject } from "vue";
import { router } from "@/router";
import { request } from "@/assets/request.js";

const yourTries = inject("yourTries");

const submit = async (event) => {
  event.preventDefault();
  const guess = document.getElementById("inputGuess").value;
  const gameId = sessionStorage.getItem("gameId");
  const url = "http://localhost:5000/game/guess";

  try {
    let response = await request(url, "POST", { gameId, guess });

    let displayResponseElement = document.getElementById("responseMessage");
    displayResponseElement.style.color = "red";
    displayResponseElement.textContent = response.detail;
    let displayTryCount = document.getElementById("tryCount");
    displayTryCount.textContent = "Anzahl deiner Versuche: " + response.tries;

    if (!sessionStorage.getItem("gameId")) {
      sessionStorage.setItem("gameId", response.gameId);
      return;
    }
    if (!response.active) {
      yourTries.value = response.tries;
      sessionStorage.removeItem("gameId");
      router.push("/highscore");
      return;
    }
  } catch (error) {
    console.log(error);
  }
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
      <p id="responseMessage"></p>
      <p id="tryCount"></p>
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

#responseMessage,
#tryCount {
  text-align: center;
}
</style>
