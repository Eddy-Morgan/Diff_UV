# Copyright 2024, Edward Morgan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from casadi import SX,  vertcat, DM, horzcat
import sympy as sp
from sympy.physics.mechanics import dynamicsymbols

# 6 DOF states vectors in body-fixed
u = SX.sym('u')
du = SX.sym('du')
v = SX.sym('v')
dv = SX.sym('dv')
w = SX.sym('w')
dw = SX.sym('dw')
v_nb = vertcat(u, v, w)  # body-fixed linear velocity
dv_nb = vertcat(du, dv, dw)

p = SX.sym('p')
dp = SX.sym('dp')
q = SX.sym('q')
dq = SX.sym('dq')
r = SX.sym('r')
dr = SX.sym('dr')
w_nb = vertcat(p, q, r)  # body-fixed angular velocity
dw_nb = vertcat(dp, dq, dr)

x_nb = vertcat(v_nb, w_nb)
dx_nb = vertcat(dv_nb, dw_nb)

vc = SX.sym('vc',6,1) #current velocity
################################################

# 6 DOF states vectors in NED
x = SX.sym('x')
dx = SX.sym('dx')
ddx = SX.sym('ddx')
y = SX.sym('y')
dy = SX.sym('dy')
ddy = SX.sym('ddy')
z = SX.sym('z')
dz = SX.sym('dz')
ddz = SX.sym('ddz')
p_n = vertcat(x, y, z)  # NED linear velocity
dp_n = vertcat(dx, dy, dz)
ddp_n = vertcat(ddx, ddy, ddz)


theta_sp, phi_sp = dynamicsymbols('theta phi')
dtheta_sp = sp.diff(theta_sp,'t')
dphi_sp =sp.diff(phi_sp,'t')

eul_sp = [theta_sp, dtheta_sp, phi_sp, dphi_sp]
# Create the sympy matrix T
T_sp = sp.Matrix([
    [1, sp.sin(phi_sp)*sp.tan(theta_sp), sp.cos(phi_sp)*sp.tan(theta_sp)],
    [0, sp.cos(phi_sp), -sp.sin(phi_sp)],
    [0, sp.sin(phi_sp)/sp.cos(theta_sp), sp.cos(phi_sp)/sp.cos(theta_sp)]
])


dT_sp = sp.diff(T_sp,'t',1)

thet = SX.sym('thet')
dthet = SX.sym('dthet')
ddthet = SX.sym('ddthet')
phi = SX.sym('phi')
dphi = SX.sym('dphi')
ddphi = SX.sym('ddphi')
psi = SX.sym('psi')
dpsi = SX.sym('dpsi')
ddpsi = SX.sym('ddpsi')

eul = vertcat(phi, thet, psi)  # NED euler angular velocity
deul = vertcat(dphi, dthet, dpsi)
ddeul = vertcat(ddphi, ddthet, ddpsi)

n = vertcat(p_n, eul)
dn  = vertcat(dp_n, deul)
ddn  = vertcat(ddp_n, ddeul)

eta,eps1,eps2,eps3 = SX.sym('eta'),SX.sym('eps1'),SX.sym('eps2'),SX.sym('eps3')
uq = vertcat(eta,eps1,eps2,eps3) #unit quaternion

# deta = -0.5*(eps1*p + eps2*q + eps3*r)
# deps1 = 0.5*(eta*p - eps3*q + eps2*r)
# deps2 = 0.5*(eps3*p + eta*q - eps1*r)
# deps3 = 0.5*(-eps2*p + eps1*q - eta*r)
# duq = vertcat(deta,deps1,deps2,deps3) # differential unit quaternion

nq = vertcat(p_n, uq)
# dnq = vertcat(dp_n, uq)
###################################################


W = SX.sym('W')  # weight
B = SX.sym('B')  # buoyancy

m = SX.sym('m')  # Mass

I_x = SX.sym('I_x')  # moment of inertia x entry
I_y = SX.sym('I_y')  # moment of inertia y entry
I_z = SX.sym('I_z')  # moment of inertia z entry
I_zx = SX.sym('I_zx')  # product of inertia zx entry
I_xz = SX.sym('I_xz')  # product of inertia zx entry
I_xy = SX.sym('I_xy')  # product of inertia yx entry
I_yx = SX.sym('I_yx')  # product of inertia yx entry
I_zy = SX.sym('I_zy')  # product of inertia zy entry
I_yz = SX.sym('I_yz')  # product of inertia zy entry

Ib_b = SX(3,3)
Ib_b[0, :] = horzcat(I_x, -I_xy, -I_xz)
Ib_b[1, :] = horzcat(-I_xy, I_y, -I_yz)
Ib_b[2, :] = horzcat(-I_xz, -I_yz, I_z)


x_g = SX.sym('x_g')  # Center of gravity, x-axis wrt to the CO
y_g = SX.sym('y_g')  # Center of gravity, y-axis wrt to the CO
z_g = SX.sym('z_g')  # Center of gravity, z-axis wrt to the CO

r_g = vertcat(x_g, y_g, z_g)

x_b = SX.sym('x_b')  # Center of buoyancy, x-axis
y_b = SX.sym('y_b')  # Center of buoyancy, y-axis
z_b = SX.sym('z_b')  # Center of buoyancy, z-axis

