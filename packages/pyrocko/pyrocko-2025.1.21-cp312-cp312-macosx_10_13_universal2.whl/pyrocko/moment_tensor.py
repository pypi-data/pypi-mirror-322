# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

'''
This module provides various moment tensor related utility functions.

It can be used to convert between strike-dip-rake and moment tensor
representations and provides different options to produce random moment
tensors.

Moment tensors are represented by :py:class:`MomentTensor` instances. The
internal representation uses a north-east-down (NED) coordinate system, but it
can convert from/to the conventions used by the Global CMT catalog
(up-south-east, USE).

If not otherwise noted, scalar moment is interpreted as the Frobenius norm
based scalar moment (see :py:meth:`MomentTensor.scalar_moment`. The scalar
moment according to the "standard decomposition" can be found in the
output of :py:meth:`MomentTensor.standard_decomposition`.
'''

import math
import numpy as num

from .guts import Object, Float

guts_prefix = 'pf'

dynecm = 1e-7


def random_axis(rstate=None):
    '''
    Get randomly oriented unit vector.

    :param rstate: :py:class:`numpy.random.RandomState` object, can be used to
        create reproducible pseudo-random sequences
    '''
    rstate = rstate or num.random
    while True:
        axis = rstate.uniform(size=3) * 2.0 - 1.0
        uabs = math.sqrt(num.sum(axis**2))
        if 0.001 < uabs < 1.0:
            return axis / uabs


def rotation_from_angle_and_axis(angle, axis):
    '''
    Build rotation matrix based on axis and angle.

    :param angle: rotation angle [degrees]
    :param axis: orientation of rotation axis, either in spherical
        coordinates ``(theta, phi)`` [degrees], or as a unit vector
        ``(ux, uy, uz)``.
    '''

    if len(axis) == 2:
        theta, phi = axis
        ux = math.sin(d2r*theta)*math.cos(d2r*phi)
        uy = math.sin(d2r*theta)*math.sin(d2r*phi)
        uz = math.cos(d2r*theta)

    elif len(axis) == 3:
        axis = num.asarray(axis)
        uabs = math.sqrt(num.sum(axis**2))
        ux, uy, uz = axis / uabs
    else:
        assert False

    ct = math.cos(d2r*angle)
    st = math.sin(d2r*angle)
    return num.array([
        [ct + ux**2*(1.-ct), ux*uy*(1.-ct)-uz*st, ux*uz*(1.-ct)+uy*st],
        [uy*ux*(1.-ct)+uz*st, ct+uy**2*(1.-ct), uy*uz*(1.-ct)-ux*st],
        [uz*ux*(1.-ct)-uy*st, uz*uy*(1.-ct)+ux*st, ct+uz**2*(1.-ct)]
        ])


def random_rotation(x=None):
    '''
    Get random rotation matrix.

    A random rotation matrix, drawn from a uniform distribution in the space
    of rotations is returned, after Avro 1992 - "Fast random rotation
    matrices".

    :param x: three (uniform random) numbers in the range [0, 1[ used as input
        to the distribution transformation. If ``None``, random numbers are
        used. Can be used to create grids of random rotations with uniform
        density in rotation space.
    '''

    if x is not None:
        x1, x2, x3 = x
    else:
        x1, x2, x3 = num.random.random(3)

    phi = math.pi*2.0*x1

    zrot = num.array([
        [math.cos(phi), math.sin(phi), 0.],
        [-math.sin(phi), math.cos(phi), 0.],
        [0., 0., 1.]])

    lam = math.pi*2.0*x2

    v = num.array([[
        math.cos(lam)*math.sqrt(x3),
        math.sin(lam)*math.sqrt(x3),
        math.sqrt(1.-x3)]]).T

    house = num.identity(3) - 2.0 * num.dot(v, v.T)
    return -num.dot(house, zrot)


def rand(mi, ma):
    return float(num.random.uniform(mi, ma))


def randdip(mi, ma):
    mi_ = 0.5*(math.cos(mi * math.pi/180.)+1.)
    ma_ = 0.5*(math.cos(ma * math.pi/180.)+1.)
    return math.acos(rand(mi_, ma_)*2.-1.)*180./math.pi


def random_strike_dip_rake(
        strikemin=0., strikemax=360.,
        dipmin=0., dipmax=90.,
        rakemin=-180., rakemax=180.):

    '''
    Get random strike, dip, rake triplet.

    .. note::

        Might not produce a homogeneous distribution of mechanisms. Better use
        :py:meth:`MomentTensor.random_dc` which is based on
        :py:func:`random_rotation`.
    '''

    strike = rand(strikemin, strikemax)
    dip = randdip(dipmin, dipmax)
    rake = rand(rakemin, rakemax)

    return strike, dip, rake


def to6(m):
    '''
    Get non-redundant components from symmetric 3x3 matrix.

    :returns: 1D NumPy array with entries ordered like
        ``(a_xx, a_yy, a_zz, a_xy, a_xz, a_yz)``
    '''

    return num.array([m[0, 0], m[1, 1], m[2, 2], m[0, 1], m[0, 2], m[1, 2]])


