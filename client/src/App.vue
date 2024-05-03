<template>
  <div id="app">
    <Sidebar />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { Sidebar } from "./layout/components";

export default defineComponent({
  name: "App",
  components: {
    Sidebar,
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
