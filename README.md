# Browser_Proxy_Setup
Python GUI App that sets up a Chrome browser session (with specified proxies).  
There are two associated files: AmazonAccounts.json and proxies.json. 

The goal here is to set to access each Amazon account via a separate proxy. 
The AmazonAccounts file contains the access information for each account as well as an entry specifying which proxy from the proxies.json file to use. 

The program will prompt you for which vendor’s site you want to access and then prompt for which particular account you want  to use . 
When the selections are made, the app will then set up a Chrome session with the proxies set up.

The values in the AmazonAccount.json file and the proxies.json file have been changed to random values. 
They can be replaced with actual account  and proxy information.
