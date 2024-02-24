from typing import Any

from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.responses import Response
from fastapi import Path

from routes import courses, users
from models import Course
from db import fake_db


app = FastAPI(title="FastAPI Learning API", description="This is a very fancy project :D", version="1.0.0")
app.include_router(courses.router, tags=["courses"])
app.include_router(users.router, tags=["users"])


# In memory database for courses model
courses = {
    1: {
        "title": "first course",
        "classes": 10,
        "hours": 20
    },
    2: {
        "title": "second course",
        "classes": 5,
        "hours": 10
    },
    3: {
        "title": "third course",
        "classes": 20,
        "hours": 40
    }
}

'''
Deprecated routes

Made for learning purposes and marked with deprecated=True tag on documentation
'''

@app.get("/courses", description="Get all courses", response_model=list[Course], deprecated=True, tags=["courses"])
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@app.get("/courses/{course_id}", name="Get Course By ID", response_model=Course, description="Get a course by its id", deprecated=True, tags=["courses"])
async def get_course(course_id: int = Path(..., title="course id", description="The id of the course", example=1, gt=0, lt=10)):
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/courses", status_code=status.HTTP_201_CREATED, deprecated=True, tags=["courses"])
async def create_course(course: Course):
    if course.id not in courses:
        course.id = len(courses) + 1
        courses[course.id] = course
        return courses[course.id]
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Course already exists with id {course.id}")

@app.put("/courses/{course_id}", deprecated=True, tags=["courses"])
async def update_course(course_id: int, course: Course):
    if course_id in courses:
        course.id = len(courses) + 1
        courses[course_id] = course
        return courses[course_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course not found with id {course_id}")

@app.delete("/courses/{course_id}", deprecated=True, tags=["courses"])
async def delete_course(course_id: int):
    if course_id in courses:
        del courses[course_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course not found with id {course_id}")


if __name__ == "__main__":
    import uvicorn

    # FIXME: debug=True is not working
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)