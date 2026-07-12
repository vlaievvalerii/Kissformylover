import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from random import choice

from aiogram import BaseMiddleware, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

VALERA_CHAT_ID = 460158653
ALLOWED_USER_ID = 930150115
MORNING_MESSAGE_HOUR = 4
MORNING_MESSAGE_MINUTE = 59
MORNING_HISTORY_FILE = Path(__file__).with_name("morning_message_history.txt")
MORNING_SETTINGS_FILE = Path(__file__).with_name("morning_messages_enabled.txt")
MORNING_REPEAT_DAYS = 7
IMAGES_DIR = Path(__file__).with_name("images")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
IMAGE_KEYWORDS = {
    "morning": ["belive", "believe", "worry", "proud", "pushing", "love you"],
    "support": ["belive", "believe", "worry", "can do", "proud", "pushing", "pinky"],
    "hug": ["hug", "take me with you"],
    "compliment": ["love you", "this much", "proud", "romantic", "tastyy"],
    "miss": ["miss", "take me with you"],
    "angry": ["angy", "angry", "fight", "wanna fight"],
    "sorry": ["sorrrry", "sorry", "pinky"],
    "fun": ["weeeee"],
    "coding_cat": ["valera coding", "coding cat", "cat mem"],
    "date_walk": ["take me with you", "weeeee", "miss"],
    "date_coffee": ["romantic", "love you", "this much"],
    "date_movie": ["love you", "miss", "pinky"],
    "date_food": ["tastyy", "love you", "this much"],
    "date_home": ["hug", "love you", "pinky"],
    "date_talk": ["miss", "hug", "romantic", "pinky"],
}


STICKERS = [
    "CAACAgIAAxkBAAPbakwUZWp04kg9qbZmvN7DpPr0nJsAAiEAA10FghbyGMUegi9alTwE",
    "CAACAgIAAxkBAAPdakwUb77KwenSaZsu1_9eGopu7AEAAiYPAAKhBmhLmwr0DL0iSrg8BA",
    "CAACAgIAAxkBAAPfakwUcXmYC8CsEDBEzJJEuf2wOBkAAr4NAAKUDWhLFQkGyIWPIYo8BA",
    "CAACAgIAAxkBAAPhakwUdfkmiDMKp2ed2ViXKbMzdM4AAoYPAAITi6lLR1SmjFGG4Y48BA",
    "CAACAgIAAxkBAAPjakwUegq2FVYEeZG791ArJoSDEeAAAgoRAAJpBuFJFrvCRwqwev48BA",
    "CAACAgIAAxkBAAPlakwUfqNRRmrm8hxM5JxQ4koT1TYAAtUVAAJiTKFLtEn4Sw0DBLY8BA",
    "CAACAgQAAxkBAAPnakwUgvrjyWXAxq2luEXbeRCNeEwAAjEAA845CA3LdQk6GshD1zwE",
    "CAACAgQAAxkBAAPpakwUlh5qtnMiqZaZGe-q2tveibIAAkIAA845CA39lygZIRS_PjwE"
    "CAACAgIAAxkBAAOYakqweEcrwYbvPuqNJSgij7dqFZ8AAh4AA10FghalOW3LAAHw8dI8BA"
]

REACTIONS = ["🤍", "🫶", "✨", "🥰", "🌷", "☕", "🍓", "🧸"]

SUPPORT_TEXTS = [
    "Я тут. Давай просто видихнемо. Не треба зараз все вирішувати.",
    "Тобі важко - це нормально. Я з тобою, без зайвих питань.",
    "Зроби ковток води і сядь зручніше. Маленька пауза вже рахується.",
    "Сьогодні можна бути не ідеальною. Просто побудь трохи до себе добрішою.",
    "Я тебе почув. Все не обов'язково має бути добре прямо зараз.",
    "Давай без паніки. Один крок, потім ще один. Ти справишся.",
    "Не поспішай збирати себе докупи. Можна просто трохи побути й перевести подих.",
    "Я поруч. Розкажеш, коли захочеш, а поки просто бережи себе.",
    "Сьогодні достатньо зробити стільки, скільки вистачає сил. Не більше.",
    "Якщо день важкий — це не означає, що з тобою щось не так.",
]