def symmat6(a_xx, a_yy, a_zz, a_xy, a_xz, a_yz):
    '''
    Create symmetric 3x3 matrix from its 6 non-redundant values.
    '''

    return num.array([[a_xx, a_xy, a_xz],
                      [a_xy, a_yy, a_yz],
                      [a_xz, a_yz, a_zz]], dtype=float)


def values_to_matrix(values):
    '''
    Convert anything to moment tensor represented as a NumPy array.

    Transforms :py:class:`MomentTensor` objects, tuples, lists and NumPy arrays
    with 3x3 or 3, 4, 6, or 7 elements into NumPy 3x3 array objects.

    The ``values`` argument is interpreted depending on shape and type as
    follows:

    * ``(strike, dip, rake)``
    * ``(strike, dip, rake, magnitude)``
    * ``(mnn, mee, mdd, mne, mnd, med)``
    * ``(mnn, mee, mdd, mne, mnd, med, magnitude)``
    * ``((mnn, mne, mnd), (mne, mee, med), (mnd, med, mdd))``
    * :py:class:`MomentTensor`
    '''

    if isinstance(values, (tuple, list)):
        values = num.asarray(values, dtype=float)

    if isinstance(values, MomentTensor):
        return values.m()

    elif isinstance(values, num.ndarray):
        if values.shape == (3,):
            strike, dip, rake = values
            rotmat1 = euler_to_matrix(d2r*dip, d2r*strike, -d2r*rake)
            return num.dot(rotmat1.T, num.dot(MomentTensor._m_unrot, rotmat1))

        elif values.shape == (4,):
            strike, dip, rake, magnitude = values
            moment = magnitude_to_moment(magnitude)
            rotmat1 = euler_to_matrix(d2r*dip, d2r*strike, -d2r*rake)
            return moment * num.dot(
                rotmat1.T, num.dot(MomentTensor._m_unrot, rotmat1))

        elif values.shape == (6,):
            return symmat6(*values)

        elif values.shape == (7,):
            magnitude = values[6]
            moment = magnitude_to_moment(magnitude)
            mt = symmat6(*values[:6])
            mt *= moment / (num.linalg.norm(mt) / math.sqrt(2.0))
            return mt

        elif values.shape == (3, 3):
            return num.asarray(values, dtype=float)

    raise Exception('cannot convert object to 3x3 matrix')


def moment_to_magnitude(moment):
    '''
    Convert scalar moment to moment magnitude Mw.

    :param moment: scalar moment [Nm]
    :returns: moment magnitude Mw

    Moment magnitude is defined as

    .. math::

        M_\\mathrm{w} = {\\frac{2}{3}}\\log_{10}(M_0 \\cdot 10^7) - 10.7

    where :math:`M_0` is the scalar moment given in [Nm].

    .. note::

        Global CMT uses 10.7333333 instead of 10.7, based on [Kanamori 1977],
        10.7 is from [Hanks and Kanamori 1979].
    '''

    return num.log10(moment*1.0e7) / 1.5 - 10.7


def magnitude_to_moment(magnitude):
    '''
    Convert moment magnitude Mw to scalar moment.

    :param magnitude: moment magnitude
    :returns: scalar moment [Nm]

    See :py:func:`moment_to_magnitude`.
    '''

    return 10.0**(1.5*(magnitude+10.7))*1.0e-7


magnitude_1Nm = moment_to_magnitude(1.0)


def euler_to_matrix(alpha, beta, gamma):
    '''
    Given euler angle triplet, create rotation matrix

    Given coordinate system `(x,y,z)` and rotated system `(xs,ys,zs)`
    the line of nodes is the intersection between the `x,y` and the `xs,ys`
    planes.

    :param alpha: is the angle between the `z`-axis and the `zs`-axis [rad]
    :param beta:  is the angle between the `x`-axis and the line of nodes [rad]
    :param gamma: is the angle between the line of nodes and the `xs`-axis
        [rad]

    Usage for moment tensors::

        m_unrot = numpy.array([[0,0,-1],[0,0,0],[-1,0,0]])
        euler_to_matrix(dip,strike,-rake, rotmat)
        m = num.dot(rotmat.T, num.dot(m_unrot, rotmat))

    '''

    ca = math.cos(alpha)
    cb = math.cos(beta)
    cg = math.cos(gamma)
    sa = math.sin(alpha)
    sb = math.sin(beta)
    sg = math.sin(gamma)

    mat = num.array([[cb*cg-ca*sb*sg,  sb*cg+ca*cb*sg,  sa*sg],
                     [-cb*sg-ca*sb*cg, -sb*sg+ca*cb*cg, sa*cg],
                     [sa*sb,           -sa*cb,          ca]], dtype=float)
    return mat


