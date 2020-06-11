<template>
  <v-card>
    <v-card-title>
      <h2>DM一斉配信</h2>
    </v-card-title>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="desserts"
      :single-select="singleSelect"
      item-key="day"
      show-select
      class="elevation-1"
    >
      <template v-slot:top>
        <!-- <v-switch
          v-model="singleSelect"
          label="Single select"
          class="pa-3"
        ></v-switch> -->
        <v-toolbar flat color="white">
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">DM送信</v-btn>
            </template>
          </v-dialog>
        </v-toolbar>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      singleSelect: false,
      selected: [],
      headers: [
        {
          text: "名前",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "担当", value: "staff" },
        { text: "登録日", value: "day" },
      ],
      desserts: [
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
        {
          name: "佐藤四郎",
          staff: "山田太郎",
          day: "2020/01/01",
        },
      ],
    };
  },
};
</script>
