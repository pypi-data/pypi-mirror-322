#[cfg(feature = "json")]
pub(crate) mod json;
#[cfg(feature = "python")]
pub(crate) mod python;

use std::cmp::PartialEq;
use std::collections::HashMap;

// adapted from https://github.com/VersesTech/genius-samples/blob/feat/vfg-schema/scripts/python/vfg_schema.json
/// Values represents a values struct in VFG.b.
/// It represents arbitrary-dimension arrays as (shape, values), similar to numpy.
/// This is a key difference from VFG, where a 1-factor is an array, a 2-factor is an array of arrays,
/// 3-factor is array of array of arrays, and so on.
/// In order to make it a bounded type, we represent it as the sequence of dimension breaks
/// that get us to a given shape. For instance:
///   - `[2, 2]`, `[1.0 2.0 3.0 4.0]` is the same as the VFG `[[1.0 2.0][3.0 4.0]]`
///   - `[2, 2, 2], `[1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0]` is the same as the VFG `[[[1.0 2.0][3.0 4.0]], [[5.0 6.0][7.0 8.0]]]`

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Debug, Clone)]
pub struct Values {
    /// The stride count of each dimension in the tensor
    /// The product of all strides must equal values.len()
    pub strides: Vec<usize>,
    /// The unshaped data in the tensor
    pub values: Vec<f32>,
}

impl Default for Values {
    fn default() -> Self {
        Values {
            strides: vec![0],
            values: vec![],
        }
    }
}

/// PartialEq implemented here to counter the issue of float diffs
impl PartialEq for Values {
    fn eq(&self, other: &Self) -> bool {
        if self.strides != other.strides {
            return false;
        }
        if self.values.len() != other.values.len() {
            return false;
        }
        for (a, b) in self.values.iter().zip(other.values.iter()) {
            if (a - b).abs() > f32::EPSILON {
                return false;
            }
        }
        true
    }
}

// serde accessory functions in json.rs

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(eq, eq_int, module = "pyvfg")
)]
#[repr(u8)]
#[derive(PartialEq, Debug, Default, Copy, Clone)]
#[non_exhaustive]
pub enum ProbabilityDistribution {
    #[default]
    Categorical = 0,
    CategoricalConditional = 1,
}

/// Role is optional can can be one of 3 values: "transition", "preference" or "likelihood".
/// There is no default value, only if specified on the factor will it exist
/// None is used for the default value in the event that it exists and the numeric value doesn't match the enum
#[cfg_attr(feature = "json", derive(serde::Deserialize, serde::Serialize))]
#[cfg_attr(feature = "json", serde(untagged))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(eq, eq_int, module = "pyvfg")
)]
#[repr(u8)]
#[derive(PartialEq, Debug, Copy, Clone, Default)]
pub enum Role {
    #[default]
    None = 0,
    Transition = 1,
    Preference = 2,
    Likelihood = 3,
}

/// A Factor represents a single factor extraction of the factor graph.
/// It contains variables, values, and a type.
#[cfg_attr(feature = "json", derive(serde::Deserialize, serde::Serialize))]
#[cfg_attr(
    feature = "python",
    pyo3::prelude::pyclass(get_all, eq, module = "pyvfg")
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, PartialEq, Default, Debug, Clone)]
pub struct Factor {
    pub variables: Vec<String>,
    pub distribution: ProbabilityDistribution,
    pub values: Values,
    // compatability with FactorV1 (enumerate in a bit?)
    #[cfg_attr(feature = "json", serde(skip_serializing_if = "Option::is_none"))]
    pub role: Option<Role>,
}

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
#[allow(clippy::upper_case_acronyms)] // I considered it. I don't like it.
pub struct VFG {
    #[cfg_attr(feature = "json", serde(default = "json::default_vfg_version"))]
    pub version: String, // 0.2.0 for this spec!
    pub factors: Vec<Factor>,
    pub variables: HashMap<String, Vec<String>>,
}

/// determine if two vectors are equal, regardless of order
pub(crate) fn check_vector_eq<T: PartialEq<T2>, T2>(vec1: &[T], vec2: &[T2]) -> bool {
    vec1.len() == vec2.len() && vec1.iter().all(|av| vec2.iter().any(|bv| av == bv))
}

