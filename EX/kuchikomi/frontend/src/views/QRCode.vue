<template>
  <v-card>
    <v-card-title>
      <h2>QRコード設定</h2>
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-row>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-col cols="12" md="100">
              <v-text-field
                v-model="inputText"
                label="変換したいURLを入力"
              ></v-text-field>
              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-8"
                @click="generate"
              >
                生成
              </v-btn>
            </v-col>
            <v-col md="10">
              <vue-qrcode
                v-if="targetText"
                :value="targetText"
                :options="option"
                tag="img"
              >
              </vue-qrcode>
              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-8"
                @click="dl"
              >
                ダウンロード
              </v-btn>
            </v-col>
          </v-form>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import VueQrcode from "@chenfengyuan/vue-qrcode";
export default {
  components: {
    VueQrcode,
  },
  data() {
    return {
      inputText: "",
      targetText: "",
      option: {
        errorCorrectionLevel: "M",
        maskPattern: 0,
        margin: 10,
        scale: 2,
        width: 300,
        color: {
          dark: "#000000FF",
          light: "#FFFFFFFF",
        },
      },
    };
  },
  methods: {
    generate: function() {
      this.targetText = this.inputText;
    },
  },
};
</script>
<style scoped></style>
