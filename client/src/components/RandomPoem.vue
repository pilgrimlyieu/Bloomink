<template>
  <div>
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
    <n-space></n-space>
    <n-collapse>
      <n-collapse-item name="翻译" title="翻译">
        <span
          v-html="t(poetries[poemID]?.fanyi.replace(/^译文\s*/, ''))"
        ></span>
      </n-collapse-item>
      <n-collapse-item name="赏析" title="赏析">
        <span v-html="t(poetries[poemID]?.shangxi)"></span>
      </n-collapse-item>
      <n-collapse-item name="额外信息" title="额外信息">
        <span v-html="t(poetries[poemID]?.about)"></span>
      </n-collapse-item>
      <n-collapse-item name="作者" title="作者">
        <n-image
          :src="poetries[poemID]?.poet.image"
          object-fit="cover"
          size="100"
        ></n-image>
        <br />
        <span v-html="t(poetries[poemID]?.poet.desc)"></span>
      </n-collapse-item>
      <n-collapse-item name="标签" title="标签">
        <n-tag
          v-for="(tag, index) in poetries[poemID].tags"
          :type="specialTagType(index)"
          style="margin: 5px 5px 0 0; cursor: pointer; user-select: none"
          round
          size="large"
        >
          {{ tag }}
        </n-tag>
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
