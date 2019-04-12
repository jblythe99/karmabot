


def mongo():
    pass


def pickle():

    USERNAME_CACHE = {}
    KARMA_CACHE = 'data'

    try:
        logging.info('Retrieving karma cache file')
        karmas = pickle.load(open(KARMA_CACHE, "rb"))

    except FileNotFoundError:
        logging.info('No cache file starting new Counter object in memory')
        karmas = Counter()

    setup = []
    return karmas,setup
