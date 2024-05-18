<template>
  <div>
    <n-space justify="center" style="margin-bottom: 3px">
      <n-button type="primary" round @click="chooseRandomPoem"
        >下一个</n-button
      ></n-space
    >
    <n-card
      :title="`📖《${getPoetryName(globalState.poemID)}》${getPoetName(
        globalState.poemID
      )}`"
      style="width: 100%"
      embedded
      header-style="font-size: 18px; font-weight: bold; text-align: center"
    >
      {{ poetries[globalState.poemID]?.content }}
    </n-card>
    <n-space></n-space>
    <n-collapse>
      <n-collapse-item name="翻译" title="翻译">
        {{ poetries[globalState.poemID]?.fanyi.replace(/^译文\s*/, "") }}
      </n-collapse-item>
      <n-collapse-item name="赏析" title="赏析">
        {{ poetries[globalState.poemID]?.shangxi }}
      </n-collapse-item>
      <n-collapse-item name="额外信息" title="额外信息">
        {{ poetries[globalState.poemID]?.about }}
      </n-collapse-item>
      <n-collapse-item name="作者" title="作者">
        <n-image
          :src="poetries[globalState.poemID]?.poet.image"
          object-fit="cover"
          size="100"
        ></n-image>
        <div>{{ poetries[globalState.poemID]?.poet.desc }}</div>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>

<script>
import { inject } from "vue";

export default {
  name: "RandomPoem",
  setup() {
    const globalState = inject("globalState");
    const keys = Object.keys(globalState.poetries);
    globalState.poemID = "71150"; // Debug default value
    return {
      globalState,
      poetries: computed(() => globalState.poetries),
      keys,
    };
  },
  methods: {
    t(text) {
      return text.replace(/\n{1,2}/g, "<br>");
    },
    chooseRandomPoem() {
      this.globalState.poemID =
        this.keys[Math.floor(Math.random() * this.keys.length)].toString();
    },
    getPoetryName(id) {
      return this.poetries[id]?.name;
    },
    getPoetName(id) {
      return this.poetries[id]?.poet.name;
    },
  },
};
</script>
