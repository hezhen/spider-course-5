// overwrite the `languages` property to use a custom getter
const setProperty = () => {
    Object.defineProperty(navigator, "languages", {
        get: function() {
            return ["en-US", "en", "es"];
        }
    });

    // Overwrite the `plugins` property to use a custom getter.
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    });

    // Pass the Webdriver test
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });

    // await page.evaluateOnNewDocument(() => {
    //     Object.defineProperty(navigator, 'webdriver', {
    //     get: () => false,
    //     });
    // });
  
    callback();
};
setProperty();