<script setup>
const submit = async (event) => {
  event.preventDefault();
  console.log(event);
  try {
    const response = fetch("http://localhost:5000/");
    // ToDo: Route definieren

    if (response.ok) {
      alert("Success! You guessed the correct number!");
    } else {
      alert("Failure! Try again!");
    }
  } catch {
    alert("Error");
  }
};
</script>

<template>
  <div class="displayBox">
    <h1 class="title">Zahlen Raten</h1>
    <form class="gameForm" :onSubmit="submit" method="post">
      <label for="Eingabefeld">Zahl von 1 - 100</label>
      <input
        type="number"
        id="inputGuess"
        name="Eingabefeld"
        pattern="[0-9]*"
        inputmode="numeric"
        min="1"
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
