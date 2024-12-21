/*
When changed, make sure to:
1. Close Firefox
2. Open profile directory in terminal
3. Execute: ./updater.sh -s
4. Execute: ./prefsCleaner.sh -s
5. Start Firefox
*/

/* override recipe: enable session restore ***/
user_pref("browser.startup.page", 3); // 0102
user_pref("privacy.clearOnShutdown_v2.historyFormDataAndDownloads", false); // 2811 FF128+

/* [SETTING] Privacy & Security>Logins and Passwords>Ask to save logins and passwords for websites */
user_pref("signon.rememberSignons", false);
