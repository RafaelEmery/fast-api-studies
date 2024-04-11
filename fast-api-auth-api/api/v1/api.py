from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article import Article
from models.user import User
from schemas.article import Article as ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def create_article(
    article: ArticleSchema, 
    db: AsyncSession = Depends(get_session), 
    session_user: User = Depends(get_current_user)
):
    new_article = Article(**article.model_dump(), author_id=session_user.id)
    
    db.add(new_article)
    await db.commit()
    
    return new_article


@router.get('/', response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Article))
    
    return result.scalars().unique().all()


@router.get('/{article_id}', response_model=ArticleSchema)
async def get_article_by_id(
    article_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        result = await session.execute(select(Article).where(Article.id == article_id))
        article: Article = result.scalars().unique().one_or_none()

        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')
        
        return article


@router.put('/{article_id}', response_model=ArticleSchema)
async def update_article(
    article_id: int,
    article: ArticleSchema,
    db: AsyncSession = Depends(get_session),
    session_user: User = Depends(get_current_user)
):
    async with db as session:
        result = await session.execute(select(Article).where(Article.id == article_id))
        article_db: Article = result.scalars().unique().one_or_none()

        if not article_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')
        
        if article_db.author_id != session_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of this article')
        
        article_db.update(article.model_dump())
        await session.commit()
        
        return article_db


@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_session),
    session_user: User = Depends(get_current_user)
):
    async with db as session:
        result = await session.execute(select(Article).where(Article.id == article_id))
        article_db: Article = result.scalars().unique().one_or_none()

        if not article_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')
        
        if article_db.author_id != session_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of this article')
        
        await session.delete(article_db)
        await session.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)