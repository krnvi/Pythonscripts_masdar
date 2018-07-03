

def calculate_visibility(qv,qc,qr,qi,qs,T,p):
    """
    Calculates visibility based on the UPP algorithm.

    See documentation in UPPV3.0/src/unipost/CALVIS.f for the description of
    input arguments and references.
    """
    Rd = 287.
    COEFLC = 144.7
    COEFLP = 2.24
    COEFFC = 327.8
    COEFFP = 10.36
    EXPLC  = 0.88
    EXPLP  = 0.75
    EXPFC  = 1.
    EXPFP  = 0.7776

    Tv   = T * (1+0.61*qv) # Virtual temperature

    rhoa = p/(Rd*Tv) # Air density [kg m^-3]
    rhow = 1e3       # Water density [kg m^-3]
    rhoi = 0.917e3   # Ice density [kg m^-3]

    vovmd = (1+qv)/rhoa + (qc+qr)/rhow + (qi+qs)/rhoi

    conc_lc = 1e3*qc/vovmd
    conc_lp = 1e3*qr/vovmd
    conc_fc = 1e3*qi/vovmd
    conc_fp = 1e3*qs/vovmd

    # Make sure all concentrations are positive
    conc_lc[conc_lc < 0] = 0
    conc_lp[conc_lp < 0] = 0
    conc_fc[conc_fc < 0] = 0
    conc_fp[conc_fp < 0] = 0

    betav = COEFFC*conc_fc**EXPFC\
          + COEFFP*conc_fp**EXPFP\
          + COEFLC*conc_lc**EXPLC\
          + COEFLP*conc_lp**EXPLP+1E-10

    vis = -np.log(0.02)/betav # Visibility [km]
    vis[vis > 24.135] = 24.135

    return vis