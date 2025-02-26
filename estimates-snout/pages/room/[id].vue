<template>
  <div class="room-container">
    <h1 class="room-name">{{ roomName }}</h1>
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
            :class="{ 'active-topic': topic.id === actualTopic.id }"
          >
            {{ topic.title }}
          </li>
        </ul>
      </div>
    </div>
    <div class="participants-list">
      <h2>Participantes</h2>
      <ul>
        <li
          v-for="(participant, index) in participants"
          :key="index"
          :class="{ self: participant.isSelf }"
        >
          <strong>{{ participant.name }}</strong
          >: {{ participant.vote }}
        </li>
      </ul>
    </div>
    <div class="cards-list">
      <h2>Cartas</h2>
      <ul>
        <li
          v-for="(card, index) in cards"
          :key="index"
          @click="sendVote(card[0])"
          class="card"
        >
          {{ card[1] }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRuntimeConfig } from "#app";
import { useRoute } from "vue-router";

const config = useRuntimeConfig();
const route = useRoute();
const socket = ref(null);
const roomName = ref("");
const topics = ref([]);
const actualTopic = ref(null);
const participants = ref([]);
const userId = ref(null);

const cards = [
  ["0", "0"],
  ["1", "1"],
  ["2", "2"],
  ["3", "3"],
  ["5", "5"],
  ["8", "8"],
  ["13", "13"],
  ["21", "21"],
  ["34", "34"],
  ["55", "55"],
  ["89", "89"],
  ["?", "?"],
  ["Cafe", "Cafe"],
];

onMounted(() => {
  socket.value = new WebSocket(
    `ws://${config.public.backendUrl}/ws/room/${route.params.id}/`
  );

  socket.value.onopen = () => {
    socket.value.send(JSON.stringify({ action: "get_topics" }));
    socket.value.send(JSON.stringify({ action: "add_user" }));
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
    if (data.type === "get_topics") {
      roomName.value = data.room_name;
      topics.value = data.topics;
      actualTopic.value = data.topics.find(
        (topic) => topic.id === data.actual_topic
      );
    } else if (data.type === "add_user") {
      userId.value = data.user_id;
      participants.value.push({
        user_id: data.user_id,
        name: data.name,
        vote: "?",
        isSelf: true,
      });

      data.participants.forEach((participant) => {
        participants.value.push({
          user_id: participant.user_id,
          name: participant.name,
          vote: "?",
          isSelf: false,
        });
      });
    } else if (data.type === "user_added") {
      const exists = participants.value.some(
        (participant) => participant.user_id === data.user.user_id
      );

      if (!exists) {
        participants.value.push({
          user_id: data.user.user_id,
          name: data.user.name,
          vote: "?",
          isSelf: false,
        });
      }
    } else if (data.type === "user_disconnected") {
      participants.value = participants.value.filter(
        (participant) => participant.user_id !== data.user_id
      );
    } else if (data.type === "user_voted") {
      const participant = participants.value.find(
        (participant) => participant.user_id === data.user_id
      );

      if (participant) {
        participant.vote = data.vote;
      }
    }
  };

  socket.value.onclose = () => {
    // navigateTo("/");
  };

  socket.value.onerror = (error) => {
    console.log("Error:", error);
  };
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.close();
  }
});

const sendVote = (voteValue) => {
  if (socket.value && userId.value) {
    const voteMessage = {
      action: "vote",
      user_id: userId.value,
      vote: voteValue,
    };
    socket.value.send(JSON.stringify(voteMessage));
  }
};
</script>

<style scoped>
.room-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.room-name {
  text-align: center;
  color: #333;
}

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
}

.participants-list li.self {
  background-color: #d3f3d3;
}

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
</style>
