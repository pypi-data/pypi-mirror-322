mod elo_system;

use pyo3::prelude::*;
use crate::elo_system::{EloSystem, GameResult};
use once_cell::sync::Lazy;
use std::sync::Mutex;
use pyo3::types::PyDict;
use pyo3::Py;

static GLOBAL_ELO_SYSTEM: Lazy<Mutex<EloSystem>> = Lazy::new(|| Mutex::new(EloSystem::new()));

#[pyfunction]
fn init_state() -> PyResult<()> {
    let mut sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    *sys = EloSystem::new();
    Ok(())
}

#[pyfunction]
fn add_player(id: &str) -> PyResult<()> {
    let mut sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    sys.add_player(id, Option::Some(false))
       .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
fn record_game(id1: &str, result: &str, id2: &str) -> PyResult<()> {
    let game_result = match result {
        "gt" | ">"  => GameResult::Player1Wins,
        "lt" | "<"  => GameResult::Player2Wins,
        "eq" | "==" => GameResult::Tie,
        _ => return Err(pyo3::exceptions::PyValueError::new_err("Invalid game result")),
    };
    let mut sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    sys.record_game(id1, game_result, id2, Option::Some(false))
       .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pyfunction]
fn get_info(id: &str, py: Python) -> PyResult<Py<PyDict>> {
    let sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    let player = sys.get_info(id)
        .ok_or_else(|| pyo3::exceptions::PyKeyError::new_err("Player not found"))?;

    let d = PyDict::new(py);
    d.set_item("id", player.0)?;
    d.set_item("elo", player.1)?;
    d.set_item("wins", player.2)?;
    d.set_item("losses", player.3)?;
    d.set_item("ties", player.4)?;
    Ok(d.into())
}

#[pyfunction]
#[pyo3(signature = (n=5))]
fn get_top_n(n: Option<usize>, py: Python) -> PyResult<Vec<Py<PyDict>>> {
    let sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    let top = sys.get_top_n(n);

    let mut result = Vec::with_capacity(top.len());
    for (id, elo, wins, losses, ties) in top {
        let d = PyDict::new(py);
        d.set_item("id", id)?;
        d.set_item("elo", elo)?;
        d.set_item("wins", wins)?;
        d.set_item("losses", losses)?;
        d.set_item("ties", ties)?;
        result.push(d.into());
    }
    Ok(result)
}

#[pyfunction]
#[pyo3(signature = (n=None))]
fn head(n: Option<usize>) {
    let sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    sys.print_top(n);
}

#[pyfunction]
fn print_info(id: &str) {
    let sys = GLOBAL_ELO_SYSTEM.lock().unwrap();
    sys.print_info(id);
}

#[pymodule]
fn belo(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init_state, m)?)?;
    m.add_function(wrap_pyfunction!(add_player, m)?)?;
    m.add_function(wrap_pyfunction!(record_game, m)?)?;
    m.add_function(wrap_pyfunction!(get_info, m)?)?;
    m.add_function(wrap_pyfunction!(get_top_n, m)?)?;
    m.add_function(wrap_pyfunction!(head, m)?)?;
    m.add_function(wrap_pyfunction!(print_info, m)?)?;
    Ok(())
}