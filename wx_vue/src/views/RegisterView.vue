<template>
	<div class="bg">
		<div id="register">
			<h2>注册页面</h2>
			<el-form ref="form" :model="form" label-width="20%">
				<el-form-item label="用户名:">
					<el-input v-model="form.username" placeholder="username"></el-input>
				</el-form-item>
				<el-form-item label="密  码:">
					<el-input v-model="form.password" type="password" placeholder="password"></el-input>
				</el-form-item>
				<el-form-item label="邮 箱:">
					<el-input v-model="form.email" placeholder="email"></el-input>
				</el-form-item>
				<el-form-item label="验证码:">
					<el-input v-model="form.emailcode" style="width: 49%;margin-right: 2%;"></el-input>
					<el-button type="primary" :disabled=yzm_disabled style="width: 49%;" @click="sendcode">{{yzm_txt}}
					</el-button>
				</el-form-item>
			</el-form>
			<el-button type="primary" round @click="register" class="btn">注册</el-button>
		</div>
	</div>
</template>
<script>
	import {ElMessage} from 'element-plus' // eslint-disable-line no-unused-vars
	import axios from 'axios'
	axios.defaults.withCredentials = true;
	export default {
		data() {
			return {
				time: 0,
				yzm_disabled: false,
				yzm_txt: "获取验证码",
				form: {
					username: '',
					password: '',
					email: '',
					emailcode: ''
				},
				isnull: false
			};
		},
		components: {},
		methods: {
			register() {
				var regstr = /^[a-zA-Z0-9_-]{3,15}$/
				if (this.form.username == '') {
					this.$message.error('用户名不能为空');
				} else if (this.form.password == '') {
					this.$message.error('密码不能为空');
				}  else if (this.form.emailcode == '') {
					this.$message.error('验证码不能为空');
				} else if(!regstr.test(this.form.username)){
					this.$message.error('用户名格式不正确(3-15字符的大小写字母和数字下划线)');
				} else if(!regstr.test(this.form.password)){
					this.$message.error('密码格式不正确(3-15字符的大小写字母和数字下划线)');
				}
				else {
					axios.post('http://localhost:8000/api/register/', {
							emailcode: this.form.emailcode,
							username: this.form.username,
							email: this.form.email,
							password: this.form.password
					}).then(res => {
						if (res.data.status == 200) {
							let self = this
							self.$confirm("注册成功", "是否返回登录页", {
								confirmButtonText: "确认",
								cancelButtonText: "取消",
								type: "success",
								distinguishCancelAndClose: false, // 设置为true才会把右上角X和取消区分开来
								closeOnClickModal: false
							}).then(function() {
								self.$router.push('/')
							}).catch(function(e) {
								if (e == 'cancel') {
									console.log("取消");
								} else if (e == 'close') {
									console.log("取消");
								}
							})
						} else if (res.data.status == 202) {
							let self = this
							self.$alert('用户名已存在', '注册失败', {
								confirmButtonText: '确定',
								callback: action => { // eslint-disable-line no-unused-vars
									this.form.username = '',
									this.form.password = ''
								}
							})
						} else if (res.data.status == 203) {
							let self = this
							self.$alert('验证码错误', '注册失败', {
								confirmButtonText: '确定',
								callback: action => { // eslint-disable-line no-unused-vars
									this.form.emailcode = ''
								}
							})
						} else {
							let self = this
							self.$alert(res.data.error, '注册失败', {
								confirmButtonText: '确定',
								callback: action => { // eslint-disable-line no-unused-vars
									this.form.emailcode = ''
								}
							})
						}
					}).catch(err => {
						console.log('操作失败' + err);
					})
				}
			},
			sendcode() {
				var regEmail = /^[a-zA-Z0-9_-]+([-_.][a-zA-Z0-9_-]+)*@([a-zA-Z0-9_-]+[-.])+[a-zA-Z0-9_-]{2,5}$/;
				if (this.form.email == '') {
					alert("请输入邮箱");
				} else if (!regEmail.test(this.form.email)) {
					alert("邮箱格式不正确");
				} else {
					this.time = 60;
					this.yzm_disabled = true;
					this.timer();
					axios.post('http://localhost:8000/api/sendcode/', {
							email: this.form.email
					}).then(res => {
						console.log('发送成功'+res);
					}).catch(err => {
						console.log('操作失败' + err);
					})
				}
			},
			timer() {
				if (this.time > 0) {
					this.time--;
					this.yzm_txt = this.time + "s后重新获取";
					setTimeout(this.timer, 1000);
				} else {
					this.time = 0;
					this.yzm_txt = "获取验证码";
					this.yzm_disabled = false;
				}
			}
		}
	}
</script>

<style scoped>
	.bg {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background: url('../assets/login-bg3.jpg');
		background-size: 100% 100%;
	}

	#register {
		min-height: 40%;
		width: 350px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.25);
		background: #ffffff;
		opacity: 0.85;
		position: absolute;
		top: 20%;
		left: 40%;
		text-align: center;
		display: flex;
		flex-direction: column;
		/*横向*/
		padding: 30px;
	}

	#register h2 {
		padding-bottom: 30px;
	}

	.btn {
		width: 60%;
		margin: auto;
	}
</style>
