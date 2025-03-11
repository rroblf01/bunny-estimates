<template>
  <div class="room-container">
    <h1 class="room-title">{{ room.name }}</h1>
    <p class="room-status">
      Estado: {{ room.finished ? "Finalizado" : "En progreso" }}
    </p>
    <div class="topics-container">
      <div v-for="topic in room.topics" :key="topic.title" class="topic">
        <h2 class="topic-title">{{ topic.title }}</h2>
        <p class="topic-description">{{ topic.description }}</p>
        <p class="topic-average">Promedio: {{ topic.average }}</p>
        <ul class="votes-list">
          <li v-for="vote in topic.votes" :key="vote.name" class="vote-item">
            {{ vote.name }}: {{ vote.value }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRuntimeConfig } from "#app";

const config = useRuntimeConfig();
const route = useRoute();
const room = ref({});

onMounted(async () => {
  const id = route.params.id;
  const backendUrl = "http://" + config.public.backendUrl;
  const response = await fetch(`${backendUrl}/api/estimates/room/${id}/resume`);
  room.value = await response.json();
});
</script>

<style scoped>
.room-container {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.room-title {
  color: #333;
  font-size: 2em;
  margin-bottom: 10px;
}

.room-status {
  color: #555;
  font-size: 1.2em;
  margin-bottom: 20px;
}

.topics-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.topic {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex: 1 1 calc(33.333% - 20px); /* Ajusta el ancho para que entre 3 por fila */
  box-sizing: border-box;
}

.topic-title {
  color: #007bff;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.topic-description {
  color: #666;
  font-size: 1.1em;
  margin-bottom: 10px;
}

.topic-average {
  color: #28a745;
  font-size: 1.2em;
  margin-bottom: 10px;
}

.votes-list {
  list-style-type: none;
  padding: 0;
}

.vote-item {
  background-color: #f1f1f1;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 5px;
  font-size: 1em;
}
</style>
