CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE incomes (
    income_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    source VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date_received TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    category VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date_incurred TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE savings (
    saving_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    category VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    date_saved TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE budgets (
    budget_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    category VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE financial_goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    goal_name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(255) NOT NULL,
    goal_amount DECIMAL(10,2) NOT NULL,
    target_date TIMESTAMP NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT NOW()
);