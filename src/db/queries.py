from datetime import date
from sqlalchemy import (
    Integer, TextClause, and_, Date,
    cast, func, text, insert, select
    )
from src.db.models import (
    User, Exercises, TUser, Roles
)

def get_exercise_statistics(target_date: date) -> TextClause:
    return (
        select(
            Exercises.exercise,
            func.sum(Exercises.count).label("count"),
        )
        .select_from(Exercises)
        .group_by(
            Exercises.exercise,
        )
        .filter(
            cast(Exercises.created_at, Date) == target_date
        )
    )

def get_users() -> TextClause:
    return (
        select(
            User
        )
        .select_from(User)
    )

def get_user_by_id(id: int) -> TextClause:
    return (
        select(
            User
        )
        .select_from(User)
        .filter(
            User.id == id
        )
    )

def get_user_by_email(email: str) -> TextClause:
    return (
        select(
            User
        )
        .select_from(User)
        .filter(
            User.email == email
        )
    )
def get_t_user_by_tuid(tuid: int) -> TextClause:
    return (
        select(
            TUser,
            Roles.role
        )
        .select_from(TUser)
        .join(Roles, Roles.uid == TUser.uid)
        .filter(
            TUser.tuid == tuid
        )
    )