def matrix_to_euler(rotmat):
    '''
    Get Eulerian angle triplet from rotation matrix.
    '''

    ex = cvec(1., 0., 0.)
    ez = cvec(0., 0., 1.)
    exs = num.dot(rotmat.T, ex)
    ezs = num.dot(rotmat.T, ez)
    enodes = num.cross(ez.T, ezs.T).T
    if num.linalg.norm(enodes) < 1e-10:
        enodes = exs
    enodess = num.dot(rotmat, enodes)
    cos_alpha = float(num.dot(ez.T, ezs)[0, 0])
    if cos_alpha > 1.:
        cos_alpha = 1.

    if cos_alpha < -1.:
        cos_alpha = -1.

    alpha = math.acos(cos_alpha)
    beta = num.mod(math.atan2(enodes[1, 0], enodes[0, 0]), math.pi*2.)
    gamma = num.mod(-math.atan2(enodess[1, 0], enodess[0, 0]), math.pi*2.)

    return unique_euler(alpha, beta, gamma)


def unique_euler(alpha, beta, gamma):
    '''
    Uniquify Eulerian angle triplet.

    Put Eulerian angle triplet into ranges compatible with
    ``(dip, strike, -rake)`` conventions in seismology::

        alpha (dip)   : [0, pi/2]
        beta (strike) : [0, 2*pi)
        gamma (-rake) : [-pi, pi)

    If ``alpha1`` is near to zero, ``beta`` is replaced by ``beta+gamma`` and
    ``gamma`` is set to zero, to prevent this additional ambiguity.

    If ``alpha`` is near to ``pi/2``, ``beta`` is put into the range
    ``[0,pi)``.
    '''

    pi = math.pi

    alpha = num.mod(alpha, 2.0*pi)

    if 0.5*pi < alpha and alpha <= pi:
        alpha = pi - alpha
        beta = beta + pi
        gamma = 2.0*pi - gamma
    elif pi < alpha and alpha <= 1.5*pi:
        alpha = alpha - pi
        gamma = pi - gamma
    elif 1.5*pi < alpha and alpha <= 2.0*pi:
        alpha = 2.0*pi - alpha
        beta = beta + pi
        gamma = pi + gamma

    alpha = num.mod(alpha, 2.0*pi)
    beta = num.mod(beta,  2.0*pi)
    gamma = num.mod(gamma+pi, 2.0*pi)-pi

    # If dip is exactly 90 degrees, one is still
    # free to choose between looking at the plane from either side.
    # Choose to look at such that beta is in the range [0,180)

    # This should prevent some problems, when dip is close to 90 degrees:
    if abs(alpha - 0.5*pi) < 1e-10:
        alpha = 0.5*pi

    if abs(beta - pi) < 1e-10:
        beta = pi

    if abs(beta - 2.*pi) < 1e-10:
        beta = 0.

    if abs(beta) < 1e-10:
        beta = 0.

    if alpha == 0.5*pi and beta >= pi:
        gamma = - gamma
        beta = num.mod(beta-pi,  2.0*pi)
        gamma = num.mod(gamma+pi, 2.0*pi)-pi
        assert 0. <= beta < pi
        assert -pi <= gamma < pi

    if alpha < 1e-7:
        beta = num.mod(beta + gamma, 2.0*pi)
        gamma = 0.

    return (alpha, beta, gamma)


def cvec(x, y, z):
    return num.array([[x, y, z]], dtype=float).T


def rvec(x, y, z):
    return num.array([[x, y, z]], dtype=float)


def eigh_check(a):
    evals, evecs = num.linalg.eigh(a)
    assert evals[0] <= evals[1] <= evals[2]
    return evals, evecs


r2d = 180. / math.pi
d2r = 1. / r2d


def random_mt(x=None, scalar_moment=1.0, magnitude=None):

    if magnitude is not None:
        scalar_moment = magnitude_to_moment(magnitude)

    if x is None:
        x = num.random.random(6)

    evals = x[:3] * 2. - 1.0
    evals /= num.sqrt(num.sum(evals**2)) / math.sqrt(2.0)
    rotmat = random_rotation(x[3:])
    return scalar_moment * num.dot(
        rotmat, num.dot(num.array(num.diag(evals)), rotmat.T))


def random_m6(*args, **kwargs):
    return to6(random_mt(*args, **kwargs))


def random_dc(x=None, scalar_moment=1.0, magnitude=None):
    if magnitude is not None:
        scalar_moment = magnitude_to_moment(magnitude)

    rotmat = random_rotation(x)
    return scalar_moment * num.dot(
        rotmat, num.dot(MomentTensor._m_unrot, rotmat.T))


def sm(m):
    return '/ %5.2F %5.2F %5.2F \\\n' % (m[0, 0], m[0, 1], m[0, 2]) + \
        '| %5.2F %5.2F %5.2F |\n' % (m[1, 0], m[1, 1], m[1, 2]) + \
        '\\ %5.2F %5.2F %5.2F /\n' % (m[2, 0], m[2, 1], m[2, 2])


