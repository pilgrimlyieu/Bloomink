<template>
  <n-space justify="center" style="margin-bottom: 3px">
    <n-button type="primary" round @click="chooseRandomPoem"
      >下一个</n-button
    ></n-space
  >
  <n-card
    :title="`📖《${getPoetryName(poemID)}》${getPoetName(poemID)}`"
    style="width: 100%"
    embedded
    header-style="font-size: 18px; font-weight: bold; text-align: center"
  >
    {{ poetries[poemID]?.content }}
  </n-card>
  <n-alert name="标签" type="info" title="标签">
    <n-tag
      v-for="(tag, index) in poetries[poemID].tags"
      :type="specialTagType(index)"
      style="margin: 5px 5px 0 0; cursor: pointer; user-select: none"
      round
      size="large"
    >
      {{ tag }}
    </n-tag>
  </n-alert>
  <n-tabs type="segment" animated>
    <n-tab-pane name="翻译">
      <span v-html="t(poetries[poemID]?.fanyi.replace(/^译文\s*/, ''))"></span>
    </n-tab-pane>
    <n-tab-pane name="赏析">
      <span v-html="t(poetries[poemID]?.shangxi)"></span>
    </n-tab-pane>
    <n-tab-pane name="额外信息">
      <span v-html="t(poetries[poemID]?.about)"></span>
    </n-tab-pane>
    <n-tab-pane name="作者">
      <n-image
        :src="poetries[poemID]?.poet.image"
        object-fit="cover"
        size="100"
      ></n-image>
      <br />
      <span v-html="t(poetries[poemID]?.poet.desc)"></span>
    </n-tab-pane>
  </n-tabs>
</template>

<script>
import { inject } from "vue";

export default {
  name: "RandomPoem",
  setup() {
    const globalState = inject("globalState");
    const keys = Object.keys(globalState.poetries);
    return {
      poemID: ref("71150"),
      poetries: computed(() => globalState.poetries),
      keys,
    };
  },
  methods: {
    t(text) {
      return text.replace(/\n{1,2}/g, "<br>");
    },
    chooseRandomPoem() {
      this.poemID =
        this.keys[Math.floor(Math.random() * this.keys.length)].toString();
    },
    getPoetryName(id) {
      return this.poetries[id]?.name;
    },
    getPoetName(id) {
      return this.poetries[id]?.poet.name;
    },
    specialTagType(id) {
      return ["default", "primary", "info", "success", "warning", "error"][
        id % 6
      ];
    },
  },
};
</script>
