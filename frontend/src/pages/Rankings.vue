<script setup>
import { onBeforeMount, ref } from "vue";
import { router } from "@/router";
import { request } from "@/assets/request.js";

const highscores = ref([]);
// TODO show tries from last game

const newGame = () => {
  try {
    sessionStorage.removeItem("gameId");
    router.push("/game");
  } catch (error) {
    console.log(error);
  }
};

onBeforeMount(async () => {
  let response = await request("http://localhost:5000/game/highscore", "GET");
  highscores.value = response.highscores;
});
</script>

<template>
  <div class="displayBox">
    <h1>Highscores</h1>
    <table style="width: 70%; min-width: max-content">
      <thead>
        <tr>
          <th style="width: 15%">Rank</th>
          <th>User</th>
          <th style="width: 25%">Score</th>
        </tr>
      </thead>
      <tbody v-for="(item, index) in highscores.slice(0, 10)">
        <tr>
          <td class="centered">{{ index + 1 }}</td>
          <td class="aligned">{{ item.username }}</td>
          <td class="centered">{{ item.tries }}</td>
        </tr>
      </tbody>
    </table>
    <button id="newGame" type="submit" @click="newGame">Neues Spiel</button>
  </div>
</template>

<style scoped>
table,
th,
td {
  border: 1px solid black;
  border-collapse: collapse;
}

.aligned {
  padding-left: 10px;
  padding-right: 10px;
}

th {
  background-color: rgb(208, 211, 225);
  text-align: center;
}

.centered {
  text-align: center;
}

#newGame {
  width: 70%;
  padding: 10px;
  cursor: pointer;
  margin-top: 15px;
}
</style>
