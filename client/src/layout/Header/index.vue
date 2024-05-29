<template>
  <h1 class="title">
    <n-button text @click="showInfo">
      <template #icon>
        <n-icon size="64">
          <img src="/assets/icons/春纷.svg" alt="春纷" width="64" height="64" />
        </n-icon>
      </template>
      <n-gradient-text
        gradient="linear-gradient(135deg, #FF9A8B 10%, #FF6A88 50%, #ff9a8b 90%)"
        style="
          font-family: 'Times New Roman', Times, KaiTi;
          font-size: 48px;
          font-weight: bold;
        "
      >
        春紛 <i>Bloomink</i>
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
      <div style="display: flex; align-items: center">
        <n-icon size="48">
          <img src="/assets/icons/春纷.svg" alt="春纷" />
        </n-icon>
        <n-gradient-text
          gradient="linear-gradient(135deg, #FF9A8B 10%, #FF6A88 50%, #ff9a8b 90%)"
          style="
            font-family: 'Times New Roman', Times, KaiTi;
            font-size: 36px;
            font-weight: bold;
          "
        >
          春紛 <i>Bloomink</i>
        </n-gradient-text>
      </div>
    </template>

    <n-scrollbar style="max-height: 480px">
      <n-alert title="简介" type="info">
        「春纷」是一款专为文艺创作者打造的多功能 Markdown
        编辑器，融合了丰富的诗词文化资源和前沿技术，旨在成为您创作道路上的灵感源泉和得力助手。「春纷」提供了如下的附加功能：
        <br />
        <ol>
          <li>
            文化库：我们将古典诗词按标签分类，并按受欢迎程度进行排序，方便您查找并插入到创作中。同时提供详细的诗词信息，帮助您更深入地理解和欣赏每一首诗。
          </li>
          <li>
            资料库：汇总整理了各类古籍、古诗词相关网站，让信息检索更便捷，助您参考与学习。
          </li>
          <li>
            AI 支持：通过 AI 聊天、AI 建议、AI 摘要和 AI
            生图等功能，「春纷」为您的创作提供实时指导和灵感启发，使内容更加丰富和多样。
          </li>
          <li>
            OCR
            功能：方便您将纸质作品电子化，或从无法复制的文本中提取信息，满足研究和引用的需求。
          </li>
          <li>
            随机诗词：每天为您展示一首随机诗词及其背后的故事，让诗词文化融入您的日常创作，增进文化学习。
          </li>
          <li>
            休闲游戏：在创作之余，我们提供了与成语和诗词相关的小游戏，让您在轻松愉快的氛围中进一步了解中国传统文化。
          </li>
        </ol>
        「春纷」结合了春天的希望和诗词的美好，多样的功能如花般绽放，致力于为用户提供一个充满灵感和文化气息的创作环境。无论您是专业作家、文学爱好者，还是文化研究者，「春纷」都将成为您不可或缺的创作伙伴。
      </n-alert>
      <br />

      <n-alert title="内涵" type="success">
        「春」象征希望与新生：春天是万物复苏的季节，象征着新的开始和希望；中国古典诗词中，春天是一个常见的主题，代表着美好、希望和新的生命，应用内的文化库、随机诗词功能等，都能让用户感受到春天的诗意。寓意成长与发展：春天是成长的季节，象征着用户在使用这个应用过程中不断提高自己的创作能力和文化素养；大模型、OCR
        等前沿技术为用户创作提供帮助，犹如春风化雨，助力用户的创作之路。
        <br />
        <br />
        「纷」既表达了多样性与丰富性：应用提供了丰富多彩的功能，从文化库到 AI
        聊天，从资料库到
        OCR，再到随机诗词和游戏，功能多样，满足用户各种创作和学习需求；通过文化库和资料库，用户可以接触到各种古籍、古诗词，感受到中国传统文化的多样性和深厚底蕴。又体现了纷繁与互动的含义：用户互动：应用通过
        AI
        功能提供即时建议和互动，帮助用户在创作过程中得到反馈和指导，就像春天万物交织互动一样。随机诗词功能和游戏不仅丰富了用户的创作素材，还能激发创作灵感，使创作过程充满活力和趣味。
        <br />
        <br />
        「春纷」与中华传统二十四节气里的「春分」谐音。「花时微雨，未减春分数。」春分过后，百花齐放，这个名字不仅反映出我们的网站与中华文化的紧密联系，还表达了对用户能够自由表达与创作的希冀。
        <br />
        <br />
        英文名 Bloomink
        结合了「Bloom（绽放）」和「Ink（墨水）」，象征着在创作过程中如春花般绽放的灵感和创意，同时「墨水」也暗示了文字和书写。
        <br />
        <br />
        我们的图标是一朵鲜艳多彩的鲜花，象征着我们希望用户在创作中百花齐放，绽放无限灵感。
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
          项目地址：<a href="https://github.com/pilgrimlyieu/Bloomink"
            >pilgrimlyieu/Bloomink</a
          >
          <iframe
            src="https://ghbtns.com/github-btn.html?user=pilgrimlyieu&repo=Bloomink&type=star&count=true&size=large"
            frameborder="0"
            scrolling="0"
            width="150"
            height="25"
            title="GitHub"
          />
        </div>
      </n-alert>
    </n-scrollbar>
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
  margin: 0;
  margin-top: -10px;
  margin-left: 15px;
  text-align: left;
  display: flex;
  align-items: center;
}
</style>
