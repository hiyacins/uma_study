<template>
  <v-card>
    <v-card-title>
      <h2>分析</h2>
    </v-card-title>
    <v-card-text>
      <img alt="Vue logo" src="../assets/analyze_sample.png" />
    </v-card-text>

    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">スタッフ名前</th>
            <th class="text-left">口コミ数</th>
            <th class="text-left">平均点</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in desserts" :key="item.name">
            <td>{{ item.name }}</td>
            <td>{{ item.kuchikomi }}</td>
            <td>{{ item.average }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      desserts: [
        {
          name: "山田太郎",
          kuchikomi: 159,
          average: 4.5,
        },
        {
          name: "山田次郎",
          kuchikomi: 15,
          average: 3.5,
        },
        {
          name: "山田三郎",
          kuchikomi: 59,
          average: 4.1,
        },
      ],
    };
  },
};
</script>
