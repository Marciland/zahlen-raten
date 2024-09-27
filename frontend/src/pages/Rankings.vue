<script setup>
const liste = [
  {
    game_id: "2fcd41b2-4e2f-477e-8f78-22cfe786958d",
    tries: 4,
    username: "testuser",
  },
  {
    game_id: "02c17766-b5d9-4be4-b712-3e30c0b6a9df",
    tries: 2,
    username: "testuser",
  },
];
// get data

// https://vuejs.org/guide/essentials/list

// present data using v-for over the list of scores
</script>

<template>
  <div class="displayBox">
    <h1>Highscores</h1>
    <div class="row">
      <div class="col custom-table table-header">Rank</div>
      <div class="col custom-table table-header">User</div>
      <div class="col custom-table table-header">Score</div>
    </div>
    <div v-for="(item, index) in liste">
      <div class="row">
        <div class="col custom-table centered">
          {{ index + 1 }}
        </div>
        <div class="col custom-table">
          {{ item.username }}
        </div>
        <div class="col custom-table centered">
          {{ item.tries }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-table {
  border: 1px solid black;
  border-collapse: collapse;
}

.table-header {
  background-color: rgb(208, 211, 225);
  text-align: center;
}

.centered {
  text-align: center;
}
</style>
