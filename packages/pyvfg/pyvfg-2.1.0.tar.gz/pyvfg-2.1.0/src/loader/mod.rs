use crate::error::FactorGraphStoreError;
use crate::loader::arena::{
    NodeArena, ADDITIONAL_DATA_FN, FACTORS_FN, METADATA_FN, METADATA_KEY, VARIABLES_FN,
    VERSION_KEY, VIS_METADATA_KEY,
};
use crate::types::{Factor, Metadata, Variable, VFG};
use heed::types::Bytes;
use heed::Error::Io;
use itertools::Itertools;
use persist::CanRead;
use persist::Persist;
use rkyv::api::low::deserialize;
use rkyv::rancor::Strategy;
use std::collections::HashSet;

pub(crate) mod arena;
pub(crate) mod persist;

const VARIABLE_SEPARATOR: &str = "\x1F";
pub(crate) const VFG_VERSION: &str = "0.4.0";

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Default, Debug, PartialEq)]
pub(crate) struct GraphNode<F> {
    input: Vec<String>,
    contents: F,
}

/// This persists a graph into the datastore
pub(crate) fn persist_graph(source: VFG, path: &str) -> Result<NodeArena, FactorGraphStoreError> {
    // set version
    let version = Persist::new(path, "version")?;
    let mut transaction = version.open_write()?;
    version.insert(&mut transaction, VERSION_KEY, source.version.try_into()?)?;
    drop(transaction);

    // create variables
    let variables = Persist::new(path, VARIABLES_FN)?;
    let mut transaction = variables.open_write()?;
    for var in source.variables.into_iter() {
        variables.insert(&mut transaction, var.0.as_bytes(), var.1)?;
    }
    drop(transaction);

    let factors = Persist::new(path, FACTORS_FN)?;
    let mut transaction = factors.open_write()?;
    for factor in source.factors.into_iter() {
        let index_var = factor.variables.iter().join(VARIABLE_SEPARATOR);
        let inputs = factor.variables.to_vec();
        let tgt_node = GraphNode {
            input: inputs,
            contents: factor,
        };
        factors.insert(&mut transaction, index_var.as_bytes(), tgt_node)?;
    }
    drop(transaction);

    let metadata = Persist::new(path, METADATA_FN)?;
    let mut transaction = metadata.open_write()?;
    if let Some(src_metadata) = source.metadata {
        metadata.insert(&mut transaction, METADATA_KEY, src_metadata)?;
    } else {
        metadata.clear(&mut transaction)?;
    }
    drop(transaction);

    let additional_data = Persist::new(path, ADDITIONAL_DATA_FN)?;
    let mut transaction = additional_data.open_write()?;
    if let Some(vis_metadata) = source.visualization_metadata {
        additional_data.insert(&mut transaction, VIS_METADATA_KEY, vis_metadata)?;
    } else {
        additional_data.clear(&mut transaction)?;
    }
    drop(transaction);

    Ok(NodeArena::new(
        path.to_string().into_boxed_str(),
        version,
        factors,
        variables,
        metadata,
        additional_data,
    ))
}

fn variable_mapping(
    arena: &NodeArena,
) -> Result<std::collections::HashMap<String, Variable>, FactorGraphStoreError> {
    let var_vals_transaction = arena.variables.open_read()?;
    arena
        .variables
        .iter(&var_vals_transaction)
        .map(|(k, v)| {
            let k = String::from_utf8(k.to_vec()).unwrap();
            let vals = deserialize::<Variable, rkyv::rancor::Error>(v)?;
            Ok((k, vals))
        })
        .collect()
}

fn variable_mapping_for(
    arena: &NodeArena,
    vars: &[String],
) -> Result<std::collections::HashMap<String, Variable>, FactorGraphStoreError> {
    let variable_mapping_transaction = arena.factors.open_read()?;
    let var_vals_transaction = arena.variables.open_read()?;
    arena
        .factors
        .iter(&variable_mapping_transaction)
        .filter_map(|(k, _)| {
            String::from_utf8(k.to_vec())
                .ok()
                .filter(|k| vars.iter().any(|part| k.contains(part)))
        })
        .flat_map(|k| {
            k.split(VARIABLE_SEPARATOR)
                .map(|s| s.to_string())
                .collect::<Vec<String>>()
        })
        .map(|k| {
            let vals = arena.variables.get(&var_vals_transaction, k.as_bytes());
            match vals {
                Some(vals) => {
                    let vals = deserialize::<Variable, rkyv::rancor::Error>(vals)?;
                    Ok((k, vals))
                }
                None => Ok((k, Variable::default())),
            }
        })
        .collect()
}

