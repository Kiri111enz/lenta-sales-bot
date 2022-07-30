from bot import bot


def main() -> None:
    bot.start()


if __name__ == '__main__':
    main()
else:
    raise ImportError('launcher.py should not be imported.')