def as_mt(mt):
    '''
    Convenience function to convert various objects to moment tensor object.

    Like :py:meth:`MomentTensor.from_values`, but does not create a new
    :py:class:`MomentTensor` object when ``mt`` already is one.
    '''

    if isinstance(mt, MomentTensor):
        return mt
    else:
        return MomentTensor.from_values(mt)


def pt_axes_to_strike_dip_rake(p_axis, t_axis):
    n_axis = num.cross(p_axis, t_axis)
    m_evecs = num.vstack([p_axis, n_axis, t_axis]).T
    if num.linalg.det(m_evecs) < 0.:
        m_evecs *= -1.
    rotmat = num.dot(m_evecs, MomentTensor._u_evecs.T).T
    if num.linalg.det(rotmat) < 0.:
        rotmat *= -1.
    alpha, beta, gamma = [r2d*x for x in matrix_to_euler(rotmat)]
    return (beta, alpha, -gamma)


def ned_to_rta(ned):
    '''
    Convert north-east-down coordinate vectors to radial-takeoff-azimuth.

    Output coordinate system has coordinates radial, takeoff angle [deg]
    (downward is zero), and azimuth [deg] (northward is zero).

    :param ned:
        Coordinate vector or array of coordinate vectors (north, east, down).
    :type ned:
        :py:class:`numpy.ndarray` of shape ``(N, 3)`` or ``(3,)``

    :returns:
        Coordinate vector or array of coordinate vectors (radial, takeoff,
        azimuth)
    :rtype:
        :py:class:`numpy.ndarray` of shape ``(N, 3)`` or ``(3,)``
    '''
    if ned.ndim == 1:
        return ned_to_rta(ned[num.newaxis, :])[0]

    rta = num.empty_like(ned)
    rta[:, 0] = num.sqrt(num.sum(ned**2, axis=1))
    rta[:, 1] = num.arccos(ned[:, 2]) * r2d
    rta[:, 2] = num.arctan2(ned[:, 1], ned[:, 0]) * r2d
    return rta


