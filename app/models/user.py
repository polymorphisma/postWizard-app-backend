from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, intpk, str100


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password: Mapped[str]
    first_name: Mapped[str100 | None]
    last_name: Mapped[str100 | None]

    # Relationship to 'Upload' table with cascade option
    uploads: Mapped[list["Upload"]] = relationship(
        "Upload", back_populates="user", cascade="all, delete-orphan"
    )


class Upload(Base):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String(255), unique=True)
    upload_options: Mapped[str] = mapped_column(String(255))
    context: Mapped[str] = mapped_column(String(255))
    generated_text: Mapped[str] = mapped_column(Text())
    uploaded_link: Mapped[str] = mapped_column(Text)

    # ForeignKey to User table
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationship to 'User' table
    user: Mapped["User"] = relationship("User", back_populates="uploads")
