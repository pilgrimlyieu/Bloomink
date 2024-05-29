<template>
  <n-modal-provider>
    <n-message-provider>
      <Header class="header" />
      <div class="content">
        <Sidebar class="sidebar" />
        <Editor class="editor" />
      </div>
    </n-message-provider>
  </n-modal-provider>
</template>

<script>
import { defineComponent } from "vue";
import { Sidebar, Editor, Header } from "./layout";

export default defineComponent({
  name: "App",
  components: {
    Sidebar,
    Editor,
    Header,
  },
});
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
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

.header {
}

.content {
  display: flex;
}

.sidebar {
  margin-right: 10px;
}

.editor {
  text-align: left;
}
</style>
