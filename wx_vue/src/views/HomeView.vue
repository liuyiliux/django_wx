<template>

	<div style="position:relative">
		<el-button style="position: fixed;right: 0%;" type="danger" size="small" @click="quit()">退出登录</el-button>
	</div>
	<div style="width: 50%;margin-left: 25%;">
		<el-input class="ss-input" @input="Search_act($event)" placeholder="模糊搜索，请输入关键字" v-model='ss_input' />
		<el-button type="button" style="border-radius: 0 50px 0 0;border-bottom: none; outline: none;height: 36px;">搜索
		</el-button>
	</div>
	<div style="" class="mydiv">
		<h3 style="margin-top: -7px">欢迎{{username}}使用首页传送门：
			<span style="font-size: small;color: gray">新增超链接请<a href="#/home" @click="show_new_link_div">点击这里</a></span>
		</h3>
		<ul style="list-style: none" id="myul">
			<li v-for="i in v_hrefs" :key="i">
				<span class="el-icon-lollipop" style="color: #e84393"></span>
				<a :href="i.url" target="_blank" :title="i.author+'创建'">{{i.name}}</a>
				<a @click="delete_link(i.id)" class="el-icon-delete">&nbsp;&nbsp;<span
						style="color: #e84393;cursor:pointer " v-bind:title="'刪除'+i.name"></span></a>
			</li>
			<div id="new_link_div" class=""
				style="display: none;height: 100px;position: fixed;top: 35%;left:25%;width: 50%;box-shadow: 4px 4px 6px darkgray;border: pink solid 2px">
				<el-input class="" id="new_link_name" type="text" placeholder="请输入超链接的名字" v-model="new_link_name"
					style="height: 50%;width: 80%;" />
				<el-input class="" id="new_link_url" type="text" placeholder="请输入超链接的URL" v-model="new_link_url"
					style="height: 50%;width: 80%;" />
				<span class="" style="width: 20%;height: 98px">
					<button @click="add_link" class="btn btn-default" type="button"
						style="height: 100%; outline: none;width: 50%;border-left: pink solid 2px;border-bottom:pink solid 2px ">保存</button>
					<button @click="uadd_link" class="btn btn-default" type="button"
						style="height: 100% ;outline: none;width: 50%;border-right: pink solid 2px;border-bottom:pink solid 2px">取消</button>
				</span>
			</div>

		</ul>
	</div>

</template>

<script>
	import axios from 'axios'
	export default {
		name: 'HomeView',
		data() {
			return {
				v_hrefs: [],
				new_link_name: '',
				new_link_url: '',
				ss_input: '',
				username: this.$cookies.get("username")

			}
		},
		components: {},
		methods: {
			status_check(err) {
				if (err.response.status == 403) {
					console.log('操作失败' + err);
					this.quit()
				}
			},
			login_check() {
				var v_token = this.$cookies.get("login-token");
				console.log('首页页面')
				console.log(v_token);
				if (v_token === null || v_token === 'null') {
					this.$router.push("/")
				} else {
					console.log('登录了')
				}
			},
			Search_act(event) {
				axios.get('api/geturl', {
					params: {
						event: event
					},
					headers: {
						'content-type': 'application/json',
						"AUTHORIZATION": 'jwt ' + this.$cookies.get("login-token") //token换成从缓存获取
					}
				}).then((response) => {
					this.v_hrefs = response.data.all_href;
				}).catch(err => {
					this.status_check(err)
				})
			},
			quit() {
				this.$cookies.set("login-token",null,0);
				this.$cookies.set("username",null,0);
				this.$cookies.remove("login-token");
				this.$cookies.remove("username");
				this.$router.push("/")
			},
			show_new_link_div() {
				document.getElementById('new_link_div').style.display = 'block'
			},
			uadd_link() {
				document.getElementById("new_link_div").style.display = 'none';
			},
			geturl() {
				axios.get('api/geturl', {
					headers: {
						'content-type': 'application/json',
						"AUTHORIZATION": 'jwt ' + this.$cookies.get("login-token") //token换成从缓存获取
					}
				}).then((response) => {
					this.v_hrefs = response.data.all_href;
				}).catch(err => {
					this.status_check(err)
				})
			},
			delete_link(id) {
				axios.post('api/delete_href/', {
					id: id,
				}, {
					headers: {
						'content-type': 'application/json',
						"AUTHORIZATION": 'jwt ' + this.$cookies.get("login-token") //token换成从缓存获取
					}
				}).then(res => {
					if (res.data.status == 200) {
						this.$message.info('删除成功');
						document.location.reload();
					} else {
						let self = this
						self.$alert(res.data.error, '删除失败', {
							confirmButtonText: '确定',
							callback: action => { // eslint-disable-line no-unused-vars
								document.location.reload();
							}
						})
					}
				}).catch(err => {
					this.status_check(err)
				})
			},
			add_link() {
				axios.post('api/add_href/', {
					new_link_name: this.new_link_name,
					new_link_url: this.new_link_url
				}, {
					headers: {
						'content-type': 'application/json',
						"AUTHORIZATION": 'jwt ' + this.$cookies.get("login-token") //token换成从缓存获取
					}
				}).then(res => {
					if (res.data.status == 200) {
						this.$message.info('添加成功');
						document.location.reload();
					} else {
						let self = this
						self.$alert(res.data.error, '添加失败', {
							confirmButtonText: '确定',
							callback: action => { // eslint-disable-line no-unused-vars
								document.location.reload();
							}
						})

					}
				}).catch(err => {
					this.status_check(err)
				})
			}
		},
		mounted() { //这个属性就可以，在里面声明初始化时要调用的方法即可
			// we can implement any method here like
			this.geturl(),
				this.login_check()
		}
	}
</script>

<style>
	.mydiv {
		border-radius: 5px;
		box-shadow: 4px 4px 8px gray;
		background-color: #eaeaea;
		height: 800px;
		margin-left: 10%;
		padding: 10px;
		margin-right: 10%;
	}

	.mydiv li {
		float: left;
		width: 25%;
	}

	.mydiv li a {
		text-decoration: none;
		color: transparent;
		background: linear-gradient(to top, black, #fd59f1);
		-webkit-background-clip: text;
		font-size: large;
	}

	.ss-input {
		width: 50%;
	}

	.el-input__inner {
		border-top-left-radius: 50px;
	}

	#new_link_name {
		margin-top: 5px;
		border-top-left-radius: 0px;
	}

	#new_link_url {
		border-top-left-radius: 0px;
	}
</style>
