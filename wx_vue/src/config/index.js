// 根据环境引入不同配置 process.env.NODE_ENV
console.log('载入环境')
console.log(process.env.NODE_ENV)
const config = require('./env.' + process.env.NODE_ENV);
module.exports = config;