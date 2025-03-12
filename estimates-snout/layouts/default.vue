<template>
  <div class="layout">
    <nav class="navbar">
      <a href="/">Inicio</a>
    </nav>
    <slot />
  </div>
</template>

<style>
html,
body,
.layout {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

.navbar {
  position: absolute;
  top: 10px;
  left: 10px;
}

.navbar a {
  text-decoration: none;
  color: #000;
  font-weight: bold;
}
</style>
