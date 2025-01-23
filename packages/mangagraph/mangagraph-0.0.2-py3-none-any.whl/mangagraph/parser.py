"""
Author: https://github.com/damirtag | https://t.me/damirtag
GH Repo: https://github.com/damirtag/mangagraph

MIT License

Copyright (c) 2025 Tagilbayev Damir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import aiohttp
import logging

from typing import List, Dict, Any, Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Chapter
from .exceptions import (
    MangagraphError,
    RequestFailedException
)
from .utils import (
    MangaLibUrl, 
    estimate_remaining_time, 
    extract_slug
)

from telegraph.aio import Telegraph

class Mangagraph:
    """
    Автор: https://github.com/damirtag

    Параметры:
        db_name (str): Имя базы данных в которой будет хранится Том, глава, название главы, ссылка на телеграф, зеркало, дата создания
        use_mirror (bool): Использовать зеркало как base url для telegraph, по дефолту False
    """
    MAX_CONCURRENT = 3
    # В 1 мин обрабатывается 12 глав 
    # что = 12 страницам телеграф в секунду
    # При учете того что запросы делаются каждые 5 сек
    CHAPTERS_PER_MINUTE = 12


    def __init__(
        self, 
        db_name: str = 'manga.db',
        use_mirror: bool = False
    ):
        self.db_name = db_name if db_name.endswith('.db') else db_name + '.db'
        self.logger = self._setup_logger()
        self.engine = create_engine(f'sqlite:///{self.db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.domain = 'telegra.ph' if not use_mirror else 'graph.org'
        self.telegraph = Telegraph(domain=self.domain)
        
        self.base_img_url = "https://img33.imgslib.link"
        self.semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)

        self.processed_count = 0
        self.total_chapters = 0
        self.flood_wait_count = 0

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def _setup_logger(self):
        logger = logging.getLogger('mangagraph')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[mangagraph]: %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    async def _make_request(self, session: aiohttp.ClientSession, url: str, params: Dict = None) -> Dict:
        async with self.semaphore:
            for attempt in range(3):
                try:
                    async with session.get(url, params=params, headers=self.headers) as response:
                        response.raise_for_status()
                        return await response.json()
                except Exception as e:
                    if attempt == 2:
                        raise RequestFailedException(url, str(e))
                    await asyncio.sleep(2 ** attempt)

    async def _get_manga_name(self, session: aiohttp.ClientSession, slug: str) -> str:
        url = f"https://api2.mangalib.me/api/manga/{slug}"
        data = await self._make_request(session, url)
        rus_name = data['data']['rus_name']
        if rus_name:
            return rus_name
        return data['data']['name']

    async def get_chapters_info(self, session: aiohttp.ClientSession, slug: str) -> List[Dict[str, Any]]:
        url = f"https://api2.mangalib.me/api/manga/{slug}/chapters"
        data = await self._make_request(session, url)
        return data['data']

    async def get_chapter_pages(
        self, 
        session: aiohttp.ClientSession, 
        slug: str, 
        volume: int, 
        chapter: int
    ) -> List[str]:
        url = f"https://api2.mangalib.me/api/manga/{slug}/chapter"
        params = {'number': chapter, 'volume': volume}
        data = await self._make_request(session, url, params)
        return [f"{self.base_img_url}{page['url']}" for page in data['data']['pages']]

    async def _create_telegraph_page(
            self, 
            title: str, 
            image_urls: List[str],
            retry_count: int = 3
        ) -> Tuple[str, str]:
        html_content = "".join(f'<img src="{url}"/>\n' for url in image_urls)
        
        for attempt in range(retry_count):
            try:
                response = await self.telegraph.create_page(
                    title=title,
                    html_content=html_content,
                    author_name='Auto-Generated by MGLParser',
                    author_url='https://t.me/damirtag'
                )
                
                return (
                    f"https://telegra.ph/{response['path']}", 
                    f"https://graph.org/{response['path']}"
                )
            except Exception as e:
                if "FLOOD_WAIT" in str(e):
                    self.flood_wait_count += 1
                    wait_time = 7
                    if "FLOOD_WAIT_" in str(e):
                        try:
                            wait_time = int(str(e).split("FLOOD_WAIT_")[1])
                        except:
                            pass
                            
                    self.logger.warning(
                        f'Flood wait #{self.flood_wait_count} detected, ' 
                        f'waiting {wait_time} seconds. ' 
                        f'Total floods: {self.flood_wait_count}'
                    )
                    
                    await asyncio.sleep(wait_time)
                    await self.telegraph.create_account(
                        short_name='Damir',
                        author_name='Auto-Generated by MGLParser',
                        author_url='https://t.me/damirtag'
                    )
                    continue
                else:
                    raise MangagraphError(f"Не удалось создать telegraph страницу: {str(e)}")

    async def _construct_chapters_list(
        self, 
        title: str, 
        chapters: List[Tuple[int, int, str, str, str]]
    ) -> str:
        """Creates a table of contents page in Telegraph."""
        content = [
            {
                "tag": "p",
                "children": ["Создано Mangagraph, developer - ", {
                    "tag": "a", 
                    "attrs": {"href": "https://t.me/damirtag"}, 
                    "children": ["@damirtag"]}
                ]
            }
        ]
        
        for volume, chapter_num, chapter_title, url, mirror_url in chapters:
            content.append({
                "tag": "p",
                "children": [
                    {
                        "tag": "a",
                        "attrs": {"href": mirror_url},
                        "children": [f"Volume {volume} Chapter {chapter_num}: {chapter_title}"]
                    }
                ]
            })

        try:
            response = await self.telegraph.create_page(
                title=title,
                author_name='Damir',
                author_url='https://github.com/damirtag/mangagraph',
                content=content
            )

            return response['url']
        except Exception as e:
            raise MangagraphError(f'Telegraph says: {str(e)}')

    async def process_manga(self, manga_url: MangaLibUrl):
        """
        Параметры:
            manga_url (str): URL манги, которую нужно обработать.

        Возвращает:

            Кортеж из двух строк:

                - URL оглавления в Telegraph.

                - URL зеркала оглавления в graph.org (если используется).

        Исключения:
            MangagraphError: Выбрасывается, если возникает ошибка при обработке манги.
            InvalidURLException: Выбрасывается, если URL манги недействителен.
            RequestFailedException: Выбрасывается, если запрос к API завершается неудачей.
        """
        db_session = self.Session()
        await self.telegraph.create_account(
            short_name='Damir',
            author_name='Создано mangagraph by @damirtag',
            author_url='https://github.com/damirtag/mangagraph'
        )

        slug = extract_slug(manga_url)
        
        async with aiohttp.ClientSession() as session:
            try:
                manga_name = await self._get_manga_name(session, slug)
                chapters = await self.get_chapters_info(session, slug)
                
                self.total_chapters = len(chapters)
                self.processed_count = 0
                processed_chapters = []

                first_chapter = chapters[0]
                pages = await self.get_chapter_pages(
                    session,
                    slug,
                    first_chapter.get('volume'),
                    first_chapter.get('number')
                )
                
                for chapter_info in chapters:
                    volume = chapter_info.get('volume')
                    chapter_num = chapter_info.get('number')
                    title = (
                        f"{manga_name} | {chapter_info.get('name')}" 
                        or 
                        f"{manga_name} | Том {volume}, Глава {chapter_num}"
                    )

                    existing_chapter = db_session.query(Chapter).filter_by(
                        volume=volume, 
                        chapter=chapter_num
                    ).first()

                    if existing_chapter:
                        self.processed_count += 1
                        processed_chapters.append(
                            (volume, chapter_num, title, existing_chapter.url, existing_chapter.mirror_url)
                        )
                        remaining = self.total_chapters - self.processed_count
                        est_time = estimate_remaining_time(remaining)
                        self.logger.info(
                            f"Глава {chapter_num} уже существует, пропускаем... " 
                            f"[{self.processed_count}/{self.total_chapters}] " 
                            f"Примерное время: {est_time}"
                        )
                        continue

                    try:
                        pages = await self.get_chapter_pages(
                            session,
                            slug, 
                            volume, 
                            chapter_num
                        )
                        
                        url, mirror_url = await self._create_telegraph_page(
                            title=title,
                            image_urls=pages
                        )
                        
                        new_chapter = Chapter(
                            volume=volume,
                            chapter=chapter_num,
                            title=title,
                            url=url,
                            mirror_url=mirror_url
                        )
                        db_session.add(new_chapter)
                        db_session.commit()
                        
                        self.processed_count += 1
                        processed_chapters.append((volume, chapter_num, title, url, mirror_url))
                        
                        remaining = self.total_chapters - self.processed_count
                        est_time = estimate_remaining_time(remaining)
                        self.logger.info(
                            f"Processed chapter: {title} " 
                            f"[{self.processed_count}/{self.total_chapters}] " 
                            f"Remaining time: {est_time}"
                        )
                        
                        await asyncio.sleep(5)
                        
                    except Exception as e:
                        self.logger.error(
                            f"Ошибка обработки главы {chapter_num}: {str(e)}\n" 
                            f"Всего обработано: {self.processed_count}/{self.total_chapters}"
                        )
                        db_session.rollback()
                        break

                if processed_chapters:
                    toc_url = await self._construct_chapters_list(
                        manga_name,
                        processed_chapters
                    )
                    mirror_toc_url = toc_url.replace("telegra.ph", "graph.org")

                    self.logger.info(f"Создано оглавление: {toc_url}")
                    self.logger.info(f"Зеркало: {mirror_toc_url}")
                    self.logger.info(f"Всего обработано: {self.processed_count}/{self.total_chapters}")

                    return toc_url, mirror_toc_url

            except (KeyboardInterrupt, SystemExit):
                self.logger.info('Sayonara!')

            finally:
                db_session.close()