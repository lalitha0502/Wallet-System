# Wallet System Service

## Overview

This repository implements a robust Wallet System designed for handling user accounts, balances, and transactions with full support for idempotency, atomic operations, and auditability. The system ensures correctness even when deployed across multiple machines, making it ideal for financial applications, fintech platforms, and internal accounting services.

## Core Features

* **Account Management**: Create and manage multiple accounts per user, each with a unique account number and currency. Accounts are fully isolated to maintain data integrity.
* **Balance Management**: Each account has a balance record, which is updated atomically during transactions to prevent race conditions and inconsistencies.
* **Transactions**: Supports secure fund transfers between accounts with transaction states (`PROCESSING`, `SUCCESS`, `FAILED`). Every transaction is logged for traceability.
* **Ledger System**: Maintains a detailed ledger for every account, recording each debit and credit with the resulting balance to ensure audit-ready records.
* **Idempotency Support**: Prevents duplicate operations even if the same request is processed multiple times. This ensures the system remains consistent and prevents double-spending.
* **Atomic Operations**: All operations, including balance updates, ledger entries, and transaction state changes, are executed within atomic database transactions.
* **Error Handling**: Gracefully handles errors such as insufficient funds, invalid account IDs, and foreign key violations while maintaining consistent state.

## System Architecture

The system is designed with modularity in mind, separating concerns across multiple services and repositories:

* **Service Layer**: Contains `AccountService`, `TransactionService`, `BalanceService`, `LedgerService`, and `IdempotencyService` that orchestrate business logic and ensure atomic operations.
* **Repository Layer**: Handles all database interactions for accounts, balances, transactions, ledgers, and idempotency keys.
* **Models & Dataclasses**: Defines structured data for accounts, balances, transactions, ledger entries, and idempotency keys using Pydantic and dataclasses for type safety and validation.
* **Enums**: Enumerations like `ProcessState` and `TransferType` provide clear, maintainable states and transaction types.

## Deployment and Scalability

* Can be deployed across multiple machines without risking duplicate transactions thanks to idempotency keys.
* Atomic transactions ensure consistency even under high concurrency or partial failures.
* Database design supports foreign key constraints and ledger-based auditing.

## Technology Stack

* **Python 3.11+**: Core language for backend logic.
* **FastAPI**: Asynchronous web framework for API endpoints.
* **SQLAlchemy (Async)**: ORM for PostgreSQL, enabling atomic and asynchronous database operations.
* **PostgreSQL**: Relational database for persistent storage.
* **UUIDs**: Universally unique identifiers for accounts, transactions, and ledger entries.
* **Pydantic**: Data validation and serialization.
* **Dataclasses**: Lightweight data containers for internal operations.

## Benefits

* Ensures safe, atomic, and idempotent operations for financial transactions.
* Provides a clear audit trail for all account and transaction activity.
* Modular design makes it easy to extend features such as notifications, multi-currency support, or reporting.
* Ready for high-concurrency and distributed deployments.

This repository serves as a foundation for building highly reliable, auditable, and scalable wallet or financial transaction systems.
