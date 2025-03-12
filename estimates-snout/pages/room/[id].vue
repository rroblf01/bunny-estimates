<template>
  <div class="room-container">
    <h1 class="room-name">{{ roomName }}</h1>
    <RoomContent :topics="topics" :actualTopic="actualTopic" />
    <ParticipantsList
      :participants="participants"
      :isCurrentUserLeader="isCurrentUserLeader"
      @assignLeader="assignLeader"
    />
    <RenameInput
      v-if="userId"
      :currentUserName="currentUserName"
      @update:currentUserName="currentUserName = $event"
      @renameUser="renameUser"
    />
    <CardsList :cards="cards" @sendVote="sendVote" />
    <StartRoundButton
      v-if="isCurrentUserLeader"
      :isRoundActive="isRoundActive"
      @startRound="startRound"
    />
    <Counter v-if="counter > 0" :counter="counter" />
  </div>
</template>

<script setup>
import RoomContent from "@/components/RoomContent.vue";
import ParticipantsList from "@/components/ParticipantsList.vue";
import RenameInput from "@/components/RenameInput.vue";
import CardsList from "@/components/CardsList.vue";
import StartRoundButton from "@/components/StartRoundButton.vue";
import Counter from "@/components/Counter.vue";
import { useRoom } from "~/composables/useRoom";

const {
  roomName,
  topics,
  actualTopic,
  participants,
  userId,
  currentUserName,
  isCurrentUserLeader,
  cards,
  counter,
  sendVote,
  renameUser,
  assignLeader,
  startRound,
  isRoundActive,
} = useRoom();
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

.counter {
  margin-top: 20px;
  text-align: center;
  font-size: 18px;
  color: #333;
}
</style>
