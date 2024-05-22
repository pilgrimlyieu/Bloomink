<template>
  <div class="attachment-container">
    <n-space justify="center" style="margin-bottom: 3px">
      <n-button type="error" secondary round size="small" @click="config = true">配置阿里云 AI API</n-button></n-space>
    <div class="chat-record" ref="chatRecord">
      <div v-for="(message, index) in messages" :key="index"
        :class="message.sender === 'user' ? 'user-message' : 'ai-message'">
        {{ message.content }}
      </div>
    </div>
    <KeepAlive>
      <n-input v-model:value="chatContent" type="textarea" :autosize="{ minRows: 6, maxRows: 8 }" placeholder="识别结果"
        style="margin: 10px 0" />
    </KeepAlive>
    <n-button @click="sendMessage" class="send-button" type="info">发送</n-button>
  </div>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="阿里云 AI API 配置">
      API Key
      <n-input v-model:value="AK" type="password" show-password-on="click" placeholder="API Key"
        style="margin: 10px 0" />
      Module Name
      <n-input v-model:value="MN" type="text" placeholder="请输入你想调用的阿里云AI模型"
        style="margin: 10px 0" />
      User Name
      <n-input v-model:value="UN" type="text" placeholder="给自己取个帅气的名字吧！"
        style="margin: 10px 0" />
      <template #password-visible-icon>
        <n-icon :size="16" :component="GlassesOutline" />
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script>
import { GlassesOutline, ArchiveOutline } from "@vicons/ionicons5";
import axios from 'axios';
import { useMessage } from "naive-ui";
import { ref } from 'vue';

export default {
  name: "Attachment",
  setup() {
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
      message,
      AK,
      MN,
      UN,
    };
  },
  data() {
    return {
      chatContent: '',
      messages: []
    };
  },
  components: {
    GlassesOutline,
  },
  methods: {
    async sendMessage() {
      this.messages.push({ sender: 'user', content: this.chatContent });
      const aiResponse = await this.callAiApi(this.chatContent);
      this.messages.push({ sender: 'ai', content: aiResponse });
      this.chatContent = '';
      this.$nextTick(() => {
        this.$refs.chatRecord.scrollTop = this.$refs.chatRecord.scrollHeight;
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
        return response.output.choices[0].message.content;
      }).catch((error) => {
        return this.message.error('AI API 请求失败');
      });
    }
  }
};
</script>

<style scoped>
.attachment-container {
  /* ADD */
  
}

.chat-record {
  height: 300px;
  /* 聊天记录框的高度 */
  width: 100%;
  overflow-y: auto;
}

.user-message {
  text-align: right;
}

.ai-message {
  text-align: left;
}
</style>