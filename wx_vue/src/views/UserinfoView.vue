<template>
	<div style="width: 50%;margin-left: 25%;">
		<!-- <el-input  placeholder="模糊搜索，请输入关键字" style="text-align: center;border-radius:50px 0 0 0 ;border-bottom: none"></el-input> -->
		<span style="">
			<button  type="button" style="border-radius: 0 50px 0 0;border-bottom: none; outline: none;">搜索</button>
		</span>
	</div>
	<div style="height: 500px;" class="mydiv">
		<h3 style="margin-top: -7px">欢迎使用首页传送门：<span style="font-size: small;color: gray">新增超链接请<a href="#" onclick="javascript:document.getElementById('new_link_div').style.display='block'">点击这里</a></span></h3>
		<ul style="list-style: none" id="myul">
			<li v-for="i in v_hrefs">
				<span class="glyphicon glyphicon-link" style="color: #e84393" ></span><a :href="[[ i.url ]]" target="_blank" :title="[[i.author]]+'创建'">[[
				i.name ]]</a><a @click="delete_link(i.id)" style="">&nbsp<span class="glyphicon glyphicon-trash" style="color: #e84393;cursor:pointer " v-bind:title="'刪除'+[[i.name]]"></span></a>
			</li>

			<div id="new_link_div" class="input-group"
				 style="display: none;height: 100px;position: fixed;top: 35%;left:25%;width: 50%;box-shadow: 4px 4px 6px darkgray;border: pink solid 2px">
				<input id="new_link_name" type="text" class="form-control" placeholder="请输入超链接的名字"
					   style="height: 50%;width: 80%">
				<input id="new_link_url" type="text" class="form-control" placeholder="请输入超链接的URL"
					   style="height: 50%;width: 80%">
				<span class="input-group-btn" style="width: 20%;height: 98px">
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

export default {
  name: 'HomeView',
  components: {
  }
}
</script>

<style>
    .mydiv{
		border-radius:5px;
		box-shadow: 4px 4px 8px gray;
		background-color: #eaeaea;
		width: 90%;
		margin-left: 5%;
		padding: 10px;
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
</style>