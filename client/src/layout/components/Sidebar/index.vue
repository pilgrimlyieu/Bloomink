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
import { NIcon } from "naive-ui";
import { Library } from "@vicons/ionicons5";
import { Magnify } from "@vicons/carbon";
import { Robot } from "@vicons/fa";
import {
  MathFormula16Regular,
  ScanText24Regular,
  Image24Regular,
  Attach12Regular,
  CalendarRtl28Regular,
} from "@vicons/fluent";
import { MessageCircle } from "@vicons/tabler";
import { TipsAndUpdatesOutlined } from "@vicons/material";
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

function renderIcon(icon) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

const sidebarWidth = "33vw";

const menuOptions = [
  {
    label: "文化库",
    key: "culture-library",
    icon: renderIcon(Library),
  },
  {
    label: "资料库",
    key: "attachment-library",
    icon: renderIcon(Attach12Regular),
  },
  {
    label: "AI",
    key: "ai",
    icon: renderIcon(Robot),
    children: [
      {
        label: "聊天",
        key: "chat-ai",
        icon: renderIcon(MessageCircle),
      },
      {
        label: "建议",
        key: "tips-ai",
        icon: renderIcon(TipsAndUpdatesOutlined),
      },
      {
        label: "图片",
        key: "image-ai",
        icon: renderIcon(Image24Regular),
      },
    ],
  },
  {
    label: "OCR",
    key: "ocr",
    icon: renderIcon(Magnify),
    children: [
      {
        label: "文本",
        key: "text-ocr",
        icon: renderIcon(ScanText24Regular),
      },
      {
        label: "公式",
        key: "formula-ocr",
        icon: renderIcon(MathFormula16Regular),
      },
    ],
  },
  {
    label: "每诗",
    key: "daily-poem",
    icon: renderIcon(CalendarRtl28Regular),
  },
];

export default defineComponent({
  name: "Sidebar",
  setup() {
    const activeComponent = ref(Attachment);
    const activateComponent = (key) => {
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
      activeComponent.value = components[key];
    };
    return {
      sidebarWidth,
      activeComponent,
      activateComponent,
      activeKey: ref(null),
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
