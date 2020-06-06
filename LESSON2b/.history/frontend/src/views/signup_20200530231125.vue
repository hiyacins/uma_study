<template>
  

    新規登録
    
      ログインは
      こちら
    
    
      

      

      新規登録
    
  </div>
</template>


<script>
export default {
	name: 'Signup',
	data () {
	  return {
	    username: '',
	    password: ''
	  }
	},
	methods: {
	  signup: function () {
	    alert("登録されたアドレスにメールを送信しました！確認してください");
	    this.$router.push('/login')
	  }
	}
}
</script>
