# Install Headless Chrome and webdriver
1. Download chrome driver

    https://sites.google.com/a/chromium.org/chromedriver/downloads

    lastest version:  
    https://chromedriver.storage.googleapis.com/index.html?path=2.38/  
    
    From Baidu Pan, including driver for MacOS, Windows 64 and Linux:  
    https://pan.baidu.com/s/1OTANr3Jy6g0bnbaxcuQqsw
    

2. Unzip then get chromedriver,put it to any directory in system PATH (e.x: /usr/local/bin/ )

3. Download Headless Chrome ( Chrome v59 ):

    * Windows 64 位版：  
    https://dl.lancdn.com/landian/software/chrome/m/index/Win64.html

    * Windows 32 位版：  
    https://dl.lancdn.com/landian/software/chrome/m/index/Win32.html

    * Debian/Ubuntu：  
    https://dl.lancdn.com/landian/software/chrome/m/index/Deb.html

    * Fedora/openSUSE：  
    https://dl.lancdn.com/landian/software/chrome/index/Rpm.html

    * Mac OS X 10.9+版：  
    https://dl.lancdn.com/landian/software/chrome/m/index/Mac.html

# Install PhantomJS

1. Install NodeJS if not yet installed
`$ yum install nodejs`
2. NPM using taobao repo
`$ npm install -g cnpm --registry=https://registry.npm.taobao.org`
3. Using Node's package manager install phantomjs: 
`$ npm -g install phantomjs-prebuilt`
4. Install selenium (in your virtualenv, if you are using that)
`$ pip install selenium`
5. After installation, you may use phantom as simple as:    
  
        from selenium import webdriver

        driver = webdriver.PhantomJS() # or add to your PATH
        driver.set_window_size(1024, 768) # optional    
        driver.get('https://google.com/')
        driver.save_screenshot('screen.png') # save a screenshot to disk
        sbtn = driver.find_element_by_css_selector('button.gbqfba')
        sbtn.click()

If your system path environment variable isn't set correctly, you'll need to specify the exact path as an argument to webdriver.PhantomJS(). Replace this:

    driver = webdriver.PhantomJS() # or add to your PATH

with:

    driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')

References:
http://selenium-python.readthedocs.org/en/latest/api.html
How do I set a proxy for phantomjs/ghostdriver in python webdriver?
http://python.dzone.com/articles/python-testing-phantomjs