<template>
  <div id="app">
    <Sidebar class="sidebar" />
    <n-space></n-space>
    <Editor class="editor" />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { Sidebar, Editor } from "./layout/components";

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

.sidebar {
  margin-right: 10px;
}

.editor {
  text-align: left;
}
</style>
