from sqlalchemy import ForeignKey, Enum as SQLAEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from App.db.database import Base
import enum
from sqlalchemy import Column, Integer, String



user_id = Column(Integer, ForeignKey("users.id"))


#  Enum for request status
class FriendRequestStatus(str, enum.Enum):
    pending  = "pending"
    accepted = "accepted"
    rejected = "rejected"
    revoked  =  "revoked"

#  User table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


#  Friend request table
class FriendRequest(Base):
    __tablename__ = 'friend_requests'
    __table_args__ = (UniqueConstraint('sender_id', 'receiver_id', name='unique_friend_request'),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    status = Column(SQLAEnum(FriendRequestStatus), default=FriendRequestStatus.pending)


class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    friend_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default="pending")  # accepted, rejected