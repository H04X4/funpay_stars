import aiosqlite
import asyncio

async def main00():
    from bot.MAIN_FUNCS.dumper import dumper
    from bot.MAIN_FUNCS.update_sales import get_sales, update_on_startup
    from TelegramBot.main_func import zapusk
    from bot.main import task_worker

    async with aiosqlite.connect('db.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                completed TEXT NOT NULL
            )
        ''')
        await db.commit()
        print("СОЗДАЛ БАЗУ ДАННЫХ")

    await update_on_startup()

    print("Успешно поставил старые ордера в бд")

    tasks = [
        zapusk(),
        dumper(),
        get_sales(),
        task_worker()
    ]
    
    await asyncio.gather(*tasks)
    print("Запустил весь софт")