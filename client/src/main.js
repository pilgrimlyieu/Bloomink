import { createApp, reactive } from "vue";
import App from "./App.vue";
import axios from "axios";

const app = createApp(App);

const globalState = reactive({
  tags: [],
  poetries: [],
  insertContent: (content) => null,
  getContent: () => null,
});

const openDB = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("PoetriesDatabase", 1);
    request.onerror = (event) => reject("Failed to open DB");
    request.onsuccess = (event) => resolve(event.target.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      db.createObjectStore("PoetriesData");
    };
  });
};

const storeData = async (key, data) => {
  const db = await openDB();
  const transaction = db.transaction("PoetriesData", "readwrite");
  const store = transaction.objectStore("PoetriesData");
  return new Promise((resolve, reject) => {
    const request = store.put(JSON.stringify(data), key);
    request.onerror = (event) => reject("Failed to store data");
    request.onsuccess = (event) => resolve(event.target.result);
  });
};

const getData = async (key) => {
  const db = await openDB();
  const transaction = db.transaction("PoetriesData");
  const store = transaction.objectStore("PoetriesData");
  return new Promise((resolve, reject) => {
    const request = store.get(key);
    request.onerror = (event) => reject("Failed to get data");
    request.onsuccess = (event) => {
      if (event.target.result) {
        resolve(JSON.parse(event.target.result));
      } else {
        resolve(null);
      }
    };
  });
};

(async () => {
  const savedTags = await getData("tags");
  if (savedTags) {
    globalState.tags = savedTags;
  } else {
    axios.get("/assets/tags.json").then(async (response) => {
      globalState.tags = response.data.tags;
      await storeData("tags", globalState.tags);
    });
  }

  const savedPoetries = await getData("poetries");
  if (savedPoetries) {
    globalState.poetries = savedPoetries;
  } else {
    axios.get("/assets/poetries.json").then(async (response) => {
      globalState.poetries = response.data.poetries;
      await storeData("poetries", globalState.poetries);
    });
  }
})();

app.provide("globalState", globalState);
app.mount("#app");
