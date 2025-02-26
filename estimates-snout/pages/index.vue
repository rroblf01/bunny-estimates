<template>
  <div class="container">
    <h1>Bienvenido a la Aplicación de Tareas</h1>
    <p>Gracias por usar nuestra aplicación.</p>

    <form @submit.prevent="submitTasks">
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
              placeholder="Descripción (opcional)"
            ></textarea>
          </div>
        </div>
      </div>
    </form>

    <!-- Modal de Confirmación -->
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

export default {
  setup() {
    const tasks = ref([{ title: "", description: "" }]);
    const showModal = ref(false);
    const taskToDelete = ref(null);

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
        const response = await fetch("http://localhost:8000/room", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(tasks.value),
        });

        if (response.ok) {
          alert("Tareas enviadas con éxito");
        } else {
          alert("Error al enviar las tareas");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    return {
      tasks,
      showModal,
      taskToDelete,
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
  height: 50vh; /* Ajusta la altura según sea necesario */
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