class MomentTensor(Object):

    '''
    Moment tensor object

    :param m: NumPy array in north-east-down convention
    :param m_up_south_east: NumPy array in up-south-east convention
    :param m_east_north_up: NumPy array in east-north-up convention
    :param strike,dip,rake: fault plane angles in [degrees]
    :param p_axis,t_axis: initialize double-couple from p and t axes
    :param scalar_moment: scalar moment in [Nm]
    :param magnitude: moment magnitude Mw

    Global CMT catalog moment tensors use the up-south-east (USE) coordinate
    system convention with :math:`r` (up), :math:`\\theta` (south), and
    :math:`\\phi` (east).

    .. math::
        :nowrap:

        \\begin{align*}
            M_{rr} &= M_{dd}, & M_{  r\\theta} &= M_{nd},\\\\
            M_{\\theta\\theta} &= M_{ nn}, & M_{r\\phi} &= -M_{ed},\\\\
            M_{\\phi\\phi} &=  M_{ee}, & M_{\\theta\\phi} &= -M_{ne}
        \\end{align*}

    '''

    mnn__ = Float.T(default=0.0)
    mee__ = Float.T(default=0.0)
    mdd__ = Float.T(default=0.0)
    mne__ = Float.T(default=0.0)
    mnd__ = Float.T(default=-1.0)
    med__ = Float.T(default=0.0)
    strike1__ = Float.T(default=None, optional=True)  # read-only
    dip1__ = Float.T(default=None, optional=True)  # read-only
    rake1__ = Float.T(default=None, optional=True)  # read-only
    strike2__ = Float.T(default=None, optional=True)  # read-only
    dip2__ = Float.T(default=None, optional=True)  # read-only
    rake2__ = Float.T(default=None, optional=True)  # read-only
    moment__ = Float.T(default=None, optional=True)  # read-only
    magnitude__ = Float.T(default=None, optional=True)  # read-only

    _flip_dc = num.array(
        [[0., 0., -1.], [0., -1., 0.], [-1., 0., 0.]], dtype=float)
    _to_up_south_east = num.array(
        [[0., 0., -1.], [-1., 0., 0.], [0., 1., 0.]], dtype=float).T
    _to_east_north_up = num.array(
        [[0., 1., 0.], [1., 0., 0.], [0., 0., -1.]], dtype=float)
    _m_unrot = num.array(
        [[0., 0., -1.], [0., 0., 0.], [-1., 0., 0.]], dtype=float)

    _u_evals, _u_evecs = eigh_check(_m_unrot)

    @classmethod
    def random_dc(cls, x=None, scalar_moment=1.0, magnitude=None):
        '''
        Create random oriented double-couple moment tensor

        The rotations used are uniformly distributed in the space of rotations.
        '''
        return MomentTensor(
            m=random_dc(x=x, scalar_moment=scalar_moment, magnitude=magnitude))

    @classmethod
    def random_mt(cls, x=None, scalar_moment=1.0, magnitude=None):
        '''
        Create random moment tensor

        Moment tensors produced by this function appear uniformly distributed
        when shown in a Hudson's diagram. The rotations used are uniformly
        distributed in the space of rotations.
        '''
        return MomentTensor(
            m=random_mt(x=x, scalar_moment=scalar_moment, magnitude=magnitude))

    @classmethod
    def from_values(cls, values):
        '''
        Alternative constructor for moment tensor objects

        This constructor takes a :py:class:`MomentTensor` object, a tuple, list
        or NumPy array with 3x3 or 3, 4, 6, or 7 elements to build a Moment
        tensor object.

        The ``values`` argument is interpreted depending on shape and type as
        follows:

        * ``(strike, dip, rake)``
        * ``(strike, dip, rake, magnitude)``
        * ``(mnn, mee, mdd, mne, mnd, med)``
        * ``(mnn, mee, mdd, mne, mnd, med, magnitude)``
        * ``((mnn, mne, mnd), (mne, mee, med), (mnd, med, mdd))``
        * :py:class:`MomentTensor` object
        '''

        m = values_to_matrix(values)
        return MomentTensor(m=m)

    def __init__(
            self, m=None, m_up_south_east=None, m_east_north_up=None,
            strike=0., dip=0., rake=0., scalar_moment=1.,
            mnn=None, mee=None, mdd=None, mne=None, mnd=None, med=None,
            strike1=None, dip1=None, rake1=None,
            strike2=None, dip2=None, rake2=None,
            p_axis=None, t_axis=None,
            magnitude=None, moment=None):

        Object.__init__(self, init_props=False)

        if any(mxx is not None for mxx in (mnn, mee, mdd, mne, mnd, med)):
            m = symmat6(mnn, mee, mdd, mne, mnd, med)

        if p_axis is not None and t_axis is not None:
            strike, dip, rake = pt_axes_to_strike_dip_rake(p_axis, t_axis)

        strike = d2r*strike
        dip = d2r*dip
        rake = d2r*rake

        if isinstance(m, num.matrix):
            m = m.A

        if isinstance(m_up_south_east, num.matrix):
            m_up_south_east = m_up_south_east.A

        if isinstance(m_east_north_up, num.matrix):
            m_east_north_up = m_east_north_up.A

        if m_up_south_east is not None:
            m = num.dot(
                self._to_up_south_east,
                num.dot(m_up_south_east, self._to_up_south_east.T))

        if m_east_north_up is not None:
            m = num.dot(
                self._to_east_north_up,
                num.dot(m_east_north_up, self._to_east_north_up.T))

        if m is None:
            if any(x is not None for x in (
                    strike1, dip1, rake1, strike2, dip2, rake2)):
                raise Exception(
                    'strike1, dip1, rake1, strike2, dip2, rake2 are read-only '
                    'properties')

            if moment is not None:
                scalar_moment = moment

            if magnitude is not None:
                scalar_moment = magnitude_to_moment(magnitude)

            rotmat1 = euler_to_matrix(dip, strike, -rake)
            m = scalar_moment * num.dot(
                rotmat1.T,
                num.dot(MomentTensor._m_unrot, rotmat1))

        self._m = m
        self._update()

    def _update(self):
        m_evals, m_evecs = eigh_check(self._m)
        if num.linalg.det(m_evecs) < 0.:
            m_evecs *= -1.

        rotmat1 = num.dot(m_evecs, MomentTensor._u_evecs.T).T
        if num.linalg.det(rotmat1) < 0.:
            rotmat1 *= -1.

        self._m_eigenvals = m_evals
        self._m_eigenvecs = m_evecs

        self._rotmats = sorted(
            [rotmat1, num.dot(MomentTensor._flip_dc, rotmat1)],
            key=lambda m: num.abs(m.flat).tolist())

    @property
    def mnn(self):
        return float(self._m[0, 0])

    @mnn.setter
    def mnn(self, value):
        self._m[0, 0] = value
        self._update()

    @property
    def mee(self):
        return float(self._m[1, 1])

    @mee.setter
    def mee(self, value):
        self._m[1, 1] = value
        self._update()

    @property
    def mdd(self):
        return float(self._m[2, 2])

    @mdd.setter
    def mdd(self, value):
        self._m[2, 2] = value
        self._update()

    @property
    def mne(self):
        return float(self._m[0, 1])

    @mne.setter
    def mne(self, value):
        self._m[0, 1] = value
        self._m[1, 0] = value
        self._update()

    @property
    def mnd(self):
        return float(self._m[0, 2])

    @mnd.setter
    def mnd(self, value):
        self._m[0, 2] = value
        self._m[2, 0] = value
        self._update()

    @property
    def med(self):
        return float(self._m[1, 2])

    @med.setter
    def med(self, value):
        self._m[1, 2] = value
        self._m[2, 1] = value
        self._update()

    @property
    def strike1(self):
        return float(self.both_strike_dip_rake()[0][0])

    @property
    def dip1(self):
        return float(self.both_strike_dip_rake()[0][1])

    @property
    def rake1(self):
        return float(self.both_strike_dip_rake()[0][2])

    @property
    def strike2(self):
        return float(self.both_strike_dip_rake()[1][0])

    @property
    def dip2(self):
        return float(self.both_strike_dip_rake()[1][1])

    @property
    def rake2(self):
        return float(self.both_strike_dip_rake()[1][2])

    def both_strike_dip_rake(self):
        '''
        Get both possible (strike,dip,rake) triplets.
        '''
        results = []
        for rotmat in self._rotmats:
            alpha, beta, gamma = [r2d*x for x in matrix_to_euler(rotmat)]
            results.append((beta, alpha, -gamma))

        return results

    def p_axis(self):
        '''
        Get direction of p axis.

        Use :py:func:`ned_to_rta` to get takeoff angle and azimuth of the
        returned vectors.

        :returns:
            Direction of P (pressure) axis as a (north, east, down) vector.
        :rtype:
            :py:class:`numpy.ndarray` of shape ``(3,)``
        '''
        return (self._m_eigenvecs.T)[0]

    def t_axis(self):
        '''
        Get direction of t axis.

        Use :py:func:`ned_to_rta` to get takeoff angle and azimuth of the
        returned vectors.

        :returns:
            Direction of T (tension) axis as a (north, east, down) vector.
        :rtype:
            :py:class:`numpy.ndarray` of shape ``(3,)``
        '''
        return (self._m_eigenvecs.T)[2]

    def null_axis(self):
        '''
        Get direction of the null axis.

        Use :py:func:`ned_to_rta` to get takeoff angle and azimuth of the
        returned vectors.

        :returns:
            Direction of null (B) axis as a (north, east, down) vector.
        :rtype:
            :py:class:`numpy.ndarray` of shape ``(3,)``
        '''
        return self._m_eigenvecs.T[1]

    def eigenvals(self):
        '''
        Get the eigenvalues of the moment tensor in ascending order.

        :returns: ``(ep, en, et)``
        '''

        return self._m_eigenvals

    def eigensystem(self):
        '''
        Get the eigenvalues and eigenvectors of the moment tensor.

        :returns: ``(ep, en, et, vp, vn, vt)``
        '''

        vp = self.p_axis().flatten()
        vn = self.null_axis().flatten()
        vt = self.t_axis().flatten()
        ep, en, et = self._m_eigenvals
        return ep, en, et, vp, vn, vt

    def both_slip_vectors(self):
        '''
        Get both possible slip directions.
        '''
        return [
            num.dot(rotmat.T, cvec(1., 0., 0.)) for rotmat in self._rotmats]

    def m(self):
        '''
        Get plain moment tensor as 3x3 matrix.
        '''
        return self._m.copy()

    def m6(self):
        '''
        Get the moment tensor as a six-element array.

        :returns: ``(mnn, mee, mdd, mne, mnd, med)``
        '''
        return to6(self._m)

    def m_up_south_east(self):
        '''
        Get moment tensor in up-south-east convention as 3x3 matrix.

        .. math::
            :nowrap:

            \\begin{align*}
                M_{rr} &= M_{dd}, & M_{  r\\theta} &= M_{nd},\\\\
                M_{\\theta\\theta} &= M_{ nn}, & M_{r\\phi} &= -M_{ed},\\\\
                M_{\\phi\\phi} &=  M_{ee}, & M_{\\theta\\phi} &= -M_{ne}
            \\end{align*}
        '''

        return num.dot(
            self._to_up_south_east.T,
            num.dot(self._m, self._to_up_south_east))

    def m_east_north_up(self):
        '''
        Get moment tensor in east-north-up convention as 3x3 matrix.
        '''

        return num.dot(
            self._to_east_north_up.T, num.dot(self._m, self._to_east_north_up))

    def m6_up_south_east(self):
        '''
        Get moment tensor in up-south-east convention as a six-element array.

        :returns: ``(muu, mss, mee, mus, mue, mse)``
        '''
        return to6(self.m_up_south_east())

    def m6_east_north_up(self):
        '''
        Get moment tensor in east-north-up convention as a six-element array.

        :returns: ``(mee, mnn, muu, men, meu, mnu)``
        '''
        return to6(self.m_east_north_up())

    def m_plain_double_couple(self):
        '''
        Get plain double couple with same scalar moment as moment tensor.
        '''
        rotmat1 = self._rotmats[0]
        m = self.scalar_moment() * num.dot(
            rotmat1.T, num.dot(MomentTensor._m_unrot, rotmat1))
        return m

    def moment_magnitude(self):
        '''
        Get moment magnitude of moment tensor.
        '''
        return moment_to_magnitude(self.scalar_moment())

    def scalar_moment(self):
        '''
        Get the scalar moment of the moment tensor (Frobenius norm based)

        .. math::

            M_0 = \\frac{1}{\\sqrt{2}}\\sqrt{\\sum_{i,j} |M_{ij}|^2}

        The scalar moment is calculated based on the Euclidean (Frobenius) norm
        (Silver and Jordan, 1982). The scalar moment returned by this function
        differs from the standard decomposition based definition of the scalar
        moment for non-double-couple moment tensors.
        '''
        return num.linalg.norm(self._m_eigenvals) / math.sqrt(2.)

    @property
    def moment(self):
        return float(self.scalar_moment())

    @moment.setter
    def moment(self, value):
        self._m *= value / self.moment
        self._update()

    @property
    def magnitude(self):
        return float(self.moment_magnitude())

    @magnitude.setter
    def magnitude(self, value):
        self._m *= magnitude_to_moment(value) / self.moment
        self._update()

    def __str__(self):
        mexp = pow(10, math.ceil(num.log10(num.max(num.abs(self._m)))))
        m = self._m / mexp
        s = '''Scalar Moment [Nm]: M0 = %g (Mw = %3.1f)
Moment Tensor [Nm]: Mnn = %6.3f,  Mee = %6.3f, Mdd = %6.3f,
                    Mne = %6.3f,  Mnd = %6.3f, Med = %6.3f    [ x %g ]
''' % (
            self.scalar_moment(),
            self.moment_magnitude(),
            m[0, 0], m[1, 1], m[2, 2], m[0, 1], m[0, 2], m[1, 2],
            mexp)

        s += self.str_fault_planes()
        return s

    def str_fault_planes(self):
        s = ''
        for i, sdr in enumerate(self.both_strike_dip_rake()):
            s += 'Fault plane %i [deg]: ' \
                 'strike = %3.0f, dip = %3.0f, slip-rake = %4.0f\n' \
                 % (i+1, sdr[0], sdr[1], sdr[2])

        return s

    def deviatoric(self):
        '''
        Get deviatoric part of moment tensor.

        Returns a new moment tensor object with zero trace.
        '''

        m = self.m()

        trace_m = num.trace(m)
        m_iso = num.diag([trace_m / 3., trace_m / 3., trace_m / 3.])
        m_devi = m - m_iso
        mt = MomentTensor(m=m_devi)
        return mt

    def standard_decomposition(self):
        '''
        Decompose moment tensor into isotropic, DC and CLVD components.

        Standard decomposition according to e.g. Jost and Herrmann 1989 is
        returned as::

            [
                (moment_iso, ratio_iso, m_iso),
                (moment_dc, ratio_dc, m_dc),
                (moment_clvd, ratio_clvd, m_clvd),
                (moment_devi, ratio_devi, m_devi),
                (moment, 1.0, m)
            ]
        '''

        epsilon = 1e-6

        m = self.m()

        trace_m = num.trace(m)
        m_iso = num.diag([trace_m / 3., trace_m / 3., trace_m / 3.])
        moment_iso = abs(trace_m / 3.)

        m_devi = m - m_iso

        evals, evecs = eigh_check(m_devi)

        moment_devi = num.max(num.abs(evals))
        moment = moment_iso + moment_devi

        iorder = num.argsort(num.abs(evals))
        evals_sorted = evals[iorder]
        evecs_sorted = (evecs.T[iorder]).T

        if moment_devi < epsilon * moment_iso:
            signed_moment_dc = 0.
        else:
            assert -epsilon <= -evals_sorted[0] / evals_sorted[2] <= 0.5
            signed_moment_dc = evals_sorted[2] * (1.0 + 2.0 * (
                min(0.0, evals_sorted[0] / evals_sorted[2])))

        moment_dc = abs(signed_moment_dc)
        m_dc_es = num.dot(signed_moment_dc, num.diag([0., -1.0, 1.0]))
        m_dc = num.dot(evecs_sorted, num.dot(m_dc_es, evecs_sorted.T))

        m_clvd = m_devi - m_dc

        moment_clvd = moment_devi - moment_dc

        ratio_dc = moment_dc / moment
        ratio_clvd = moment_clvd / moment
        ratio_iso = moment_iso / moment
        ratio_devi = moment_devi / moment

        return [
            (moment_iso, ratio_iso, m_iso),
            (moment_dc, ratio_dc, m_dc),
            (moment_clvd, ratio_clvd, m_clvd),
            (moment_devi, ratio_devi, m_devi),
            (moment, 1.0, m)]

    def rotated(self, rot):
        '''
        Get rotated moment tensor.

        :param rot: ratation matrix, coordinate system is NED
        :returns: new :py:class:`MomentTensor` object
        '''

        rotmat = num.array(rot)
        return MomentTensor(m=num.dot(rotmat, num.dot(self.m(), rotmat.T)))

    def random_rotated(self, angle_std=None, angle=None, rstate=None):
        '''
        Get distorted MT by rotation around random axis and angle.

        :param angle_std: angles are drawn from a normal distribution with
            zero mean and given standard deviation [degrees]
        :param angle: set angle [degrees], only axis will be random
        :param rstate: :py:class:`numpy.random.RandomState` object, can be
            used to create reproducible pseudo-random sequences
        :returns: new :py:class:`MomentTensor` object
        '''

        assert (angle_std is None) != (angle is None), \
            'either angle or angle_std must be given'

        if angle_std is not None:
            rstate = rstate or num.random
            angle = rstate.normal(scale=angle_std)

        axis = random_axis(rstate=rstate)
        rot = rotation_from_angle_and_axis(angle, axis)
        return self.rotated(rot)


