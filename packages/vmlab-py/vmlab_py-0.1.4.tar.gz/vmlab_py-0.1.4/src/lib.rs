mod audio;
mod compact_mask;

use audio::{PreAudio2ExpTrait, PreAudio2ExpV1, MINIMUM_MEL_V1};
use compact_mask::reconstruct_ndarray;
use image::GrayImage;
use ndarray::{Array1, Array2};
use numpy::{PyArray1, PyArray2, PyArrayMethods};
use pyo3::types::PyBytes;
use pyo3::{exceptions::PyValueError, prelude::*};

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
    scale: Option<(f32,)>,
) -> PyResult<Py<PyArray2<f32>>> {
    let b = bytes.as_bytes();
    // decode the msgpack from b
    let Ok(compact_model) = rmp_serde::from_slice(b) else {
        return Err(PyErr::new::<PyValueError, _>(
            "Failed to deserialize CompactMaskModel",
        ));
    };

    // Logic to reconstruct the mask
    let result: Array2<u8> = reconstruct_ndarray(&compact_model, width, height);

    // resize using image crate the result if scale is provided and scale it not 1.0
    // and convert result type into f32
    if let Some((scale,)) = scale {
        //let result = image::imageops::resize(&image::ImageBuffer::from_raw(width as u32, height as u32, result.to_vec()).unwrap(), (scale * width as f32) as u32, (scale * height as f32) as u32, image::imageops::FilterType::Nearest);
        //let result = Array2::from_shape_vec((result.len() / width, width), result).unwrap();
        let (result, _) = result.into_raw_vec_and_offset();

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
            resized.pixels().map(|p| p[0] as f32 / 255.0).collect(),
        )
        .unwrap();

        return Ok(Python::with_gil(|py| {
            PyArray2::from_owned_array(py, result).into()
        }));
    }

    // Convert u8 into f32
    let result: Array2<f32> = result.mapv(|x| x as f32 / 255.0);
    Ok(Python::with_gil(|py| {
        PyArray2::from_owned_array(py, result).into()
    }))
}

#[pyfunction]
pub fn dummy_func(
    py: Python,
)->PyResult<u32>{
    Ok(0)
}

#[pyfunction]
pub fn a2ev1_melspectrogram(
    py: Python,
    wav: &Bound<'_, PyAny>,
    sample_rate: u32,
) -> PyResult<Vec<Py<PyBytes>>> {
    // Convert input numpy array to ndarray Array1<f32>

    let wav  = wav
        .downcast::<PyArray1<f32>>()
        .map_err(|_| pyo3::exceptions::PyTypeError::new_err("Expected a NumPy ndarray of type float32"))?;

    let wav = wav.readonly().as_array().to_owned();
    

    // Resample wav to 16000 Hz if the sample rate is 44100 Hz
    let resampled_wav = if sample_rate == 44100 {
        let ratio = 16000.0 / 44100.0;
        let new_len = (wav.len() as f32 * ratio).round() as usize;
        let mut resampled = Array1::zeros(new_len);

        // Nearest neighbor resampling
        for (i, value) in resampled.iter_mut().enumerate() {
            let nearest_index = ((i as f32 / ratio).round() as usize).min(wav.len() - 1);
            *value = wav[nearest_index];
        }
        resampled
    } else {
        wav
    };

    let audio: Vec<f32> = resampled_wav.to_vec();
    let result = PreAudio2ExpV1::new()
        .transform(audio.clone())
        .to_preprocessed_bytes(MINIMUM_MEL_V1)
        .unwrap().into_iter().map(|chunk| {
            let bytes = bytemuck::cast_slice(chunk.as_slice()); // Convert chunk to bytes
            PyBytes::new(py, bytes).into() // Convert to PyBytes and store in Vec
        })
        .collect();


    // Return as tuple
    Ok(result)
}

#[pymodule(name = "vmlab_py")]
fn vmlab_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(dummy_func, m)?)?;
    m.add_function(wrap_pyfunction!(reconstruct_mask, m)?)?;
    m.add_function(wrap_pyfunction!(a2ev1_melspectrogram, m)?)?;
    Ok(())
}
