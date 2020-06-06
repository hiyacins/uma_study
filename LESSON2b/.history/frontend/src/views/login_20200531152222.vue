<template>
  <div class="signup">
    <div>
      <h3>メールアドレス：</h3>
      <input type="email" v-model="mailaddress" />
    </div>
    <div>
      style="text-align:left;"
      <h3>パスワード：</h3>
      <input type="password" v-model="password" />
    </div>

    <button @click="signUp">登録</button>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    login: function() {
      this.$router.push("/");
    },
  },
};
</script>
