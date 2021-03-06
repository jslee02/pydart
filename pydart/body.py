import pydart_api as papi
import numpy as np
from contact import Contact


class Body(object):
    def __init__(self, _skel, _id):
        self.skel = _skel
        self._id = _id
        self.name = papi.getSkeletonBodyName(self.wid, self.sid, self.id)

    @property
    def id(self):
        return self._id

    @property
    def wid(self):
        return self.skel.world.id

    @property
    def sid(self):
        return self.skel.id

    def num_contacts(self):
        return papi.getBodyNodeNumContacts(self.wid, self.sid, self.id)

    def contacts(self):
        n = self.num_contacts()
        contacts = papi.getBodyNodeContacts(self.wid, self.sid, self.id, 7 * n)
        return [Contact(contacts[7 * i: 7 * (i + 1)]) for i in range(n)]

    def mass(self):
        return papi.getBodyNodeMass(self.wid, self.sid, self.id)

    @property
    def m(self):
        return self.mass()

    def inertia(self):
        return papi.getBodyNodeInertia(self.wid, self.sid, self.id)

    @property
    def I(self):
        return self.inertia()

    def local_com(self):
        return papi.getBodyNodeLocalCOM(self.wid, self.sid, self.id)

    def world_com(self):
        return papi.getBodyNodeWorldCOM(self.wid, self.sid, self.id)

    def to_world(self, x):
        x_ = np.append(x, [1.0])
        return (self.T.dot(x_))[:3]

    @property
    def C(self):
        return self.world_com()

    def world_com_velocity(self):
        return papi.getBodyNodeWorldCOMVelocity(self.wid, self.sid, self.id)

    @property
    def Cdot(self):
        return self.world_com_velocity()

    def transformation(self):
        return papi.getBodyNodeTransformation(self.wid, self.sid, self.id)

    @property
    def T(self):
        return self.transformation()

    def world_linear_jacobian(self, offset=None):
        if offset is None:
            offset = np.zeros(3)
        J = np.zeros((3, self.skel.ndofs))
        papi.getBodyNodeWorldLinearJacobian(self.wid, self.sid,
                                            self.id, offset, J)
        return J

    @property
    def J(self):
        return self.world_linear_jacobian()

    def add_ext_force(self, f):
        papi.addBodyNodeExtForce(self.wid, self.sid, self.id, f)

    def add_ext_force_at(self, f, offset):
        papi.addBodyNodeExtForceAt(self.wid, self.sid, self.id, f, offset)

    def __repr__(self):
        return '<Body.%d.%s>' % (self.id, self.name)
