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
