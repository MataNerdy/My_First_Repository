import asyncio


async def waiter(event, name):
    print(f"Ожидающий {name} начал ждать")
    await event.wait()
    print(f"Ожидающий {name} дождался и продолжает работу")

async def setter(event):
    print("Установщик: подожду 2 секунды...")
    await asyncio.sleep(2)
    print("Установщик: устанавливаю событие!")
    event.set()

async def main():
    event = asyncio.Event()
    await asyncio.gather(
        waiter(event, 'A'),
        waiter(event, 'B'),
        waiter(event, 'C'),
        setter(event)
    )

asyncio.run(main())