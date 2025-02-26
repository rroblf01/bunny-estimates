// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['nuxt-socket-io'],
  io: {
    // module options
    sockets: [{
      name: 'main',
      url: 'estimates-tail:8000/'
    }]
  }
})
