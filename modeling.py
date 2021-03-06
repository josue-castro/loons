import math as m


def free_space_loss(distance, frequency, gtx=0, grx=0):
    # Distance in km and frequency in GHz. FSPL result in dBs
    # gtx overall transmitter antenna gain including feeder losses
    # grx overall receiver antenna gain including feeder losses
    fspl = 20*m.log10(distance*frequency*1000) + 32.44 - gtx - grx
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


def precipitation_loss(rr, freq, distance=1, vertical=False):
    # rr = Rain Rate (mm/h)
    # freq = Frequency (GHz)
    # distance (Km)
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

    return k * pow(rr, alpha) * distance


def cloudfog_loss(freq, density, temp, distance=1):
    # Frequency (GHz), Temperature (K)
    # Density - liquid water density in the cloud or fog (g/m3)
    f = freq
    theta = 300 / temp
    e0 = 77.6 + 103.3*(theta - 1)
    e1 = 5.48
    e2 = 3.51

    # principal and secondary relaxation frequencies
    fp = 20.09 - 142*(theta - 1) + 294*(theta - 1)**2  # GHz
    fs = 590 - 1500*(theta - 1)  # GHz

    # e'(f) and e''(f)
    E1 = ((e0 - e1)/(1+(f/fp)**2) + ((e1 - e2)/(1+(f/fs)**2)) + e2)
    E2 = ((f/fp)*(e0 - e1)/(1+(f/fp)**2) + (f/fs)*((e1 - e2)/(1+(f/fs)**2)))

    N = (2 + E1)/E2

    # specific attenuation coefficient
    K = (0.819*f)/(E2*(1+N**2))
    return K*density*distance  # with distance = 1 result dB/Km else dB


if __name__ == '__main__':
    print(precipitation_loss(3.3, 100))
