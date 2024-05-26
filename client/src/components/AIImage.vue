<template>
  <n-space justify="center" style="margin-bottom: 3px">
    <n-button type="error" secondary round size="small" @click="config = true"
      >配置通义万相 API</n-button
    ></n-space
  >

  <n-carousel
    autoplay
    direction="vertical"
    mousewheel
    dot-placement="right"
    :space-between="10"
    style="
      width: 100%;
      height: 360px;
      border-top: 2px solid rgba(106, 115, 125, 0.2);
      border-bottom: 2px solid rgba(106, 115, 125, 0.2);
      margin: 10px 0;
    "
  >
    <n-image
      v-if="imagesStorage.length === 0"
      object-fit="contain"
      height="360px"
      width="100%"
      key="basic-image"
      src="/assets/images/basic-1.png"
    />
    <n-image
      v-if="imagesStorage.length === 0"
      object-fit="contain"
      height="360px"
      width="100%"
      key="basic-image"
      src="/assets/images/basic-2.png"
    />
    <n-image
      v-if="imagesStorage.length === 0"
      object-fit="contain"
      height="360px"
      width="100%"
      key="basic-image"
      src="/assets/images/basic-3.png"
    />
    <n-image
      v-if="imagesStorage.length === 0"
      object-fit="contain"
      height="360px"
      width="100%"
      key="basic-image"
      src="/assets/images/basic-4.png"
    />
    <n-image
      v-if="imagesStorage.length === 0"
      object-fit="contain"
      height="360px"
      width="100%"
      key="basic-image"
      src="/assets/images/basic-5.png"
    />
    <n-image
      v-for="image in imagesStorage"
      object-fit="contain"
      height="360px"
      width="100%"
      :key="updateKey"
      :src="image"
    />
  </n-carousel>

  风格
  <n-select v-model:value="imageStyle" :options="imageStyles"> </n-select>
  分辨率
  <n-select v-model:value="imageSize" :options="imageSizes"> </n-select>
  图片张数
  <n-input-number
    v-model:value="imageNumber"
    placeholder="图片张数"
    :min="1"
    :max="4"
  ></n-input-number>

  <n-space justify="center" style="margin: 5px">
    <n-button type="info" size="small" round @click="() => generateImage(true)"
      >重新生成题图</n-button
    >
    <n-button
      type="success"
      size="small"
      round
      @click="() => generateImage(false)"
      >使用旧 Prompt 生成题图</n-button
    >
  </n-space>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="通义万相 API 配置">
      API Key
      <n-input
        v-model:value="apiKey"
        type="password"
        show-password-on="click"
        placeholder="API Key"
        style="margin: 10px 0"
      />
      <br />
      文生图 Prompt 使用模型
      <n-select v-model:value="textModule" :options="textModules"> </n-select>
      文生图模型
      <n-select v-model:value="imageModule" :options="imageModules"> </n-select>
      <template #password-visible-icon>
        <n-icon :size="16" :component="GlassesOutline" />
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script>
import { GlassesOutline } from "@vicons/ionicons5";
import { inject, ref } from "vue";
import axios from "axios";