X_du = SX.sym('X_du') # Added mass in surge
X_dv = SX.sym('X_dv') # coupled Added mass in surge & sway
X_dw = SX.sym('X_dw') # coupled Added mass in surge & heave
X_dp = SX.sym('X_dp') # coupled Added mass in surge & roll
X_dq = SX.sym('X_dq') # coupled Added mass in surge & pitch
X_dr = SX.sym('X_dr') # coupled Added mass in surge & pitch

Y_du = SX.sym('Y_du') # Added mass in sway & surge
Y_dv = SX.sym('Y_dv') # Added mass in sway
Y_dw = SX.sym('Y_dw') # coupled Added mass in sway & heave
Y_dp = SX.sym('Y_dp') # coupled Added mass in sway & roll
Y_dq = SX.sym('Y_dq') # coupled Added mass in sway & pitch
Y_dr = SX.sym('Y_dr') # coupled Added mass in sway & yaw

Z_du = SX.sym('Z_du') # coupled Added mass in heave & surge
Z_dv = SX.sym('Z_dv') # coupled Added mass in heave & sway
Z_dw = SX.sym('Z_dw') # Added mass in heave
Z_dp = SX.sym('Z_dp') # coupled Added mass in heave & roll
Z_dq = SX.sym('Z_dq') # coupled Added mass in heave & pitch
Z_dr = SX.sym('Z_dr') # coupled Added mass in heave & yaw

K_du = SX.sym('K_du') # coupled Added mass in roll & surge
K_dv = SX.sym('K_dv') # coupled Added mass in roll & sway
K_dw = SX.sym('K_dw') # coupled Added mass in roll & heave
K_dp = SX.sym('K_dp') # Added mass in roll
K_dq = SX.sym('K_dq') # coupled Added mass in roll & pitch
K_dr = SX.sym('K_dr') # coupled Added mass in roll & yaw

M_du = SX.sym('M_du') # coupled Added mass in pitch & surge
M_dv = SX.sym('M_dv') # coupled Added mass in pitch & sway
M_dw = SX.sym('M_dw') # coupled Added mass in pitch & heave
M_dp = SX.sym('M_dp') # coupled Added mass in pitch & roll
M_dq = SX.sym('M_dq') # Added mass in pitch
M_dr = SX.sym('M_dr') # coupled Added mass in pitch & yaw

N_du = SX.sym('N_du') # coupled Added mass in yaw & surge
N_dv = SX.sym('N_dv') # coupled Added mass in yaw & sway
N_dw = SX.sym('N_dw') # coupled Added mass in yaw & heave
N_dp = SX.sym('N_dp') # coupled Added mass in yaw & roll
N_dq = SX.sym('N_dq') # coupled Added mass in yaw & pitch
N_dr = SX.sym('N_dr') # Added mass in yaw

_MA = SX(6, 6)
_MA[0, :] = horzcat(X_du, X_dv, X_dw, X_dp, X_dq, X_dr)
_MA[1, :] = horzcat(Y_du, Y_dv, Y_dw, Y_dp, Y_dq, Y_dr)
_MA[2, :] = horzcat(Z_du, Z_dv, Z_dw, Z_dp, Z_dq, Z_dr)
_MA[3, :] = horzcat(K_du, K_dv, K_dw, K_dp, K_dq, K_dr)
_MA[4, :] = horzcat(M_du, M_dv, M_dw, M_dp, M_dq, M_dr)
_MA[5, :] = horzcat(N_du, N_dv, N_dw, N_dp, N_dq, N_dr)
MA = -_MA

###################################################################

X_u = SX.sym('X_u') # linear Drag coefficient in surge
Y_v = SX.sym('Y_v') # linear Drag coefficient in sway
Z_w = SX.sym('Z_w') # linear Drag coefficient in heave
K_p = SX.sym('K_p') # linear Drag coefficient in roll
M_q = SX.sym('M_q') # linear Drag coefficient in pitch
N_r = SX.sym('N_r') # linear Drag coefficient in yaw

K_v = SX.sym('K_v') # coupled Drag coefficient in sway & roll
N_v = SX.sym('N_v') # coupled Drag coefficient in sway & yaw
M_w = SX.sym('M_w') # coupled Drag coefficient in pitch & heave
Y_p = SX.sym('Y_p') # coupled Drag coefficient in sway & roll
N_p = SX.sym('N_p') # coupled Drag coefficient in roll & yaw
Z_q = SX.sym('Z_q') # coupled Drag coefficient in heave & pitch
Y_r = SX.sym('Y_r') # coupled Drag coefficient in sway & yaw
K_r = SX.sym('K_r') # coupled Drag coefficient in roll & yaw


X_uu = SX.sym('X_uu') # quadratic Drag coefficient in surge
Y_vv = SX.sym('Y_vv') # quadratic Drag coefficient in sway
Z_ww = SX.sym('Z_ww') # quadratic Drag coefficient in heave
K_pp = SX.sym('K_pp') # quadratic Drag coefficient in roll
M_qq = SX.sym('M_qq') # quadratic Drag coefficient in pitch
N_rr = SX.sym('N_rr') # quadratic Drag coefficient in yaw

###################################################################
tau_b = SX.sym('tau_b',6,1) #body generalized forces and torque
thru_u = SX.sym('thruForces',8,1) #thruster inputs

K = SX.sym('k',8,8) #thrust coefficient matrix
Tc = SX.sym('T',6,8) #thruster configuration

###################################################################
# Starboard–port and fore/aft symmetrical underwater vehicles config
sb_fft_config = DM([[1, 0, 0, 0, 1, 0],
                        [0, 1, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 1, 0, 0],
                        [1, 0, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 1]
                        ])
