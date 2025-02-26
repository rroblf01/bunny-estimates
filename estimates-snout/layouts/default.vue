<template>
    <div class="layout">
      <slot />
    </div>
  </template>
  
  <style>
  html, body, .layout {
    height: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    font-family: Arial, sans-serif;
  }
  
  </style>