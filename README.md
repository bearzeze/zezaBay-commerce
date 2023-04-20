# **Online Commerce Website**

## Fully implemented online comerce website for auction selling items using Django Framework

Website which enables registred user to post item for auction sales, and to buy items as well. Website have next major specifications:

* Functional register and login validation
* Viewing all active listings
* Viewing all active listings order by categories
* Accessing every active/inactive listing
* Creating, editing, closing and deleting listings by user
* Adding/removing active item to/from watchlist
* Placing bids by users
* Adding, removing and viewing the comments

## **How To Use App**
Website is very easy to use and it is shown in the video available on the [LINK](https://www.youtube.com/watch?v=USWia_9mXqI).

## **Technical Specifications**
Frontend design was not main goal of this website, so it can be additionaly improved, even tough there are some specific details that had been done using Bootstrap 5 and own CSS styles. 

Funcionality was the primary goal of this project, so backend development was done using Python 3 Django web framework, alongside with HTML, Jinja and CSS.

### **User Authentication**
Most of the preformance requires user to be registred and logged in so authentication is carried out properly.

Registration proccess will check whether username is at least 4 character, whether password is at least 6 character and password confirmation matched. And afterwards it will check whether username is already being used. After successful registration it will be redirect to the index page

Login proccess is straightforward. Checking whether user exits and if the password is correct and redirect user to the home page

### **Active Listings**
All website visitors can see all of the active listings and can visit every item individualy.

### **Categories**
All website visitors can see all of the active listings filtered by categories and can visit every item individualy.

### **User Listing**
All website visitors can see all of the listings created by specific user.

### **Watchlist**
Users can view the watchlist and all items that had been added to watchlist.

### **Item**
Every active/inactive item can be visited by any visitors and can see title, current price, details and comments about visited item. 

User can edit item if he owns it - title, price, condition, and [price](#NTBD) (this should be improved), user can close the listing, and can delete the item from the database.

Only authenticated users can place bids, post comments, remove comments, add to watchlist, etc. On the closed item there is no possibility for the further bidding. If the item is closed (inactive), and current visitor-user have highest bid, message box will say so.

User is able to create new item.


## <a name="NTBD"></a>**Needs To Be Done**
- User should be able to edit the price of the item only if the price is the starting one and no user placed bid on the item.
- Frontend can be masssively improved - especially frontend functionality using JavaScript

## **Contact**
Any information, bugs or questions can be sent on the e-mail adress: i.zejd@hotmail.com