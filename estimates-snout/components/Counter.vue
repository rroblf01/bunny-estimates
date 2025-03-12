<template>
  <div class="counter">
    <p>Tiempo restante: {{ counter }} segundos</p>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  counter: Number,
});
</script>

<style scoped>
.counter {
  margin-top: 20px;
  text-align: center;
  font-size: 18px;
  color: #333;
}
</style>
