<template>
  <div class="container login-container">
    <div class="row">
      <div class="col-md-6 login-form-1">
        <h3>ログイン画面</h3>
        <form action="" method="POST">
          <div class="form-group">
            <input
              type="text"
              name="id_name"
              class="form-control"
              placeholder="Your ID *"
              value=""
            />
          </div>
          <div class="form-group">
            <input
              type="password"
              name="password"
              class="form-control"
              placeholder="Your Password *"
              value=""
            />
          </div>
          <div class="form-group">
            <input type="submit" class="btnSubmit" value="ログイン" />
          </div>
          <div class="form-group">
            <a href="#" class="ForgetPwd">＞＞パスワードを忘れた方</a>
          </div>
        </form>
      </div>
    </div>
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
<style></style>