/// determines if two Map<String, Vec<String>> are equal, regardless of Vec<String> order
pub(crate) fn check_map_eq(
    map1: &HashMap<String, Vec<String>>,
    map2: &HashMap<String, Vec<String>>,
) -> bool {
    map1.len() == map2.len()
        && map1.iter().all(|(map1_key, map1_value)| {
            map2.get(map1_key)
                .map_or(false, |map2_value| check_vector_eq(map1_value, map2_value))
        })
}

impl PartialEq for VFG {
    fn eq(&self, other: &Self) -> bool {
        check_vector_eq(&other.factors, &self.factors)
            && check_map_eq(&self.variables, &other.variables)
    }
}

impl Default for VFG {
    fn default() -> Self {
        VFG {
            version: "0.2.0".to_string(),
            factors: Default::default(),
            variables: Default::default(),
        }
    }
}

#[cfg(feature = "python")]
impl VFG {
    fn __str__(&self) -> String {
        format!("{:?}", self)
    }
}

/// These tests are only run if the "json_loader" feature is enabled.
#[cfg(all(test, feature = "json"))]
mod json_tests {
    use super::*;
    use crate::test_util::sprinkler_graph_as_json_value_0_2_0;
    use serde_json::json;

    /// Description: This test that we can retrieve a Vec<Values> from a list of `[1.54, 2.3]`
    /// Outcomes: The elements of the list are properly reshaped into a Values
    #[test]
    fn test_json_numbers() {
        let json = json!([1.54, 2.3]);
        let values: Values = serde_json::from_value(json).unwrap();
        assert_eq!(values.strides.len(), 1, "We have one stride");
        assert_eq!(
            values.strides.get(0),
            Some(&2),
            "Stride two elements long (so it's a 1-dim vector)"
        );
        assert_eq!(values.values.len(), 2, "We have two values");
        assert_eq!(values.values, vec![1.54, 2.3], "Values match input");
    }

    /// Description: Loads our sprinkler test-VFG file from inline JSON
    /// Outcomes: The item is successfully loaded
    #[test]
    fn test_load_from_json() {
        // our test sprinkler file
        let human_vfg_json = sprinkler_graph_as_json_value_0_2_0();
        println!("{:#?}", human_vfg_json);

        // asserts that this is successfully loaded
        let human_vfg: VFG = serde_json::from_value(human_vfg_json).unwrap();
        assert_eq!(
            human_vfg.variables.len(),
            4,
            "We have all four expected variables"
        );
        // assert that we have all four factors
        assert_eq!(
            human_vfg.factors.len(),
            4,
            "We have all four expected factors"
        );
    }

    /// Description: Check serialization back out to json for compliance with VFG
    /// Outcomes: We get back out the same json doc we put in
    #[test]
    fn test_rt_json() {
        let json = sprinkler_graph_as_json_value_0_2_0();
        let mem_type: VFG =
            serde_json::from_value(json.clone()).expect("Can deserialize from json");
        assert_eq!(
            mem_type
                .factors
                .get(0)
                .map(|v| &v.values.strides)
                .expect("size matches"),
            &vec![2],
            "values is of the right shape"
        );
        let json2 = serde_json::to_value(mem_type).expect("Can serialize to json");
        println!("A: {}\nB: {}", json.to_string(), json2.to_string());
        assert_eq!(json, json2, "Round trip serialization matches input");
    }
}

/// These tests are only enabled if persistence (ie, rkyv) is enabled
#[cfg(test)]
mod rkyv_tests {
    use super::*;
    use crate::test_util::generate_test_vfg_v0_2_0 as generate_test_vfg;

    /// Description: Tests a round-trip in rkyv
    /// Outcomes: Round-trip through u8 using rkyv doesn't change the value
    #[test]
    fn test_rt_rkyv() {
        let graph: crate::types::v0_2_0::VFG = generate_test_vfg();
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
    use super::*;
    use crate::test_util::generate_test_vfg_v0_2_0 as generate_test_vfg;
    use crate::test_util::init_py_test;
    use pyo3::prelude::*;
    use pyo3::py_run;

    #[test]
    fn test_creation() {
        init_py_test();
        Python::with_gil(|py| {
            let vfg: Py<VFG> = Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
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
            let a: Py<VFG> = Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
            let b: Py<VFG> = Py::new(py, PyClassInitializer::from(generate_test_vfg())).unwrap();
            py_run!(py, a b, r#"
                assert a == b, "equivalent in python"
            "#);
        });
    }
}
