use pyo3::{prelude::*, py_run};
use crate::Workflow;

#[pymodule]
fn functions(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_workflow, m)?)?;
    Ok(())
}

pub fn make_module(py: Python) -> PyResult<&PyModule> {
    let sub = PyModule::new(py, "functions")?;

    py_run!(py, sub, "import sys; sys.modules['flowrs.functions'] = sub");

    functions(py, sub)?;
    Ok(sub)
}

/*  --------------------- Module Implementation --------------------- */

#[pyfunction]
fn create_workflow(name: String) -> PyResult<Workflow> {
    Ok(Workflow::new(name)?)
}