COMPLIMENTS = [
    "Ти дуже красива. От просто факт.",
    "У тебе така усмішка, що день стає кращим.",
    "Ти мила, але з характером. Дуже сильне комбо.",
    "З тобою тепло. Навіть через чат.",
    "Ти сьогодні точно заслуговуєш на щось приємне.",
    "Ти класна. І я не перебільшую.",
    "У тебе дуже гарні очі. Так, це треба було сказати.",
    "Ти виглядаєш як людина, яку хочеться берегти.",
    "Мені дуже подобається, як ти думаєш і помічаєш дрібниці.",
    "З тобою навіть звичайний день відчувається особливим.",
    "Ти неймовірно мила, особливо коли сама цього не помічаєш.",
    "У тобі є щось дуже рідне й затишне.",
]

HUGS = [
    "Обіймаю. Тихо-тихо. Без лекцій.",
    "Тримай обійми в чаті. Я старався зробити їх теплими.",
    "Підійди подумки ближче. Все, обійняв.",
    "Я б зараз просто посидів поруч і дав тобі відпочити.",
    "Іди до мене. Обійму міцно й нікуди не відпущу кілька хвилин.",
    "Уяви, що я поруч, накрив тебе пледом і тихенько обійняв.",
    "Тримай великі теплі обійми. Саме такі, як тобі зараз треба.",
]

SURPRISES = [
    "Сюрприз: сьогодні ти маєш право нічого не доводити.",
    "Маленьке завдання: зроби собі чай або щось смачне.",
    "Нагадування: ти не занадто емоційна. Ти жива.",
    "Твій план на 10 хвилин: видихнути і не сварити себе.",
    "Сьогодні офіційно можна хотіти уваги.",
    "Термінове повідомлення: я скучив і хочу тебе обійняти.",
    "Маленький сюрприз: сьогодні я люблю тебе ще сильніше, ніж учора.",
    "Обери собі щось смачне — сьогодні це обов'язкова частина плану.",
]

MORNING_MESSAGES = [
    "Доброго ранку. Нехай сьогодні буде трохи легше, ніж ти очікуєш.",
    "Новий день. Пий воду, не спіши і не забувай, що ти класна.",
    "Доброго ранку. Сьогодні не треба бути ідеальною, достатньо бути собою.",
    "Прокидайся потихеньку. Нехай день буде м'який і без зайвого шуму.",
    "Ранкове нагадування: ти справишся. А якщо ні - можна зробити паузу і спробувати ще раз.",
    "Хай сьогодні буде щось смачне, щось смішне і хоч один дуже хороший момент.",
    "Доброго ранку. Нехай люди сьогодні не нервують тебе більше, ніж треба.",
    "Сьогодні твоя місія проста: берегти себе і не сварити себе за дрібниці.",
    "Нехай день буде нормальний. А якщо стане важко, я тут.",
    "Ранок прийшов, а значить можна почати дуже повільно і все одно молодець.",
    "Доброго ранку. Нехай кава або чай сьогодні будуть смачні, а люди - адекватні.",
    "Сьогодні можна не поспішати серцем. Все важливе встигне.",
    "Нехай день буде добрий до тебе. А якщо ні, ми з ним поговоримо.",
    "Ранковий план: не забути поїсти, не забути видихнути, не забути, що ти хороша.",
    "Доброго ранку. Хай сьогодні знайдеться причина усміхнутись просто так.",
    "Ти вже молодець, бо почала цей день. Далі можна маленькими кроками.",
    "Нехай сьогодні буде менше хаосу і більше маленьких приємностей.",
    "Доброго ранку. Бережи себе так, ніби ти для себе дуже важлива. Бо так і є.",
    "Хай день буде м'який. Без зайвих драм, різких людей і дурних думок.",
    "Ранкове нагадування: ти не повинна тягнути все на собі.",
    "Нехай сьогодні щось хороше саме знайде тебе.",
    "Доброго ранку. Не забувай: іноді найкращий темп - повільний.",
    "Хай сьогодні буде хоч один момент, який захочеться запам'ятати.",
    "Починай день ніжно. Світ зачекає, поки ти прокинешся нормально.",
    "Доброго ранку. Ти не робот, тому маєш право втомлюватись і робити паузи.",
    "Сьогодні без героїзму, добре? Просто живемо, їмо щось смачне і не сваримо себе.",
    "Нехай день буде легкий на серці і теплий у дрібницях.",
    "Ранок каже: час бути до себе трохи добрішою.",
    "Доброго ранку. Я вірю, що сьогодні в тебе вийде більше, ніж здається.",
    "Хай цей день не кусається. А якщо буде - я на твоєму боці.",
    "Доброго ранку, сонечко. Сподіваюсь, ти виспалась і сьогодні матимеш хороший день.",
    "Прокидайся, красуне. Нехай ранок буде спокійним, а настрій — теплим.",
    "Доброго ранку. Не забудь поснідати й узяти з собою гарний настрій. Люблю тебе.",
    "Нехай сьогодні все складається легко. А ввечері обов'язково розкажеш мені про свій день.",
    "Доброго ранку, моя хороша. Бажаю тобі сил, спокою і приємних людей поруч.",
    "Я просто хотів нагадати зранку, що ти в мене найкраща. Гарного тобі дня.",
    "Прокидайся потихеньку. Я вже думаю про тебе й дуже хочу, щоб ти сьогодні усміхалась.",
    "Доброго ранку, кохана. Нехай сьогодні станеться щось маленьке, але дуже приємне.",
    "Бажаю тобі теплого ранку, смачної кави й дня без зайвих переживань.",
    "Новий день почався, а я знову радий, що ти є в моєму житті. Доброго ранку.",
]

