import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRuntimeConfig } from "#app";
import { useRoute, navigateTo } from "#app";

export function useRoom() {
  const config = useRuntimeConfig();
  const route = useRoute();
  const socket = ref(null);
  const roomName = ref("");
  const topics = ref([]);
  const actualTopic = ref(null);
  const participants = ref([]);
  const userId = ref(null);
  const newName = ref("");
  const counter = ref(0);
  const isRoundActive = ref(false);
  let countdownInterval = null;
  const temporaryVotes = ref({});

  const currentUserName = computed({
    get() {
      const user = participants.value.find((p) => p.isSelf);
      return user ? user.name : "";
    },
    set(value) {
      newName.value = value;
    },
  });

  const isCurrentUserLeader = computed(() => {
    const user = participants.value.find((p) => p.isSelf);
    return user ? user.isLeader : false;
  });

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
    if (!socket.value || socket.value.readyState === WebSocket.CLOSED) {
      console.log("Connecting to room", route.params.id);
      socket.value = new WebSocket(
        `ws://${config.public.backendUrl}/ws/room/${route.params.id}/`
      );

      socket.value.onopen = () => {
        socket.value.send(JSON.stringify({ action: "get_topics" }));
        socket.value.send(JSON.stringify({ action: "add_user" }));
      };

      socket.value.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "get_topics") {
          if (!data.actual_topic) {
            navigateTo(`/room/resume/${route.params.id}/`);
          }

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
            isLeader: data.is_leader,
          });

          data.participants.forEach((participant) => {
            participants.value.push({
              user_id: participant.user_id,
              name: participant.name,
              vote: "?",
              isSelf: false,
              isLeader: participant.is_leader,
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
              isLeader: false,
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
            if (participant.isSelf) {
              participant.vote = data.vote;
            } else {
              temporaryVotes.value[data.user_id] = data.vote;
            }
          }
        } else if (data.type === "user_renamed") {
          const participant = participants.value.find(
            (participant) => participant.user_id === data.user_id
          );

          if (participant) {
            participant.name = data.name;
          }
        } else if (data.type === "leader_assigned") {
          participants.value = participants.value.map((participant) => ({
            ...participant,
            isLeader: participant.user_id === data.user_id,
          }));
        } else if (data.type === "start_round") {
          startCountdown(data.seconds);
        } else if (data.type === "end_round") {
          isRoundActive.value = false;
          if (!data.next_topic_id) {
            navigateTo(`/room/resume/${route.params.id}/`);
          }

          revealVotes();

          if (actualTopic.value) {
            actualTopic.value.average = data.average;
          }

          actualTopic.value = topics.value.find(
            (topic) => topic.id === data.next_topic_id
          );
        } else {
          console.log("Unknown message:", data);
        }
      };

      socket.value.onclose = () => {
        navigateTo(`/room/resume/${route.params.id}/`);
      };

      socket.value.onerror = (error) => {
        console.log("Error:", error);
      };
    }
  });

  onUnmounted(() => {
    if (socket.value) {
      socket.value.close();
    }
    clearInterval(countdownInterval);
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

  const renameUser = () => {
    if (socket.value && userId.value && newName.value.trim() !== "") {
      const renameMessage = {
        action: "rename",
        user_id: userId.value,
        name: newName.value.trim(),
      };
      socket.value.send(JSON.stringify(renameMessage));
      newName.value = "";
    }
  };

  const assignLeader = (newLeaderId) => {
    if (socket.value && userId.value) {
      const leaderMessage = {
        action: "assign_leader",
        user_id: userId.value,
        new_leader_id: newLeaderId,
      };
      socket.value.send(JSON.stringify(leaderMessage));
    }
  };

  const startRound = () => {
    if (socket.value && userId.value) {
      const startRoundMessage = {
        action: "start_round",
        user_id: userId.value,
      };
      socket.value.send(JSON.stringify(startRoundMessage));
      isRoundActive.value = true;
    }
  };

  const startCountdown = (seconds) => {
    counter.value = seconds;
    clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
      if (counter.value > 0) {
        counter.value--;
      } else {
        clearInterval(countdownInterval);
      }
    }, 1000);
  };

  const revealVotes = () => {
    participants.value.forEach((participant) => {
      if (temporaryVotes.value[participant.user_id] !== undefined) {
        participant.vote = temporaryVotes.value[participant.user_id];
      }
    });
    temporaryVotes.value = {};
  };

  return {
    roomName,
    topics,
    actualTopic,
    participants,
    userId,
    newName,
    counter,
    currentUserName,
    isCurrentUserLeader,
    cards,
    sendVote,
    renameUser,
    assignLeader,
    startRound,
    isRoundActive,
  };
}
