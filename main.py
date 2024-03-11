from pathlib import Path
# директория под логи
Path("logs").mkdir(parents=True, exist_ok=True)

import asyncio
from sys import argv
from utils.loggers import main_logger

async def main():
    from telegram.owner import account
    from telegram.bot import run_bot
    from reddit import stream

    if await account.check_owner():
        main_logger()
        await asyncio.gather(run_bot(), stream.event_loop())
    else:
        pint("turn OFFs program")


if __name__ == "__main__":

    if 0<len(argv[1:])<2 and str(argv[1:][0]) in ['-R', '--run',
                                            '-U', '--upload']:
        option = str(argv[1:][0])

        if option in ['-R', '--run']:

            asyncio.run(main())

        if option in ['-U', '--upload']:

            from telegram.owner import sing_in
            asyncio.run(sing_in.main())
                
    else:
        print("""usage: main.py [option]

    options:
    -R, --run Запустить проект

    -U, --upload Загрузить новый аккаунт
    """)