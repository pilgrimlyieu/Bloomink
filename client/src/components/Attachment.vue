<template>
  <n-card style="text-align: center">
    <n-image
      class="attachment-image"
      src="https://ziyuan.guwendao.net/siteimg/24jie/%e6%af%8d%e4%ba%b2%e8%8a%82.jpg"
    />
    <n-button text @click="() => openWebsite('https://www.gushiwen.cn')">
      <template #icon>
        <n-icon>
          <Newspaper />
        </n-icon>
      </template>
      古诗文网
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image
      class="attachment-image"
      src="https://www.shuge.org/wp-content/uploads/2024/05/tianhouanlan.jpg"
    />
    <n-button text @click="() => openWebsite('https://www.shuge.org')">
      <template #icon>
        <n-icon>
          <LibrarySharp />
        </n-icon>
      </template>
      书阁
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image
      class="attachment-image"
      src="http://www.dacihai.com.cn/static/img/bg.jpg"
    />
    <n-button text @click="() => openWebsite('http://www.dacihai.com.cn')">
      <template #icon>
        <n-icon>
          <BookSearch24Filled />
        </n-icon>
      </template>
      大辞海
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image class="attachment-image" src="https://www.zdic.net/images/home_logo.png" />
    <n-button text @click="() => openWebsite('https://www.zdic.net')">
      <template #icon>
        <n-icon>
          <BookSearch24Filled />
        </n-icon>
      </template>
      汉典
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image class="attachment-image" src="https://photo.16pic.com/00/38/49/16pic_3849884_b.jpg" />
    <n-button text @click="() => openWebsite('https://www.gzct.com')">
      <template #icon>
        <n-icon>
          <Library />
        </n-icon>
      </template>
      经典国学
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image class="attachment-image"
      src="https://baike.baidu.com/pic/%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AD%A6%E7%BD%91/9256297/1/8605f5f86d1c9131d9f9fdb4?fromModule=lemma_top-image&ct=single#aid=1&pic=8605f5f86d1c9131d9f9fdb4" />
    <n-button text @click="() => openWebsite('http://www.guoxue.com')">
      <template #icon>
        <n-icon>
          <BookLetter24Filled />
        </n-icon>
      </template>
      中国国学网
    </n-button>
  </n-card>

  <n-card style="text-align: center">
    <n-image class="attachment-image"
      src="https://raw.githubusercontent.com/xiaoyifang/goldendict-ng/3856e1e8e88b6272effaf9e8981e5bddbd92f9fe/icons/icon.svg" />
    <n-button text @click="() => openWebsite('goldendict://')">
      <template #icon>
        <n-icon>
          <BookSearch24Filled />
        </n-icon>
      </template>
      GoldenDict
    </n-button>
    <br />
    <span style="font-size: 6px">
      （需要安装
      <a href="https://github.com/xiaoyifang/goldendict-ng/releases/latest" target="_blank">GoldenDict-ng</a>
      以打开 GoldenDict 应用）</span>
  </n-card>
</template>

<script>
import { Newspaper, LibrarySharp, Library } from "@vicons/ionicons5";
import { BookSearch24Filled, BookLetter24Filled } from "@vicons/fluent";

export default {
  name: "Attachment",
  components: {
    Newspaper,
    LibrarySharp,
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
