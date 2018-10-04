# Install AnyProxy
1. Install NodeJS first

    Linux:      $yum install nodejs 

    Windows:    https://nodejs.org/dist/v9.0.0/node-v9.0.0-x86.msi

    Mac:        $brew install

2. Change NPM to use taobao repository

    $ npm install -g cnpm --registry=https://registry.npm.taobao.org

3. Install AnyPorxy

    npm install -g anyproxy

4. Generate root certificate and trust it

    anyproxy-ca

5. Fix AnyProxy crash issue:

    Replace [_/usr/local/lib/nodemodules/anyproxy/lib/requestHandler.js_]() with local **requestHandler.js**. Anyproxy crashes when connection is reset
    For Windows System, find anyproxy's anyproxy root dir then replace **requestHandler.js**

6. Start AnyProxy ( -i means parse https )

    Use --rule to specify rule defined by javascript
    anyproxy -i --rule wxrule.js

# Evnironment
1. set username, host and password to dbconfig of mysqlmgr.py for Mysql config
2. set config info for mongodb in mongomgr.py


# Files
-- wxrule.js 指定了抓取微信公众号的规则，用来上报HOME消息和更多的历史消息

-- biz_collect_rule.js 用来协助收集微信公众号的 __biz 

-- mysqlmgr.py MySQL数据库代码，需要修改数据库的地址、用户名和密码

-- mongomgr.py MongoDB 数据库代码，用来存储抓取的微信公众号历史消息

-- webservice.py 后台的web服务，基于 python3，可以通过 http://127.0.0.1:9999 来访问

# Run it
1. Open url http://[Your Computer IP]:8001 to install certificate to your mobile phone
2. Set proxy to Host: [Your Computer IP], Port: 8002 on your mobile phone
3. Start webservice: python3 webservice.py
4. Make sure MongoDB and Mysql server are correctly configured and started