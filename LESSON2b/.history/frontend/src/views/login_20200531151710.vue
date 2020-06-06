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
      <h3>メールアドレス：</h3>
      <input type="email" v-model="mailaddress" />
    </div>
    <div>
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
