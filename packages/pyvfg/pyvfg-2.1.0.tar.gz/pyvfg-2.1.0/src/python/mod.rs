mod convert;

use crate::error::FactorGraphStoreError;
use crate::{FactorGraphStore, VFG};
use pyo3::prelude::*;

type FGResult<T> = Result<T, FactorGraphStoreError>;

fn get_fg() -> FGResult<FactorGraphStore> {
    // we must create a separate DB handle for every call, due to how python handles multiprocessing
    FactorGraphStore::new("factor_graph_data")
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn get_graph() -> FGResult<VFG> {
    // call get_graph on the global FG, mapping exceptions, and returning a default FG is one was not yet set
    Ok(get_fg()?.get_graph()?.unwrap_or_default().into())
}

#[pyfunction]
fn set_graph(new_graph: VFG) -> FGResult<()> {
    get_fg()?.replace_graph(new_graph)?;
    Ok(())
}

#[pyfunction]
fn validate_graph(graph: VFG) -> FGResult<()> {
    get_fg()?.validate_graph(&graph)?;
    Ok(())
}

#[pyfunction]
fn get_subgraph_from(variable_name: Vec<String>) -> FGResult<VFG> {
    Ok(get_fg()?
        .get_subgraph_from(&variable_name)?
        .unwrap_or_default()
        .into())
}

/// A Python module implemented in Rust.
/// See: https://github.com/PyO3/maturin?tab=readme-ov-file#mixed-rustpython-projects
#[pymodule]
#[pyo3(name = "_pyvfg")]
fn pyvfg(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // register classes
    m.add_class::<VFG>()?;
    m.add_class::<crate::types::ProbabilityDistribution>()?;
    m.add_class::<crate::types::FactorRole>()?;
    m.add_class::<crate::types::VariableRole>()?;
    m.add_class::<crate::types::Factor>()?;
    m.add_class::<crate::types::DiscreteVariableNamedElements>()?;
    m.add_class::<crate::types::DiscreteVariableAnonymousElements>()?;
    m.add_class::<crate::types::Metadata>()?;
    m.add_class::<crate::types::ModelType>()?;

    // register exceptions
    m.add(
        "FileManipulationError",
        py.get_type::<convert::FileManipulationError>(),
    )?;
    m.add(
        "DatabaseError",
        py.get_type::<convert::DatabaseError>(),
    )?;
    m.add(
        "RkyvDeserializationError",
        py.get_type::<convert::RkyvDeserializationError>(),
    )?;
    m.add(
        "JsonSerializationError",
        py.get_type::<convert::JsonSerializationError>(),
    )?;
    m.add(
        "ValidationError",
        py.get_type::<convert::ValidationError>(),
    )?;
    m.add(
        "InvalidVersionSpecification",
        py.get_type::<convert::InvalidVersionSpecification>(),
    )?;

    // env!() gets the environment variable value at *compile* time; this is from the build system
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    // bind subgraph functions
    m.add_function(wrap_pyfunction!(get_graph, m)?)?;
    m.add_function(wrap_pyfunction!(validate_graph, m)?)?;
    m.add_function(wrap_pyfunction!(set_graph, m)?)?;
    m.add_function(wrap_pyfunction!(get_subgraph_from, m)?)?;

    // bind json functions
    #[cfg(feature = "json")]
    m.add_function(wrap_pyfunction!(crate::python::convert::vfg_to_json, m)?)?;
    #[cfg(feature = "json")]
    m.add_function(wrap_pyfunction!(crate::python::convert::vfg_from_json, m)?)?;

    Ok(())
}
