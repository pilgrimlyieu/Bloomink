<template>
  <div class="attachment-container">
    <n-space justify="center" style="margin-bottom: 3px">
      <n-button type="error" secondary round size="small" @click="config = true">配置阿里云 AI API</n-button>
    </n-space>
    <n-divider />
    <n-button @click="getAdvice" class="send-button" type="primary">来点建议！</n-button>
    <div class="ai-response" :class="{ 'error-response': aiResponseError }">{{ aiResponse }}</div>
  </div>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="阿里云 AI API 配置">
      API Key
      <n-input v-model:value="apiKey" type="password" show-password-on="click" placeholder="API Key"
        style="margin: 10px 0" />
      <br />
      Module Name
      <n-select v-model:value="moduleType" :options="moduleTypes"> </n-select>
      <br />
      User Name
      <n-input v-model:value="userName" type="text" placeholder="给自己取个帅气的名字吧！" style="margin: 10px 0" />
      <template #password-visible-icon>
        <n-icon :size="16" :component="GlassesOutline" />
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script>
import { GlassesOutline } from "@vicons/ionicons5";
import { inject,ref } from "vue";
import axios from 'axios';
import { useMessage } from "naive-ui";

export default {
  name: "AITips",
  setup() {
    const globalState = inject('globalState');
    const message = useMessage();
    const apiKey = ref(localStorage.getItem("AI_apiKey") ?? "");
    const userName = ref(localStorage.getItem("AI_userName") ?? "");
    const moduleType = ref(
      localStorage.getItem("AITips_moduleType") ?? "qwen-turbo"
    );
    const moduleTypes = [
      { label: "qwen-turbo", value: "qwen-turbo" },
      { label: "qwen-plus", value: "qwen-plus" },
      { label: "qwen-max", value: "qwen-max" },
      { label: "qwen-max-longcontext", value: "qwen-max-longcontext" },
    ];
    watchEffect(() => {
      localStorage.setItem("AI_apiKey", apiKey.value);
      localStorage.setItem("AI_userName", userName.value);
      localStorage.setItem("AITips_moduleType", moduleType.value);
    });
    
    return { 
      config: ref(false),
      globalState,
      message,
      apiKey,
      userName,
      moduleType,
      moduleTypes
    };
  },
  data() {
    return {
      aiResponse: '',
      aiResponseError: false
    };
  },
  components: {
    GlassesOutline,
  },
  methods: {
    getAdvice() {
      this.aiResponseError = false;
      this.aiResponse = '正在获取建议...';
      const editorContent = this.globalState.getContent();
      const advice = `这是我写的一段文本：\n\n${editorContent}\n\n请帮我总结一下写的内容,请务必真实地评价一下写的怎么样,再给点建议。`;

      this.callAiApi(advice).then((response) => {
        this.aiResponse = response;
      }).catch((error) => {
        this.message.error('获取建议失败');
        this.aiResponseError = true;
        this.aiResponse = '获取建议失败';
      });
    },
    async callAiApi(advice) {
      let options = {
        method: 'POST',
        url: '/alitongyiai/api/v1/services/aigc/text-generation/generation',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        data: JSON.stringify({
          model: `${this.moduleType}`,
          input: {
            messages: [
              {
                role: 'user',
                content: advice
              }
            ]
          },
        }),
      };

      try {
        const response = await axios(options);
        return response.data.output.text;
      } catch (error) {
        throw error;
      }
    },
  },
};
</script>

<style scoped>
.send-button {
  width: 100%;
}

.ai-response {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid rgb(64, 191, 115);
  border-radius: 5px;
  background-color: rgb(64, 191, 115);
  color: white;
}

.error-response {
  border-color: rgb(199, 21, 21);
  background-color: rgb(199, 21, 21);
}
</style>
