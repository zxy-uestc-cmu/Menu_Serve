
<Git comit and branch>
At the half stage of this homework, I commit and push to the master branch. And I used hw6 branch for the next half stage.
**** So please check my "git commit" information both in master branch and hw6 branch. ****
And the final-version codes, including the yml file for CD, for my webapp is in hw6 branch :)


A. URL
URL My azure website is: http://xinyanzhmenuapp.azurewebsites.net/ 
My website git url is: https://xinyanzhmenuapp.scm.azurewebsites.net/xinyanzhmenuapp.git
My Enviorment variables:
export DBHOST="xinyanzhcmu.postgres.database.azure.com"
export DBUSER="xinyanzhh@xinyanzhcmu"
export DBNAME="memuapp"
export DBPASS="Woshihabao97020*"


B. Settings for my Azure CD app:
(1)  To use and deploy Azure via CD/Ci tool, I created my own CD project and pipline for this app, and use one yml file to build, test and push automatically. 
The actual yml file used is in branch "hw6", which is only triggered by the push of branch hw6.
      
(2) The requirements.txt file is used to install some packages needed for this app, and it uses selenuim 3.3, django 2.2.1 and python 3.7



C. Some tips/information:

(1) In order-food page and order-list(remember to select differnt stores) page, Ajax is used to communicate with server and update the page without reloading. If ajax fails to retrive data, the page will display an alert message.   

(2) For non-log-in user, if they click the "create-order-now" link, they will be redirect to the page of login/register.

(3) According to the navigation bar, managers have "menu, staff, order list, edit menu", employees have "menu, order list", and costomers have "menu, create order, your lists".
PS: Managers and Employees can't create orders.

(4) Customers can only create orders after managers opening the first store.

(5) One store could have multiple managers and employees.

(6) When ordering the food, customer need to select the store they are buying from (by clicking buttoms) before adding the first item. And the defaut store is the first store in database.

(7) When managers/employees seeing all ordered lists, they are seperated by different stores, so they should select certain store to display by buttons. But customer's order lists are diaplyed together.



D. Summary:
This homework used Jquery to implement DOM and Ajax to accomplish (1)food-ordering(add,minus,delete) without reloading, (2) update order lists evey 5s without reloading. 
It also includes unit tests for each model, and high-level selenium test for actions in each page. 
It uses reverse URL resolution, vanlidation (form), authentication model(build-in and self-defined), and also many technoogies from previous homework.





