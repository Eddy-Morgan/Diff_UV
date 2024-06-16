from casadi import inv
from diffUV.base import Base
from diffUV.utils.symbols import *
from diffUV.utils import quaternion_ops as Tquat

class DynamicsQuat(Base):
    def __init__(self):
        super().__init__()
        self.J, R, T = Tquat.Jq_kin(uq)
        self.Jq_INV, _,_ = Tquat.inv_Jq_kin(uq)
        self.Jq_INV_T = self.Jq_INV.T
        self.Jq_dot, dRq ,dTq = Tquat.Jq_dot(uq, w_nb)
        # self.state_vector = vertcat(uq,..)

    def __repr__(self) -> str:
        """Quaternion representation of the Dynamics instance in ned frame"""
        return f'{super().__repr__()} --> (quat in ned frame)'
    
    def ned_quat_inertia_matrix(self):
        """Compute and return the UV inertia matrix with configuration adjustments in ned for quaternion"""
        M = self.body_inertia_matrix()
        M_ned_q = self.Jq_INV_T@M@self.Jq_INV
        return M_ned_q

    def ned_quat_coriolis_ned_centripetal_matrix(self):
        """Compute and return the Coriolis and centripetal matrix based on current vehicle state in body"""
        C = self.body_coriolis_centripetal_matrix()
        M = self.body_inertia_matrix()
        C_ned_q = self.Jq_INV_T@(C - M@self.Jq_INV@self.Jq_dot)@self.Jq_INV
        return C_ned_q
    
    def ned_quat_restoring_vector(self):
        g = self.body_restoring_vector()
        g_ned = self.Jq_INV_T@g
        return g_ned

    def ned_quat_damping(self):
        D_v = self.body_damping_matrix()
        D = self.Jq_INV_T@D_v@self.Jq_INV
        return D

    def forward_dynamics_ned_quat(self):
        M = self.ned_quat_inertia_matrix()
        C = self.ned_quat_coriolis_ned_centripetal_matrix()
        g = self.ned_quat_restoring_vector()
        D = self.ned_quat_damping()
        ned_acc_quat = M  #inv(M)@(self.Jq_INV_T@tau_b - C@nq - g - D@nq)
        return ned_acc_quat
    
    # def inverse_dynamics_ned_quat(self):
    #     resultant_torque = self.get_body_inertia_matrix()@ddn + self.coriolis_body_centripetal_matrix()@dn + self.gvect_body() + self.damping_body()@dn
    #     return resultant_torque