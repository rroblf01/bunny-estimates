<template>
  <div></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRuntimeConfig } from "#app";

const config = useRuntimeConfig();
const route = useRoute();
const socket = ref(null);
const messages = ref([]);
const newMessage = ref("");

onMounted(() => {
  socket.value = new WebSocket(
    `ws://${config.public.backendUrl}/ws/room/${route.params.id}/`
  );

  socket.value.onopen = () => {
    console.log("Conectado al servidor WebSocket");
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    messages.value.push(data);
  };

  socket.value.onclose = (event) => {
    navigateTo("/");
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

const sendMessage = () => {
  if (newMessage.value.trim() !== "") {
    const messageData = { message: newMessage.value, room_name: "tortugas" };
    socket.value.send(JSON.stringify(messageData));
    newMessage.value = "";
  }
};
</script>
