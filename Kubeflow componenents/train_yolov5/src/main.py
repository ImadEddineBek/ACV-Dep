import fire

from augmenter import augment


COMMANDS = {
    'augment': augment,
}

if __name__ == '__main__':
    fire.Fire(COMMANDS)
