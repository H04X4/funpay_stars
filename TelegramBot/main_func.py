from aiogram import *
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import *
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram import *
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import json
import aiohttp
from bs4 import BeautifulSoup

async def zapusk():
    from SETTINGS import TOKEN
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    def main():
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text="🤖 Настройка дампера"), types.KeyboardButton(text="🤖 Настройка дампера мелких звёзд"))
        builder.row(types.KeyboardButton(text="💧 Получить список активных обьявлений"))

        return builder.as_markup(resize_keyboard=True)

    def start_btn():
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📈 50 stars", callback_data="edit-50 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 75 stars", callback_data="edit-75 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 100 stars", callback_data="edit-100 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 150 stars", callback_data="edit-150 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 200 stars", callback_data="edit-200 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 250 stars", callback_data="edit-250 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 350 stars", callback_data="edit-350 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 500 stars", callback_data="edit-500 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 1000 stars", callback_data="edit-1000 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📈 2500 stars", callback_data="edit-2500 звёзд"))
        
        return builder.as_markup(resize_keyboard=True)
    

    def start_btn1():
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📉 10 stars", callback_data="edit-10 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📉 15 stars", callback_data="edit-15 звёзд"))
        builder.row(types.InlineKeyboardButton(text="📉 25 stars", callback_data="edit-25 звёзд"))
        
        return builder.as_markup(resize_keyboard=True)

    def edit_btn(stars):
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="💎 Сменить айди обьявы", callback_data=f"smena-{stars}"))
        builder.row(types.InlineKeyboardButton(text="💎 Удалить конкурента со списка", callback_data=f"delete-{stars}"))
        builder.row(types.InlineKeyboardButton(text="💎 Добавить конкурента в список", callback_data=f"add-{stars}"))

        return builder.as_markup(resize_keyboard=True)

    def load_data(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Проверьте формат файла.")
            return []

    def save_data(filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_value(spisok, comment, new_value):
        for item in spisok:
            if item['comment'] == comment:
                item['value'] = new_value
                return f"Value updated for comment '{comment}' to '{new_value}'."
        return f"Comment '{comment}' not found."

    def add_to_nums(spisok, comment, new_num):
        for item in spisok:
            if item['comment'] == comment:
                if new_num not in item['nums']:
                    item['nums'].append(new_num)
                    return f"Number '{new_num}' added to nums for comment '{comment}'."
                else:
                    return f"Number '{new_num}' already exists in nums for comment '{comment}'."
        return f"Comment '{comment}' not found."

    def remove_from_nums(spisok, comment, num_to_remove):
        for item in spisok:
            if item['comment'] == comment:
                if num_to_remove in item['nums']:
                    item['nums'].remove(num_to_remove)
                    return f"Number '{num_to_remove}' removed from nums for comment '{comment}'."
                else:
                    return f"Number '{num_to_remove}' not found in nums for comment '{comment}'."
        return f"Comment '{comment}' not found."

    def print_nums(spisok, comment):
        for item in spisok:
            if item['comment'] == comment:
                return item['nums']
        return f"Comment '{comment}' not found."

    class A(StatesGroup):
        edit = State()
        delete = State()
        add = State()

    @dp.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext):
        await bot.send_message(message.from_user.id, f"""<b>👑 Открываю клавиатуру...</b>""", reply_markup=main(), parse_mode=ParseMode.HTML)

    @dp.message(F.text == "🤖 Настройка дампера")
    async def start_handler(message: Message, state: FSMContext):
        await bot.send_message(message.from_user.id, f"""<b>🧊 Выбирите что настраивать</b>""", reply_markup=start_btn(), parse_mode=ParseMode.HTML)

    @dp.message(F.text == "🤖 Настройка дампера мелких звёзд")
    async def start_handler(message: Message, state: FSMContext):
        await bot.send_message(message.from_user.id, f"""<b>🧊 Выбирите что настраивать</b>""", reply_markup=start_btn1(), parse_mode=ParseMode.HTML)

    @dp.message(F.text == "💧 Получить список активных обьявлений")
    async def start_handler(message: Message, state: FSMContext):
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest"
        }
        from main import Data
        from SETTINGS import PROXY

        data_instance = Data()
        with open("data.json", 'r') as f:
            data_dict = json.load(f)
            data_instance = Data()
            data_instance.__dict__.update(data_dict)

        ord = []
        ord_today = []
        ord_yesterday = []

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://funpay.com/orders/trade?state=paid", headers={**data_instance.headers, **headers}, proxy=PROXY) as resp:
                reader = resp.content
                data = await reader.read()
                html_response = data.decode('utf-8')

            parser = BeautifulSoup(html_response, "lxml")

            next_order_id = parser.find("input", {"type": "hidden", "name": "continue"})
            next_order_id = next_order_id.get("value") if next_order_id else None

            order_divs = parser.find_all("a", {"class": "tc-item"})

            sales = []
            for div in order_divs:
                classname = div.get("class")
                if "info" in classname:
                    order_date_text = div.find("div", {"class": "tc-date-time"}).text
                    order_id = div.find("div", {"class": "tc-order"}).text[1:]
                    if order_date_text.count(" ") == 2:
                        ord.append(order_id)
                    elif any(today in order_date_text for today in ("сегодня", "сьогодні", "today")):
                        ord_today.append(order_id)
                    elif any(yesterday in order_date_text for yesterday in ("вчера", "вчора", "yesterday")):
                        ord_yesterday.append(order_id)

        await bot.send_message(message.from_user.id, f"""<b>🔗 Не закрытые обьявления сегодня: {ord_today}</b>""", parse_mode=ParseMode.HTML)
        await bot.send_message(message.from_user.id, f"""<b>🔗 Не закрытые обьявления вчера: {ord_yesterday}</b>""", parse_mode=ParseMode.HTML)
        await bot.send_message(message.from_user.id, f"""<b>🔗 Не закрытые обьявления в этом году: {ord}</b>""", parse_mode=ParseMode.HTML)

    @dp.callback_query(F.data.startswith("edit-"))
    async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        ref = callback_query.data.split("-")[1]
        await bot.send_message(callback_query.from_user.id, f"""<b>💳 Выбирите действие</b>""", reply_markup=edit_btn(ref), parse_mode=ParseMode.HTML)

    @dp.callback_query(F.data.startswith("edit-"))
    async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        ref = callback_query.data.split("-")[1]
        await bot.send_message(callback_query.from_user.id, f"""<b>💳 Выбирите действие</b>""", reply_markup=edit_btn(ref), parse_mode=ParseMode.HTML)

    @dp.callback_query(F.data.startswith("smena-"))
    async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        ref = callback_query.data.split("-")[1]
        await state.update_data(ref=ref)
        await state.set_state(A.edit)
        await bot.send_message(callback_query.from_user.id, f"""<b>💳 Введите id нового обьявления</b>""", parse_mode=ParseMode.HTML)

    @dp.message(A.edit)
    async def start_handler(message: Message, state: FSMContext):
        data = await state.get_data()
        await state.clear()
        spisok = load_data("dump.json")

        update = update_value(spisok, data["ref"], message.text)
        save_data("dump.json", spisok)

        if "Value updated for comment" in str(update):
            await bot.send_message(message.from_user.id, f"""<b>🍀 Обьялвение успешно сменено</b>""", parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(message.from_user.id, str(update), parse_mode=ParseMode.HTML)

    @dp.callback_query(F.data.startswith("delete-"))
    async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        ref = callback_query.data.split("-")[1]
        await state.update_data(ref=ref)
        await state.set_state(A.delete)
        spisok = load_data("dump.json")
        obj = print_nums(spisok, ref)
        await bot.send_message(callback_query.from_user.id, f"""<b>💳 Введите id обьявления для удаления, текущие обьявления: {str(obj)}</b>""", parse_mode=ParseMode.HTML)

    @dp.message(A.delete)
    async def start_handler(message: Message, state: FSMContext):
        data = await state.get_data()
        await state.clear()
        spisok = load_data("dump.json")

        update = remove_from_nums(spisok, data["ref"], message.text)
        save_data("dump.json", spisok)

        if "removed from nums for comment " in str(update):
            await bot.send_message(message.from_user.id, f"""<b>🍀 Обьявление было успешно удалено</b>""", parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(message.from_user.id, str(update), parse_mode=ParseMode.HTML)

    @dp.callback_query(F.data.startswith("add-"))
    async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        ref = callback_query.data.split("-")[1]
        await state.update_data(ref=ref)
        await state.set_state(A.add)
        spisok = load_data("dump.json")
        obj = print_nums(spisok, ref)
        await bot.send_message(callback_query.from_user.id, f"""<b>💳 Введите id обьявления для добавления, текущие обьявления: {str(obj)}</b>""", parse_mode=ParseMode.HTML)

    @dp.message(A.add)
    async def start_handler(message: Message, state: FSMContext):
        data = await state.get_data()
        await state.clear()
        spisok = load_data("dump.json")

        update = add_to_nums(spisok, data["ref"], message.text)
        save_data("dump.json", spisok)

        if "added to nums for comment " in str(update):
            await bot.send_message(message.from_user.id, f"""<b>🍀 Обьялвение было успешно добавлено</b>""", parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(message.from_user.id, str(update), parse_mode=ParseMode.HTML)
    
    await dp.start_polling(bot)