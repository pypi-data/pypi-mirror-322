use crate::types::v0_2_0::Values;
use crate::types::{DiscreteVariableAnonymousElements, DiscreteVariableNamedElements, Variable};
use ndarray::{Array, IntoDimension};
use numpy::IntoPyArray;
use pyo3::prelude::PyAnyMethods;
use pyo3::types::PyDict;
use pyo3::{Bound, IntoPyObject, IntoPyObjectExt, PyAny, Python};
use std::collections::HashMap;

pub(crate) fn convert_variables_from_pydict(variables: Bound<PyDict>) -> HashMap<String, Variable> {
    variables
        .into_iter()
        .map(|(key, any)| {
            let key = key.extract::<String>().unwrap();
            let var = match any.extract::<DiscreteVariableNamedElements>() {
                Ok(var) => Variable::DiscreteVariableNamedElements(var),
                Err(_) => {
                    let var = any.extract::<DiscreteVariableAnonymousElements>().unwrap();
                    Variable::DiscreteVariableAnonymousElements(var)
                }
            };
            (key, var)
        })
        .collect()
}

impl<'py> IntoPyObject<'py> for Values {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = pyo3::PyErr;

    fn into_pyobject(self, py: Python<'py>) -> pyo3::PyResult<Self::Output> {
        let strides = self
            .strides
            .into_iter()
            .map(|x| x)
            .collect::<Vec<usize>>();
        let arr = Array::from_shape_vec(strides.into_dimension(), self.values)
            .expect("can create ndarray");
        arr.into_pyarray(py).into_bound_py_any(py)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pyo3::py_run;

    fn init_py_test() {
        pyo3::prepare_freethreaded_python();
    }

    #[test]
    fn test_into_py() {
        init_py_test();
        let values = Values {
            values: vec![1.0, 2.0, 3.0],
            strides: vec![1, 3],
        };
        Python::with_gil(|py| {
            let py_obj = values.into_pyobject(py).unwrap();
            py_run!(
                py,
                py_obj,
                r#"
                assert py_obj.shape == (1, 3)
                assert py_obj[0, 0] == 1.0
                assert py_obj[0, 1] == 2.0
                assert py_obj[0, 2] == 3.0
            "#
            );
        });
    }
}
