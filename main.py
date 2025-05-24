import aiogram
import asyncio
import os
import sys
from g4f import Client
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile
from aiogram import Router, types
from dotenv import load_dotenv, find_dotenv

client = Client()

load_dotenv(find_dotenv())
dp = Dispatcher()

async def generate(prompt_text: str) -> str | None:
    try:
        response = await client.images.async_generate(
            model="flux",
            prompt=prompt_text,
            response_format="url"
        )
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            return image_url
        else:
            print("Error")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


@dp.message()
async def command_start_handler(message: types.Message) -> None:
    input_text = message.text
    print(f"Input: {input_text}")

    image_url = await generate(input_text)

    if image_url:
        print(f"Output: {image_url}")
        await message.answer_photo(URLInputFile(image_url))
    else:
        await message.answer("Error")


async def main() -> None:
    token = os.getenv('TOKEN')
    if not token:
        print("Token not found")
        sys.exit(1)

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
