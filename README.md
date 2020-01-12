
A. URL
URL My azure website is: http://xinyanzhmenuapp.azurewebsites.net/ 


B. Some tips/information:
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