def other_plane(strike, dip, rake):
    '''
    Get the respectively other plane in the double-couple ambiguity.
    '''

    mt = MomentTensor(strike=strike, dip=dip, rake=rake)
    both_sdr = mt.both_strike_dip_rake()
    w = [sum([abs(x-y) for x, y in zip(both_sdr[i], (strike, dip, rake))])
         for i in (0, 1)]

    if w[0] < w[1]:
        return both_sdr[1]
    else:
        return both_sdr[0]


def dsdr(sdr1, sdr2):
    s1, d1, r1 = sdr1
    s2, d2, r2 = sdr2

    s1 = s1 % 360.
    s2 = s2 % 360.
    r1 = r1 % 360.
    r2 = r2 % 360.

    ds = abs(s1 - s2)
    ds = ds if ds <= 180. else 360. - ds

    dr = abs(r1 - r2)
    dr = dr if dr <= 180. else 360. - dr

    dd = abs(d1 - d2)

    return math.sqrt(ds**2 + dr**2 + dd**2)


def order_like(sdrs, sdrs_ref):
    '''
    Order strike-dip-rake pair post closely to a given reference pair.

    :param sdrs: tuple, ``((strike1, dip1, rake1), (strike2, dip2, rake2))``
    :param sdrs_ref: as above but with reference pair
    '''

    d1 = min(dsdr(sdrs[0], sdrs_ref[0]), dsdr(sdrs[1], sdrs_ref[1]))
    d2 = min(dsdr(sdrs[0], sdrs_ref[1]), dsdr(sdrs[1], sdrs_ref[0]))
    if d1 < d2:
        return sdrs
    else:
        return sdrs[::-1]


