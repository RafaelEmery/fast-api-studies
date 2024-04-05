from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.course import Course
from core.deps import get_session


# Bypass warning for SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

Select.inherit_cache = True # type: ignore
SelectOfScalar.inherit_cache = True # type: ignore
# End bypass warning

router = APIRouter()


@router.get('/', response_model=List[Course])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        courses = await session.execute(select(Course))
        res: List[Course] = courses.scalars().all()
        
        return res


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=Course)
async def get_course(db: AsyncSession = Depends(get_session), id: int = None):
    async with db as session:
        course = await session.get(Course, id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Course not found'
            )
        return course


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course: Course, db: AsyncSession = Depends(get_session)):
    new_course = Course(
        title=course.title,
        description=course.description, 
        classes=course.classes, 
        hours=course.hours
    )

    db.add(new_course)
    db.commit()

    return new_course


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=Course)
async def update_course(course: Course, db: AsyncSession = Depends(get_session), id: int = None):
    async with db as session:
        course = await session.get(Course, id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Course not found'
            )

        course.title = course.title
        course.description = course.description
        course.classes = course.classes
        course.hours = course.hours

        db.commit()

        return course


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(db: AsyncSession = Depends(get_session), id: int = None):
    async with db as session:
        course = await session.get(Course, id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Course not found'
            )

        db.delete(course)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)