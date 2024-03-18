from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.prof_keyboards import make_row_keyboard
from keyboards.keyboards import kb1, kb2



router = Router()


available_prof_names = ["Разработчик", "Аналитик", "Тестировщик"]
available_prof_grades = ["Junior", "Middle", "Senior"]
available_prof_salary = ["от 100 000 до 150 000", "от 150 000 до 200 000", "от 200 000 до 300 000", "более 300 000"]


class ChoiceProfNames(StatesGroup):
    choice_prof_names = State()
    choice_prof_grades = State()
    choice_prof_salary = State()

#Хэндлер на команду /prof
@router.message(Command('prof'))
async def cmd_prof(message: types.Message, state: FSMContext):
    name = message.chat.first_name
    await message.answer(
        f'{name}, Выбери свою профессию',
        reply_markup=make_row_keyboard(available_prof_names)
    )
    await state.set_state(ChoiceProfNames.choice_prof_names)


@router.message(ChoiceProfNames.choice_prof_names, F.text.in_(available_prof_names))
async def grade_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_prof=message.text.lower())
    await message.answer(
        text='Спасибо, Теперь выбери свой уровень',
        reply_markup=make_row_keyboard(available_prof_grades)
    )
    await state.set_state(ChoiceProfNames.choice_prof_grades)


@router.message(ChoiceProfNames.choice_prof_grades, F.text.in_(available_prof_grades))
async def salary_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_grades=message.text.lower())
    await message.answer(
        text='Спасибо, Теперь выбери желаемый уровень зарплаты',
        reply_markup=make_row_keyboard(available_prof_salary)
    )
    await state.set_state(ChoiceProfNames.choice_prof_salary)



@router.message(ChoiceProfNames.choice_prof_salary, F.text.in_(available_prof_salary))
async def prof_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_salary=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        f'Вы выбрали {user_data.get("chosen_grades")} уровень.\nВаша профессия {user_data.get("chosen_prof")}.\nУровень зарплаты {user_data.get("chosen_salary")}\n'
        f'Мы свяжемся с Вами при наличии вакансии Вашего уровня', reply_markup=kb1
    )
    await state.clear()


@router.message(ChoiceProfNames.choice_prof_names)
async def prof_chosen_incorrectly(message: types.Message):
    await message.answer(
        'Я не знаю такой профессии',
        reply_markup=make_row_keyboard(available_prof_names)
    )

@router.message(ChoiceProfNames.choice_prof_grades)
async def grade_chosen_incorrectly(message: types.Message):
    await message.answer(
        'Я не знаю такой уровень',
        reply_markup=make_row_keyboard(available_prof_grades)
    )

@router.message(ChoiceProfNames.choice_prof_salary)
async def salary_chosen_incorrectly(message: types.Message):
    await message.answer(
        'Выберите из предложенных уровней зарплаты',
        reply_markup=make_row_keyboard(available_prof_salary)
    )

