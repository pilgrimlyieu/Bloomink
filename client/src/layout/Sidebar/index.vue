<template>
  <n-flex vertical>
    <n-layout has-sider>
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="160"
        :collapsed="collapsed"
        show-trigger
        @collapse="collapsed = true"
        @expand="collapsed = false"
      >
        <n-menu
          v-model:value="activeKey"
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          :default-expand-all="defaultExpandAll"
          @update:value="activateComponent"
        />
      </n-layout-sider>
      <n-layout-content style="padding-left: 2px">
        <div
          class="content-container"
          :style="{
            width: `calc(${sidebarWidth} - ${collapsed ? 64 : 160}px)`,
          }"
        >
          <n-layout
            :native-scrollbar="false"
            style="height: 85vh; padding: 5px"
          >
            <component :is="activeComponent" />
          </n-layout>
        </div>
      </n-layout-content>
    </n-layout>
  </n-flex>
</template>

<script>
import { defineComponent, h, ref } from "vue";
import { useModal, NIcon, NButton, NLayout } from "naive-ui";
import {
  AIChat,
  AIImage,
  AITips,
  Attachment,
  CultureLibrary,
  FormulaOCR,
  RandomPoem,
  TextOCR,
} from "@/components";

function renderIcon(iconName) {
  return () =>
    h(NIcon, null, {
      default: () =>
        h("img", { src: `/assets/icons/${iconName}.svg`, alt: iconName }),
    });
}

const sidebarWidth = "33vw";

export default defineComponent({
  name: "Sidebar",
  setup() {
    const modal = useModal();
    const menuOptions = [
      {
        label: "文化库",
        key: "culture-library",
        icon: renderIcon("Library"),
      },
      {
        label: "资料库",
        key: "attachment-library",
        icon: renderIcon("Attach12Regular"),
      },
      {
        label: "AI",
        key: "ai",
        icon: renderIcon("Robot"),
        children: [
          {
            label: "聊天",
            key: "chat-ai",
            icon: renderIcon("MessageCircle"),
          },
          {
            label: "建议",
            key: "tips-ai",
            icon: renderIcon("TipsAndUpdatesOutlined"),
          },
          {
            label: "图片",
            key: "image-ai",
            icon: renderIcon("Image24Regular"),
          },
        ],
      },
      {
        label: "OCR",
        key: "ocr",
        icon: renderIcon("Magnify"),
        children: [
          {
            label: "文本",
            key: "text-ocr",
            icon: renderIcon("ScanText24Regular"),
          },
          {
            label: "公式",
            key: "formula-ocr",
            icon: renderIcon("MathFormula16Regular"),
          },
        ],
      },
      {
        label: "每诗",
        key: "daily-poem",
        icon: renderIcon("CalendarRtl28Regular"),
      },
      {
        label: "游戏",
        key: "game",
        icon: renderIcon("GameController"),
        children: [
          {
            label: "汉兜",
            key: "handle",
            icon: renderIcon("Handle"),
          },
          {
            label: "成语",
            key: "idiom-wordle",
            icon: renderIcon("MdBookmarks"),
          },
          {
            label: "猜词",
            key: "guess-word",
            icon: renderIcon("Drafts24Filled"),
          },
        ],
      },
    ];
    const components = {
      "culture-library": CultureLibrary,
      "attachment-library": Attachment,
      "chat-ai": AIChat,
      "tips-ai": AITips,
      "image-ai": AIImage,
      "text-ocr": TextOCR,
      "formula-ocr": FormulaOCR,
      "daily-poem": RandomPoem,
    };
    const activeKey = ref("chat-ai");
    const activeComponent = ref(components[activeKey.value]);
    const activateComponent = (key) => {
      const games = {
        handle: "https://handle.antfu.me",
        "idiom-wordle": "https://cheeaun.github.io/chengyu-wordle",
        "guess-word": "https://caici.vercel.app/#/?topic=shici5",
      };
      if (key in games) {
        modal.create({
          preset: "card",
          title: "",
          style: {
            width: "1200px",
            height: "720px",
            overflow: "hidden", // 解决滚动穿透问题
          },
          content: () =>
            h("iframe", {
              src: games[key],
              width: "1408px",
              height: "791px",
              style: {
                transform: "scale(0.8)",
                transformOrigin: "0 0",
              },
              frameborder: "no",
            }),
        });
      } else {
        activeComponent.value = components[key];
      }
    };
    return {
      modal,
      sidebarWidth,
      activeComponent,
      activeKey,
      activateComponent,
      collapsed: ref(true),
      defaultExpandAll: ref(true),
      menuOptions,
    };
  },
});
</script>

<style scoped>
.content-container {
  height: 85vh;
  border: 2px solid #f0f0f0bd;
  text-align: left;
}
</style>
