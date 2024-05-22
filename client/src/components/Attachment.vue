<template>
  <n-card
    v-for="attachment in attachments"
    :key="attachment.name"
    style="text-align: center"
  >
    <n-image class="attachment-image" :src="attachment.image" />
    <n-button text @click="() => openWebsite(attachment.url)">
      <template #icon>
        <n-icon>
          <component :is="attachment.icon" />
        </n-icon>
      </template>
      {{ attachment.name }}
    </n-button>
    <span v-html="attachment.extra" />
  </n-card>
</template>

<script>
import { Newspaper, Library } from "@vicons/ionicons5";
import { BookSearch24Filled, BookLetter24Filled } from "@vicons/fluent";

export default {
  name: "Attachment",
  data() {
    return {
      attachments: [
        {
          name: "古诗文网",
          url: "https://www.gushiwen.cn",
          image:
            "https://ziyuan.guwendao.net/siteimg/24jie/%e6%af%8d%e4%ba%b2%e8%8a%82.jpg",
          icon: Newspaper,
          extra: "",
        },
        {
          name: "书阁",
          url: "https://www.shuge.org",
          image:
            "https://www.shuge.org/wp-content/uploads/2024/05/tianhouanlan.jpg",
          icon: Library,
          extra: "",
        },
        {
          name: "经典国学",
          url: "https://www.gzct.com",
          image: "https://photo.16pic.com/00/38/49/16pic_3849884_b.jpg",
          icon: Library,
          extra: "",
        },
        {
          name: "中国国学网",
          url: "http://www.guoxue.com",
          image:
            "https://pilgrimlyieu.github.io/daily/2024-01/12-Raizakura.jpg",
          icon: BookLetter24Filled,
          extra: "",
        },
        {
          name: "大辞海",
          url: "http://www.dacihai.com.cn",
          image: "http://www.dacihai.com.cn/static/img/bg.jpg",
          icon: BookSearch24Filled,
          extra: "",
        },
        {
          name: "汉典",
          url: "https://www.zdic.net",
          image: "https://www.zdic.net/images/home_logo.png",
          icon: BookSearch24Filled,
          extra: "",
        },
        {
          name: "GoldenDict",
          url: "goldendict://",
          image:
            "https://raw.githubusercontent.com/xiaoyifang/goldendict-ng/3856e1e8e88b6272effaf9e8981e5bddbd92f9fe/icons/icon.svg",
          icon: BookSearch24Filled,
          extra:
            '<span style="font-size: 6px"><br /> （需要安装 <a href="https://github.com/xiaoyifang/goldendict-ng/releases/latest" target="_blank" >GoldenDict-ng</a > 以打开 GoldenDict 应用）</span >',
        },
      ],
    };
  },
  components: {
    Newspaper,
    BookSearch24Filled,
    Library,
    BookLetter24Filled,
  },
  methods: {
    openWebsite(url) {
      window.open(url);
    },
  },
};
</script>

<style scoped>
.attachment-image {
  height: 250px;
  width: 250px;
  margin: auto;
  overflow: hidden;
}
.attachment-image img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>
