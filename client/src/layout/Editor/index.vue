<template>
  <div id="vditor"></div>
</template>

<script setup>
import Vditor from "vditor";
import "vditor/dist/index.css";
import { onMounted, ref, inject } from "vue";

const vditor = ref(null);
const globalState = inject("globalState");

onMounted(() => {
  vditor.value = new Vditor("vditor", {
    height: "85vh",
    width: "65vw",
    toolbar: [
      "emoji",
      "headings",
      "bold",
      "italic",
      "strike",
      "link",
      "|",
      "list",
      "ordered-list",
      "check",
      "outdent",
      "indent",
      "|",
      "quote",
      "line",
      "code",
      "inline-code",
      "insert-before",
      "insert-after",
      "|",
      "upload",
      "table",
      "|",
      "undo",
      "redo",
      "|",
      "fullscreen",
      "edit-mode",
      "both",
      "preview",
      "help",
    ],
    toolbarConfig: {
      pin: true,
    },
    preview: {
      delay: 500,
    },
    mode: "wysiwyg",
    placeholder: "开启文化传承之旅吧！",
  });
});

globalState.insertContent = (content) => {
  vditor.value.insertValue(content);
};
globalState.getContent = () => {
  return vditor.value.getValue();
};
</script>
