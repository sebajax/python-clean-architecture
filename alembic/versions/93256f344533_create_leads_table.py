"""create products table

Revision ID: 93256f344533
Revises: 
Create Date: 2023-03-09 18:01:14.689685

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from passlib.context import CryptContext
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision = '93256f344533'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create table users
    table_users = op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", TIMESTAMP, nullable=False, default=datetime.utcnow),
        sa.Column("updated_at", TIMESTAMP, nullable=False, default=datetime.utcnow),
    )
    # create indexes for table users
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_is_active"), "users", ["is_active"], unique=False)
    # create table products
    op.create_table(
        "products",
        sa.Column("product_id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column("created_at", TIMESTAMP, nullable=True, default=datetime.utcnow),
        sa.Column("updated_at", TIMESTAMP, nullable=True, default=datetime.utcnow),
    )
    # create indexes for table products
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)

    # generate password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash('Admin2023')

    # create admin user
    op.bulk_insert(table_users,
                   [
                       {
                           "email": "user@admin.com",
                           "first_name": "User",
                           "last_name": "Admin",
                           "hashed_password": hashed_password,
                           "is_active": True,
                           "is_admin": True,
                       },
                   ])


def downgrade() -> None:
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_is_active"), table_name="users")
    op.drop_table("users")
