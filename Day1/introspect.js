const os = require('os');
const process = require('process');

console.log('OS:',os.type());
console.log('Architecture:',os.arch());
console.log('CPU Cores:',os.cpus() ,'\nAll CPU Cores:',os.cpus().length);
console.log('Total memory:',os.totalmem(),'Bytes');
console.log('System Uptime:', os.uptime(),'Seconds');
console.log('Current Logged User:',os.userInfo().username);
console.log('Node Path:',process.execPath);