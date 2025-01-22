pub fn vfg_schema_version() -> String {
    "0.4.0".to_string()
}

pub mod visualization_metadata {
    use serde::{Deserialize, Deserializer, Serialize, Serializer};
    use serde_json::Value;

    pub fn serialize<S>(value: &Option<String>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        value
            .as_ref()
            .map(|s| serde_json::from_str::<Value>(s).expect("infallible"))
            .serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Option<String>, D::Error>
    where
        D: Deserializer<'de>,
    {
        Ok(Option::<Value>::deserialize(deserializer)?
            .map(|v| serde_json::to_string(&v).expect("infallible")))
    }
}

#[cfg(test)]
mod tests {
    use crate::types::VFG;

    #[test]
    fn test_load_sprinkler_with_version_metadata() {
        let json = include_str!("../../../test_data/small/sprinkler_factor_graph_vfg.json");
        let vfg: VFG = serde_json::from_str(&json).unwrap();
        assert!(vfg.metadata.is_some(), "Check that version exists");
        assert_eq!(
            vfg.metadata
                .as_ref()
                .unwrap()
                .model_version
                .as_ref()
                .unwrap(),
            "2q",
            "Check that version is equal to loaded value"
        );
    }
}
