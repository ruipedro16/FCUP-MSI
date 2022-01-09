from sage.all import *


def gen_pub_key(A, B, p, x_p, y_p):
    Fp = FiniteField(p)
    E = EllipticCurve(Fp, [A, B])
    assert(E.is_on_curve(x_p, y_p))

    P = E([x_p, y_p])
    n_a = ZZ(Fp.random_element())  # secret multiplier
    Q_A = n_a * P  # public key

    return (Q_A, n_a)


def encrypt(A, B, p, x_p, y_p, Q_A, m_1, m_2):
    Fp = FiniteField(p)
    E = EllipticCurve(Fp, [A, B])
    assert(E.is_on_curve(x_p, y_p))

    P = E([x_p, y_p])
    k = ZZ(Fp.random_element())  # ephemeral key
    R = k * P

    S = k * Q_A
    c_1 = (S[0] * m_1) % p
    c_2 = (S[1] * m_2) % p

    return (R, c_1, c_2)


def decrypt(A, B, p, x_p, y_p, R, n_a, c_1, c_2):
    Fp = FiniteField(p)
    E = EllipticCurve(Fp, [A, B])
    assert(E.is_on_curve(x_p, y_p))

    T = n_a * R
    m_1 = (T[0] ** (-1) * c_1) % p
    m_2 = (T[1] ** (-1) * c_2) % p

    return (m_1, m_2)
