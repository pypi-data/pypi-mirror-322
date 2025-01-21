#![allow(clippy::unused_unit)]
use polars::prelude::*;
use geographiclib::Geodesic;
use pyo3_polars::derive::polars_expr;
use rayon::prelude::*;


#[polars_expr(output_type=Float64)]
fn distance(inputs: &[Series]) -> PolarsResult<Series> {
    let (ca_lat_a, ca_lng_a, ca_lat_b, ca_lng_b) = (inputs[0].f64()?, inputs[1].f64()?, inputs[2].f64()?, inputs[3].f64()?);

    let val_lat_a = to_values(ca_lat_a);
    let val_lng_a = to_values(ca_lng_a);
    let val_lat_b = to_values(ca_lat_b);
    let val_lng_b = to_values(ca_lng_b);

    let distances: Vec<Option<f64>> = (val_lat_a, val_lng_a, val_lat_b, val_lng_b).into_par_iter()
        .map(|(lat_a, lng_a, lat_b, lng_b)| geodesic_distance(*lat_a, *lng_a, *lat_b, *lng_b) )
        .collect();

    let chunked_distances: Float64Chunked = distances
        .into_par_iter()
        .map(|cell| cell)
        .collect();

     Ok(chunked_distances.into_series())

}

fn to_values(ca: &ChunkedArray<Float64Type>) -> &[f64] {
    ca.cont_slice().expect("No nulls expected")
}

fn geodesic_distance(lat_a: f64, lng_a: f64, lat_b: f64, lng_b: f64) -> Option<f64> {
    let g = Geodesic::wgs84();
    let (_d_deg, d_m, _az1, _az2) = g.inverse(lat_a, lng_a, lat_b, lng_b);

    return Some(d_m);
}
