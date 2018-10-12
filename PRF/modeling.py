import math as m


def free_space_loss(distance, frequency, gtx=0, grx=0):
    # Distance in km and frequency in MHz. FSPL result in dBs
    # Gtx overall transmitter antenna gain including feeder losses
    # grx overall receiver antenna gain including feeder losses
    fspl = 20*m.log10(distance*frequency) + 32.44 - gtx - grx
    return fspl


cff_kh = [
    [-5.33980, -0.10008, 1.13098],
    [-0.35351, 1.26970, 0.45400],
    [-0.23789, 0.86036, 0.15354],
    [-0.94158, 0.64552, 0.16817]
]

cff_kv = [
    [-3.80595, 0.56934, 0.81061],
    [-3.44965, -0.22911, 0.51059],
    [-0.39902, 0.73042, 0.11899],
    [0.50167, 1.07319, 0.27195]
]

cff_ah = [
    [-0.14318, 1.82442, -0.55187],
    [0.29591, 0.77564, 0.19822],
    [0.32177, 0.63773, 0.13164],
    [-5.37610, -0.96230, 1.47828],
    [16.1721, -3.29980, 3.43990]
]

cff_av = [
    [-0.07771, 2.33840, -0.76284],
    [0.56727, 0.95545, 0.54039],
    [-0.20238, 1.14520, 0.26809],
    [-48.2991, 0.791669, 0.116226],
    [48.5833, 0.791459, 0.116479],

]


def precipitation_loss(rr, freq, vertical=False):
    if vertical:
        mk = -0.16398
        ck = 0.63297
        ma = -0.053739
        ca = 0.83433
        cff_k = cff_kv
        cff_a = cff_av
    else:
        mk = -0.18961
        ck = 0.71147
        ma = 0.67849
        ca = -1.95537
        cff_k = cff_kh
        cff_a = cff_ah

    # Calculating K
    sigmak = 0
    for i in range(0, 4):  # Sum
        aj, bj, cj = cff_k[i]
        sigmak += aj * m.exp(-pow((m.log10(freq)-bj)/cj, 2))
    logk = sigmak + mk * m.log10(freq) + ck
    k = pow(10, logk)

    # Calculating Alpha
    sigma = 0
    for i in range(0, 5):  # Sum
        aj, bj, cj = cff_a[i]
        sigma += aj * m.exp(-pow((m.log10(freq)-bj)/cj, 2))
    alpha = sigma + ma * m.log10(freq) + ca

    return k * pow(rr, alpha)


def main():
    print(free_space_loss(100, 20))


if __name__ == '__main__':
    main()
