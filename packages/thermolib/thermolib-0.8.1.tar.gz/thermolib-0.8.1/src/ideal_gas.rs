use crate::f64consts::{C, FRAC_H_K, R};
#[cfg(feature = "with_pyo3")]
use pyo3::{pyclass, pymethods};
#[cfg_attr(feature = "with_pyo3", pyclass)]
pub struct IdealGas {
    c: f64,
    v: Vec<f64>,
}
impl IdealGas {
    pub fn new_fluid() -> Self {
        Self {
            c: 1.5, // Translation contribution = 1.5
            v: Vec::new(),
        }
    }
}
#[cfg_attr(feature = "with_pyo3", pymethods)]
#[allow(non_snake_case)]
impl IdealGas {
    #[cfg(feature = "with_pyo3")]
    #[new]
    pub fn new_py() -> Self {
        Self::new_fluid()
    }
    pub fn set_linear_molecule(&mut self) {
        // Translation contribution = 1.5
        // Rotation contribution = 1.0
        self.c = 2.5;
    }
    pub fn set_nonlinear_molecule(&mut self) {
        // Translation contribution = 1.5
        // Rotation contribution = 1.5
        self.c = 3.0;
    }
    pub fn set_wave_length(&mut self, waves: Vec<f64>) {
        self.v = waves.iter().map(|wave| C * wave * 100.0).collect();
    }
    pub fn calc_cv(&self, T: f64) -> f64 {
        R * (self.c
            + self
                .v
                .iter()
                .map(|vi| {
                    let temp = -FRAC_H_K * vi / T;
                    temp.exp() * (temp / temp.exp_m1()).powi(2)
                })
                .sum::<f64>())
    }
    pub fn calc_cp(&self, T: f64) -> f64 {
        self.calc_cv(T) + R
    }
}
