<template>
  <n-modal-provider>
    <n-message-provider>
      <div id="app">
        <Sidebar class="sidebar" />
        <n-space></n-space>
        <Editor class="editor" /></div
    ></n-message-provider>
  </n-modal-provider>
</template>

<script>
import { defineComponent } from "vue";
import { Sidebar, Editor } from "./layout";

export default defineComponent({
  name: "App",
  components: {
    Sidebar,
    Editor,
  },
});
</script>

<style>
#app {
  display: flex;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

body {
  background-image: url("https://pilgrimlyieu.github.io/daily/2024-01/12-Raizakura.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}
body::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: rgba(255, 255, 255, 0.5);
}

.sidebar {
  margin-right: 10px;
}

.editor {
  text-align: left;
}
</style>
