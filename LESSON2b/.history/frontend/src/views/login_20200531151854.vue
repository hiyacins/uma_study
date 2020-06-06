<template>
  <div class="signup">
	  <table>
		  <tr>
			  <td><h3>メールアドレス：</h3></td>
		  </tr>
		  <tr>
			  <td><input type="email" v-model="mailaddress" /></td>
		  </tr>
		  <tr>
			  <td><h3>パスワード：</h3></td>
		  </tr>
		  <tr>
			  <td><input type="password" v-model="password" /></td>
		  </tr>
	  </table>
    <div>
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
