const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://frontend-service:5173',
    supportFile: false,
    video: true,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {},
  },
  viewportWidth: 1280,
  viewportHeight: 720,
});