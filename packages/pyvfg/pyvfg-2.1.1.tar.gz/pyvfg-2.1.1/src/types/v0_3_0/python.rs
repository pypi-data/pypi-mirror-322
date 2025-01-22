use crate::types::v0_3_0::{DiscreteVariableNamedElements, Factor, Values, VariableRole, VFG};
use crate::types::{
    DiscreteVariableAnonymousElements, FactorRole, ProbabilityDistribution, VariableID,
};
use pyo3::prelude::PyAnyMethods;
use pyo3::types::PyDict;
use pyo3::{pymethods, Bound, IntoPyObject, PyAny, Python};

impl<'py> IntoPyObject<'py> for super::Variable {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = pyo3::PyErr;

    fn into_pyobject(self, py: Python<'py>) -> pyo3::PyResult<Self::Output> {
        // in-place conversion here
        let mapped: Bound<'py, PyAny> = match self {
            super::Variable::DiscreteVariableNamedElements(dvne) => dvne.into_pyobject(py)?.into_any(),
            super::Variable::DiscreteVariableAnonymousElements(dvae) => dvae.into_pyobject(py)?.into_any(),
        };
        Ok(mapped)
    }
}

#[pymethods]
impl VFG {
    #[new]
    fn new(factors: Vec<Factor>, variables: Bound<PyDict>) -> Self {
        let variables = variables
            .into_iter()
            .map(|(key, any)| {
                let key = key.extract::<String>().unwrap();
                let var = match any.extract::<DiscreteVariableNamedElements>() {
                    Ok(var) => super::Variable::DiscreteVariableNamedElements(var),
                    Err(_) => {
                        let var = any.extract::<DiscreteVariableAnonymousElements>().unwrap();
                        super::Variable::DiscreteVariableAnonymousElements(var)
                    }
                };
                (key, var)
            })
            .collect();
        VFG {
            version: crate::loader::VFG_VERSION.to_string(),
            factors,
            variables,
        }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        VFG::default()
    }
}

#[pymethods]
impl Factor {
    #[new]
    #[pyo3(signature = (variables, distribution, role = None))]
    fn new(
        variables: Vec<VariableID>,
        distribution: ProbabilityDistribution,
        role: Option<FactorRole>,
    ) -> Self {
        let role = role.unwrap_or(FactorRole::NoRole);
        Factor {
            variables,
            distribution,
            values: Values::default(), // todo fix!!
            role,
        }
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    fn py_default() -> Self {
        Factor::default()
    }
}

#[pymethods]
impl DiscreteVariableNamedElements {
    #[new]
    #[pyo3(signature = (elements, role = None))]
    fn new(elements: Vec<String>, role: Option<VariableRole>) -> Self {
        let role = role.unwrap_or(VariableRole::NoRole);
        DiscreteVariableNamedElements { elements, role }
    }
}

#[pymethods]
impl DiscreteVariableAnonymousElements {
    #[new]
    #[pyo3(signature = (cardinality, role = None))]
    fn new(cardinality: u32, role: Option<VariableRole>) -> Self {
        let role = role.unwrap_or(VariableRole::NoRole);
        DiscreteVariableAnonymousElements { cardinality, role }
    }
}
