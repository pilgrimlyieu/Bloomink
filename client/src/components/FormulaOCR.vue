<template>
  <n-space justify="center" style="margin-bottom: 3px">
    <n-button type="error" secondary round size="small" @click="config = true"
      >配置 MathpixOCR API</n-button
    ></n-space
  >
  <KeepAlive>
    <n-upload multiple directory-dnd :max="1" :custom-request="handleUpload">
      <n-upload-dragger>
        <div style="margin-bottom: 8px">
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
      v-model:value="ocrLaTeX"
      type="text"
      rows="1"
      placeholder="LaTeX"
      disabled
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => insertToEditor(ocrLaTeX)"
    >复制 LaTeX</n-button
  >
  <n-button
    secondary
    type="info"
    size="small"
    round
    @click="() => insertToEditor(ocrLaTeX)"
    >插入 LaTeX</n-button
  >
  <br />
  <KeepAlive>
    <n-input
      v-model:value="ocrInline"
      type="text"
      rows="1"
      placeholder="行内公式"
      disabled
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => insertToEditor(ocrInline)"
    >复制行内公式</n-button
  >
  <n-button
    secondary
    type="info"
    size="small"
    round
    @click="() => insertToEditor(ocrInline)"
    >插入行内公式</n-button
  >
  <br />
  <KeepAlive>
    <n-input
      v-model:value="ocrDisplay"
      type="text"
      rows="1"
      placeholder="行间公式"
      disabled
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => insertToEditor(ocrDisplay)"
    >复制行间公式</n-button
  >
  <n-button
    secondary
    type="info"
    size="small"
    round
    @click="() => insertToEditor(ocrDisplay)"
    >插入行间公式</n-button
  >
  <br />
  <KeepAlive>
    <n-input
      v-model:value="ocrMarkdown"
      type="text"
      rows="1"
      placeholder="Mathpix Markdown"
      disabled
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => insertToEditor(ocrMarkdown)"
    >复制 MD</n-button
  >
  <n-button
    secondary
    type="info"
    size="small"
    round
    @click="() => insertToEditor(ocrMarkdown)"
    >插入 MD</n-button
  >

  <n-progress
    type="line"
    :percentage="confidence"
    :indicator-placement="'inside'"
    :stroke-width="10"
    :status="'warning'"
    style="margin: 5px 0"
  >
    置信度 {{ confidence.toFixed(2) }}%
  </n-progress>

  <n-drawer v-model:show="config" :width="500" placement="right">
    <n-drawer-content title="百度 OCR API 配置">
      App ID
      <n-input
        v-model:value="ID"
        type="password"
        show-password-on="click"
        placeholder="App ID"
        style="margin: 10px 0"
      />
      App Key
      <n-input
        v-model:value="KY"
        type="password"
        show-password-on="click"
        placeholder="App Key"
        style="margin: 10px 0"
      />
      <br />
      行内公式分隔符
      <n-select v-model:value="inlineDelimiter" :options="inlineDelimiters">
      </n-select>
      行间公式分隔符
      <n-select v-model:value="displayDelimiter" :options="displayDelimiters">
      </n-select>
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
  name: "FormulaOCR",
  setup() {
    const globalState = inject("globalState");
    const message = useMessage();
    const ID = ref(localStorage.getItem("ID"));
    const KY = ref(localStorage.getItem("KY"));
    const inlineDelimiter = ref(localStorage.getItem("inlineDelimiter") || "$");
    const displayDelimiter = ref(
      localStorage.getItem("displayDelimiter") || "$$"
    );
    const inlineDelimiters = [
      { label: "$...$", value: "$" },
      { label: "\\(...\\)", value: "()" },
    ];
    const displayDelimiters = [
      { label: "$$ ... $$", value: "$$" },
      { label: "\\[ ... \\]", value: "[]" },
      {
        label: "\\begin{equation} ... \\end{equation}",
        value: "equation",
      },
    ];
    watchEffect(() => {
      localStorage.setItem("ID", ID.value);
      localStorage.setItem("KY", KY.value);
      localStorage.setItem("inlineDelimiter", inlineDelimiter.value);
      localStorage.setItem("displayDelimiter", displayDelimiter.value);
    });
    return {
      config: ref(false),
      globalState,
      message,
      ID,
      KY,
      inlineDelimiter,
      displayDelimiter,
      inlineDelimiters,
      displayDelimiters,
      ocrLaTeX: ref(null),
      ocrInline: ref(null),
      ocrDisplay: ref(null),
      ocrMarkdown: ref(null),
      confidence: ref(0),
    };
  },
  components: {
    GlassesOutline,
    ArchiveOutline,
  },
  methods: {
    handleUpload({ file }) {
      let reader = new FileReader();
      reader.onload = (e) => {
        const imgBase64 = e.target.result;
        let formData = new FormData();
        let inlineDelimiter = {
          $: ["$", "$"],
          "()": ["\\(", "\\)"],
        }[this.inlineDelimiter];
        let displayDelimiter = {
          $$: ["$$", "$$"],
          "[]": ["\\[", "\\]"],
          equation: ["\\begin{equation}", "\\end{equation}"],
        }[this.displayDelimiter];
        formData.append("src", imgBase64);
        formData.append("idiomatic_eqn_arrays", "true");
        formData.append("formats", ["text", "latex_styled"]);
        formData.append("math_inline_delimiter", inlineDelimiter);
        formData.append("math_display_delimiter", displayDelimiter);
        let options = {
          method: "POST",
          url: `/mathpixocr/v3/text`,
          headers: {
            "Content-Type": "application/json",
            app_id: this.ID,
            app_key: this.KY,
            Accept: "application/json",
          },
          data: formData,
        };
        axios(options)
          .then((response) => {
            this.message.success("识别成功");
            this.ocrLaTeX = response.data.latex_styled;
            this.ocrInline = `${inlineDelimiter[0]}${response.data.text}${inlineDelimiter[1]}`;
            this.ocrDisplay = `${displayDelimiter[0]}\n${response.data.text}\n${displayDelimiter[1]}`;
            this.ocrMarkdown = response.data.text;
            this.this.confidence = response.data.confidence;
            return response.data;
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
