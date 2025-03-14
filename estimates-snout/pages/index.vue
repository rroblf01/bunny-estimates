<template>
  <div class="container">
    <h1>Bienvenido a la Aplicación de Tareas</h1>
    <p>Gracias por usar nuestra aplicación.</p>

    <form @submit.prevent="submitTasks">
      <!-- Input para el nombre de la sala -->
      <div class="room-name-input">
        <label for="roomName">Nombre de la sala:</label>
        <input
          v-model="roomName"
          id="roomName"
          placeholder="Introduce el nombre de la sala"
          required
        />
      </div>

      <button type="button" @click="addTask" class="add-button">
        Añadir tarea
      </button>
      <button type="submit" class="submit-button">Enviar</button>
      <div class="task-list">
        <div v-for="(task, index) in tasks" :key="index" class="task-form">
          <button
            type="button"
            @click="showDeleteModal(index)"
            class="delete-button"
          >
            Eliminar
          </button>
          <div class="task-inputs">
            <input
              v-model="task.title"
              placeholder="Título de la tarea"
              required
            />
            <textarea
              v-model="task.description"
              placeholder="Descripción"
            ></textarea>
          </div>
        </div>
      </div>
    </form>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <p>¿Estás seguro de que quieres eliminar esta tarea?</p>
        <button @click="confirmDelete" class="confirm-button">Sí</button>
        <button @click="cancelDelete" class="cancel-button">No</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useRuntimeConfig } from "#app";

export default {
  setup() {
    const config = useRuntimeConfig();
    const tasks = ref([{ title: "", description: "" }]);
    const showModal = ref(false);
    const taskToDelete = ref(null);
    const roomName = ref("");

    const addTask = () => {
      tasks.value.push({ title: "", description: "" });
    };

    const showDeleteModal = (index) => {
      taskToDelete.value = index;
      showModal.value = true;
    };

    const confirmDelete = () => {
      if (taskToDelete.value !== null) {
        tasks.value.splice(taskToDelete.value, 1);
        taskToDelete.value = null;
      }
      showModal.value = false;
    };

    const cancelDelete = () => {
      taskToDelete.value = null;
      showModal.value = false;
    };

    const submitTasks = async () => {
      try {
        const response = await fetch(
          `http://${config.public.backendUrl}/api/estimates/room`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              tasks: tasks.value,
              room_name: roomName.value,
            }),
          }
        );

        if (response.ok) {
          response.json().then((data) => {
            navigateTo(`/room/${data.public_name}`);
          });
        } else {
          alert(response.statusText);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    return {
      tasks,
      showModal,
      taskToDelete,
      roomName,
      addTask,
      showDeleteModal,
      confirmDelete,
      cancelDelete,
      submitTasks,
    };
  },
};
</script>

<style>
.container {
  width: 50vw;
  margin: 0 auto;
  padding: 1rem;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  color: #333;
}

p {
  text-align: center;
  color: #666;
}

.room-name-input {
  margin-bottom: 1rem;
}

.room-name-input label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
}

.room-name-input input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  width: 100%;
}

.task-form {
  margin-bottom: 1rem;
  display: flex;
  align-items: flex-start;
}

.task-inputs {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

input,
textarea {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  width: 90%;
}

textarea {
  resize: vertical;
  height: 5rem;
}

.add-button,
.submit-button,
.delete-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.add-button {
  background-color: #28a745;
  color: white;
  margin-right: 10px;
}

.submit-button {
  background-color: #007bff;
  color: white;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  margin-right: 10px;
}

.add-button:hover,
.submit-button:hover,
.delete-button:hover {
  opacity: 0.9;
}

.task-list {
  margin-top: 1rem;
  height: 50vh;
  overflow-y: auto;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.confirm-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.confirm-button {
  background-color: #dc3545;
  color: white;
  margin-right: 10px;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}
</style>
