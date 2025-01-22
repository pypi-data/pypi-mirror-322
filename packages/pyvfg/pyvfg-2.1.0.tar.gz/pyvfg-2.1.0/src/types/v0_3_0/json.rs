pub fn vfg_schema_version() -> String {
    "0.3.0".to_string()
}

/// Returns true if the factor role is none.
pub fn factor_role_is_none(role: &super::FactorRole) -> bool {
    *role == super::FactorRole::NoRole
}

/// Returns true if the variable role is none.
pub fn variable_role_is_none(role: &super::VariableRole) -> bool {
    *role == super::VariableRole::NoRole
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_v3_no_allow_vis_metadata() {
        let m: Result<crate::types::VFGMeta, _> = serde_json::from_value(serde_json::json!({
            "factors": [
              {
                "distribution": "categorical",
                "values": [],
                "variables": [
                  "cloudy"
                ]
              }
            ],
            "variables": {
              "cloudy": {
                "elements": [
                  "no",
                  "yes"
                ]
              }
            },
            "visualization_metadata": {
                "hi": "bob",
            },
            "version": "0.3.0"
        }));
        match m {
            Err(_) => {}
            Ok(crate::types::VFGMeta::VFGv0_3_0(_)) => {
                panic!("should not have allowed visualization metadata");
            }
            _ => {
                panic!("wrong version");
            }
        }
    }

    #[test]
    fn test_v3_no_allow_metadata() {
        let m: Result<crate::types::VFGMeta, _> = serde_json::from_value(serde_json::json!({
            "factors": [
              {
                "distribution": "categorical",
                "values": [],
                "variables": [
                  "cloudy"
                ]
              }
            ],
            "variables": {
              "cloudy": {
                "elements": [
                  "no",
                  "yes"
                ]
              }
            },
            "metadata": {
                "model_version": "2q"
            },
            "version": "0.3.0"
        }));
        match m {
            Err(_) => {}
            Ok(crate::types::VFGMeta::VFGv0_3_0(_)) => {
                panic!("should not have allowed metadata");
            }
            _ => {
                panic!("wrong version");
            }
        }
    }
}