MOOD_REPLIES = {
    "😔 Мені сумно": [
        "Іди сюди. Сумно - це не соромно. Я побуду поруч.",
        "Мені шкода, що так. Давай без тиску: просто переживемо цей момент.",
        "Я поруч, моя хороша. Не треба зараз удавати, що все нормально.",
        "Хочеш — розкажи мені все. Не хочеш — просто побудемо разом.",
        "Обіймаю тебе. Цей настрій мине, а я нікуди не подінусь.",
    ],
    "😤 Я злюсь": [
        "Маєш право злитися. Серйозно. Спочатку видих, потім уже рішення.",
        "Не тримай все в собі. Злість теж щось хоче сказати.",
        "Розповідай, хто тебе розізлив. Я уважно слухаю.",
        "Твоя злість має причину. Давай спокійно розберемося разом.",
        "Зараз нічого не вирішуй на емоціях. Видихни, я з тобою.",
    ],
    "🫠 Я втомилась": [
        "Тоді режим тиші й відпочинку. Ніяких подвигів сьогодні.",
        "Втомилась - значить треба відновитись, а не добивати себе.",
        "Відклади все, що може почекати. Тобі справді треба відпочити.",
        "Іди полеж трохи, моя хороша. Решта справ нікуди не втече.",
        "Ти сьогодні вже достатньо зробила. Тепер час подбати про себе.",
    ],
    "🥺 Хочу уваги": [
        "Хочу уваги - це нормальна фраза. Ти не просиш забагато.",
        "Прийняв. Тобі зараз треба трохи тепла і щоб тебе не ігнорили.",
        "Уся моя увага зараз твоя. Розповідай, чого тобі хочеться.",
        "Іди сюди, я вже поруч. Можу слухати, обіймати й нагадувати, яка ти гарна.",
        "Ти заслуговуєш на увагу без жодних пояснень. Я тут.",
    ],
}

CALL_SENT_REPLIES = [
    "Передав. Він уже знає, що ти хочеш почути його голос.",
    "Готово, попросив його тобі зателефонувати.",
    "Передав прохання. Чекай на дзвінок 🤍",
]

WRITE_SENT_REPLIES = [
    "Передав. Він уже знає, що ти чекаєш на повідомлення.",
    "Готово, попросив його тобі написати.",
    "Прохання передано. Скоро він з'явиться в чаті 🤍",
]

DATE_SENT_REPLIES = [
    "Передав. Звучить як дуже хороший план.",
    "Він уже знає. Сподіваюсь, скоро домовитесь 🤍",
    "Готово, ідею побачення передано.",
]

