<template>
  <v-card>
    <v-card-title>
      <h2>アンケート作成</h2>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="10">
            Q. 総合評価はどれくらいでしょうか？<br />
            ★1：不満 ⇔ ★5：満足
            <v-rating
              v-model="rating"
              background-color="orange lighten-3"
              color="orange"
            ></v-rating>
          </v-col>
          <v-col cols="12" sm="6" md="5">
            <v-textarea label="Q. ご意見ご感想をお願い致します。"></v-textarea>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>
