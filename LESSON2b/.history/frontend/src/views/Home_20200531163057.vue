<template>
  <div>
    <button @click="logout">ログアウト</button>
    <h1>ログイン成功！</h1>
    <img alt="Vue logo" src="../assets/logo.png" />
  </div>
</template>

<script>
export default {
  name: "Home",
  methods: {
    logout: function() {
      this.$router.push("/login");
    },
  },
};
</script>
<style>
@import url(https://fonts.googleapis.com/css?family=Open+Sans:400, 700);

.body {
  background: rgb(175, 175, 175);
  font-family: "Open Sans", sans-serif;
}
</style>