def _tpb2q(t, p, b):
    eps = 0.001
    tqw = 1. + t[0] + p[1] + b[2]
    tqx = 1. + t[0] - p[1] - b[2]
    tqy = 1. - t[0] + p[1] - b[2]
    tqz = 1. - t[0] - p[1] + b[2]

    q = num.zeros(4)
    if tqw > eps:
        q[0] = 0.5 * math.sqrt(tqw)
        q[1:] = p[2] - b[1], b[0] - t[2], t[1] - p[0]
    elif tqx > eps:
        q[0] = 0.5 * math.sqrt(tqx)
        q[1:] = p[2] - b[1], p[0] + t[1], b[0] + t[2]
    elif tqy > eps:
        q[0] = 0.5 * math.sqrt(tqy)
        q[1:] = b[0] - t[2], p[0] + t[1], b[1] + p[2]
    elif tqz > eps:
        q[0] = 0.5 * math.sqrt(tqz)
        q[1:] = t[1] - p[0], b[0] + t[2], b[1] + p[2]
    else:
        raise Exception('should not reach this line, check theory!')
        # q[0] = max(0.5 * math.sqrt(tqx), eps)
        # q[1:] = p[2] - b[1], p[0] + t[1], b[0] + t[2]

    q[1:] /= 4.0 * q[0]

    q /= math.sqrt(num.sum(q**2))

    return q


_pbt2tpb = num.array(((0., 0., 1.), (1., 0., 0.), (0., 1., 0.)))


def kagan_angle(mt1, mt2):
    '''
    Given two moment tensors, return the Kagan angle in degrees.

    After Kagan (1991) and Tape & Tape (2012).
    '''

    ai = num.dot(_pbt2tpb, mt1._m_eigenvecs.T)
    aj = num.dot(_pbt2tpb, mt2._m_eigenvecs.T)

    u = num.dot(ai, aj.T)

    tk, pk, bk = u

    qk = _tpb2q(tk, pk, bk)

    return 2. * r2d * math.acos(num.max(num.abs(qk)))


def rand_to_gutenberg_richter(rand, b_value, magnitude_min):
    '''
    Draw magnitude from Gutenberg Richter distribution.
    '''
    return magnitude_min + num.log10(1.-rand) / -b_value


def magnitude_to_duration_gcmt(magnitudes):
    '''
    Scaling relation used by Global CMT catalog for most of its events.
    '''

    mom = magnitude_to_moment(magnitudes)
    return (mom / 1.1e16)**(1./3.)


if __name__ == '__main__':

    import sys
    v = list(map(float, sys.argv[1:]))
    mt = MomentTensor.from_values(v)
    print(mt)
