<template>
  <n-space justify="center" style="margin-bottom: 3px">
    <n-button type="error" secondary round size="small" @click="config = true"
      >配置百度 OCR API</n-button
    ></n-space
  >
  <KeepAlive>
    <n-upload multiple directory-dnd :max="1" :custom-request="handleUpload">
      <n-upload-dragger>
        <div style="margin-bottom: 12px">
          <n-icon size="48" :depth="3">
            <ArchiveOutline />
          </n-icon>
        </div>
        <n-text style="font-size: 16px">
          点击或者拖动图片到该区域来上传
        </n-text>
        <n-p depth="3" style="margin: 8px 0 0 0">
          一次仅能上传一张图片，如需识别下一张图片，请先删除当前图片
        </n-p>
      </n-upload-dragger>
    </n-upload></KeepAlive
  >
  <KeepAlive>
    <n-input
      v-model:value="ocrResult"
      type="textarea"
      :autosize="{ minRows: 6, maxRows: 8 }"
      placeholder="识别结果"
      style="margin: 10px 0"
    />
  </KeepAlive>

  <KeepAlive>
    <n-progress
      type="line"
      :percentage="confidence"
      :indicator-placement="'inside'"
      :stroke-width="10"
      :status="'warning'"
      style="margin: 2px 0"
    >
      置信度 {{ confidence.toFixed(2) }}%
    </n-progress>
  </KeepAlive>

  <n-button
    type="info"
    size="small"
    secondary
    round
    @click="() => insertToEditor(ocrResult)"
    >插入</n-button
  >

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="百度 OCR API 配置">
      API Key
      <n-input
        v-model:value="apiKey"
        type="password"
        show-password-on="click"
        placeholder="API Key"
        style="margin: 10px 0"
      />
      Secret Key
      <n-input
        v-model:value="secretKey"
        type="password"
        show-password-on="click"
        placeholder="Secret Key"
        style="margin: 10px 0"
      />
      Access Token
      <n-input
        v-model:value="accessToken"
        type="password"
        show-password-on="click"
        placeholder="Access Token"
        style="margin: 10px 0"
      />
      <n-button
        @click="identificationRecognize"
        type="primary"
        style="margin: 10px 0"
        >更新 Access Token</n-button
      >
      <br />
      OCR 类型
      <n-select v-model:value="ocrType" :options="ocrTypes"> </n-select>
      <template #password-visible-icon>
        <n-icon :size="16" :component="GlassesOutline" />
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script>
import { GlassesOutline, ArchiveOutline } from "@vicons/ionicons5";
import { inject, ref } from "vue";
import axios from "axios";

export default {
  name: "TextOCR",
  setup() {
    const globalState = inject("globalState");
    const message = useMessage();
    const apiKey = ref(localStorage.getItem("TextOCR_apiKey"));
    const secretKey = ref(localStorage.getItem("TextOCR_secretKey"));
    const accessToken = ref(localStorage.getItem("TextOCR_accessToken"));
    const ocrType = ref(
      localStorage.getItem("TextOCR_ocrType") ?? "general_basic"
    );
    const confidence = ref(
      parseFloat(localStorage.getItem("TextOCR_confidence")) ?? 0
    );
    const ocrResult = ref(localStorage.getItem("TextOCR_ocrResult") ?? "");
    const ocrTypes = [
      { label: "通用文字识别（标准版）", value: "general_basic" },
      { label: "通用文字识别（高精度版）", value: "accurate_basic" },
      { label: "网络图片文字识别", value: "webimage" },
      { label: "手写文字识别", value: "handwriting" },
    ];
    watchEffect(() => {
      localStorage.setItem("TextOCR_apiKey", apiKey.value);
      localStorage.setItem("TextOCR_secretKey", secretKey.value);
      localStorage.setItem("TextOCR_accessToken", accessToken.value);
      localStorage.setItem("TextOCR_ocrType", ocrType.value);
      localStorage.setItem("TextOCR_confidence", confidence.value);
      localStorage.setItem("TextOCR_ocrResult", ocrResult.value);
    });
    return {
      config: ref(false),
      ocrType,
      ocrTypes,
      globalState,
      message,
      apiKey,
      secretKey,
      accessToken,
      confidence,
      ocrResult,
    };
  },
  components: {
    GlassesOutline,
    ArchiveOutline,
  },
  methods: {
    identificationRecognize() {
      let options = {
        method: "POST",
        url: `/baiduocr/oauth/2.0/token?client_id=${this.apiKey}&client_secret=${this.secretKey}&grant_type=client_credentials`,
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      };
      axios(options)
        .then((response) => {
          this.message.success("获取 Access Token 成功");
          this.accessToken = response.data.access_token;
          return response.data.access_token;
        })
        .catch((error) => {
          return this.message.error("获取 Access Token 失败");
        });
    },
    handleUpload({ file }) {
      let reader = new FileReader();
      reader.onload = (e) => {
        const imgBase64 = e.target.result;
        let formData = new FormData();
        formData.append("image", imgBase64);
        formData.append(
          "access_token",
          this.accessToken || this.identificationRecognize()
        );
        formData.append("paragraph", "true");
        formData.append("probability", "true");
        let options = {
          method: "POST",
          url: `/baiduocr/rest/2.0/ocr/v1/${this.ocrType}?access_token=${this.accessToken}`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Accept: "application/json",
          },
          data: formData,
        };
        axios(options)
          .then((response) => {
            if (this.ocrType === "webimage" || this.ocrType === "handwriting") {
              this.ocrResult = response.data.words_result
                .map((word) => word.words)
                .join("");
            } else {
              const paragraphsResult = response.data.paragraphs_result;
              const wordsResult = response.data.words_result;
              this.ocrResult = paragraphsResult
                .map((paragraph) => {
                  const words = paragraph.words_result_idx.map(
                    (idx) => wordsResult[idx].words
                  );
                  return words.join("");
                })
                .join("\n");
            }
            try {
              this.confidence =
                (response.data.words_result
                  .map((word) => word.probability.average)
                  .reduce((a, b) => a + b, 0) /
                  response.data.words_result_num) *
                100;
            } catch (error) {
              this.confidence = 0;
            }
          })
          .catch((error) => {
            return this.message.error("识别失败");
          });
      };
      reader.readAsDataURL(file.file);
    },
    insertToEditor(content) {
      this.globalState.insertContent = content
        .toString()
        .replace(/\n/g, "<br>");
    },
  },
};
</script>
