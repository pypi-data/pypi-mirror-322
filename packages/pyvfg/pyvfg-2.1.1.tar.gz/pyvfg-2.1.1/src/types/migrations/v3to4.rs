impl From<crate::types::v0_3_0::VFG> for crate::types::v0_4_0::VFG {
    fn from(val: crate::types::v0_3_0::VFG) -> Self {
        crate::types::v0_4_0::VFG {
            version: "0.4.0".to_string(),
            metadata: Default::default(),
            visualization_metadata: None,
            factors: val.factors,
            variables: val.variables,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::test_util::generate_test_vfg_v0_3_0;

    #[test]
    fn test_3to4_migration() {
        let v3 = generate_test_vfg_v0_3_0();
        let v4: crate::types::v0_4_0::VFG = v3.into();

        assert_eq!(v4.version, "0.4.0");
        assert!(v4.metadata.is_none());
        assert!(v4.visualization_metadata.is_none());

        // Verify that core data is preserved
        assert!(!v4.factors.is_empty());
        assert!(!v4.variables.is_empty());
    }
}
