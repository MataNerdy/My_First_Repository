import asyncio


async def cook_pasta(name, time):
    print(f"{name}: Начинаю варить пасту")
    await asyncio.sleep(time)
    print(f"{name}: Паста готова!")
    return f'{name} готово'

async def main():
    task1 = asyncio.create_task(cook_pasta("Повар А", 3))
    task2 = asyncio.create_task(cook_pasta("Повар Б", 2))

    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())