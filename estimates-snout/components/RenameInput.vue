<template>
  <div class="rename-input">
    <label for="rename">Cambiar nombre:</label>
    <input
      :value="currentUserName"
      @input="$emit('update:currentUserName', $event.target.value)"
      @keyup.enter="$emit('renameUser')"
      placeholder="Cambiar nombre"
    />
    <button @click="$emit('renameUser')">Cambiar</button>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  currentUserName: String,
});
</script>

<style scoped>
.rename-input {
  margin-top: 10px;
  display: flex;
  gap: 5px;
  width: fit-content;
}

.rename-input input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 150px;
}

.rename-input button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}
</style>
