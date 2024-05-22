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
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => copyToClipboard(ocrLaTeX)"
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
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => copyToClipboard(ocrInline)"
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
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => copyToClipboard(ocrDisplay)"
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
      style="margin: 8px 0"
    />
  </KeepAlive>
  <n-button
    secondary
    type="primary"
    size="small"
    round
    @click="() => copyToClipboard(ocrMarkdown)"
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
        v-model:value="appID"
        type="password"
        show-password-on="click"
        placeholder="App ID"
        style="margin: 10px 0"
      />
      App Key
      <n-input
        v-model:value="appKey"
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
import useClipboard from "vue-clipboard3";

export default {
  name: "FormulaOCR",
  setup() {
    const globalState = inject("globalState");
    const message = useMessage();
    const appID = ref(localStorage.getItem("FormulaOCR_appID"));
    const appKey = ref(localStorage.getItem("FormulaOCR_appKey"));
    const inlineDelimiter = ref(
      parseInt(localStorage.getItem("FormulaOCR_inlineDelimiter")) ?? 0
    );
    const displayDelimiter = ref(
      parseInt(localStorage.getItem("FormulaOCR_displayDelimiter")) ?? 0
    );
    const inlineDelimiterList = [
      ["$", "$"],
      ["\\(", "\\)"],
    ];
    const displayDelimiterList = [
      ["$$", "$$"],
      ["\\[", "\\]"],
      ["\\begin{equation}", "\\end{equation}"],
    ];
    const inlineDelimiters = inlineDelimiterList.map((item, index) => ({
      label: `${item[0]}...${item[1]}`,
      value: index,
    }));
    const displayDelimiters = displayDelimiterList.map((item, index) => ({
      label: `${item[0]} ... ${item[1]}`,
      value: index,
    }));
    const currentInlineDelimiter = inlineDelimiterList[inlineDelimiter.value];
    const currentDisplayDelimiter =
      displayDelimiterList[displayDelimiter.value];
    const ocrLaTeX = ref(localStorage.getItem("FormulaOCR_ocrLaTeX") ?? "");
    const ocrInline = ref(
      localStorage.getItem("FormulaOCR_ocrInline") ??
        (ocrLaTeX.value
          ? `${currentInlineDelimiter[0]}${ocrLaTeX.value}${currentInlineDelimiter[1]}`
          : "")
    );
    const ocrDisplay = ref(
      localStorage.getItem("FormulaOCR_ocrDisplay") ??
        (ocrLaTeX.value
          ? `${currentDisplayDelimiter[0]}\n${ocrLaTeX.value}\n${currentDisplayDelimiter[1]}`
          : "")
    );
    const ocrMarkdown = ref(
      localStorage.getItem("FormulaOCR_ocrMarkdown") ?? ""
    );
    const confidence = ref(
      parseFloat(localStorage.getItem("FormulaOCR_confidence")) ?? 0
    );
    watchEffect(() => {
      localStorage.setItem("FormulaOCR_appID", appID.value);
      localStorage.setItem("FormulaOCR_appKey", appKey.value);
      localStorage.setItem("FormulaOCR_inlineDelimiter", inlineDelimiter.value);
      localStorage.setItem(
        "FormulaOCR_displayDelimiter",
        displayDelimiter.value
      );
      localStorage.setItem("FormulaOCR_ocrLaTeX", ocrLaTeX.value);
      localStorage.setItem("FormulaOCR_ocrInline", ocrInline.value);
      localStorage.setItem("FormulaOCR_ocrDisplay", ocrDisplay.value);
      localStorage.setItem("FormulaOCR_ocrMarkdown", ocrMarkdown.value);
      localStorage.setItem("FormulaOCR_confidence", confidence.value);
    });
    return {
      config: ref(false),
      globalState,
      message,
      appID,
      appKey,
      inlineDelimiter,
      displayDelimiter,
      inlineDelimiters,
      displayDelimiters,
      inlineDelimiterList,
      displayDelimiterList,
      ocrLaTeX,
      ocrInline,
      ocrDisplay,
      ocrMarkdown,
      confidence,
      copy: async (content) => {
        const { toClipboard } = useClipboard();
        await toClipboard(content);
      },
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
        let inlineDelimiter = this.inlineDelimiterList[this.inlineDelimiter];
        let displayDelimiter = this.displayDelimiterList[this.displayDelimiter];
        let data = {
          src: imgBase64,
          idiomatic_eqn_arrays: true,
          formats: ["text", "latex_styled"],
          math_inline_delimiters: inlineDelimiter,
          math_display_delimiters: displayDelimiter,
        };
        let options = {
          method: "POST",
          url: `/mathpixocr/v3/text`,
          headers: {
            "Content-Type": "application/json",
            app_id: this.appID,
            app_key: this.appKey,
          },
          data: JSON.stringify(data),
        };
        axios(options)
          .then((response) => {
            if (response.data.latex_styled !== undefined) {
              this.ocrLaTeX = response.data.latex_styled;
              this.ocrInline = `${inlineDelimiter[0]}${response.data.latex_styled}${inlineDelimiter[1]}`;
              this.ocrDisplay = `${displayDelimiter[0]}\n${response.data.latex_styled}\n${displayDelimiter[1]}`;
            }
            this.ocrMarkdown = response.data.text ?? "";
            this.confidence = response.data.confidence * 100;
            return response.data;
          })
          .catch((error) => {
            return this.message.error("识别失败");
          });
      };
      reader.readAsDataURL(file.file);
    },
    insertToEditor(content) {
      this.globalState.insertContent(content.toString().replace(/\n/g, "<br>"));
    },
    copyToClipboard(content) {
      this.copy(content)
        .then(() => {
          this.message.success("复制成功");
        })
        .catch(() => {
          this.message.error("复制失败");
        });
    },
  },
};
</script>
