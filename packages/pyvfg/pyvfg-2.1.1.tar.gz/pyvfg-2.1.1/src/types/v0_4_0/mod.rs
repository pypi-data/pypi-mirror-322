#[cfg(feature = "json")]
mod json;
#[cfg(feature = "python")]
mod python;

use std::collections::HashMap;

// Re-export unchanged types
use crate::types::v0_2_0::check_vector_eq;
pub use crate::types::v0_2_0::{ProbabilityDistribution, Values};
use crate::types::v0_3_0::check_map_eq;
pub use crate::types::v0_3_0::{
    DiscreteVariableAnonymousElements, DiscreteVariableNamedElements, Factor, FactorRole, Variable,
    VariableRole,
};

pub type VariableID = String;

/// Represents the entire VFG.
/// A VFG consists of a list of factors, and a map of variables to their metadata.
/// For discrete variables, the only metadata is a list of their possible values.
#[cfg_attr(feature = "json", derive(serde::Deserialize, serde::Serialize))]
#[cfg_attr(feature = "json", serde(deny_unknown_fields))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(get_all, eq, module = "pyvfg")
)]
#[derive(Clone, Debug)]
pub struct VFG {
    #[cfg_attr(feature = "json", serde(default = "json::vfg_schema_version"))]
    pub version: String, // 0.4.0 for this spec!
    pub factors: Vec<Factor>,
    pub variables: HashMap<VariableID, Variable>,
    #[cfg_attr(
        feature = "json",
        serde(default, skip_serializing_if = "Option::is_none")
    )]
    pub metadata: Option<Metadata>,
    #[cfg_attr(
        feature = "json",
        serde(
            with = "json::visualization_metadata",
            default,
            skip_serializing_if = "Option::is_none"
        )
    )]
    pub visualization_metadata: Option<String>,
}

impl PartialEq for VFG {
    fn eq(&self, other: &Self) -> bool {
        self.version == other.version
            && check_vector_eq(&other.factors, &self.factors)
            && check_map_eq(&self.variables, &other.variables)
            && self.metadata == other.metadata
            && self.visualization_metadata == other.visualization_metadata
    }
}

impl Default for VFG {
    fn default() -> Self {
        VFG {
            version: "0.4.0".to_string(),
            factors: Default::default(),
            variables: Default::default(),
            metadata: None,
            visualization_metadata: None,
        }
    }
}

#[cfg_attr(feature = "json", derive(serde::Deserialize, serde::Serialize))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, PartialEq, Default, Debug, Clone)]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(get_all, eq, module = "pyvfg")
)]
pub struct Metadata {
    #[cfg_attr(feature = "json", serde(skip_serializing_if = "Option::is_none"))]
    pub model_type: Option<ModelType>,
    #[cfg_attr(feature = "json", serde(skip_serializing_if = "Option::is_none"))]
    pub model_version: Option<String>,
    #[cfg_attr(feature = "json", serde(skip_serializing_if = "Option::is_none"))]
    pub description: Option<String>,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, PartialEq, Debug, Copy, Clone)] // Default skipped on purpose; if you don't know, specify None at the Metadata level
#[cfg_attr(feature = "json", derive(serde::Deserialize, serde::Serialize))]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(eq, eq_int, module = "pyvfg")
)]
#[repr(u8)]
pub enum ModelType {
    #[cfg_attr(feature = "json", serde(rename = "bayesian_network"))]
    BayesianNetwork = 0,
    #[cfg_attr(feature = "json", serde(rename = "markov_random_field"))]
    MarkovRandomField = 1,
    #[cfg_attr(feature = "json", serde(rename = "pomdp"))]
    Pomdp = 2,
    #[cfg_attr(feature = "json", serde(rename = "factor_graph"))]
    FactorGraph = 3,
}

/// These tests are only run if the "json_loader" feature is enabled.
#[cfg(all(test, feature = "json"))]
mod json_tests {
    use super::*;

    #[test]
    fn test_metadata_serialization() {
        let vfg = VFG {
            version: "0.4.0".to_string(),
            metadata: Some(Metadata {
                model_type: Some(ModelType::MarkovRandomField),
                model_version: Some("1.0.0".to_string()),
                description: Some("Test description".to_string()),
            }),
            visualization_metadata: Some(
                r#"{"layout":"force-directed","node_size":10}"#.to_string(),
            ),
            factors: vec![],
            variables: HashMap::new(),
        };

        let json = serde_json::to_value(&vfg).unwrap();
        let deserialized: VFG = serde_json::from_value(json.clone()).unwrap();
        assert_eq!(vfg, deserialized);
    }

    #[test]
    fn test_optional_field_skipped() {
        // Test that optional fields are skipped when None
        let minimal_vfg = VFG::default();
        let minimal_json = serde_json::to_value(&minimal_vfg).unwrap();
        let obj = minimal_json.as_object().unwrap();
        assert!(!obj.contains_key("visualization_metadata"));
        assert!(!obj.contains_key("metadata"));
    }
}

/// These tests are only enabled if persistence (ie, rkyv) is enabled
#[cfg(test)]
mod rkyv_tests {
    use super::*;
    use crate::test_util::generate_test_vfg;

    /// Description: Tests a round-trip in rkyv
    /// Outcomes: Round-trip through u8 using rkyv doesn't change the value
    #[test]
    fn test_rt_rkyv() {
        let graph = generate_test_vfg();
        let serialized: Vec<u8> = rkyv::to_bytes::<rkyv::rancor::Error>(&graph)
            .unwrap()
            .to_vec();
        let deserialized: VFG = rkyv::from_bytes::<VFG, rkyv::rancor::Error>(&serialized).unwrap();
        assert_eq!(
            graph, deserialized,
            "Round-trip through rkyv does not change the value"
        );
    }
}

#[cfg(all(test, feature = "python"))]
mod python_tests {
    use crate::test_util::generate_test_vfg_v0_2_0 as generate_test_vfg;
    use crate::test_util::init_py_test;
    use pyo3::prelude::*;
    use pyo3::py_run;

    #[test]
    fn test_creation() {
        init_py_test();
        Python::with_gil(|py| {
            let vfg: Py<crate::types::v0_2_0::VFG> =
                Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
            py_run!(
                py,
                vfg,
                r#"
                assert len(vfg.factors) == 2, "two factors"
                assert len(vfg.variables) == 2, "two variables"
            "#
            );
        });
    }

    #[test]
    fn test_python_eq() {
        init_py_test();
        Python::with_gil(|py| {
            let a: Py<crate::types::v0_2_0::VFG> =
                Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
            let b: Py<crate::types::v0_2_0::VFG> =
                Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
            py_run!(py, a b, r#"
                assert a == b, "equivalent in python"
            "#);
        });
    }
}
