<template>
  

    
      ログイン成功！
      <img alt="Vue logo" src="../assets/logo.png" />
    
    <button @click="logout">ログアウト</button>
  </div>
</template>

<script>
export default {
  name: "Home",
  methods: {
    logout: function() {
      this.$router.push("/login")
    }
  }
};
</script>
