import argparse
import asyncio
import logging

from .parser import Mangagraph
from .exceptions import MangagraphError

def main():
    parser = argparse.ArgumentParser(description="Mangagraph")
    parser.add_argument('url', type=str, help='URL of the manga to process')
    parser.add_argument('--db', type=str, default='manga.db', help='Database file name')
    parser.add_argument('--mirror', action='store_true', help='Use graph.org as mirror')
    # parser.add_argument('--log', type=str, default='manga_parser.log', help='Log file name')
    
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    try:
        parser_instance = Mangagraph(
            db_path=args.db,
            use_mirror=args.mirror
        )
        toc_url, mirror_toc_url = asyncio.run(parser_instance.process_manga(args.url))
        logger.info(f"База данных создана!")
        logger.info(f"Оглавление: {toc_url}")
        logger.info(f"Зеркало оглавления: {mirror_toc_url}")
    except MangagraphError as e:
        logger.error(f"Parser error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()