/// Finds all factor keys in the arena that contain the given variable
fn find_factor_keys_for_var(
    arena: &NodeArena,
    var: &str,
) -> Result<Vec<String>, FactorGraphStoreError> {
    {
        let transaction = arena.factors.open_read()?;

        let vec = arena
            .factors
            .iter(&transaction)
            .filter_map(|(key, _)| {
                String::from_utf8(key.to_vec())
                    .ok()
                    .filter(|k| k.split(VARIABLE_SEPARATOR).any(|part| part == var))
            })
            .collect();
        Ok(vec)
    }
}

type OptionalHeedResult<T> = Result<Option<T>, heed::Error>;
/// Loads a type from a transaction, returning None on FileNotFound errors.
/// The type (T) should be `#[derive(Archive, Deserialize)]`.
fn load_optional_from_tx<T>(
    tx: Result<persist::ReadTransaction, heed::Error>,
    db: &heed::Database<Bytes, Bytes>,
    key: &[u8],
) -> OptionalHeedResult<T>
where
    for<'a> T: rkyv::Serialize<
        Strategy<
            rkyv::ser::Serializer<
                rkyv::util::AlignedVec,
                rkyv::ser::allocator::ArenaHandle<'a>,
                rkyv::ser::sharing::Share,
            >,
            rkyv::rancor::Error,
        >,
    >,
    <T as rkyv::Archive>::Archived: rkyv::Deserialize<T, Strategy<(), rkyv::rancor::Error>>,
{
    match tx {
        Err(e) => match e {
            // allow the metadata to not exist
            Io(io) if io.kind() == std::io::ErrorKind::NotFound => Ok(None),
            _ => Err(e),
        },
        Ok(tx) => {
            // on successful retrieval, deserialize and return the metadata
            Ok(
                <persist::ReadTransaction<'_> as CanRead<T>>::get(&tx, db, key)
                    .map(|v| deserialize::<T, rkyv::rancor::Error>(v).unwrap()),
            )
        }
    }
}

/// Loads the metadata key for this graph.
/// Unlike other retrieval methods, this will return None on error, as metadata is optional.
fn load_metadata(arena: &NodeArena) -> OptionalHeedResult<Metadata> {
    let tx = arena.metadata.open_read();
    load_optional_from_tx(tx, &arena.metadata.db, METADATA_KEY)
}

/// Loads the visualization metadata for this graph
/// Unlike other retrieval methods, this will return None on error, as visualization metadata is optional.
fn load_visualization_metadata(arena: &NodeArena) -> OptionalHeedResult<String> {
    let tx = arena.additional_data.open_read();
    load_optional_from_tx(tx, &arena.additional_data.db, VIS_METADATA_KEY)
}

/// Loads the entire graph from the arena
/// Returns a VFG containing the entire graph.
/// Returns an error if there is an error retrieving the graph.
pub(crate) fn retrieve_graph(arena: &NodeArena) -> Result<Option<VFG>, FactorGraphStoreError> {
    let mut factors = Vec::new();
    let transaction = arena.factors.open_read()?;

    for (_, node) in arena.factors.iter(&transaction) {
        factors.push(rkyv::deserialize::<GraphNode<Factor>, rkyv::rancor::Error>(node)?.contents);
    }

    let variables = variable_mapping(arena)?;

    let metadata = load_metadata(arena)?;
    let visualization_metadata = load_visualization_metadata(arena)?;

    Ok(Some(VFG {
        version: VFG_VERSION.to_string(),
        factors,
        variables,
        metadata,
        visualization_metadata,
    }))
}

