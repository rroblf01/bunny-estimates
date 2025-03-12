<template>
  <div class="room-content">
    <div class="topic-section">
      <h2>Tema Actual</h2>
      <div v-if="actualTopic" class="actual-topic">
        <h3>{{ actualTopic.title }}</h3>
        <p>{{ actualTopic.description }}</p>
      </div>
    </div>
    <div class="topics-list">
      <h2>Lista de Temas</h2>
      <ul>
        <li
          v-for="topic in topics"
          :key="topic.id"
          :class="{
            'active-topic': actualTopic && topic.id === actualTopic.id,
          }"
        >
          {{ topic.title }}
          <p v-if="topic.average">
            Promedio:
            {{ topic.average }}
          </p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  topics: Array,
  actualTopic: Object,
});
</script>

<style scoped>
.room-content {
  display: flex;
  justify-content: space-between;
}

.topic-section,
.topics-list {
  width: 48%;
}

.actual-topic {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}

.topics-list ul {
  list-style-type: none;
  padding: 0;
}

.topics-list li {
  padding: 8px;
  border: 1px solid #ccc;
  margin-bottom: 5px;
  border-radius: 4px;
}

.topics-list li.active-topic {
  background-color: #f0f0f0;
}
</style>
