const { defineConfig } = require("@vue/cli-service");
const AutoImport = require("unplugin-auto-import/webpack");
const Components = require("unplugin-vue-components/webpack");
const { NaiveUiResolver } = require("unplugin-vue-components/resolvers");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    open: true,
    client: {
      overlay: false,
    },
    proxy: {
      "/baiduocr": {
        target: "https://aip.baidubce.com",
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          "^/baiduocr": "",
        },
      },
      "/mathpixocr": {
        target: "https://api.mathpix.com",
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          "^/mathpixocr": "",
        },
      },
      "/aliyunai": {
        target: "https://dashscope.aliyuncs.com/api",
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          "^/aliyunai": "",
        },
      },
    },
  },
  configureWebpack: {
    plugins: [
      require("unplugin-auto-import/webpack").default({
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
      require("unplugin-vue-components/webpack").default({
        resolvers: [NaiveUiResolver()],
      }),
    ],
  },
});
