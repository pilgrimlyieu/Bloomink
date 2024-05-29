<template>
  <h1 class="title">
    <n-icon size="64">
      <img src="/assets/icons/春纷.svg" alt="春纷" />
    </n-icon>
    <n-button text @click="showInfo">
      <n-gradient-text
        gradient="linear-gradient(135deg, #FF9A8B 10%, #FF6A88 50%, #ff9a8b 90%)"
        style="font-size: 48px; font-weight: bold"
      >
        春紛
      </n-gradient-text>
    </n-button>
  </h1>

  <n-modal
    v-model:show="showModal"
    preset="card"
    :style="{
      width: '720px',
      height: '600px',
    }"
    title=""
  >
    <template #header>
      <n-gradient-text
        gradient="linear-gradient(135deg, #FF9A8B 10%, #FF6A88 50%, #ff9a8b 90%)"
        style="font-family: KaiTi; font-size: 36px; font-weight: bold"
      >
        春紛
      </n-gradient-text>
    </template>
    <n-alert title="内涵" type="success">
      「春」乃 「春」乃 「春」乃 「春」乃 「春」乃 「春」乃 「春」乃
    </n-alert>
    <br />
    <n-alert title="简介" type="info">
      「春」乃 「春」乃 「春」乃 「春」乃 「春」乃 「春」乃 「春」乃
    </n-alert>
    <br />
    <n-alert title="" type="warning" :show-icon="false">
      本项目是一个基于
      <a href="https://cn.vuejs.org/">Vue3</a> 的前端项目，使用了
      <a href="https://cn.vitejs.dev/">Vite</a> 作为构建工具，<a
        href="https://www.naiveui.com/zh-CN"
        >Naive UI</a
      >
      作为 UI 框架。
      <br />
      <div style="display: flex; align-items: center">
        项目地址：<a href="https://github.com/pilgrimlyieu/ELProject"
          >pilgrimlyieu/ELProject</a
        >
        <iframe
          src="https://ghbtns.com/github-btn.html?user=pilgrimlyieu&repo=ELProject&type=star&count=true&size=large"
          frameborder="0"
          scrolling="0"
          width="150"
          height="25"
          title="GitHub"
        />
      </div>
    </n-alert>
  </n-modal>
</template>

<script>
import { NGradientText, useModal } from "naive-ui";

export default {
  name: "Header",
  setup() {
    const modal = useModal();
    const showModal = ref(false);
    return {
      modal,
      showModal,
      showInfo: () => (showModal.value = true),
    };
  },
};
</script>

<style>
body {
  margin: 0;
}

h1 {
  font-family: KaiTi;
  margin: 0;
  margin-top: -10px;
  text-align: left;
  display: flex;
  align-items: center;
}
</style>
