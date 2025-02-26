<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
    <h1>hola mundo!</h1>
  </div>
</template>

<script>
export default {
  mounted() {
    this.socket = this.$nuxtSocket({
      channel: '/ws/room/caracoles/'
    })
    /* Listen for events: */
    this.socket
    .on('someEvent', (msg, cb) => {
      console.log(msg)
    })
  },
}
</script>