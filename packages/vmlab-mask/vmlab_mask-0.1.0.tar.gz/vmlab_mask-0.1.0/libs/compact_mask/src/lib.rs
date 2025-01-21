use image::GrayImage;
use ndarray::Array2;
use numpy::PyArray2;
use pyo3::{exceptions::PyValueError, prelude::*};
use pyo3::types::PyBytes;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct CompactMaskModel {
    pub data: Vec<Vec<(u16, u16)>>,
}

pub fn compact_mask(mask: &GrayImage) -> CompactMaskModel {
    let mut compact_data: Vec<Vec<(u16, u16)>> = Vec::new();

    for row in mask.rows() {
        let mut row_compact: Vec<(u16, u16)> = Vec::new();
        let mut previous_value: u8 = 0;

        for (index, pixel) in row.enumerate() {
            let value = pixel[0]; // Extract the grayscale value (Luma<u8>)
            if value != previous_value {
                row_compact.push((index as u16, value as u16));
                previous_value = value;
            }
        }

        compact_data.push(row_compact);
    }

    CompactMaskModel { data: compact_data }
}

pub fn reconstruct_ndarray(
    compact_model: &CompactMaskModel,
    width: usize,
    height: usize,
) -> Array2<u8> {
    let mut result = Array2::<u8>::zeros((height, width));

    // Correct below code
    for (row_index, row_data) in compact_model.data.iter().enumerate() {
        let mut col_start = 0;
        for &(col_index, value) in row_data {
            for col in col_start..(col_index as usize) {
                result[(row_index, col)] = result[(row_index, col_start.saturating_sub(1))];
            }
            result[(row_index, col_index as usize)] = value as u8;
            col_start = (col_index as usize) + 1;
        }

        // Fill remaining columns in the row
        if col_start < width {
            let fill_value = if col_start > 0 {
                result[(row_index, col_start - 1)]
            } else {
                0
            };
            for col in col_start..width {
                result[(row_index, col)] = fill_value;
            }
        }
    }

    result
}

#[pyfunction]
#[pyo3(signature = (bytes, width, height, scale=None))]
/// Reconstructs a grayscale mask from a serialized CompactMaskModel.
///
/// # Arguments
/// - `bytes` (`PyBytes`): The serialized CompactMaskModel.
/// - `width` (`usize`): The width of the output image.
/// - `height` (`usize`): The height of the output image.
/// - `scale` (`f32`): The height of the output image.
///
/// # Returns
/// A `numpy.ndarray` representing the reconstructed mask.
pub fn reconstruct_mask(
    bytes: &Bound<'_, PyBytes>,
    width: usize,
    height: usize,
    scale: Option<(f32, )>,
) -> PyResult<Py<PyArray2<f32>>> {

    let b = bytes.as_bytes();
    // decode the msgpack from b
    let Ok(compact_model) = rmp_serde::from_slice(b)
    else{
        return Err(PyErr::new::<PyValueError, _>("Failed to deserialize CompactMaskModel"));
    };

    // Logic to reconstruct the mask
    let result: Array2<u8> = reconstruct_ndarray(&compact_model, width, height);

    // resize using image crate the result if scale is provided and scale it not 1.0
    // and convert result type into f32
    if let Some((scale, )) = scale {
        //let result = image::imageops::resize(&image::ImageBuffer::from_raw(width as u32, height as u32, result.to_vec()).unwrap(), (scale * width as f32) as u32, (scale * height as f32) as u32, image::imageops::FilterType::Nearest);
        //let result = Array2::from_shape_vec((result.len() / width, width), result).unwrap();
        let (result, _) =  result.into_raw_vec_and_offset();

        let img = GrayImage::from_raw(width as u32, height as u32, result).unwrap();
        let resized = image::imageops::resize(
            &img,
            (scale * width as f32) as u32,
            (scale * height as f32) as u32,
            image::imageops::FilterType::Nearest,
        );

        // convert u8 into Array2<f32> result
        let resized_height = resized.height() as usize;
        let resized_width = resized.width() as usize;
        let result: Array2<f32> = Array2::from_shape_vec(
            (resized_height, resized_width),
            resized
                .pixels()
                .map(|p| p[0] as f32 / 255.0)
                .collect()
        ).unwrap();

        return Ok(Python::with_gil(|py| PyArray2::from_owned_array(py, result).into()));
    }

    // Convert u8 into f32
    let result: Array2<f32> = result.mapv(|x| x as f32 / 255.0);
    Ok(Python::with_gil(|py| PyArray2::from_owned_array(py, result).into()))
}

#[pymodule(name = "vmlab_mask")]
fn vm_compact_mask(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reconstruct_mask, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use image::GrayImage;
    use ndarray::Array2;

    #[test]
    fn test_compact_mask() {
        let mask = GrayImage::from_raw(3, 3, vec![0, 0, 0, 0, 255, 255, 255, 255, 255]).unwrap();
        let compact_model = compact_mask(&mask);

        assert_eq!(compact_model.data[0], vec![]);
        assert_eq!(compact_model.data[1], vec![(1, 255)]);
        assert_eq!(compact_model.data[2], vec![(0, 255)]);
    }

    #[test]
    fn test_reconstruct_ndarray() {
        let width = 4;
        let height = 4;
        let compact_model = CompactMaskModel {
            data: vec![
                vec![(0, 255), (1, 0), (2, 225)],
                vec![(1, 255), (3, 0)],
                vec![(2, 255)],
                vec![],
            ],
        };
        let result = reconstruct_ndarray(&compact_model, width, height);
        let expected = Array2::from_shape_vec(
            (height, width),
            vec![
                255u8, 0, 225, 225, 0, 255, 255, 0, 0, 0, 255, 255, 0, 0, 0, 0,
            ],
        )
        .unwrap();

        assert_eq!(result, expected);
    }
}
