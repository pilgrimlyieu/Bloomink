<template>
  <n-space justify="center" style="margin-bottom: 3px">
    <div class="tag ai-tag">{{ moduleType }}</div>
    <n-button
      type="error"
      class="setting"
      secondary
      round
      size="small"
      @click="config = true"
      >配置通义千问 API</n-button
    >
    <div class="tag user-tag">{{ userName }}</div>
  </n-space>
  <n-divider />
  <div class="chat-container">
    <n-layout class="chat-area" :native-scrollbar="false">
      <div
        v-for="message in filterMessages"
        :key="updateKey"
        :class="[
          'message-wrapper',
          message.role === 'user' ? 'user-wrapper' : 'ai-wrapper',
        ]"
      >
        <div
          :class="[
            message.role === 'user' ? 'user-message' : 'ai-message',
            message.status === 'error' ? 'error-message' : '',
          ]"
        >
          {{ message.content }}
        </div>
      </div>
    </n-layout>
    <div class="input-area">
      <KeepAlive>
        <n-input
          v-model:value="chatContent"
          type="textarea"
          :autosize="{ minRows: 6, maxRows: 6 }"
          placeholder="聊点什么？"
          style="margin: 10px 0"
        />
      </KeepAlive>
      <div style="display: flex; justify-content: space-between">
        <n-button @click="clearMessages" type="error" round
          >清除聊天记录</n-button
        >
        <n-button @click="sendMessage" type="info" round>发送</n-button>
      </div>
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
      用户名
      <n-input
        v-model:value="userName"
        type="text"
        placeholder="给自己取个帅气的名字吧！"
        style="margin: 10px 0"
      />
      <template #password-visible-icon>
        <n-icon :size="16" :component="GlassesOutline" />
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script>
import { GlassesOutline } from "@vicons/ionicons5";
import axios from "axios";
import { useMessage } from "naive-ui";
import { ref } from "vue";

export default {
  name: "Attachment",
  setup() {
    const message = useMessage();
    const initMessages = (userName) => {
      return [
        {
          role: "system",
          content: `你是一个提供有关中国传统文化文学创作的大语言模型。和你进行对话用户的名称为「${userName}」。`,
        },
      ];
    };
    const apiKey = ref(localStorage.getItem("AI_apiKey") ?? "");
    const userName = ref(localStorage.getItem("AI_userName") ?? "达令");
    const moduleType = ref(
      localStorage.getItem("AIChat_moduleType") ?? "qwen-turbo"
    );
    const messages = ref(
      JSON.parse(localStorage.getItem("AIChat_messages")) ||
        initMessages(userName)
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
      messages,
      apiKey,
      userName,
      moduleType,
      moduleTypes,
      updateKey: ref(false),
      chatContent: ref(null),
      initMessages,
    };
  },
  computed: {
    filterMessages() {
      return this.messages.filter((message) => message.role !== "system");
    },
  },
  components: {
    GlassesOutline,
  },
  methods: {
    async sendMessage() {
      this.messages.push({ role: "user", content: this.chatContent });
      this.chatContent = "";
      this.updateMessages();
      this.callAiApi()
        .then((response) => {
          this.messages.push(response);
          this.updateMessages();
        })
        .catch((error) => {
          this.message.error("AI API 请求失败");
          this.messages.push({
            role: "assistant",
            content: "请求失败!",
            status: "error",
          });
          this.updateMessages();
        });
    },
    async callAiApi() {
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
            messages: this.messages,
          },
          parameters: {
            result_format: "message",
          },
        }),
      };
      try {
        const response = await axios(options);
        return response.data.output.choices[0].message;
      } catch (error) {
        throw error;
      }
    },
    updateMessages() {
      localStorage.setItem("AIChat_messages", JSON.stringify(this.messages));
      this.updateKey = !this.updateKey;
    },
    clearMessages() {
      this.messages = this.initMessages(this.userName);
      this.updateMessages();
    },
  },
};
</script>

<style scoped>
.tag {
  padding: 3px;
  border-radius: 15px;
  position: absolute;
}

.ai-tag {
  background-color: rgb(145, 205, 169);
  color: white;
  left: 0;
}

.user-tag {
  background-color: rgb(174, 211, 231);
  color: white;
  right: 0;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-area {
  height: 340px;
  width: 100%;
  overflow-y: auto;
  flex-grow: 1;
}

.input-area {
  position: sticky;
  bottom: 0;
  flex-shrink: 0;
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
  text-align: left;
  background-color: rgb(205, 222, 232);
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 20px;
}

.ai-message {
  display: inline-block;
  text-align: left;
  background-color: rgb(184, 236, 205);
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 20px;
}

.error-message {
  background-color: rgb(225, 183, 183);
}
</style>
