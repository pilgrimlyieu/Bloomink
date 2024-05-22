<template>
  <div class="attachment-container">
    <n-space justify="center" style="margin-bottom: 3px">
      <n-button type="error" secondary round size="small" @click="config = true">配置阿里云 AI API</n-button></n-space>
    <n-button @click="getAdvice" class="send-button" type="primary">来点建议！</n-button>
    <div class="ai-response">{{ aiResponse }}</div>
  </div>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="阿里云 AI API 配置">
      API Key
      <n-input v-model:value="AK" type="password" show-password-on="click" placeholder="API Key"
        style="margin: 10px 0" />
      Module Name
      <n-input v-model:value="MN" type="text" placeholder="请输入你想调用的阿里云AI模型" style="margin: 10px 0" />
      User Name
      <n-input v-model:value="UN" type="text" placeholder="给自己取个帅气的名字吧！" style="margin: 10px 0" />
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

export default {
  name: "AITips",
  setup() {
    const globalState = inject('globalState');
    const message = useMessage();
    const AK = ref(localStorage.getItem("AK"));
    const MN = ref(localStorage.getItem("MN"));
    const UN = ref(localStorage.getItem("UN"));
    watchEffect(() => {
      localStorage.setItem("AK", AK.value);
      localStorage.setItem("MN", MN.value);
      localStorage.setItem("UN", UN.value);
    });
    
    return { 
      config: ref(false),
      globalState,
      message,
      AK,
      MN,
      UN, 
    };
  },
  methods: {
    getAdvice() {
      const editorContent = this.globalState.insertContent;
      const advice = `这是我写的一段文本：\n\n${editorContent}\n\n请帮我总结一下写的内容，评价一下写的怎么样，再给点建议。`;
      this.callAiApi(advice).then((advice) => {
        this.aiResponse = advice;
      }).catch((error) => {
        this.message.error('获取建议失败');
      });
    },
    async callAiApi(message) {
      let options = {
        method: 'POST',
        url: '/alitongyiai/api/v1/services/aigc/text-generation/generation',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.AK}`
        },
        data: JSON.stringify({
          model: `${this.MN}`,
          input: {
            messages: [
              {
                role: 'user',
                content: message
              }
            ]
          },
          parameters: {
            result_format: 'message'
          }
        }),
      };
      axios(options).then((response) => {
        return response.data.output.choices[0].message.content;
      }).catch((error) => {
        console.error(error);
        throw error;
      });
    }
  }
};
</script>

<style scoped>
.attachment-container {
  /* Add anything */
}
</style>
