from tasks import ParseTendersTask

def main():
    ParseTendersTask.apply_async(args = (2, ))

if __name__ == "__main__":
    main()
