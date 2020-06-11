<template>
  <!-- <div class="kuchikomi">
    <h1>口コミ</h1> -->
  <v-card>
    <v-card-title>
      <h2>請求書一覧</h2>
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
          text: "店舗名",
          align: "start",
          sortable: false,
          value: "tempo",
        },
        { text: "会社名", value: "company" },
        { text: "担当者名", value: "staff" },
        { text: "プラン名", value: "plan" },
        { text: "請求額", value: "bill" },
        { text: "決算タイプ", value: "type" },
        { text: "支払いインターバル", value: "interval" },
        { text: "請求日", value: "day" },
      ],
      desserts: [
        {
          tempo: "大阪駅前店",
          company: "あいうエステ",
          staff: "山田太郎",
          plan: "",
          bill: 1000,
          type: "",
          interval: "",
          day: "2020/01/01",
        },
        {
          tempo: "大阪駅前店",
          company: "あいうエステ",
          staff: "山田太郎",
          plan: "",
          bill: 1000,
          type: "",
          interval: "",
          day: "2020/01/01",
        },
        {
          tempo: "大阪駅前店",
          company: "あいうエステ",
          staff: "山田太郎",
          plan: "",
          bill: 1000,
          type: "",
          interval: "",
          day: "2020/01/01",
        },
        {
          tempo: "大阪駅前店",
          company: "あいうエステ",
          staff: "山田太郎",
          plan: "",
          bill: 1000,
          type: "",
          interval: "",
          day: "2020/01/01",
        },
      ],
    };
  },
};
</script>
