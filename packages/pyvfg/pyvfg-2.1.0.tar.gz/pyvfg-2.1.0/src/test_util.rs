use crate::types::{
    DiscreteVariableNamedElements, Factor, Metadata, ProbabilityDistribution, Values, VFG,
};

#[cfg(all(test, feature = "python"))]
pub fn init_py_test() {
    pyo3::prepare_freethreaded_python();
}

/// includes all possible values for roles
#[cfg(all(test, feature = "json"))]
pub fn gridworld_graph_as_json_value() -> serde_json::Value {
    serde_json::json!({
        "version": "0.3.0",
        "variables": {
            "position": {
                "elements": [
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8"
                ]
            },
            "observation": {
                "elements": [
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8"
                ],
                "role": "latent"
            },
            "action": {
                "elements": [
                    "UP",
                    "DOWN",
                    "LEFT",
                    "RIGHT",
                    "STAY"
                ],
                "role": "control_state"
            }
        },
        "factors": [
            {
                "variables": ["action"],
                "distribution": "categorical",
                "values": [0.2, 0.2, 0.2, 0.2, 0.2],
                "role": "transition"
            },
            {
                "variables": ["action"],
                "distribution": "categorical",
                "values": [0.2, 0.2, 0.2, 0.2, 0.2],
                "role": "preference"
            },
            {
                "variables": ["action"],
                "distribution": "categorical",
                "values": [0.2, 0.2, 0.2, 0.2, 0.2],
                "role": "initial_state_prior"
            },
            {
                "variables": [
                    "observation",
                    "position"
                ],
                "role": "likelihood",
                "distribution": "categorical_conditional",
                "values": [
                    [
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ]
            }
        ]
    })
}

#[cfg(all(test, feature = "json"))]
pub fn sprinkler_graph_as_json_value() -> serde_json::Value {
    serde_json::json!({
      "version": "0.4.0",
      "variables": {
          "cloudy": {
                "elements": ["no", "yes"]
          },
          "rain": {
                "elements": ["no", "yes"]
          },
          "sprinkler": {
                "elements": ["off", "on"]
          },
          "wet_grass": {
            "elements": ["no", "yes"]
          }
      },
      "factors": [
          {
            "variables": ["cloudy"],
            "distribution": "categorical",
            "values": [
                0.5, 0.5
            ]
          },
          {
              "variables": ["rain", "cloudy"],
              "distribution": "categorical_conditional",
              "values": [
                  [8.0, 2.0],
                  [2.0, 8.0]
              ]
          },
          {
              "variables": ["sprinkler", "cloudy"],
              "distribution": "categorical_conditional",
              "values": [
                  [5.0, 5.0],
                  [9.0, 1.0]
              ],
          },
          {
              "variables": ["wet_grass", "sprinkler", "rain"],
              "distribution": "categorical_conditional",
              "values": [
                  [
                    [10.0, 0.0],
                    [1.0, 9.0]
                  ],
                  [
                    [1.0, 9.0],
                    [1.0, 99.0]
                  ]
              ]
          }
      ]
    })
}

#[cfg(all(test, feature = "json"))]
pub fn sprinkler_graph_as_json_value_0_2_0() -> serde_json::Value {
    serde_json::json!({
      "version": "0.2.0",
      "variables": {
          "cloudy": ["no", "yes"],
          "rain": ["no", "yes"],
          "sprinkler": ["off", "on"],
          "wet_grass": ["no", "yes"]
      },
      "factors": [
          {
            "variables": ["cloudy"],
            "distribution": "categorical",
            "values": [
                0.5, 0.5
            ]
          },
          {
              "variables": ["rain", "cloudy"],
              "distribution": "categorical_conditional",
              "values": [
                  [8.0, 2.0],
                  [2.0, 8.0]
              ]
          },
          {
              "variables": ["sprinkler", "cloudy"],
              "distribution": "categorical_conditional",
              "values": [
                  [5.0, 5.0],
                  [9.0, 1.0]
              ]
          },
          {
              "variables": ["wet_grass", "sprinkler", "rain"],
              "distribution": "categorical_conditional",
              "values": [
                  [
                    [10.0, 0.0],
                    [1.0, 9.0]
                  ],
                  [
                    [1.0, 9.0],
                    [1.0, 99.0]
                  ]
              ]
          }
      ]
    })
}

#[cfg(test)]
pub(crate) fn generate_test_vfg_v0_2_0() -> crate::types::v0_2_0::VFG {
    crate::types::v0_2_0::VFG {
        version: "0.2.0".to_string(),
        factors: vec![
            crate::types::v0_2_0::Factor {
                variables: vec!["rain".to_string(), "cloudy".to_string()],
                distribution: ProbabilityDistribution::CategoricalConditional,
                values: Values {
                    strides: vec![2, 2],
                    values: vec![0.2, 0.8, 0.1, 0.9],
                },
                ..crate::types::v0_2_0::Factor::default()
            },
            crate::types::v0_2_0::Factor {
                variables: vec!["cloudy".to_string()],
                distribution: ProbabilityDistribution::Categorical,
                values: Values {
                    strides: vec![2],
                    values: vec![0.5, 0.5],
                },
                ..crate::types::v0_2_0::Factor::default()
            },
        ],
        variables: vec![
            (
                "rain".to_string(),
                vec!["no".to_string(), "yes".to_string()].into(),
            ),
            (
                "cloudy".to_string(),
                vec!["no".to_string(), "yes".to_string()].into(),
            ),
        ]
        .into_iter()
        .collect(),
    }
}

pub fn generate_test_vfg_v0_3_0() -> crate::types::v0_3_0::VFG {
    crate::types::v0_3_0::VFG {
        version: "0.3.0".to_string(),
        factors: vec![
            Factor {
                variables: vec!["rain".to_string(), "cloudy".to_string()],
                distribution: ProbabilityDistribution::CategoricalConditional,
                values: Values {
                    strides: vec![2, 2],
                    values: vec![0.8, 0.2, 0.2, 0.8],
                },
                ..Factor::default()
            },
            Factor {
                variables: vec!["cloudy".to_string()],
                distribution: ProbabilityDistribution::Categorical,
                values: Values {
                    strides: vec![2],
                    values: vec![0.5, 0.5],
                },
                ..Factor::default()
            },
            Factor {
                variables: vec!["sprinkler".to_string(), "cloudy".to_string()],
                distribution: ProbabilityDistribution::CategoricalConditional,
                values: Values {
                    strides: vec![2, 2],
                    values: vec![0.5, 0.9, 0.5, 0.1],
                },
                ..Factor::default()
            },
        ],
        variables: vec![
            (
                "rain".to_string(),
                vec!["no".to_string(), "yes".to_string()].into(),
            ),
            (
                "cloudy".to_string(),
                vec!["no".to_string(), "yes".to_string()].into(),
            ),
            (
                "sprinkler".to_string(),
                vec!["off".to_string(), "on".to_string()].into(),
            ),
        ]
        .into_iter()
        .collect(),
    }
}

pub fn generate_test_vfg_v0_4_0() -> VFG {
    VFG {
        version: "0.4.0".to_string(),
        factors: vec![
            Factor {
                variables: vec!["rain".to_string(), "cloudy".to_string()],
                distribution: ProbabilityDistribution::CategoricalConditional,
                values: Values {
                    strides: vec![2, 2],
                    values: vec![0.8, 0.2, 0.2, 0.8],
                },
                ..Factor::default()
            },
            Factor {
                variables: vec!["cloudy".to_string()],
                distribution: ProbabilityDistribution::Categorical,
                values: Values {
                    strides: vec![2],
                    values: vec![0.5, 0.5],
                },
                ..Factor::default()
            },
            Factor {
                variables: vec!["sprinkler".to_string(), "cloudy".to_string()],
                distribution: ProbabilityDistribution::CategoricalConditional,
                values: Values {
                    strides: vec![2, 2],
                    values: vec![0.5, 0.9, 0.5, 0.1],
                },
                ..Factor::default()
            },
        ],
        variables: vec![
            (
                "rain".to_string(),
                crate::types::v0_4_0::Variable::DiscreteVariableNamedElements(
                    DiscreteVariableNamedElements {
                        elements: vec!["no".to_string(), "yes".to_string()],
                        ..Default::default()
                    },
                ),
            ),
            (
                "cloudy".to_string(),
                crate::types::v0_4_0::Variable::DiscreteVariableNamedElements(
                    DiscreteVariableNamedElements {
                        elements: vec!["no".to_string(), "yes".to_string()],
                        ..Default::default()
                    },
                ),
            ),
            (
                "sprinkler".to_string(),
                crate::types::v0_4_0::Variable::DiscreteVariableNamedElements(
                    DiscreteVariableNamedElements {
                        elements: vec!["off".to_string(), "on".to_string()],
                        ..Default::default()
                    },
                ),
            ),
        ]
        .into_iter()
        .collect(),
        metadata: Some(Metadata {
            model_type: None,
            model_version: Some("2q".to_string()),
            description: None,
        }),
        visualization_metadata: Some(
            r#"{
            "test": "value",
            "something_else": 5
        }"#
            .to_string(),
        ),
    }
}

pub(crate) fn generate_test_vfg() -> VFG {
    generate_test_vfg_v0_4_0()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::validation::validate_vfg;

    /// Description: Create and validate a v0.4.0 VFG using the generate_test_vfg_v0_4_0() method
    /// Objectives: 1. Create a VFG using the generate_test_vfg_v0_4_0() method
    ///            2. Verify that the generated VFG passes validation
    #[test]
    fn test_create_and_validate_v0_4_0_success() {
        let result = validate_vfg(&generate_test_vfg_v0_4_0());

        if let Err(e) = &result {
            println!("VFG format is invalid: {}", e);
        }

        assert!(result.is_ok());
    }
}
