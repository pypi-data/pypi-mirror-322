use crate::types::v0_2_0::VFG as VFGv2;
use crate::types::v0_4_0::VFG as VFGv4;

/// very simple conversion here; we'll just chain 2->3 then 3->4
impl From<VFGv2> for VFGv4 {
    fn from(v2: VFGv2) -> Self {
        let v3: crate::types::v0_3_0::VFG = v2.into();
        v3.into()
    }
}
