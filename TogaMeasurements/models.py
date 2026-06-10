from django.db import models
from TogaClients.models import Client
from auditlog.registry import auditlog

class BaseMeasurement(models.Model):
    """
    Abstract base class to centralize common fields and logic.
    Provides shared audit timestamps and metadata for all measurement types.
    """
    date = models.DateField(auto_now_add=True)
    tailors_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Recorded By")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-date"]

class MenMeasurement(BaseMeasurement):
    client = models.ForeignKey(Client, related_name="men_measurements", on_delete=models.CASCADE)
    
    # Original field definitions preserved for workflow continuity
    sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    nk = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    slv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    r_slv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tom = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    cuff = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    kn = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ft = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    trl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    laps = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    agb_fl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    agb_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    cap = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_fl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    und_kn = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w_kn = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rsm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    half_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_h_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tr_hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_rs = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    frt_lap = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    back_fp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jalamia_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    agb_h_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    skirt_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    arm_hole = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jckt_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    shorthole = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    collar_inch = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    slit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jckt_ch = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    walk = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    skt_hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    pocket = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_ch = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dsk_hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Men's Measurement for {self.client.name} ({self.date})"


class WomenMeasurement(BaseMeasurement):
    client = models.ForeignKey(Client, related_name="women_measurements", on_delete=models.CASCADE)
    
    # Original field definitions preserved for workflow continuity
    sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    b = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ub = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sh_bp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    offsh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    skl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    slv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    rsv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ch = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    nk = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    laps = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    frt_fl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sh_w = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w_floor = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    kn = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    short = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    pen = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tom = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    top_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tr_w = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tr_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ft = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    hl = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    arms_h = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    r_ub = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    band = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jckt_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    r_kn = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    gown_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    short_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    cleavage = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    back_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    cuff = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    acc_b = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    acc_bk = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bpoint = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    skirt_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    h_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    hoodie_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    jumpsuit_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w_ub = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    v_point = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    nip_nip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    vh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    w_hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bicep = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sh_cif = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sh_hip = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ub_sec = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    burst_lt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    slit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    skt_w = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    b_gap = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    round_sh = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    r_neck = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Women's Measurement for {self.client.name} ({self.date})"

# Register with auditlog
auditlog.register(MenMeasurement)
auditlog.register(WomenMeasurement)