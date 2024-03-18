from aiogram import types, F, Router
from aiogram.filters.command import Command
import logging
import random
import requests
from keyboards.keyboards import kb1, kb2
from utils.random_fox import fox


router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'Здравствуйте, {name}! Я бот техподдержки. Для выбора команды воспользуйтесь кнопками ниже или введите сообщение в чате.', reply_markup=kb1)

#Хендлер на команду weather
@router.message(Command('weather'))
async def process_message(message: types.Message):
        data = requests.get('https://wttr.in/?format=3')
        await message.answer(data.text)

@router.message(Command('weather1'))
async def process_weather_command(message: types.Message):
    city = message.get_args()
    url ="http://api.openweathermap.org/data/2.5/weather?q={city}&appid=43213d417b53045aa1b6617c529c910&units"/f"=metric&lang=ru "
    res = requests.get(url)
    data = res.json()['main']
    temp = data['temp']
    weather1 = str(temp)
    await bot.send_message(message.from_user.id, f'В городе *{city}* {weather1}градусов по цельсия',parse_mode="Markdown")

#Хендлер на команду info
@router.message(Command('info'))
async def info_command(message: types.Message):
    # await message.reply('/start\n/weather\n/stop\n фраза "Покажи лису"')
    await message.reply(f'"/start" запускает бота и(или) вызывает клавиатуру \n"/weather" показывает погоду в Москве\n"/stop" прекращает работу с ботом\n '\
                        f'фраза "Покажи лису" показывает случайное фото лисы\n "/prof" запускает диалог по квалификации IT специалистов\n'\
                        f'при выборе фразы "Кинь кость", бот бросает игральную кость\n при выборе фразы "Забей мяч", бот бьет по футбольным воротам\n'\
                        f'если в фразе есть "умеешь" или "можешь", бот предлагает клавиатуру с кнопками "Покажи лису", "/weather", "кость" или "ворота"\n'\
                        f'На вопрос "ты кто" или "как тебя зовут" бот представляется')


#Хендлер на команду stop
@router.message(Command('stop'))
async def cmd_stop(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'До свидания, {name}')


@router.message(F.text.lower() == 'покажи лису')
async def cmd_fox(message: types.Message):
    name = message.chat.first_name
    img_fox = fox()
    await message.answer(f'Держи лису, {name}')
    await message.answer_photo(photo=img_fox)


#Хендлер на сообщения
@router.message(F.text)
async def msg_echo(message: types.Message):
    msg_user = message.text.lower()
    name = message.chat.first_name
    if 'привет' in msg_user:
        await message.answer(f'Привет, {name}')
    elif 'пока' in msg_user or 'до свидания' in msg_user:
        await message.answer(f'До свидания! Удачи!, {name}')
    elif 'Кинь' and 'кость' in msg_user:
        await message.answer_dice(emoji="🎲")
    elif 'Забей' and 'мяч' in msg_user:
        await message.answer_dice(emoji="⚽")
    elif 'умеешь' in msg_user or 'можешь' in msg_user:
        await message.answer(f'{name}, Смотри что у меня есть', reply_markup = kb2)
    elif 'ты кто' in msg_user or 'Как тебя зовут' in msg_user:
        await message.answer(f'Я бот, {name}')

    else:
        await message.answer(f'Я не знаю таких слов')


