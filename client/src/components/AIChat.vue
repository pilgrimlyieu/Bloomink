<template>
  <div class="attachment-container">
    <n-space justify="center" style="margin-bottom: 3px">
      <div class="tag ai-tag">{{ moduleType }}</div>
      <n-button type="error" class="setting" secondary round size="small" @click="config = true">配置阿里云 AI API</n-button>
      <div class="tag user-tag">{{ userName }}</div>
    </n-space>
    <n-divider />
    <div class="chat-record" ref="chatRecord">
      <div v-for="(message, index) in messages" :key="index" class="message-wrapper"
        :class="message.sender === 'user' ? 'user-wrapper' : 'ai-wrapper'">
        <div
          :class="[message.sender === 'user' ? 'user-message' : 'ai-message', message.status === 'error' ? 'error-message' : '']">
          {{ message.content }}
        </div>
      </div>
      <div class="input-area">
        <KeepAlive>
          <n-input v-model:value="chatContent" type="textarea" :autosize="{ minRows: 6, maxRows: 8 }" placeholder="你想说啥"
            style="margin: 10px 0" />
        </KeepAlive>
        <n-button @click="sendMessage" class="send-button" type="info">发送</n-button>
      </div>
    </div>
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
import axios from 'axios';
import { useMessage } from "naive-ui";
import { ref } from 'vue';

export default {
  name: "Attachment",
  setup() {
    const message = useMessage();
    const apiKey = ref(localStorage.getItem("AI_apiKey") ?? "");
    const userName = ref(localStorage.getItem("AI_userName") ?? "");
    const moduleType = ref(
      localStorage.getItem("AIChat_moduleType") ?? "qwen-turbo"
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
      localStorage.setItem("AIChat_moduleType", moduleType.value);
    });

    return {
      config: ref(false),
      message,
      apiKey,
      userName,
      moduleType,
      moduleTypes
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
      this.callAiApi(this.chatContent).then((response) => {
        this.messages.push({ sender: 'ai', content: response });
      }).catch((error) => {
        this.message.error('AI API 请求失败');
        this.messages.push({ sender: 'ai', content: '请求失败!', status: 'error' });
      });
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
          'Authorization': `Bearer ${this.apiKey}`
        },
        data: JSON.stringify({
          model: `${this.moduleType}`,
          input: {
            messages: [
              {
                role: 'user',
                content: message
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
    }
  },
};
</script>

<style scoped>
.attachment {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tag {
  padding: 5px;
  border-radius: 5px;
  position: absolute;
}

.ai-tag {
  background-color: rgb(64, 191, 115);
  border: rgb(64, 191, 115);
  color: white;
  left: 0;
}

.user-tag {
  background-color: rgb(0, 162, 255);
  border: 1px solid rgb(0, 162, 255);
  color: white;
  right: 0;
}

.chat-record {
  height: 590px; /* 聊天记录框的高度 */
  width: 100%;
  overflow-y: auto;
}

.message-wrapper {
  display: flex;
  justify-content: flex-end;
}

.ai-wrapper {
  justify-content: flex-start;
}

.user-message {
  display: inline-block;
  text-align: right;
  background-color: rgb(0, 162, 255);
  border: 1px solid rgb(0, 162, 255);
  border-radius: 5px;
  color: white;
  padding: 10px;
  margin-bottom: 20px;
}

.ai-message {
  display: inline-block;
  text-align: left;
  background-color: rgb(64, 191, 115);
  border: 1px solid rgb(64, 191, 115);
  border-radius: 5px;
  color: white;
  padding: 10px;
  margin-bottom: 20px;
}

.error-message {
  background-color: rgb(199, 21, 21);
  border: 1px solid rgb(199, 21, 21);
}

.input-area {
  position: sticky;
  bottom: 0;
  background-color: white;
}
</style>