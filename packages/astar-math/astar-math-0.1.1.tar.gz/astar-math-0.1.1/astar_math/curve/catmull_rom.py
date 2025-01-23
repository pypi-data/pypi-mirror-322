import numpy as np

npa = np.array


def get_lineabc_use2pt(p1_in, p2_in):
    A = p1_in[1] - p2_in[1]
    B = p2_in[0] - p1_in[0]
    C = np.cross(p1_in, p2_in)
    return A, B, C


def catmullrom_use4pt(ti, p_1, p0, p1, p2, *, alpha=0.5):
    """
    http://graphics.cs.cmu.edu/nsp/course/15-462/Fall04/assts/catmullRom.pdf
    :param t:
    :param p_1:
    :param p0:
    :param p1:
    :param p2:
    :param alpha:
    :return:
    """
    t = np.repeat([ti], 4, axis=0)
    t[0] = 1
    mat1 = np.cumprod(t, axis=0)
    mat1 = mat1.T
    s = alpha
    mat2 = np.array(
        [[0, 1, 0, 0],
         [-s, 0, s, 0],
         [2 * s, s - 3, 3 - 2 * s, -s],
         [-s, 2 - s, s - 2, s]]
    )
    ps = npa([p_1, p0, p1, p2])
    cmat = np.matmul(mat1, mat2)
    # pt = cmat[0][0] * p_1 + cmat[0][1] * p0 + cmat[0][2] * p1 + cmat[0][3] * p2
    pt = cmat @ ps
    return pt


def get_p_symm_l(pt_in, p1_in, p2_in):
    """
    函数功能：得到pt关于p12直线的对称点
    :param pt_in:
    :param p1_in:
    :param p2_in:
    :return:
    """
    A, B, C = get_lineabc_use2pt(p1_in, p2_in)
    x = pt_in[0] - 2 * A * (A * pt_in[0] + B * pt_in[1] + C) / (A ** 2 + B ** 2)
    y = pt_in[1] - 2 * B * (A * pt_in[0] + B * pt_in[1] + C) / (A ** 2 + B ** 2)
    return x, y


def get_vec_v(p1_in, p2_in):
    """
    得到p1->p2向量的垂直单位向量，在逆时针方向
    :param p1_in:
    :param p2_in:
    :return:
    """
    tmph = (p2_in[0] - p1_in[0], p2_in[1] - p1_in[1])
    tmpv = [-tmph[1], tmph[0]]  # 这样是逆时针
    norm = (tmpv[0] ** 2 + tmpv[1] ** 2) ** 0.5
    tmpv = [tmpv[0] / norm, tmpv[1] / norm]
    return tmpv


def catmullrom_spline(pts_in, intervals_in):
    """
    see also: http://graphics.cs.cmu.edu/nsp/course/15-462/Fall04/assts/catmullRom.pdf
    :param pts_in:
    :param intervals_in:
    :return:
    """
    pts_out = []
    ptsc = npa(pts_in)
    if len(pts_in) <= 1:
        return pts_in
    elif len(pts_in) == 2:
        # 直线方式添加首尾点
        ptsc = np.vstack((2 * np.array(ptsc[0]) - np.array(ptsc[1]), ptsc))
        ptsc = np.vstack((2 * np.array(ptsc[-1]) - np.array(ptsc[-2]), ptsc))
    else:
        # 等腰梯形方式添加首尾点
        tmpmid = (np.array(ptsc[0]) + np.array(ptsc[1])) / 2
        tmpv = np.array(get_vec_v(ptsc[0], ptsc[1]))
        tmppt = get_p_symm_l(ptsc[2], tmpmid, tmpmid + tmpv)
        ptsc = np.vstack((tmppt, ptsc))
        tmpmid = (np.array(ptsc[-1]) + np.array(ptsc[-2])) / 2
        tmpv = np.array(get_vec_v(ptsc[-1], ptsc[-2]))
        tmppt = get_p_symm_l(ptsc[-3], tmpmid, tmpmid + tmpv)
        ptsc = np.vstack((ptsc, tmppt))
    ptsc = np.array(ptsc)
    ti = np.linspace(0, 1, intervals_in)
    for i in range(1, len(ptsc) - 2):
        p = catmullrom_use4pt(ti, ptsc[i - 1], ptsc[i], ptsc[i + 1], ptsc[i + 2])
        pts_out.append(p)
    res = np.vstack(pts_out)
    res = np.vstack((res, ptsc[-2]))
    return res
