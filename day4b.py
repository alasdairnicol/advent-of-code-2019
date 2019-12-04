#!/usr/bin/env python


def test_password(password):

    # Does it have two adjacent digits that are the same
    password_str = str(password)
    for (i, x) in enumerate(password_str[:-1]):
        if (i > 0 and x == password_str[i-1]):
            # Same as previous digit, ignore so we don't get three in a row
            continue
        if x == password_str[i+1]:
            # if i + 2 == len(password_str) then password_str[i + 2] would be out of range
            if i + 2 == len(password_str) or password_str[i + 1] != password_str[i+2]:
                # Success, we've found xAAy
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
    count = sum(test_password(x) for x in range(start, end + 1))

    print(count)


if __name__ == "__main__":
    main()
