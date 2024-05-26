<template>
  <div class="attachment-container">
    <n-space justify="center" style="margin-bottom: 3px">
      <n-button type="error" secondary round size="small" @click="config = true"
        >配置通义千问 API</n-button
      >
    </n-space>
    <n-divider />
    <n-space
      justify="center"
      style="margin-bottom: 3px; justify-content: space-between"
    >
      <n-button @click="getAbstract" class="send-button" type="info" round
        >给我摘要！</n-button
      >
      <n-button @click="getAdvice" class="send-button" type="primary" round
        >来点建议！</n-button
      >
    </n-space>
    <div v-if="aiAbstract" class="ai-abstract">
      <span v-html="aiAbstract.replace(/\n+/g, '<br />')"></span>
    </div>
    <div v-if="aiAdvice" class="ai-advice">
      <span v-html="aiAdvice.replace(/\n+/g, '<br />')"></span>
    </div>
  </div>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="通义千问 API 配置">
      API Key
      <n-input
        v-model:value="apiKey"
        type="password"
        show-password-on="click"
        placeholder="API Key"
        style="margin: 10px 0"
      />
      <br />
      模型
      <n-select v-model:value="moduleType" :options="moduleTypes"> </n-select>
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
import { useMessage } from "naive-ui";

export default {
  name: "AITips",
  setup() {
    const globalState = inject("globalState");
    const message = useMessage();
    const apiKey = ref(localStorage.getItem("AI_apiKey") ?? "");
    const moduleType = ref(
      localStorage.getItem("AITips_moduleType") ?? "qwen-turbo"
    );
    const moduleTypes = [
      { label: "qwen-turbo", value: "qwen-turbo" },
      { label: "qwen-plus", value: "qwen-plus" },
      { label: "qwen-max", value: "qwen-max" },
      { label: "qwen-max-longcontext", value: "qwen-max-longcontext" },
    ];
    const aiAbstract = ref(localStorage.getItem("AITips_aiAbstract") ?? "");
    const aiAdvice = ref(localStorage.getItem("AITips_aiAdvice") ?? "");
    watchEffect(() => {
      localStorage.setItem("AI_apiKey", apiKey.value);
      localStorage.setItem("AITips_moduleType", moduleType.value);
      localStorage.setItem("AITips_aiAbstract", aiAbstract.value);
      localStorage.setItem("AITips_aiAdvice", aiAdvice.value);
    });
    return {
      config: ref(false),
      globalState,
      message,
      apiKey,
      moduleType,
      moduleTypes,
      aiAbstract,
      aiAdvice,
    };
  },
  components: {
    GlassesOutline,
  },
  methods: {
    getAbstract() {
      this.aiAbstract = "正在获取摘要……";
      const editorContent = this.globalState.getContent();
      const abstract = `请根据下面的文章，生成一个摘要：\n\n${editorContent}。不要返回多余的内容。`;
      this.callAiApi(abstract)
        .then((response) => {
          this.aiAbstract = response;
        })
        .catch((error) => {
          this.message.error("获取摘要失败");
        });
    },
    getAdvice() {
      this.aiAdvice = "正在获取建议……";
      const editorContent = this.globalState.getContent();
      const advice = `请根据下面我写的文章，为我提供一点建议：\n\n${editorContent}`;

      this.callAiApi(advice)
        .then((response) => {
          this.aiAdvice = response;
        })
        .catch((error) => {
          this.message.error("获取建议失败");
        });
    },
    async callAiApi(advice) {
      let options = {
        method: "POST",
        url: "/aliyunai/v1/services/aigc/text-generation/generation",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        data: JSON.stringify({
          model: `${this.moduleType}`,
          input: {
            messages: [
              {
                role: "user",
                content: advice,
              },
            ],
          },
        }),
      };
      try {
        const response = await axios(options);
        return response.data.output.text; // 虽然文档建议的是用 message，但是我懒得改了 qwq
      } catch (error) {
        throw error;
      }
    },
  },
};
</script>

<style scoped>
.ai-abstract {
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  background-color: rgb(186, 233, 241);
}

.ai-advice {
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  background-color: rgb(185, 225, 172);
}
</style>
