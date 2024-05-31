import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { NaiveUiResolver } from "unplugin-vue-components/resolvers";

export default defineConfig({
  base: "/Bloomink/",
  resolve: {
    alias: {
      "@": "/src",
    },
  },
  plugins: [
    vue(),
    AutoImport({
      imports: [
        "vue",
        {
          "naive-ui": [
            "useDialog",
            "useMessage",
            "useNotification",
            "useLoadingBar",
          ],
        },
      ],
    }),
    Components({
      resolvers: [NaiveUiResolver()],
    }),
  ],
  server: {
    open: true,
    client: {
      overlay: false,
    },
    proxy: {
      "/baiduocr": {
        target: "https://aip.baidubce.com",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/baiduocr/, ""),
      },
      "/mathpixocr": {
        target: "https://api.mathpix.com",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/mathpixocr/, ""),
      },
      "/aliyunai": {
        target: "https://dashscope.aliyuncs.com/api",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/aliyunai/, ""),
      },
    },
  },
});