/// Loads the subgraph that produces the output for a given variable
/// Returns an Option<VFG> where the VFG is the subgraph that produces the output for the given variable,
/// or None if the variable is not found in the graph.
/// Returns an error if there is an error retrieving the graph.
pub(crate) fn retrieve_subgraph(
    arena: &NodeArena,
    vars: &[String],
) -> Result<Option<VFG>, FactorGraphStoreError> {
    // convert from user variable to internal variable
    let mut stack = vars.to_vec();
    // tree traversal
    let mut visited = HashSet::new();
    let mut factors = Vec::new();
    let transaction = arena.factors.open_read()?;
    while let Some(var_ref) = stack.pop() {
        let factor_keys = find_factor_keys_for_var(arena, &var_ref)?;
        for key in factor_keys {
            if visited.contains(&key) {
                continue;
            }
            visited.insert(key.clone());
            if let Some(node) = arena.factors.get(&transaction, key.as_bytes()) {
                factors.push(
                    rkyv::deserialize::<GraphNode<Factor>, rkyv::rancor::Error>(node)
                        .unwrap()
                        .contents,
                );
                stack.extend(
                    node.input
                        .iter()
                        .map(|s| rkyv::deserialize::<String, rkyv::rancor::Error>(s).unwrap()),
                );
            } else {
                return Ok(None);
            }
        }
    }

    let variables = variable_mapping_for(arena, vars)?;

    if variables.is_empty() && factors.is_empty() {
        return Ok(None);
    }

    let metadata = load_metadata(arena)?;
    let visualization_metadata = load_visualization_metadata(arena)?;

    Ok(Some(VFG {
        version: VFG_VERSION.to_string(),
        factors,
        variables,
        metadata,
        visualization_metadata,
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_util::generate_test_vfg;

    /// Description: Tests if we can oad a graph into the NodeArena
    /// Objectives: Loading a graph from the "wire" format results in a change to the
    /// factor graph store
    #[test]
    fn test_load_graph() {
        let wire_graph = generate_test_vfg();
        let arena =
            persist_graph(wire_graph, "factor_graph_data/test_load_graph").expect("can load graph");
        let variable_mapping_transaction = arena.factors.open_read().unwrap();
        let var_vals_transaction = arena.variables.open_read().unwrap();
        assert_eq!(arena.factors.len(&variable_mapping_transaction).unwrap(), 3);
        assert_eq!(arena.variables.len(&var_vals_transaction).unwrap(), 3);
        drop(var_vals_transaction);
        drop(variable_mapping_transaction);
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_load_graph").unwrap();
    }

    /// Description: Tests if we can load a graph with empty values
    /// Objectives: Loading a graph with empty values should not result in an error
    /// Regression test for GPAI-155.
    #[test]
    #[cfg(feature = "json")]
    fn test_load_graph_var_empty_values() {
        let wire_graph = serde_json::from_value(serde_json::json!({
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
            "version": "0.4.0"
        }))
        .unwrap();
        let test_fn = format!("factor_graph_data/test_{}", nanoid::nanoid!());
        {
            let arena = persist_graph(wire_graph, &test_fn).expect("can load graph");
            let variable_mapping_transaction = arena.factors.open_read().unwrap();
            let var_vals_transaction = arena.variables.open_read().unwrap();
            assert_eq!(arena.factors.len(&variable_mapping_transaction).unwrap(), 1);
            assert_eq!(arena.variables.len(&var_vals_transaction).unwrap(), 1);
            let vfg = retrieve_graph(&arena).unwrap().unwrap();
            assert_eq!(vfg.variables.len(), 1);
            assert_eq!(vfg.factors.len(), 1);
            let _json = serde_json::to_value(vfg).expect("Can reserialize");
        }

        std::fs::remove_dir_all(&test_fn).unwrap();
    }

    /// Description: Persist a graph with empty metadata after persisting a graph with metadata
    /// Objectives: Metadata should now be empty
    ///
    #[test]
    #[cfg(feature = "json")]
    fn test_save_graph_empty_metadata() {
        let wire_graph = serde_json::from_value(serde_json::json!({
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
            "version": "0.4.0",
            "metadata": {
                "model_type": "bayesian_network",
                "model_version": "2q",
                "description": "A simple sprinkler demo"
            }

        }))
        .unwrap();
        let wire_graph_no_metadata = serde_json::from_value(serde_json::json!({
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
            "version": "0.4.0"
        }))
        .unwrap();

        let test_fn = format!("factor_graph_data/test_{}", nanoid::nanoid!());
        {
            // persist a graph with metadata
            let arena = persist_graph(wire_graph, &test_fn).expect("can load graph");
            let vfg = retrieve_graph(&arena).unwrap().unwrap();
            assert!(vfg.metadata.is_some(), "Metadata Exists");
            let _json = serde_json::to_value(vfg).expect("Can reserialize");

            //persist a graph without metadata
            let arena = persist_graph(wire_graph_no_metadata, &test_fn).expect("can load graph");
            let vfg = retrieve_graph(&arena).unwrap().unwrap();
            assert!(vfg.metadata.is_none(), "Metadata Gone");
            let _json = serde_json::to_value(vfg).expect("Can reserialize");
        }

        std::fs::remove_dir_all(&test_fn).unwrap();
    }

    /// Description: Tests if we can fetch a subgraph from the arena
    /// Objectives: We can retrieve a subgraph from the arena
    #[test]
    fn test_retrieve_subgraph() {
        let wire_graph = generate_test_vfg();
        let arena = persist_graph(wire_graph, "factor_graph_data/test_retrieve_subgraph")
            .expect("can load graph");
        let deps = retrieve_subgraph(&arena, &["rain".to_string()]).expect("can retrieve subgraph");
        assert!(deps.is_some());
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_retrieve_subgraph").unwrap();
    }

    #[test]
    fn test_retrieve_subgraph_multiple() {
        let wire_graph = generate_test_vfg();
        let arena = persist_graph(
            wire_graph,
            "factor_graph_data/test_retrieve_subgraph_multiple",
        )
        .expect("can load graph");
        let deps = retrieve_subgraph(&arena, &["rain".to_string(), "cloudy".to_string()])
            .expect("can retrieve subgraph");
        assert!(deps.is_some());
        drop(arena);
        std::fs::remove_dir_all("factor_graph_data/test_retrieve_subgraph_multiple").unwrap();
    }

    /// A *deliberately incomplete* version of persist_graph_v0_3_0, to prove we can load items saved
    /// with the previous version of this loader.
    fn persist_graph_v0_3_0(source: VFG, path: &str) -> Result<NodeArena, FactorGraphStoreError> {
        let version = Persist::new(path, "version")?;
        let mut transaction = version.open_write()?;
        version.insert(&mut transaction, VERSION_KEY, source.version.try_into()?)?;
        drop(transaction);

        // create variables
        let variables = Persist::new(path, VARIABLES_FN)?;
        let mut transaction = variables.open_write()?;
        for var in source.variables.into_iter() {
            variables.insert(&mut transaction, var.0.as_bytes(), var.1)?;
        }
        drop(transaction);

        let factors = Persist::new(path, FACTORS_FN)?;
        let mut transaction = factors.open_write()?;
        for factor in source.factors.into_iter() {
            let index_var = factor.variables.iter().join(VARIABLE_SEPARATOR);
            let inputs = factor.variables.to_vec();
            let tgt_node = GraphNode {
                input: inputs,
                contents: factor,
            };
            factors.insert(&mut transaction, index_var.as_bytes(), tgt_node)?;
        }
        drop(transaction);

        // we create these but DO NOT POPULATE. They'll then be deleted.
        let metadata = Persist::new(path, METADATA_FN)?;
        let additional_data = Persist::new(path, ADDITIONAL_DATA_FN)?;

        Ok(NodeArena::new(
            path.to_string().into_boxed_str(),
            version,
            factors,
            variables,
            metadata,
            additional_data,
        ))
    }

    #[test]
    fn test_load_graph_without_metadata() {
        let path = "factor_graph_data/load_graph_without_metadata";

        // serialize as normal
        let wire_graph = generate_test_vfg();
        assert!(
            !wire_graph.metadata.is_none(),
            "checking input graph has metadata"
        );
        let save_arena =
            persist_graph_v0_3_0(wire_graph, "factor_graph_data/load_graph_without_metadata")
                .expect("can load graph");
        drop(save_arena);

        // remove metadata and additional data, simulating a DB without these
        std::fs::remove_file(format!("{path}/{METADATA_FN}")).unwrap();
        std::fs::remove_file(format!("{path}/{ADDITIONAL_DATA_FN}")).unwrap();

        // load the graph like FGS does
        let load_arena = NodeArena {
            path: path.into(),
            version: arena::migration::handle_db_migration(path).unwrap(),
            factors: Persist::new(path, FACTORS_FN).unwrap(),
            variables: Persist::new(path, VARIABLES_FN).unwrap(),
            metadata: Persist::new(path, METADATA_FN).unwrap(),
            additional_data: Persist::new(path, ADDITIONAL_DATA_FN).unwrap(),
        };

        // check if data still exists
        let deps_option = retrieve_graph(&load_arena).expect("can retrieve graph");
        assert!(
            deps_option.is_some(),
            "we can successfully retrieve the graph after deleting metadata and extra data"
        );
        let deps = deps_option.unwrap();
        assert!(
            deps.metadata.is_none(),
            "and we \"successfully\" retrieve a None for the metadata"
        );
        assert!(
            deps.visualization_metadata.is_none(),
            "and we \"successfully\" retrieve a None for the visualization metadata"
        );
        drop(load_arena);

        // cleanup
        std::fs::remove_dir_all("factor_graph_data/load_graph_without_metadata").unwrap();
    }
}
