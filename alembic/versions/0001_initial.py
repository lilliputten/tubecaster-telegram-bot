"""Initial schema translated from Prisma.

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-04
"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = '0001_initial'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('userStr', sa.String(), nullable=False, server_default=sa.text("''")),
        sa.Column('isDeleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('deletedAt', sa.DateTime(timezone=True), nullable=True),
        sa.Column('languageCode', sa.String(), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('Users_isDeleted_idx', 'Users', ['isDeleted'], unique=False)

    op.create_table(
        'Commands',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('messageId', sa.BigInteger(), nullable=False),
        sa.Column('updateId', sa.BigInteger(), nullable=False),
        sa.Column('userId', sa.BigInteger(), nullable=False),
        sa.Column('userStr', sa.String(), nullable=False, server_default=sa.text("''")),
        sa.Column('repeated', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('isActive', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'TempMessages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('messageId', sa.BigInteger(), nullable=False),
        sa.Column('commandId', sa.Integer(), nullable=False),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['commandId'], ['Commands.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'UserStatus',
        sa.Column('userId', sa.BigInteger(), nullable=False),
        sa.Column('userMode', sa.String(), nullable=False, server_default='GUEST'),
        sa.Column('statusChangedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('paidAt', sa.DateTime(timezone=True), nullable=True),
        sa.Column('paymentValidUntil', sa.DateTime(timezone=True), nullable=True),
        sa.Column('paymentId', sa.String(), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['userId'], ['Users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('userId'),
    )

    op.create_table(
        'TotalStats',
        sa.Column('userId', sa.BigInteger(), nullable=False),
        sa.Column('requests', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('infoRequests', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('failures', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('volume', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updatedAt', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['userId'], ['Users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('userId'),
    )

    op.create_table(
        'MonthlyStats',
        sa.Column('userId', sa.BigInteger(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('requests', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('infoRequests', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('failures', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('volume', sa.BigInteger(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['userId'], ['Users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('userId', 'year', 'month'),
    )
    op.create_index('MonthlyStats_year_month_idx', 'MonthlyStats', ['year', 'month'], unique=False)
    op.create_index('MonthlyStats_userId_year_idx', 'MonthlyStats', ['userId', 'year'], unique=False)
    op.create_index('MonthlyStats_userId_idx', 'MonthlyStats', ['userId'], unique=False)


def downgrade() -> None:
    op.drop_index('MonthlyStats_userId_idx', table_name='MonthlyStats')
    op.drop_index('MonthlyStats_userId_year_idx', table_name='MonthlyStats')
    op.drop_index('MonthlyStats_year_month_idx', table_name='MonthlyStats')
    op.drop_table('MonthlyStats')
    op.drop_table('TotalStats')
    op.drop_table('UserStatus')
    op.drop_table('TempMessages')
    op.drop_table('Commands')
    op.drop_index('Users_isDeleted_idx', table_name='Users')
    op.drop_table('Users')
