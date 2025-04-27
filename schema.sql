CREATE TYPE transaction_category_enum AS ENUM ('income', 'expense');

CREATE TABLE accounts_user (
    _id UUID PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    soft_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    hard_deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE TABLE accounts_profile (
    _id UUID PRIMARY KEY,
    _user_id UUID UNIQUE NOT NULL,
    first_name VARCHAR(125) NOT NULL,
    last_name VARCHAR(125) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    soft_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    hard_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    FOREIGN KEY (_user_id) REFERENCES accounts_user(_id) ON DELETE CASCADE
);

CREATE TABLE transactions_transactioncategory (
    _id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id UUID NULL,
    category_type transaction_category_enum NOT NULL DEFAULT 'expense',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    soft_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    hard_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    FOREIGN KEY (parent_id) REFERENCES transactions_transactioncategory(_id) ON DELETE CASCADE
);

-- index for the parent_id field to improve performance in tree-based queries
CREATE INDEX idx_category_parent_id ON transactions_transactioncategory (parent_id);

CREATE TABLE transactions_transaction (
    _id UUID PRIMARY KEY,
    _user_id UUID NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    _category_id UUID NULL,
    description TEXT NOT NULL,
    tag VARCHAR(50) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    soft_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    hard_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    FOREIGN KEY (_user_id) REFERENCES accounts_user(_id) ON DELETE CASCADE,
    FOREIGN KEY (_category_id) REFERENCES transactions_transactioncategory(_id) ON DELETE SET NULL
);

-- index for the _user_id field to improve performance in queries for user transactions
CREATE INDEX idx_transaction_user_id ON transactions_transaction (_user_id);

-- index for the _category_id field to improve performance in queries for transactions by category
CREATE INDEX idx_transaction_category_id ON transactions_transaction (_category_id);

CREATE TABLE tokens_token (
    _id UUID PRIMARY KEY,
    _user_id UUID NOT NULL,
    is_active BOOLEAN NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expired_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    soft_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    hard_deleted_at TIMESTAMP WITH TIME ZONE NULL,
    FOREIGN KEY (_user_id) REFERENCES accounts_user(_id) ON DELETE CASCADE
);