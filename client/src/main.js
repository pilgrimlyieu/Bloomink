import { VueElement, createApp, reactive } from "vue";
import App from "./App.vue";
import axios from "axios";

const app = createApp(App);

const globalState = reactive({
  tagLimit: 1,
  tags: [],
  poetries: [],
  insertContent: "",
});

if (globalState.tags.length === 0) {
  for (let i = 1; i <= globalState.tagLimit; i++) {
    axios
      .get(`/assets/tag/${String(i).padStart(3, "0")}.json`)
      .then((response) => {
        globalState.tags.push(response.data);
        for (const poem of response.data.poems) {
          if (!globalState.poetries[poem.id]) {
            axios.get(`/assets/poetry/${poem.id}.json`).then((response) => {
              globalState.poetries[poem.id] = response.data;
            });
          }
        }
      });
  }
}
app.provide("globalState", globalState);
app.mount("#app");
