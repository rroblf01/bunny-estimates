<template>
  <div class="cards-list">
    <h2>Cartas</h2>
    <ul>
      <li
        v-for="(card, index) in cards"
        :key="index"
        @click="$emit('sendVote', card[0])"
        :class="['card', { selected: card[0] === selectedCard }]"
      >
        {{ card[1] }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  cards: Array,
  selectedCard: String,
});
</script>

<style scoped>
.cards-list {
  margin-top: 20px;
}

.cards-list ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.cards-list .card {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  background-color: #f9f9f9;
}

.cards-list .card:hover {
  background-color: #e0e0e0;
}

.cards-list .card.selected {
  background-color: #d3f3d3;
}
</style>
