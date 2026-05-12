import pytest
from pydantic import ValidationError

from pals import (
    ApertureParameters,
    BeamBeamParameters,
    BendParameters,
    BodyShiftParameters,
    ElectricMultipoleParameters,
    FloorShiftParameters,
    ForkParameters,
    MagneticMultipoleParameters,
    MetaParameters,
    PatchParameters,
    ReferenceChangeParameters,
    ReferenceParameters,
    RFParameters,
    SolenoidParameters,
    # TrackingParameters,  # not yet tested
)


def test_ParameterClasses():
    """Test parameter classes"""
    # Test ApertureParameters
    aperture = ApertureParameters(x_limits=[-0.1, 0.1], y_limits=[-0.05, 0.05])
    assert aperture.x_limits == [-0.1, 0.1]

    with pytest.raises(ValidationError):
        _ = ApertureParameters(
            x_limits=[-0.1, 0.1], y_limits=[-0.05, 0.05, 0.1], shape="wrong"
        )

    # Test BodyShiftParameters
    body_shift = BodyShiftParameters(x_offset=0.01, y_rot=0.02)
    assert body_shift.x_offset == 0.01

    # Test MetaParameters
    meta = MetaParameters(alias="test", description="test element")
    assert meta.alias == "test"

    # Test ElectricMultipoleParameters
    emp = ElectricMultipoleParameters(tilt1=1.2, En1=1.0, Es1=0.5)
    assert emp.tilt1 == 1.2
    assert emp.En1 == 1.0
    assert emp.Es1 == 0.5

    emp2 = ElectricMultipoleParameters(En1L=1.0, Es1L=0.5)
    assert emp2.En1L == 1.0
    assert emp2.Es1L == 0.5

    #  catch typos
    with pytest.raises(ValidationError):
        _ = ElectricMultipoleParameters(Em1=1.0, Es1=0.5)
    with pytest.raises(ValidationError):
        _ = ElectricMultipoleParameters(En1=1.0, Ev1=0.5)
    with pytest.raises(ValidationError):
        _ = ElectricMultipoleParameters(En01=1.0, Es01=0.5)
    with pytest.raises(ValidationError):
        _ = ElectricMultipoleParameters(En1v=1.0, Es1l=0.5)
    with pytest.raises(ValidationError):
        _ = ElectricMultipoleParameters(tilt1L=1.2)

    # Test MagneticMultipoleParameters
    mmp = MagneticMultipoleParameters(tilt1=1.2, Bn1=1.0, Bs1=0.5)
    assert mmp.tilt1 == 1.2
    assert mmp.Bn1 == 1.0
    assert mmp.Bs1 == 0.5

    mmp2 = MagneticMultipoleParameters(Kn0=1.0, Ks1=0.5)
    assert mmp2.Kn0 == 1.0
    assert mmp2.Ks1 == 0.5

    mmp3 = MagneticMultipoleParameters(Bn1L=1.0, Bs1L=0.5)
    assert mmp3.Bn1L == 1.0
    assert mmp3.Bs1L == 0.5

    #  catch typos
    with pytest.raises(ValidationError):
        _ = MagneticMultipoleParameters(Bm1=1.0, Bs1=0.5)
    with pytest.raises(ValidationError):
        _ = MagneticMultipoleParameters(Bn1=1.0, Bv1=0.5)
    with pytest.raises(ValidationError):
        _ = MagneticMultipoleParameters(Bn01=1.0, Bs01=0.5)
    with pytest.raises(ValidationError):
        _ = MagneticMultipoleParameters(Bn1v=1.0, Bs1l=0.5)
    with pytest.raises(ValidationError):
        _ = MagneticMultipoleParameters(tilt1L=1.2)

    # Test SolenoidParameters
    sol = SolenoidParameters(Ksol=0.1, Bsol=0.2)
    assert sol.Ksol == 0.1

    # Test RFParameters
    rf = RFParameters(frequency=1e9, voltage=1e6)
    assert rf.frequency == 1e9

    with pytest.raises(ValidationError):
        _ = RFParameters(frequency=1e9, voltage=1e6, n_cell=0)
    with pytest.raises(ValidationError):
        _ = RFParameters(frequency=1e9, voltage=1e6, n_cell=-1)

    # Test BendParameters
    bend = BendParameters(rho_ref=1.0, bend_field_ref=2.0)
    assert bend.rho_ref == 1.0

    # Test PatchParameters
    patch = PatchParameters(x_offset=0.1, flexible=True)
    assert patch.x_offset == 0.1

    # Test FloorShiftParameters
    floor = FloorShiftParameters(x_offset=0.5, z_offset=1.0)
    assert floor.x_offset == 0.5

    # Test ForkParameters
    fork = ForkParameters(to_line="line1", direction="FORWARDS")
    assert fork.to_line == "line1"

    # Test ReferenceParameters
    ref = ReferenceParameters(species_ref="electron", pc_ref=1e6)
    assert ref.species_ref == "electron"

    # TODO: Test TrackingParameters
    # tracking = TrackingParameters(...)
    # assert tracking.i..

    # TODO: Test FloorParameters

    # Test ReferenceChangeParameters
    ref_change = ReferenceChangeParameters(extra_dtime_ref=1e6, dE_ref=1e-9)
    assert ref_change.extra_dtime_ref == 1e6
    assert ref_change.dE_ref == 1e-9

    # Test BeamBeamParameters
    beambeam = BeamBeamParameters()
    assert beambeam is not None


