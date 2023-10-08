# Personal finance tracker

Project repository for University of Helsinki's course Tietokannat ja web-ohjelmointi.

This README is a WIP and is subject to change as the project evolves.

## How to run the application

Clone this repository to your computer and move to repository's root folder. Create .env -file in root folder with the following content:

```
DATABASE_URL=yourdatabaseurlhere
SECRET_KEY=yoursecretkeyhere
```

Activate the virtual environment and install the necessary dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Define the database schema with the command below:

```
psql < src/schema.sql
```

Move to src -folder and start the application:

```
cd src
flask run
```

## Features

- Personal finance tracker allows users to input income, expenses, and savings. The software provides visualization tools to display financial data over time, such as expense trends and savings goals.

- Users can create a unique user ID and use it to log in to the system
- Users can delete their user ID and delete all data that is behind the user ID

## Current situation of project

- Main page / Login page

  - User can login to the application

  - User can click link that redirects to the registration page

  - Pop-up alerts will be displayed upon invalid username or password submission.

- Registration page

  - Registration page has instructions about username and password constraints.

  - User can create a new account and upon succesful account creation is directed back to main page / login page.

  - Pop-up alerts will instruct user, if there username or password doesn't pass the constraints.

- Dashboard

  - Dashboard displays the currently logged in user.

  - Dashboard has a functional logout button.

  - User can submit income information: source of income and amount of income.

    - Total income, income past week, income past month and income past year are displayed.

  - User can submit expense information: select a category for expense and submit expense amount.

    - Total expenses, expenses past week, expenses past month and expenses past year are displayed.

  - User can submit savings information: select a savings category and submit amount they are saving.

    - Total savings, savings past week, savings past month, savings past year are displayed.

  - User can submit budget information: select budget category and budget amount.

    - Budget categories and how much budget is left for the category is displayed.

  - User can submit financial goal information, which is related to savings: select savings category, input goal amount and select a target date.

    - Goal name, category, goal amount, current amount, target date and progress are shown on a table. Progress bar fills depending on the currently saved amount.

  - User can delete their submitted transactions

- Security

  - Application has enhanced security with CSRF token validation for all POST requests

### What needs to be done

- Application security needs to be strenghtened (check for XSS vulnerability and review previously implemented CSRF token validations)

- Application doesn't have proper styling and current look doesn't represent the final product

- Code refactoring needs to be done, import statements need to be uniform and repetitive code should not exist. Current product has plenty of repetitive code.

- Dashboard needs to have chart visualization for the data

- User needs to be able to delete their account and all the data associated with the account.
