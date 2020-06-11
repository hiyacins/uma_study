<template>
  <!-- <div class="kuchikomi">
    <h1>口コミ</h1> -->
  <v-card>
    <v-card-title>
      <h2>口コミ</h2>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="10"
      class="elevation-1"
    ></v-data-table>
  </v-card>
  <!-- </div> -->
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "日時",
          align: "start",
          sortable: false,
          value: "day",
        },
        { text: "名前", value: "name" },
        { text: "点数", value: "point" },
        { text: "内容", value: "kuchikomi" },
        { text: "担当者", value: "staff" },
        { text: "GoogleMap投稿", value: "post" },
      ],
      desserts: [
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
        {
          day: "20/01/01",
          name: "佐藤太郎",
          point: 5,
          kuchikomi: "丁寧な対応だった。",
          staff: "山田太郎",
          post: "投稿済み",
        },
      ],
    };
  },
};
</script>
