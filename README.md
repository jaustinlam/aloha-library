# Aloha Library
A fictional library built that allows user sign up, see books and check books in and out

## Installation
1. Go to https://github.com/jaustinlam/Swiss_system_tournament.git and download.
2. Install [Python](https://www.python.org/downloads/)
3. Install [Vagrant](https://www.vagrantup.com)
4. Install [VirtualBox](https://www.virtualbox.org)
5. Launch the Vagrant VM and configure. the enter 'cd /vagrant' to navigate to project
6. To intiate and populate your database. enter 'python database_setup.py' and then 'python populate_database.py'
7. To run the project enter 'python project.py'.
8. Open your browser and enter in 'localhost:8500'

## Usage
* Logging in
> Click the login button in the top right corner. You must have a [Facebook account](https://www.facebook.com) to log in.

* Logging out
> Click the logout button in the top right corner. This resets the session and clears the user.

* Editing a User
> Click the users name on the top right when logged in.
> ** Note only users can change their own information. Admins can change anyone.**
> ** Admins on this edit page will be presented with an additional 'admin console' button to view, delete and edit all users.**

**** FOR DEVELOPMENT ONLY ****
* Making a user Admin
> If you modify your nickname to "Admin" you will automatically be assigned as an admin.
******************************
* Viewing a Categories Books
> Click on the Category name

* Edit a Category
> Click on the Edit button below the Category name
> ** Note only authors of categories or admins can edit categories**

* Delete a Category
> Click on the Delete button below the Category name
> ** Note only authors of categories or admins can delete categories**

* Add a Category
> Click on the "+" button on the Category page

* View a Books information
> Click on the book image

* Edit a Book
> Click on the Edit button below the Books name
> ** Note only authors of books or admins can edit books**

* Delete a Book
> Click on the Delete button below the Books name
> ** Note only authors of books or admins can delete books**

* Checkout a Book
> If book is availible to check out there will be a check button below the book image. Click it!

* Checkin a Book
> If the book is checkout an "X" will be below the book image. Click to check in.
> ** Note only the user who checked out the book or admin can check the book back in**



## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits
Built with Flask, SQL Alchemy, Materialize JSS, Jinja,
Image from pixabay.com

## History

v1. Our first version

