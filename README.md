# Personal finance tracker

## Summary

**Personal finance tracker** is a simple web application where users can input their income, expense, saving, budget and saving goal related data.

## How to run the application

Clone this repository to your computer and move to repository's root folder. Create .env -file in root folder with the following content:

```
DATABASE_URL=yourdatabaseurlhere
SECRET_KEY=yoursecretkeyhere
```

Activate the virtual environment and install the necessary dependencies:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r ./requirements.txt
```

Define the database schema with the command below:

```
psql < src/schema.sql
```

Move to src -folder and start the application:

```
cd src
```

```
flask run
```

## Features

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

  - User can log out from their current session.

  - User can delete their account and all the related data with `Delete account` -button

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

  - User can delete their submitted transactions.

- Security

  - Application has enhanced security with CSRF token validation for all POST requests

### What could be done in future, if the project is continued

- Overhaul the application styling to be more visually appealing.

- Users could search for individual incomes and expenses and see the related data.

- Add charts to display data changes over time.

- Users could download a .csv file with their financial data.

- Refactor underlying code