DATE_IDEAS = {
    "date_walk": ("хоче з тобою погуляти", "Побачення: прогулянка 🚶‍♀️"),
    "date_coffee": ("хоче з тобою на каву або щось смачне", "Побачення: кава ☕"),
    "date_movie": ("хоче разом подивитись кіно або серіал", "Побачення: кіно 🎬"),
    "date_food": ("хоче сходити з тобою поїсти щось смачне", "Побачення: поїсти 🍕"),
    "date_home": ("хоче спокійний вечір разом вдома", "Побачення: вечір вдома 🛋"),
    "date_talk": ("хоче просто посидіти і поговорити з тобою", "Побачення: поговорити 🤍"),
}

router = Router()


def allowed_user_id() -> int | None:
    if is_valera(ALLOWED_USER_ID):
        return None

    return ALLOWED_USER_ID


def valera_chat_id() -> int | None:
    return VALERA_CHAT_ID


def is_valera(user_id: int) -> bool:
    return user_id == valera_chat_id()


def remember_first_user(user_id: int) -> bool:
    return False


class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        allowed_id = allowed_user_id()

        if user and allowed_id and user.id == allowed_id:
            await notify_button_press(event, user)
            return await handler(event, data)

        if not user or not allowed_id or is_valera(user.id):
            return await handler(event, data)

        if isinstance(event, Message):
            if event.text == "/myid":
                await event.answer(f"Твій Telegram ID: {user.id}")
                return None

            await event.answer("Вибач, цей бот тільки для однієї людини.")
            return None

        if isinstance(event, CallbackQuery):
            await event.answer("Доступ закритий", show_alert=True)
            return None

        return None


router.message.middleware(AccessMiddleware())
router.callback_query.middleware(AccessMiddleware())


CALLBACK_BUTTON_NAMES = {
    "support": "🫶 Підтримай",
    "hug": "🤍 Обійми",
    "mood_sad": "😔 Сумно",
    "mood_tired": "🫠 Втомилась",
    "mood_angry": "😤 Злюсь",
    "mood_attention": "🥺 Хочу уваги",
    "compliment": "✨ Комплімент",
    "surprise": "🎁 Сюрприз",
}

REPLY_BUTTON_NAMES = {
    "🫶 Підтримка",
    "📞 Зв'язок",
    "💕 Побачення",
    "✨ Ще",
    "🫶 Підтримай мене",
    "✨ Комплімент",
    "🤍 Обійми словами",
    "🎁 Сюрприз",
    "💕 Режим побачення",
    *MOOD_REPLIES.keys(),
}


async def notify_button_press(event, user) -> None:
    """Notify Valera about buttons which do not already send a notification."""
    button_name = None
    bot = None

    if isinstance(event, CallbackQuery):
        button_name = CALLBACK_BUTTON_NAMES.get(event.data)
        bot = event.bot
    elif isinstance(event, Message) and event.text in REPLY_BUTTON_NAMES:
        button_name = event.text
        bot = event.bot

    if not button_name or not bot or not valera_chat_id():
        return

    name = user.full_name
    username = f"@{user.username}" if user.username else "без username"
    try:
        await bot.send_message(
            chat_id=valera_chat_id(),
            text=f"{name} ({username}) натиснула: {button_name}",
        )
    except Exception:
        # A notification failure must not stop the bot from answering her.
        pass


def main_keyboard() -> ReplyKeyboardMarkup:
    morning_button = (
        "🌅 Ранкові: увімкнені"
        if morning_messages_enabled()
        else "🌙 Ранкові: вимкнені"
    )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🫶 Підтримка"), KeyboardButton(text="📞 Зв'язок")],
            [KeyboardButton(text="💕 Побачення"), KeyboardButton(text="✨ Ще")],
            [KeyboardButton(text=morning_button)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Що тобі зараз хочеться?",
    )


def support_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🫶 Підтримай", callback_data="support"),
                InlineKeyboardButton(text="🤍 Обійми", callback_data="hug"),
            ],
            [
                InlineKeyboardButton(text="😔 Сумно", callback_data="mood_sad"),
                InlineKeyboardButton(text="🫠 Втомилась", callback_data="mood_tired"),
            ],
            [
                InlineKeyboardButton(text="😤 Злюсь", callback_data="mood_angry"),
                InlineKeyboardButton(text="🥺 Хочу уваги", callback_data="mood_attention"),
            ],
        ]
    )


