var logMap = {}
var fs = require('fs');
var f = fs.createWriteStream('./videos.json', {
    flags: 'a' // 'a' means appending (old data will be preserved)
})

module.exports = {
    summary: 'a rule to modify response',
    * beforeSendResponse(requestDetail, responseDetail) {
        console.log("========================================");
        console.log(requestDetail.url);
        if (/https:\/\/aweme.snssdk.com\/aweme\/v1\/aweme\/post\//i.test(requestDetail.url)) {
            try { //防止报错退出程序
                console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                f.write(responseDetail.response.body + '\r\n');
            } catch (e) {    
                console.log(e);
            }
        }
    },
};