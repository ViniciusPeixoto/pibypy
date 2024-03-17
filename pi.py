from utils.aggregate import aggregate


def main() -> None:
    output = aggregate()
    print(output.number)


if __name__ == "__main__":
    main()