def test_multipole_numpy_coercion():
    """Regression test for issue #67: numpy scalars passed to multipole parameter
    classes must be coerced to Python-native numeric types at construction time,
    so YAML/JSON serialization produces clean output regardless of input type."""
    np = pytest.importorskip("numpy")

    # MagneticMultipoleParameters: cover all prefixes and several numpy dtypes
    mmp = MagneticMultipoleParameters(
        tilt1=np.float64(0.1),
        Bn1=np.float64(1.5),
        Bn2=np.float32(2.5),
        Bs1=np.int64(3),
        Kn0=np.int32(-1),
        Ks1=np.float64(0.25),
    )
    assert type(mmp.tilt1) is float and mmp.tilt1 == 0.1
    assert type(mmp.Bn1) is float and mmp.Bn1 == 1.5
    assert type(mmp.Bn2) is float and mmp.Bn2 == 2.5
    assert type(mmp.Bs1) is int and mmp.Bs1 == 3
    assert type(mmp.Kn0) is int and mmp.Kn0 == -1
    assert type(mmp.Ks1) is float and mmp.Ks1 == 0.25

    # 0-d numpy array also works
    mmp_arr = MagneticMultipoleParameters(Bn1=np.array(4.2))
    assert type(mmp_arr.Bn1) is float and mmp_arr.Bn1 == 4.2

    # Length-integrated variants
    mmp_L = MagneticMultipoleParameters(Bn1L=np.float64(7.0), Ks1L=np.float64(8.0))
    assert type(mmp_L.Bn1L) is float and mmp_L.Bn1L == 7.0
    assert type(mmp_L.Ks1L) is float and mmp_L.Ks1L == 8.0

    # ElectricMultipoleParameters: cover all prefixes
    emp = ElectricMultipoleParameters(
        tilt1=np.float64(0.2),
        En1=np.float64(0.5),
        Es1=np.int64(2),
    )
    assert type(emp.tilt1) is float and emp.tilt1 == 0.2
    assert type(emp.En1) is float and emp.En1 == 0.5
    assert type(emp.Es1) is int and emp.Es1 == 2

    emp_L = ElectricMultipoleParameters(En1L=np.float64(1.0), Es1L=np.float64(0.5))
    assert type(emp_L.En1L) is float and emp_L.En1L == 1.0
    assert type(emp_L.Es1L) is float and emp_L.Es1L == 0.5

    # Plain Python values must still pass through unchanged
    mmp_plain = MagneticMultipoleParameters(Bn1=1.5)
    assert type(mmp_plain.Bn1) is float and mmp_plain.Bn1 == 1.5
