<template>
  <div class="signup">
    <table>
      <tr>
        <th>メールアドレス：</th>
      </tr>
      <tr>
        <td></td>
      </tr>
      <tr>
        <th>パスワード：</th>
      </tr>
      <tr>
        <td></td>
      </tr>
    </table>

    <div>
      <h2>メールアドレス：</h2>
      <input type="email" v-model="mailaddress" />
    </div>
    <input type="password" v-model="password" />
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
