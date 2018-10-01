import math as m


def free_space_loss(distance, frequency, gtx=0, grx=0):
    # Distance in km and frequency in MHz. FSPL result in dBs
    # Gtx overall transmitter antenna gain including feeder losses
    # grx overall receiver antenna gain including feeder losses
    fspl = 20*m.log10(distance*frequency) + 32.44 - gtx - grx
    return fspl


def main():
    print(free_space_loss(20, 150))


if __name__ == '__main__':
    main()