<template>
  <div class="login">
    <div class="login-triangle"></div>

    <h2 class="login-header">Log in</h2>

    <form class="login-container">
      <p>
        <input v-model="id_name" type="text" placeholder="Email" />
      </p>
      <p>
        <input v-model="password" type="text" placeholder="Password" />
      </p>
      <p>
        <input @click="userLogin" type="submit" value="ログイン" />
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "login",
  data() {
    return {
      authinfo:[],
      id_name: "",
      password: "",
      baseUrl: "http://127.0.0.1:5000/"
    };
  },
  created() {
    this.getLoginOk();
    // axios.get("http://127.0.0.1:5000/login").then(res => {
    //   console.log(res.data.id_name);
    //   console.log(res.data.password);
    // });
    // this.$router.push("/");
  },
  methods: {
    // ログイン認証の結果を受け取る。
    async getLoginOk(){
      try{
        let response = await axios.get(this.baseUrl + "login");
        this.authinfo = response.data;
      }catch(e){
        console.log(e);
      }
    }
    async userLogin() {
      if (!this.id_name || !this.password){
        return;
      }
      try{
        let params = {
          id_name: this.id_name,
          password: this.password
        }
      }

      // var article = {
      //   id_name: this.id_name,
      //   password: this.password
      // };
      // axios.post("http://127.0.0.1:5000/login", article).then(function(res) {
      //   console.log(res.data.id_name);
      //   console.log(res.data.password);
      // });
      // this.id_name = "";
      // this.password = "";
    }
  }
};
</script>
<style>
@import url(https://fonts.googleapis.com/css?family=Open+Sans:400, 700);

body {
  background: rgb(255, 255, 255);
  font-family: "Open Sans", sans-serif;
}

.login {
  width: 400px;
  margin: 16px auto;
  font-size: 16px;
}

/* Reset top and bottom margins from certain elements */
.login-header,
.login p {
  margin-top: 0;
  margin-bottom: 0;
}

/* The triangle form is achieved by a CSS hack */
.login-triangle {
  width: 0;
  margin-right: auto;
  margin-left: auto;
  border: 12px solid transparent;
  border-bottom-color: #28d;
}

.login-header {
  background: #28d;
  padding: 20px;
  font-size: 1.4em;
  font-weight: normal;
  text-align: center;
  text-transform: uppercase;
  color: #fff;
}

.login-container {
  background: #ebebeb;
  padding: 12px;
}

/* Every row inside .login-container is defined with p tags */
.login p {
  padding: 12px;
}

.login input {
  box-sizing: border-box;
  display: block;
  width: 100%;
  border-width: 1px;
  border-style: solid;
  padding: 16px;
  outline: 0;
  font-family: inherit;
  font-size: 0.95em;
}

.login input[type="email"],
.login input[type="password"] {
  background: #fff;
  border-color: #bbb;
  color: #555;
}

/* Text fields' focus effect */
.login input[type="email"]:focus,
.login input[type="password"]:focus {
  border-color: #888;
}

.login input[type="submit"] {
  background: #28d;
  border-color: transparent;
  color: #fff;
  cursor: pointer;
}

.login input[type="submit"]:hover {
  background: #17c;
}

/* Buttons' focus effect */
.login input[type="submit"]:focus {
  border-color: #05a;
}
</style>
