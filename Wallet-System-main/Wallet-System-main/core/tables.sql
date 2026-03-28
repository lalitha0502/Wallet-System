CREATE TABLE users
(
    user_id UUID PRIMARY KEY,

    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,

    password_hash TEXT NOT NULL,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    address TEXT,

    created_at TIMESTAMP
    WITH TIME ZONE NOT NULL DEFAULT NOW
    (),
    updated_at TIMESTAMP
    WITH TIME ZONE NOT NULL DEFAULT NOW
    (),

    CONSTRAINT users_username_key UNIQUE
    (username),
    CONSTRAINT users_email_key UNIQUE
    (email)
);

    CREATE SEQUENCE account_number_seq
    START 1001;

    CREATE TABLE currency_serial
    (
        currency VARCHAR(10) NOT NULL UNIQUE,
        id INTEGER NOT NULL DEFAULT nextval('account_number_seq')
    );

    CREATE TYPE account_status AS ENUM
    (
    'ACTIVE',
    'FROZEN',
    'CLOSED'
);

    CREATE TABLE accounts
    (
        account_id UUID PRIMARY KEY,
        user_id UUID NOT NULL,

        account_number VARCHAR(50) NOT NULL UNIQUE,
        currency VARCHAR(10) NOT NULL,

        status account_status NOT NULL DEFAULT 'ACTIVE',

        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        CONSTRAINT fk_accounts_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
    );

    CREATE TABLE balances
    (
        balance_id UUID PRIMARY KEY,

        account_id UUID NOT NULL UNIQUE,

        version INTEGER NOT NULL DEFAULT 0,

        amount BIGINT NOT NULL DEFAULT 0,

        CONSTRAINT fk_balances_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE
    );

    CREATE TYPE idempotency_status AS ENUM
    (
    'CREATED',
    'PROCESSING',
    'FAILED',
    'SUCCESS'
);
    CREATE TABLE idempotency_keys
    (
        idempotency_key VARCHAR(255) NOT NULL,
        user_id UUID NOT NULL,

        request_hash TEXT NOT NULL,
        status idempotency_status NOT NULL DEFAULT 'CREATED',

        transaction_id UUID,
        response TEXT,

        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        PRIMARY KEY (idempotency_key, user_id)
    );

    CREATE TYPE transaction_state AS ENUM
    (
    'CREATED',
    'PROCESSING',
    'FAILED',
    'SUCCESS'
);

    CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,

    idempotency_key VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL,

    sender_account_id UUID NOT NULL,
    receiver_account_id UUID NOT NULL,

    amount BIGINT NOT NULL,
    currency VARCHAR(10) NOT NULL,

    reference_type VARCHAR(100) NOT NULL,
    reference_id VARCHAR(100) NOT NULL,

    state transaction_state NOT NULL DEFAULT 'CREATED',

    metadata JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_transaction_idempotency
        FOREIGN KEY (idempotency_key, user_id)
        REFERENCES idempotency_keys(idempotency_key, user_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_transaction_sender
        FOREIGN KEY
    (sender_account_id)
        REFERENCES accounts
    (account_id),

    CONSTRAINT fk_transaction_receiver
        FOREIGN KEY
    (receiver_account_id)
        REFERENCES accounts
    (account_id)
);

    CREATE TYPE transfer_type AS ENUM
    (
    'CREDIT',
    'DEBIT'
);
    CREATE TABLE ledger_entries
    (
        ledger_id UUID PRIMARY KEY,

        account_id UUID NOT NULL,
        transaction_id UUID NOT NULL,

        amount BIGINT NOT NULL,
        type transfer_type NOT NULL,

        balance_after BIGINT NOT NULL,

        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        CONSTRAINT fk_ledger_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        ON DELETE CASCADE,

        CONSTRAINT fk_ledger_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE CASCADE
    );

    CREATE TYPE transfer_type AS ENUM
    ('CREDIT', 'DEBIT');

    -- Create Ledger table
    CREATE TABLE ledger
    (
        ledger_id UUID PRIMARY KEY,
        account_id UUID NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
        transaction_id UUID NOT NULL REFERENCES transactions(transaction_id) ON DELETE CASCADE,
        amount BIGINT NOT NULL,
        -- smallest currency unit
        type transfer_type NOT NULL,
        -- CREDIT / DEBIT
        balance_after BIGINT NOT NULL,
        -- balance after this transaction
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );