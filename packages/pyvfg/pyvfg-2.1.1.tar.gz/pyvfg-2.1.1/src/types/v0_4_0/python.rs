use crate::types::v0_2_0::python::convert_variables_from_pydict;
use crate::types::v0_4_0::{Factor, VFG};
use crate::types::{Metadata, ModelType};
use pyo3::types::PyDict;
use pyo3::{pymethods, Bound, IntoPyObject, PyErr, PyObject, Python};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::PyAnyMethods;
use pyo3::PyResult;
use serde::Serialize;

#[pymethods]
impl VFG {
    #[new]
    #[pyo3(signature = (factors, variables, metadata=None, visualization_metadata=None))]
    fn new(
        factors: Vec<Factor>,
        variables: Bound<PyDict>,
        metadata: Option<Metadata>,
        visualization_metadata: Option<String>,
    ) -> Self {
        let variables = convert_variables_from_pydict(variables);
        VFG {
            version: crate::loader::VFG_VERSION.to_string(),
            factors,
            variables,
            metadata,
            visualization_metadata,
        }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        Self::default()
    }

    #[pyo3(signature = (indent=None))]
    fn model_dump_json(&self, indent: Option<usize>) -> PyResult<String> {
        use std::io::BufWriter;

        // set up for serializing with given indent
        let mut buf = BufWriter::new(Vec::new());
        let indent_string = std::iter::repeat(b' ').take(indent.unwrap_or(0)).collect::<Vec<u8>>();
        let fmt = serde_json::ser::PrettyFormatter::with_indent(&indent_string);
        let mut ser = serde_json::Serializer::with_formatter(&mut buf, fmt);
        // actually serialize
        self.serialize(&mut ser).map_err(|e| PyErr::new::<PyValueError, _>(format!("{:?}", e)))?;
        // then get a String out of it for Python
        let json_str = String::from_utf8(buf.into_inner().map_err(|e| PyErr::new::<PyValueError, _>(format!("{:?}", e)))?).map_err(|e| PyErr::new::<PyValueError, _>(format!("{:?}", e)))?;
        Ok(json_str)
    }

    /// Dumps the model to a python dict by first, dumping it to a JSON string, then, loading the json
    /// string in python. There has to be a better way! (Is that way cutting out rust?)
    fn model_dump_python(&self) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            // literally call json.loads() from python with the result of self.model_dump_json()
            let binding = py.import("json").unwrap().getattr("loads").unwrap();
            let json_str = self.model_dump_json(None)?;
            let json_str_ref: &str = &json_str; // needed for binding type inference
            Ok(binding.call1((json_str_ref,)).unwrap().into())
        })
    }

    // see https://github.com/pydantic/pydantic-core/issues/1364 if we want to borrow a proc macro for this
    #[pyo3(signature = (*, mode = "python", indent = None))]
    fn model_dump(&self, mode: &str, indent: Option<usize>) -> PyResult<PyObject> {
        Python::with_gil(|py| match mode {
            // error handling here is to ensure match arms have the same type
            "json" => Ok(self.model_dump_json(indent)?.into_pyobject(py).unwrap().as_any().clone().unbind()),
            "python" => Ok(self.model_dump_python()?),
            _ => Err(PyErr::new::<PyValueError, _>(format!("Unsupported model dump mode: {}", mode))),
        })
    }
}

#[pymethods]
impl Metadata {
    #[new]
    #[pyo3(signature = (model_type=None, model_version=None, description=None))]
    fn new(
        model_type: Option<ModelType>,
        model_version: Option<String>,
        description: Option<String>,
    ) -> Self {
        Metadata {
            model_type,
            model_version,
            description,
        }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        Self::default()
    }
}
