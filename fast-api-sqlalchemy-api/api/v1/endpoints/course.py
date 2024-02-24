from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course import Course
from schemas.course import CourseSchema
from core.deps import get_session


router = APIRouter()


@router.get("/", response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course)
        result = await session.execute(query)
        courses: List[Course] = result.scalars().all()

        return courses


@router.get("/{course_id}", response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        return course


@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        try:
            new_course = Course(
                title=course.title, 
                description=course.description, 
                author_name=course.author_name, 
                classes=course.classes, 
                hours=course.hours
            )

            session.add(new_course)
            await session.commit()

            return new_course
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{course_id}", response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def update_course(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course_to_update = result.scalar_one_or_none()

        if not course_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        course_to_update.title = course.title
        course_to_update.description = course.description
        course_to_update.author_name = course.author_name
        course_to_update.classes = course.classes
        course_to_update.hours = course.hours

        await session.commit()

        return course_to_update


@router.patch("/activate/{course_id}", response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def activate_course(course_id: int, is_active: bool,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course_to_activate = result.scalar().one_or_none()

        if not course_to_activate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        if is_active == course_to_activate.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is already active" if is_active else "Course is already inactive")

        course_to_activate.is_active = is_active
        await session.commit()

        return course_to_activate


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course_to_delete = result.scalar_one_or_none()

        if not course_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        await session.delete(course_to_delete)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)