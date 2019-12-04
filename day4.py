#!/usr/bin/env python


def test_password(password):

    # Does it have two adjacent digits that are the same
    password_str = str(password)
    for x, y in zip(password_str, password_str[1:]):
        if x == y:
            break
    else:
        return False

    # Do digits never decrease?
    for x, y in zip(password_str, password_str[1:]):
        if int(x) > int(y):
            return False

    return True


def main():
    start = 254032
    end = 789860

    print(test_password(111111))
    print(test_password(223450))
    print(test_password(123789))

    count = sum(test_password(x) for x in range(start, end + 1))

    print(count)


if __name__ == "__main__":
    main()
