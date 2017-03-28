from . import settings

def usage():
    print("BooliPy >> Access to Booli API with CALLER_ID={id}".format(id=settings.CALLER_ID))

def main():
    usage()


if __name__ == '__main__':
    main()
