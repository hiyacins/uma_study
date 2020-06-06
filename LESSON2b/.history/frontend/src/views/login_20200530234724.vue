<template>
  <div>
    <h1>ログイン</h1>
    <button @click="login">ログイン</button>
    <p>
      新規登録は
      <router-link to="/signup">こちら</router-link>
    </p>
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