def more_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✨ Комплімент", callback_data="compliment"),
                InlineKeyboardButton(text="🎁 Сюрприз", callback_data="surprise"),
            ],
        ]
    )


def contact_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💌 Нехай напише", callback_data="ask_write"),
                InlineKeyboardButton(text="📞 Нехай набере", callback_data="ask_call"),
            ],
        ]
    )


def date_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚶‍♀️ Прогулянка", callback_data="date_walk"),
                InlineKeyboardButton(text="☕ Кава", callback_data="date_coffee"),
            ],
            [
                InlineKeyboardButton(text="🎬 Кіно", callback_data="date_movie"),
                InlineKeyboardButton(text="🍕 Поїсти", callback_data="date_food"),
            ],
            [
                InlineKeyboardButton(text="🛋 Вдома", callback_data="date_home"),
                InlineKeyboardButton(text="🤍 Поговорити", callback_data="date_talk"),
            ],
        ]
    )


async def send_sticker_safe(message: Message) -> None:
    try:
        await message.answer_sticker(choice(STICKERS))
    except Exception:
        await message.answer(choice(REACTIONS))


def local_images(category: str | None = None) -> list[Path]:
    if not IMAGES_DIR.exists():
        return []

    images = [
        path
        for path in IMAGES_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not category:
        return images

    keywords = IMAGE_KEYWORDS.get(category, [])
    matched = [
        path
        for path in images
        if any(keyword in path.stem.lower() for keyword in keywords)
    ]
    return matched or images


async def send_local_image(
    message: Message,
    caption: str | None = None,
    category: str | None = None,
) -> bool:
    images = local_images(category)
    if not images:
        return False

    try:
        await message.answer_photo(photo=FSInputFile(choice(images)), caption=caption)
        return True
    except Exception:
        return False


async def send_one_media(
    message: Message,
    category: str | None = None,
    caption: str | None = None,
    prefer_image: bool = True,
) -> None:
    if prefer_image:
        sent = await send_local_image(message, caption=caption, category=category)
        if sent:
            return

    await send_sticker_safe(message)


async def send_surprise_media(message: Message) -> None:
    category = choice(["fun", "fun", "coding_cat"])
    caption = None
    prefer_image = choice([True, False])

    if category == "coding_cat":
        caption = "Це Валера зараз пише код для цього бота."
        prefer_image = True

    await send_one_media(
        message,
        category=category,
        caption=caption,
        prefer_image=prefer_image,
    )


async def notify_valera(message: Message, action: str, user=None) -> bool:
    if not VALERA_CHAT_ID:
        await message.answer("Я хотів передати, але VALERA_CHAT_ID не налаштований у коді.")
        return False

    user = user or message.from_user
    name = user.full_name if user else "Вона"
    username = f"@{user.username}" if user and user.username else "без username"
    await message.bot.send_message(
        chat_id=VALERA_CHAT_ID,
        text=f"{name} ({username}) просить: {action}",
    )
    return True


async def forward_text_to_valera(message: Message) -> bool:
    valera_id = valera_chat_id()
    if not valera_id or is_valera(message.from_user.id):
        return False

    user = message.from_user
    name = user.full_name if user else "Vona"
    username = f"@{user.username}" if user and user.username else "bez username"
    await message.bot.send_message(
        chat_id=valera_id,
        text=f"Message from {name} ({username}):\n\n{message.text}",
    )
    return True

def seconds_until_next_morning() -> float:
    now = datetime.now()
    next_run = now.replace(
        hour=MORNING_MESSAGE_HOUR,
        minute=MORNING_MESSAGE_MINUTE,
        second=0,
        microsecond=0,
    )

    if next_run <= now:
        next_run += timedelta(days=1)

    return (next_run - now).total_seconds()


def morning_history() -> list[str]:
    if not MORNING_HISTORY_FILE.exists():
        return []

    return [
        line.strip()
        for line in MORNING_HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def remember_morning_message(text: str) -> None:
    history = morning_history()
    history.append(text)
    history = history[-MORNING_REPEAT_DAYS:]
    MORNING_HISTORY_FILE.write_text("\n".join(history), encoding="utf-8")


def choose_morning_message() -> str:
    recent = set(morning_history()[-MORNING_REPEAT_DAYS:])
    available = [text for text in MORNING_MESSAGES if text not in recent]

    if not available:
        available = MORNING_MESSAGES

    return choice(available)


def morning_messages_enabled() -> bool:
    if not MORNING_SETTINGS_FILE.exists():
        return True

    return MORNING_SETTINGS_FILE.read_text(encoding="utf-8").strip() != "0"


def set_morning_messages_enabled(enabled: bool) -> None:
    MORNING_SETTINGS_FILE.write_text("1" if enabled else "0", encoding="utf-8")


async def morning_messages_loop(bot) -> None:
    while True:
        await asyncio.sleep(seconds_until_next_morning())

        chat_id = allowed_user_id()
        if not chat_id:
            await asyncio.sleep(300)
            continue

        if not morning_messages_enabled():
            continue

        text = choose_morning_message()

        try:
            images = local_images("morning")
            if images:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=FSInputFile(choice(images)),
                    caption=text,
                    disable_notification=True,
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    disable_notification=True,
                )
            remember_morning_message(text)

            valera_id = valera_chat_id()
            if valera_id:
                await bot.send_message(
                    chat_id=valera_id,
                    text="✅ Ранкове повідомлення доставлено — бот активний.\n\n" + text,
                    disable_notification=True,
                )
        except Exception as error:
            valera_id = valera_chat_id()
            if valera_id:
                try:
                    await bot.send_message(
                        chat_id=valera_id,
                        text=(
                            "⚠️ Не вдалося доставити ранкове повідомлення. "
                            "Можливо, користувач заблокував бота або Telegram недоступний.\n"
                            f"Помилка: {type(error).__name__}"
                        ),
                    )
                except Exception:
                    pass
            await asyncio.sleep(300)


@router.message(Command("start"))
async def start(message: Message):
    user_was_saved = remember_first_user(message.from_user.id)
    await send_sticker_safe(message)
    if user_was_saved:
        await message.answer("Я запам'ятав тебе. Тепер цей бот тільки твій.")

    await message.answer(
        "Привіт. Я тут, щоб підтримати, підняти настрій або швидко передати прохання.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
async def help_message(message: Message):
    await message.answer(
        "Тисни кнопку. Я можу підтримати, дати комплімент або передати, що треба написати чи набрати.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("myid"))
async def my_id(message: Message):
    await message.answer(f"Твій Telegram ID: {message.from_user.id}")


@router.message(F.text == "🫶 Підтримка")
async def support_menu(message: Message):
    await message.answer("Що зараз треба?", reply_markup=support_keyboard())


@router.message(F.text == "📞 Зв'язок")
async def contact_menu(message: Message):
    await message.answer("Що передати?", reply_markup=contact_keyboard())


@router.message(F.text == "💕 Побачення")
async def date_menu(message: Message):
    await message.answer("Що хочеться?", reply_markup=date_keyboard())


@router.message(F.text == "✨ Ще")
async def more_menu(message: Message):
    await message.answer("Тримай ще трохи приємного.", reply_markup=more_keyboard())


@router.message(F.text.in_({"🌅 Ранкові: увімкнені", "🌙 Ранкові: вимкнені"}))
async def toggle_morning_messages(message: Message):
    enabled = not morning_messages_enabled()
    set_morning_messages_enabled(enabled)

    status = "увімкнула" if enabled else "вимкнула"
    await message.answer(
        f"Ранкові повідомлення {status}.",
        reply_markup=main_keyboard(),
    )

    if valera_chat_id():
        user = message.from_user
        name = user.full_name if user else "Вона"
        username = f"@{user.username}" if user and user.username else "без username"
        try:
            await message.bot.send_message(
                chat_id=valera_chat_id(),
                text=f"🌅 {name} ({username}) {status} ранкові повідомлення.",
            )
        except Exception:
            pass


@router.message(F.text == "🫶 Підтримай мене")
async def support(message: Message):
    await message.answer(choice(SUPPORT_TEXTS))
    await send_one_media(
        message,
        category="support",
        caption=choice(["Тримай трохи тепла.", "Я поруч.", "Для настрою."]),
    )


@router.message(F.text == "✨ Комплімент")
async def compliment(message: Message):
    await message.answer(choice(COMPLIMENTS))
    await send_local_image(message, category="compliment")


@router.message(F.text == "🤍 Обійми словами")
async def hug(message: Message):
    await message.answer(choice(HUGS))
    await send_local_image(message, category="hug")


@router.message(F.text == "🎁 Сюрприз")
async def surprise(message: Message):
    await message.answer(choice(SURPRISES))
    await send_surprise_media(message)


@router.message(F.text == "📞 Набери мене")
async def ask_call(message: Message):
    sent = await notify_valera(message, "набрати")
    if sent:
        await message.answer(choice(CALL_SENT_REPLIES))
        await send_local_image(message, category="miss")


@router.message(F.text == "💌 Напиши мені")
async def ask_write(message: Message):
    sent = await notify_valera(message, "написати")
    if sent:
        await message.answer(choice(WRITE_SENT_REPLIES))
        await send_local_image(message, category="miss")


@router.message(F.text == "💕 Режим побачення")
async def date_mode(message: Message):
    await message.answer(
        "Що хочеться? Обери, а я передам.",
        reply_markup=date_keyboard(),
    )


@router.callback_query(F.data == "ask_call")
async def ask_call_inline(callback: CallbackQuery):
    sent = await notify_valera(callback.message, "набрати", callback.from_user)
    await callback.answer("Передав" if sent else "Не налаштовано")
    if sent:
        await callback.message.answer(choice(CALL_SENT_REPLIES))
        await send_local_image(callback.message, category="miss")


@router.callback_query(F.data == "ask_write")
async def ask_write_inline(callback: CallbackQuery):
    sent = await notify_valera(callback.message, "написати", callback.from_user)
    await callback.answer("Передав" if sent else "Не налаштовано")
    if sent:
        await callback.message.answer(choice(WRITE_SENT_REPLIES))
        await send_local_image(callback.message, category="miss")


@router.callback_query(F.data == "support")
async def support_inline(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(choice(SUPPORT_TEXTS))
    await send_one_media(
        callback.message,
        category="support",
        caption=choice(["Тримай трохи тепла.", "Я поруч.", "Для настрою."]),
    )


@router.callback_query(F.data == "hug")
async def hug_inline(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(choice(HUGS))
    await send_local_image(callback.message, category="hug")


@router.callback_query(F.data == "compliment")
async def compliment_inline(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(choice(COMPLIMENTS))
    await send_local_image(callback.message, category="compliment")


@router.callback_query(F.data == "surprise")
async def surprise_inline(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(choice(SURPRISES))
    await send_surprise_media(callback.message)


@router.callback_query(F.data.startswith("mood_"))
async def mood_inline(callback: CallbackQuery):
    mood_map = {
        "mood_sad": "😔 Мені сумно",
        "mood_angry": "😤 Я злюсь",
        "mood_tired": "🫠 Я втомилась",
        "mood_attention": "🥺 Хочу уваги",
    }
    text = mood_map.get(callback.data)
    await callback.answer()
    if text:
        await callback.message.answer(choice(MOOD_REPLIES[text]))
        category = "angry" if callback.data == "mood_angry" else "support"
        await send_local_image(callback.message, category=category)


@router.callback_query(F.data.in_(DATE_IDEAS.keys()))
async def date_choice(callback: CallbackQuery):
    action, title = DATE_IDEAS[callback.data]
    sent = await notify_valera(callback.message, action, callback.from_user)
    await callback.answer("Передав" if sent else "Не налаштовано")
    if sent:
        await callback.message.answer(f"{title}\n{choice(DATE_SENT_REPLIES)}")
        await send_local_image(callback.message, category=callback.data)


@router.message(F.text.in_(MOOD_REPLIES.keys()))
async def mood(message: Message):
    await message.answer(choice(MOOD_REPLIES[message.text]))


@router.message(F.text)
async def fallback(message: Message):
    text = message.text.strip().lower()

    if any(word in text for word in ["напиши", "написати"]):
        await ask_write(message)
        return

    if any(word in text for word in ["набери", "подзвони", "дзвони", "набрати"]):
        await ask_call(message)
        return
    await forward_text_to_valera(message)

    await message.answer(
        "Я почув. Вибери кнопку нижче, так буде швидше.",
        reply_markup=main_keyboard(),
    )