export default {
  name: "AIImage",
  setup() {
    const globalState = inject("globalState");
    const message = useMessage();
    const apiKey = ref(localStorage.getItem("AI_apiKey") ?? "");
    const textModules = [
      { label: "qwen-turbo", value: "qwen-turbo" },
      { label: "qwen-plus", value: "qwen-plus" },
      { label: "qwen-max", value: "qwen-max" },
      { label: "qwen-max-longcontext", value: "qwen-max-longcontext" },
    ];
    const textModule = ref(
      localStorage.getItem("AIImage_textModule") ?? "qwen-turbo"
    );
    const imageModules = [{ label: "wanx-v1", value: "wanx-v1" }];
    const imageModule = ref(
      localStorage.getItem("AIImage_imageModule") ?? "wanx-v1"
    );
    const imagesStorage = ref(
      JSON.parse(localStorage.getItem("AIImage_imagesStorage") ?? "[]")
    );
    const imageStyles = [
      { label: "默认", value: "<auto>" },
      { label: "3D 卡通", value: "<3d cartoon>" },
      { label: "动画", value: "<anime>" },
      { label: "油画", value: "<watercolor>" },
      { label: "素描", value: "<sketch>" },
      { label: "中国画", value: "<chinese painting>" },
      { label: "扁平插画", value: "<flat illustration>" },
    ];
    const imageStyle = ref(
      localStorage.getItem("AIImage_imageStyle") ?? "<auto>"
    );
    const imageSizes = [
      { label: "1024x1024", value: "1024*1024" },
      { label: "720x1280", value: "720*1280" },
      { label: "1280x720", value: "1280*720" },
    ];
    const imageSize = ref(
      localStorage.getItem("AIImage_imageSize") ?? "1024*1024"
    );
    const imageNumber = ref(
      parseInt(localStorage.getItem("AIImage_imageNumber") ?? 1)
    );
    const imagePrompt = ref(localStorage.getItem("AIImage_imagePrompt") ?? "");
    watchEffect(() => {
      localStorage.setItem("AI_apiKey", apiKey.value);
      localStorage.setItem("AIImage_textModule", textModule.value);
      localStorage.setItem("AIImage_imageModule", imageModule.value);
      localStorage.setItem("AIImage_imageStyle", imageStyle.value);
      localStorage.setItem("AIImage_imageSize", imageSize.value);
      localStorage.setItem("AIImage_imageNumber", imageNumber.value);
      localStorage.setItem("AIImage_imagePrompt", imagePrompt.value);
    });
    return {
      config: ref(false),
      globalState,
      message,
      apiKey,
      imagesStorage,
      textModules,
      textModule,
      imageModules,
      imageModule,
      imageStyle,
      imageStyles,
      imageSize,
      imageSizes,
      imageNumber,
      imagePrompt,
      updateKey: ref(false),
    };
  },
  components: {
    GlassesOutline,
  },
  methods: {
    async generatePrompt() {
      let data = {
        model: this.textModule,
        input: {
          messages: [
            {
              role: "system",
              content:
                "你是一个通义万相-文本生成图片的提示词生成器。用户将 Markdown 格式的文章提供给你，请你根据文章的内容构思一幅题图。然后提供给用户可以输入到通义万相-文本生成图片模型的描述画面的不超过 500 字的提示词信息。提示词信息应当详细的描述画面的各个细节，同时直接返回纯文本格式的提示词，不要包含其它额外内容。",
            },
            {
              role: "user",
              content: this.getEditorContent(),
            },
          ],
        },
        parameters: {
          result_format: "message",
          max_tokens: 500,
        },
      };
      let options = {
        method: "POST",
        url: "/aliyunai/v1/services/aigc/text-generation/generation",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        data: JSON.stringify(data),
      };
      try {
        let response = await axios(options);
        this.message.success("生成 Prompt 成功");
        this.imagePrompt = response.data.output.choices[0].message.content;
        return this.imagePrompt;
      } catch (error) {
        this.message.error("生成 Prompt 失败");
        return null;
      }
    },
    async generateImage(newPrompt) {
      let imagePrompt = this.imagePrompt;
      if (newPrompt) {
        let imagePrompt = await this.generatePrompt();
        if (!imagePrompt) {
          return this.message.error("生成 Prompt 失败");
        }
      }
      let data = {
        model: this.imageModule,
        input: {
          prompt: imagePrompt,
        },
        parameters: {
          style: this.imageStyle,
          size: this.imageSize,
          n: this.imageNumber,
        },
      };
      let options = {
        method: "POST",
        url: "/aliyunai/v1/services/aigc/text2image/image-synthesis",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
          "X-DashScope-Async": "enable",
        },
        data: JSON.stringify(data),
      };
      axios(options)
        .then((response) => {
          let taskID = response.data.output.task_id;
          let infoHandle = null;
          let checkStatusInterval = setInterval(() => {
            let options = {
              method: "GET",
              url: `/aliyunai/v1/tasks/${taskID}`,
              headers: {
                Authorization: `Bearer ${this.apiKey}`,
              },
            };
            axios(options)
              .then((response) => {
                if (response.data.output.task_status !== "RUNNING") {
                  if (response.data.output.task_status === "FAILED") {
                    throw new Error("生成图片失败");
                  }
                  clearInterval(checkStatusInterval);
                  this.imagesStorage = [];
                  for (let image of response.data.output.results) {
                    this.imagesStorage.push(image.url);
                  }
                  localStorage.setItem(
                    "AIImage_imagesStorage",
                    JSON.stringify(this.imagesStorage)
                  );
                  this.updateKey = !this.updateKey;
                  if (infoHandle) {
                    infoHandle.destroy();
                    infoHandle = null;
                  }
                  this.message.success("生成图片成功");
                } else {
                  if (!infoHandle) {
                    infoHandle = this.message.loading("正在生成图片", {
                      duration: 0,
                    });
                  }
                }
              })
              .catch((error) => {
                clearInterval(checkStatusInterval);
                if (infoHandle) {
                  infoHandle.destroy();
                  infoHandle = null;
                }
                this.message.error("生成图片失败");
              });
          }, 3000);
        })
        .catch((error) => {
          return this.message.error("生成图片失败");
        });
    },
    getEditorContent() {
      return this.globalState.getContent();
    },
  },
};
</script>
