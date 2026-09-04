from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'
    __table_args__ = (Index('Users_isDeleted_idx', 'isDeleted'),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    userStr: Mapped[str] = mapped_column(String, nullable=False, default='')
    isDeleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    languageCode: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    userStatus: Mapped[Optional['UserStatus']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        uselist=False,
    )
    totalStats: Mapped[Optional['TotalStats']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        uselist=False,
    )
    monthlyStats: Mapped[list['MonthlyStats']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Command(Base):
    __tablename__ = 'Commands'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    messageId: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updateId: Mapped[int] = mapped_column(BigInteger, nullable=False)
    userId: Mapped[int] = mapped_column(BigInteger, nullable=False)
    userStr: Mapped[str] = mapped_column(String, nullable=False, default='')
    repeated: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    isActive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    tempMessages: Mapped[list['TempMessage']] = relationship(
        back_populates='command',
        cascade='all, delete-orphan',
    )


class TempMessage(Base):
    __tablename__ = 'TempMessages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    messageId: Mapped[int] = mapped_column(BigInteger, nullable=False)
    commandId: Mapped[int] = mapped_column(Integer, ForeignKey('Commands.id', ondelete='CASCADE'), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    command: Mapped['Command'] = relationship(back_populates='tempMessages')


class UserStatus(Base):
    __tablename__ = 'UserStatus'

    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    userMode: Mapped[str] = mapped_column(String, nullable=False, default='GUEST')
    statusChangedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    paidAt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    paymentValidUntil: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    paymentId: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    user: Mapped['User'] = relationship(back_populates='userStatus')


class TotalStats(Base):
    __tablename__ = 'TotalStats'

    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    requests: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    infoRequests: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    failures: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    user: Mapped['User'] = relationship(back_populates='totalStats')


class MonthlyStats(Base):
    __tablename__ = 'MonthlyStats'
    __table_args__ = (
        Index('MonthlyStats_year_month_idx', 'year', 'month'),
        Index('MonthlyStats_userId_year_idx', 'userId', 'year'),
        Index('MonthlyStats_userId_idx', 'userId'),
    )

    userId: Mapped[int] = mapped_column(BigInteger, ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    month: Mapped[int] = mapped_column(Integer, primary_key=True)
    requests: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    infoRequests: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    failures: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    user: Mapped['User'] = relationship(back_populates='monthlyStats')


__all__ = [
    'Base',
    'Command',
    'MonthlyStats',
    'TempMessage',
    'TotalStats',
    'User',
    'UserStatus',
    'utc_now',
]
