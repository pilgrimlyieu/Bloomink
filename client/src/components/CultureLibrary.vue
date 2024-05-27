<template>
  <KeepAlive>
    <n-collapse>
      <n-collapse-item
        v-for="tag in tags"
        :name="tag.tid"
        :title="`${tag.tag}（${tag.sum}）`"
      >
        <n-tag
          v-for="poem in tag.poems"
          @click="showPoetryDetail(poem.id)"
          :type="specialTagType(poem.pid)"
          style="margin: 5px 5px 0 0; cursor: pointer; user-select: none"
          size="small"
          round
        >
          《{{ getPoetryName(poem.id) }}》{{ getPoetName(poem.id) }}
        </n-tag>
      </n-collapse-item>
    </n-collapse>
  </KeepAlive>
</template>

<script>
import { useModal, NButton, NTabs, NTabPane, NImage, NTag } from "naive-ui";
import { inject } from "vue";

export default {
  name: "CultureLibrary",
  setup() {
    const globalState = inject("globalState");
    const modal = useModal();

    return {
      globalState,
      modal: modal,
      tags: globalState.tags,
      poetries: globalState.poetries,
      dialogVisible: ref(false),
    };
  },
  methods: {
    t(text) {
      return text.replace(/\n{1,2}/g, "<br>");
    },
    getPoetryName(id) {
      return this.poetries[parseInt(id)]?.name;
    },
    getPoetName(id) {
      return this.poetries[parseInt(id)]?.poet.name;
    },
    showPoetryDetail(id) {
      const poetry = this.poetries[parseInt(id)];
      const poetryDetail = this.modal.create({
        preset: "card",
        title: `《${poetry.name}》${poetry.poet.name}`,
        content: () =>
          h(
            // 添加多个 tab 切换
            NTabs,
            { type: "card" },
            {
              default: () => [
                h(NTabPane, { name: "内容" }, () => [
                  h("div", { innerHTML: this.t(poetry.content) }),
                ]),
                h(NTabPane, { name: "翻译" }, () => [
                  h("div", { innerHTML: this.t(poetry.fanyi) }),
                ]),
                h(NTabPane, { name: "赏析" }, () => [
                  h("div", { innerHTML: this.t(poetry.shangxi) }),
                ]),
                h(NTabPane, { name: "额外信息" }, () => [
                  h("div", {
                    innerHTML: this.t(poetry.about),
                  }),
                ]),
                poetry.poet?.desc
                  ? h(NTabPane, { name: "作者" }, () => [
                      h(NImage, {
                        size: 180,
                        src: poetry.poet.image,
                        "object-fit": "cover",
                      }),
                      h("div", {
                        innerHTML: this.t(`${poetry.poet.desc}`),
                      }),
                    ])
                  : null,
                h(NTabPane, { name: "其他标签" }, () => [
                  h(
                    "div",
                    { style: { display: "flex", flexWrap: "wrap" } },
                    poetry.tags.map((tag, index) =>
                      h(
                        NTag,
                        {
                          size: "large",
                          round: true,
                          style: {
                            margin: "5px 5px 0 0",
                          },
                          type: this.specialTagType(index),
                        },
                        () => tag
                      )
                    )
                  ),
                ]),
              ],
            }
          ),
        style: {
          width: "60vw",
          height: "80vh",
          overflow: "auto",
          "native-scrollbar": false,
        },
        footer: () => [
          h(
            NButton,
            {
              type: "primary",
              onClick: () => this.insertToEditor(poetry.content, poetryDetail),
              style: {
                margin: "0 10px",
              },
            },
            () => "插入"
          ),
          h(
            NButton,
            { type: "error", onClick: () => poetryDetail.destroy() },
            () => "关闭"
          ),
        ],
      });
    },
    insertToEditor(content, poetryDetail) {
      this.globalState.insertContent(
        `<blockquote>${this.t(content)}</blockquote>`
      );
      poetryDetail.destroy();
    },
    specialTagType(id) {
      return ["default", "primary", "info", "success", "warning", "error"][
        id % 6
      ];
    },
  },
};
</script>
