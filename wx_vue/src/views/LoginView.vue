<template>
  <div class="login-view">
    <div class="login" id="login" v-loading="waiting">
      <!-- 背景图 -->
      <div class="log-bg">
        <div class="log-cloud cloud1"></div>
        <div class="log-cloud cloud2"></div>
        <div class="log-cloud cloud3"></div>
        <div class="log-cloud cloud4"></div>
        <div class="log-logo">欢迎光临!</div>
        <div class="log-text">登录页面</div>
      </div>
      <!-- 输入区 -->
      <div class="log-email">
        <input type="text" placeholder="username" :class="'log-input' + (username==''?' log-input-empty':'')" v-model="username">
        <input type="password" placeholder="Password" :class="'log-input' + (password==''?' log-input-empty':'')"  v-model="password">
        <button href="javascript:;"  class="log-btn" @click="registerHandle()"  style="border-style: none;">注册</button>
        <button href="javascript:;" class="log-btn" @click="loginHandle()"  style="border-style: none;">登录</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import axios from 'axios'
export default {
  data() {
    return {
      waiting: false,
      username: "",
      password: "",
    }
  },
  components: {
  },
  methods: {
	logined_check() {
	var v_token = this.$cookies.get("login-token");
	console.log('登录页面')
	console.log(v_token)
	if (v_token === null || v_token === 'null'){
		console.log('请登录')
	}else{
		this.$router.push("/home")
	}
	}
	,
    loginHandle() {
		if (this.username === "" || this.password === "") {
			ElMessage("请填写用户名和密码")
        return;
		}
		// 向后端发送登录参数
		axios.post('api/login/', {
				username: this.username,
				password: this.password
		}).then(res => {
			if (res.data.status == 200) {
				let expireTime = 1000 * 60 * 120;
				var v_headers = res.headers
				this.$cookies.set("login-token",v_headers.token , expireTime);
				this.$cookies.set("username", this.username, expireTime);
				this.$router.push("/home");
			} else {
				let self = this
				self.$alert(res.data.error, '登录失败', {
					confirmButtonText: '确定',
					callback: action => { // eslint-disable-line no-unused-vars
						this.username = '',
						this.password = ''
					}
				})
			}
		}).catch(err => {
			console.log('操作失败' + err);
		})		
    },
    registerHandle() {
        this.$router.push("/register");
    }
  },
	mounted() { //这个属性就可以，在里面声明初始化时要调用的方法即可
			// we can implement any method here like
		console.log('测试全局变量')
		console.log(this.$config)
		this.logined_check()
		}
}
</script>

<style scoped>
.login-view {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  background-image: url(../assets/bg-page.jpg);
   background-size: 100% 100%;
}

.login{position: fixed; overflow: hidden;left: 50%; margin-left: -250px; top:50%; margin-top: -350px; width: 500px; min-height: 555px; z-index: 10; right: 140px; background: #fff;-webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px; -webkit-box-shadow:  0px 3px 16px -5px #070707; box-shadow:  0px 3px 16px -5px #070707}
.log-close{display: block; position: absolute; top:12px; right: 12px; opacity: 1;}
.log-close:hover .icons{transform: rotate(180deg);}
.log-close .icons{opacity: 1; transition: all .3s}
.log-cloud{background-image: url(../assets/login-cloud.png); width: 63px ;height: 40px; position: absolute; z-index: 1}
.login .cloud1{top:21px; left: -30px; transform: scale(.6); animation: cloud1 20s linear infinite;}
.login .cloud2{top:87px; right: 20px; animation: cloud2 19s linear infinite;}
.login .cloud3{top:160px; left: 5px;transform: scale(.8);animation: cloud3 21s linear infinite;}
.login .cloud4{top:150px; left: -40px;transform: scale(.4);animation: cloud4 19s linear infinite;}
.log-bg{background: url(../assets/login-bg3.jpg); background-size: cover; width: 100%; height: 312px; overflow: hidden;}
.log-logo{height: 80px; margin: 120px auto 25px; text-align: center; color: #ffeb73 /* #1fcab3 */; font-weight: bold; font-size: 40px;}
.log-text{color: #57d4c3; font-size: 13px; text-align: center; margin: 0 auto;}
.log-logo,.log-text{z-index: 2}
.icons{background:url(../assets/icons.png) no-repeat; display: inline-block;}
.close{height:16px;width:16px;background-position:-13px 0;}
.login-email{height:17px;width:29px;background-position:-117px 0;}

/* .log-btns{padding: 15px 0; margin: 0 auto;} */
.log-btn{width:200px; display: inline-block; text-align: left; line-height: 50px;margin-left:2px; height:50px; color:#fff; font-size:13px;-webkit-border-radius: 5px; 
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;
position: relative;}
.log-btn:hover,.log-btn:focus{color: #fff; opacity: .8;}

.log-btn{background-color: #50E3CE;text-align: center;}
.log-input-empty{border: 1px solid #f37474 !important;}
.isloading{background: #d6d6d6}
.log-btn .icons{margin-left: 30px; vertical-align: middle;}
.log-btn .text{left: 95px; line-height: 50px; text-align: left; position: absolute;}
.log-input{width: 370px;overflow: hidden; padding: 0 15px;font-size: 13px; border: 1px solid #EBEBEB; margin:0 auto 15px; height: 48px; line-height: 48px; -webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px;}
.log-input.warn{border: 1px solid #f88787}

 @-webkit-keyframes cloud1 {  
    0%{left: 200px}  
    100%{left:-130px;} 
}
@keyframes cloud1{
    0%{left: 200px}  
    100%{left:-130px;} 
}

 @-webkit-keyframes cloud2 {  
    0%{left:500px;}  
    100%{left:-90px;} 
}
@keyframes cloud2{
    0%{left:500px;}  
    100%{left:-90px;} 
}

@-webkit-keyframes cloud3 {  
    0%{left:620px;}  
    100%{left:-70px;} 
}
@keyframes cloud3{
    0%{left:620px;}  
    100%{left:-70px;} 
}@-webkit-keyframes cloud4 {  
    0%{left:100px;}  
    100%{left:-70px;} 
}
@keyframes cloud4{
    0%{left:100px;}  
    100%{left:-70px;} 
}
</style>