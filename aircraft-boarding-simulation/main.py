from boarding import BoardingFTB, BoardingBTF, BoardingWTA, BoardingATW, BoardingRandom, BoardingSteffen

def main():
    # select one boarding method
    test = BoardingFTB()
    # test = BoardingBTF()
    # test = BoardingWTA()
    # test = BoardingATW()
    # test = BoardingRandom()
    # test = BoardingSteffen()

    avg, steps = test.test_boarding_method(12, 50)

    print("Boarding took {} steps on average".format(avg))
    print(steps)

if __name__ == '__main__':
    main()
