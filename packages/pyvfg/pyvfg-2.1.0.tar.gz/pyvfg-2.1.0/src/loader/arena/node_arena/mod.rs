use crate::loader::persist::Persist;
use crate::types::{Factor, Metadata, Variable};

pub(crate) struct NodeArena {
    /// path to the storage for this NodeArena
    pub(crate) path: Box<str>,
    /// the version *important for future compatability*
    /// This is not DIRECTLY used in this code, but is important because it "forces" the user to call
    /// "perform_db_migration" to get one. It is also important to hold onto the Persist handle
    /// for the duration of the Arena's lifetime, for the same reason we hold onto factors and variables.
    #[allow(unused)] // see comment
    pub(crate) version: Persist<super::Version>,
    /// keys are variable names; values are the graph nodes.
    pub(crate) factors: Persist<crate::loader::GraphNode<Factor>>,
    /// keys are the variable names; value is the metadata for the variable, including values for
    /// named categoricals.
    pub(crate) variables: Persist<Variable>,
    /// key is "metadata", value is the metadata for the graph
    pub(crate) metadata: Persist<Metadata>,
    /// key is "visualization_metadata", value is the metadata for the visualization
    /// other opaque types should be stored here
    pub(crate) additional_data: Persist<String>,
}

impl NodeArena {
    pub(crate) fn new(
        path: Box<str>,
        version: Persist<super::Version>,
        factors: Persist<crate::loader::GraphNode<Factor>>,
        variables: Persist<Variable>,
        metadata: Persist<Metadata>,
        additional_data: Persist<String>,
    ) -> Self {
        NodeArena {
            path,
            version,
            factors,
            variables,
            metadata,
            additional_data,
        }
    }

    pub fn path(&self) -> &str {
        &self.path
    }
}
