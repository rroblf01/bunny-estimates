<template>
  <div class="participants-list">
    <h2>Participantes</h2>
    <ul>
      <li
        v-for="participant in participants"
        :key="participant.user_id"
        :class="{ self: participant.isSelf, leader: participant.isLeader }"
      >
        <strong>{{ participant.name }}</strong>
        <p>Voto: {{ participant.vote }}</p>
        <button
          v-if="isCurrentUserLeader && !participant.isSelf"
          @click="$emit('assignLeader', participant.user_id)"
        >
          Hacer Líder
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  participants: Array,
  isCurrentUserLeader: Boolean,
});
</script>

<style scoped>
.participants-list {
  margin-top: 20px;
  max-width: 60vw;
  overflow-x: auto;
  white-space: nowrap;
}

.participants-list ul {
  list-style-type: none;
  padding: 0;
  display: flex;
}

.participants-list li {
  max-width: 15vw;
  min-width: 15vw;
  max-height: 20vh;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  text-align: center;
  position: relative;
}

.participants-list li.self {
  background-color: #d3f3d3;
}

.participants-list li.leader::after {
  content: "Líder";
  position: absolute;
  top: -15px;
  right: 0;
  background-color: #ffeb3b;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 12px;
}

.participants-list li button {
  margin-top: 5px;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}
</style>
