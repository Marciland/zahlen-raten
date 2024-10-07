const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5173",
    specPattern: "**/*.e2e.js",
    supportFile: false,
    fixturesFolder: "test/e2e/fixtures",
  },
});
