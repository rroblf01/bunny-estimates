<template>
  <div class="start-round-button">
    <button :disabled="isRoundActive" @click="$emit('startRound')">
      Iniciar Ronda
    </button>
  </div>
</template>

<script setup>
defineProps({
  isRoundActive: Boolean,
});
</script>

<style scoped>
.start-round-button {
  margin-top: 20px;
  text-align: center;
}

.start-round-button button {
  padding: 10px 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  background-color: #ffeb3b;
  font-size: 16px;
}

.start-round-button button:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}
</style>
