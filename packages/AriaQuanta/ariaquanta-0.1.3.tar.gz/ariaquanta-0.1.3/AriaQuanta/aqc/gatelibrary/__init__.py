
#------------------------------------------------------------------------------------
from .gatesingle import (
    GateSingleQubit,
    I,
    Ph,
    X,
    Y,
    Z,
    S,
    Xsqrt,
    H,
    P,
    T,
    RX,
    RY,
    RZ,
    Rot,
)

#------------------------------------------------------------------------------------
from .gatedouble import (
    GateDoubleQubit,
    SWAP,
    ISWAP,
    SWAPsqrt,
    ISWAPsqrt,
    SWAPalpha,
    RXX,
    RYY,
    RZZ,
    RXY,
    Barenco,
    Berkeley,
    Canonical,
    Givens,
    Magic,
)

#------------------------------------------------------------------------------------
from .gatetriple import (
    GateTripleQubit,
    CCX,
    RCCX,
    CSWAP,
)

#------------------------------------------------------------------------------------
from .gatecustom import (
    GateCustom,
    Custom,
)

#------------------------------------------------------------------------------------
from .gatecontrol import (
    GateControl,
    CX,
    CZ,
    CP,
    CS,
    CSX,
    CU,
)

#------------------------------------------------------------------------------------
from .gatecontroln import (
    CNZ
)