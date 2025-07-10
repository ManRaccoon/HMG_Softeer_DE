import logger


def main():
    logger.start("EXTRACT")

    logger.end("EXTRACT")

    logger.start("TRANSFORM")

    logger.end("TRANSFORM")

    logger.start("LOAD")

    logger.end("LOAD")


if __name__ == "__main__":
    main()