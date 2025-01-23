use chrono::{DateTime, Utc};
use nzb_rs::{File as RustFile, Meta as RustMeta, Segment as RustSegment, NZB as RustNZB};
use pyo3::create_exception;
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use std::fmt;
use std::fmt::Formatter;
use std::path::PathBuf;
use std::{fmt::Debug, fs};

create_exception!(rnzb, InvalidNzbError, pyo3::exceptions::PyException);

// Wrapper around a Vec<T> to implement IntoPyObject for Python tuple.
#[derive(Clone, PartialEq, Eq, Hash)]
struct Tuple<T>(Vec<T>);

impl<'py, T: IntoPyObject<'py>> IntoPyObject<'py> for Tuple<T> {
    type Target = PyTuple;
    type Output = Bound<'py, Self::Target>;
    type Error = std::convert::Infallible;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        Ok(PyTuple::new(py, self.0).unwrap())
    }
}

// Format the tuple as a Python tuple.
impl<T: Debug> Debug for Tuple<T> {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        // Handle empty tuple
        if self.0.is_empty() {
            return write!(f, "()");
        }

        // Handle single element tuple (with trailing comma)
        if self.0.len() == 1 {
            return write!(f, "({:?},)", self.0[0]);
        }

        // Handle multiple elements
        write!(
            f,
            "({})",
            self.0.iter().map(|x| format!("{:?}", x)).collect::<Vec<_>>().join(", ")
        )
    }
}

// Python wrapper class for RustSegment
#[pyclass(frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash)]
struct Segment {
    #[pyo3(get)]
    size: u32,
    #[pyo3(get)]
    number: u32,
    #[pyo3(get)]
    message_id: String,
}

// Implement conversion from RustSegment to Segment
impl From<RustSegment> for Segment {
    fn from(s: RustSegment) -> Self {
        Self {
            size: s.size,
            number: s.number,
            message_id: s.message_id.clone(),
        }
    }
}

#[pymethods]
impl Segment {
    fn __repr__(&self) -> String {
        format!(
            "Segment(size={}, number={}, message_id={:?})",
            self.size, self.number, self.message_id
        )
    }
}

// Python wrapper class for Meta
#[pyclass(frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash)]
struct Meta {
    #[pyo3(get)]
    title: Option<String>,
    #[pyo3(get)]
    passwords: Tuple<String>,
    #[pyo3(get)]
    tags: Tuple<String>,
    #[pyo3(get)]
    category: Option<String>,
}

// Implement conversion from RustMeta to Meta
impl From<RustMeta> for Meta {
    fn from(m: RustMeta) -> Self {
        Self {
            title: m.title.clone(),
            passwords: Tuple(m.passwords.clone()),
            tags: Tuple(m.tags.clone()),
            category: m.category.clone(),
        }
    }
}

#[pymethods]
impl Meta {
    fn __repr__(&self) -> String {
        format!(
            "Meta(title={}, passwords={:?}, tags={:?}, category={})",
            self.title.as_ref().map_or("None".to_string(), |t| format!("{:?}", t)),
            self.passwords,
            self.tags,
            self.category
                .as_ref()
                .map_or("None".to_string(), |t| format!("{:?}", t))
        )
    }
}

// Python wrapper class for File
#[pyclass(frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash)]
struct File {
    #[pyo3(get)]
    poster: String,
    #[pyo3(get)]
    datetime: DateTime<Utc>,
    #[pyo3(get)]
    subject: String,
    #[pyo3(get)]
    groups: Tuple<String>,
    #[pyo3(get)]
    segments: Tuple<Segment>,
    inner: RustFile,
}

// Implement conversion from RustFile to File
impl From<RustFile> for File {
    fn from(f: RustFile) -> Self {
        Self {
            poster: f.poster.clone(),
            datetime: f.datetime,
            subject: f.subject.clone(),
            groups: Tuple(f.groups.clone()),
            segments: Tuple(f.segments.clone().into_iter().map(Into::into).collect()),
            inner: f,
        }
    }
}

#[pymethods]
impl File {
    fn __repr__(&self) -> String {
        format!(
            "File(poster={:?}, datetime={:?}, subject={:?}, groups={:?}, segments={})",
            self.poster,
            self.datetime.to_rfc3339(),
            self.subject,
            self.groups,
            self.segments
                .0
                .iter()
                .map(|s| s.__repr__())
                .collect::<Vec<String>>()
                .join(", "),
        )
    }

    // Size of the file calculated from the sum of segment sizes.
    #[getter]
    fn size(&self) -> u64 {
        self.inner.size()
    }

    // Complete name of the file with it's extension extracted from the subject.
    // May return [`None`] if it fails to extract the name.
    #[getter]
    fn name(&self) -> Option<&str> {
        self.inner.name()
    }

    // Base name of the file without it's extension extracted from the [`File::name`].
    // May return [`None`] if it fails to extract the stem.
    #[getter]
    fn stem(&self) -> Option<&str> {
        self.inner.stem()
    }

    //  Extension of the file extracted from the [`File::name`].
    // May return [`None`] if it fails to extract the extension.
    #[getter]
    fn extension(&self) -> Option<&str> {
        self.inner.extension()
    }

    // Return [`true`] if the file is a `.par2` file, [`false`] otherwise.
    fn is_par2(&self) -> bool {
        self.inner.is_par2()
    }

    // Return [`true`] if the file is a `.rar` file, [`false`] otherwise.
    fn is_rar(&self) -> bool {
        self.inner.is_rar()
    }

    // Return [`true`] if the file is obfuscated, [`false`] otherwise.
    fn is_obfuscated(&self) -> bool {
        self.inner.is_obfuscated()
    }
}

// Python wrapper class for NZB
#[pyclass(frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash)]
struct Nzb {
    #[pyo3(get)]
    meta: Meta,
    #[pyo3(get)]
    files: Tuple<File>,
    inner: RustNZB,
}

// Implement conversion from RustNZB to NZB
#[pymethods]
impl Nzb {
    fn __repr__(&self) -> String {
        format!(
            "NZB(meta={}, files={})",
            self.meta.__repr__(),
            self.files
                .0
                .iter()
                .map(|s| s.__repr__())
                .collect::<Vec<String>>()
                .join(", "),
        )
    }

    #[getter]
    fn file(&self) -> File {
        // self.files is guranteed to have atleast one file, so we can safely unwrap().
        File::from(self.inner.file().clone())
    }

    // Total size of all the files in the NZB.
    #[getter]
    fn size(&self) -> u64 {
        self.inner.size()
    }

    // Vector of unique file names across all the files in the NZB.
    #[getter]
    fn filenames(&self) -> Tuple<&str> {
        Tuple(self.inner.filenames())
    }

    // Vector of unique posters across all the files in the NZB.
    #[getter]
    fn posters(&self) -> Tuple<&str> {
        Tuple(self.inner.posters())
    }

    // Vector of unique groups across all the files in the NZB.
    #[getter]
    fn groups(&self) -> Tuple<&str> {
        Tuple(self.inner.groups())
    }

    // Total size of all the `.par2` files.
    #[getter]
    fn par2_size(&self) -> u64 {
        self.inner.par2_size()
    }

    // Percentage of the size of all the `.par2` files relative to the total size.
    #[getter]
    fn par2_percentage(&self) -> f64 {
        self.inner.par2_percentage()
    }

    // Return [`true`] if there's at least one `.par2` file in the NZB, [`false`] otherwise.
    fn has_par2(&self) -> bool {
        self.inner.has_par2()
    }

    // Return [`true`] if any file in the NZB is a `.rar` file, [`false`] otherwise.
    fn has_rar(&self) -> bool {
        self.inner.has_rar()
    }

    // Return [`true`] if every file in the NZB is a `.rar` file, [`false`] otherwise.
    fn is_rar(&self) -> bool {
        self.inner.is_rar()
    }

    // Return [`true`] if any file in the NZB is obfuscated, [`false`] otherwise.
    fn is_obfuscated(&self) -> bool {
        self.inner.is_obfuscated()
    }
}

#[pyfunction]
fn parse(nzb: &str) -> PyResult<Nzb> {
    match RustNZB::parse(nzb) {
        Ok(nzb) => {
            let meta = Meta::from(nzb.meta.clone());
            let files = Tuple(nzb.files.clone().into_iter().map(Into::into).collect());

            Ok(Nzb {
                meta,
                files,
                inner: nzb,
            })
        }
        Err(e) => Err(InvalidNzbError::new_err(e.message)),
    }
}

#[pyfunction]
fn parse_file(nzb: PathBuf) -> PyResult<Nzb> {
    let content = fs::read_to_string(nzb).map_err(|e| InvalidNzbError::new_err(e.to_string()))?;
    match RustNZB::parse(content.as_str()) {
        Ok(nzb) => {
            let meta = Meta::from(nzb.meta.clone());
            let files = Tuple(nzb.files.clone().into_iter().map(Into::into).collect());

            Ok(Nzb {
                meta,
                files,
                inner: nzb,
            })
        }
        Err(e) => Err(InvalidNzbError::new_err(e.message)),
    }
}

#[pymodule]
fn rnzb(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(parse_file, m)?)?;
    m.add_class::<Nzb>()?;
    m.add_class::<Meta>()?;
    m.add_class::<File>()?;
    m.add_class::<Segment>()?;
    m.add("InvalidNzbError", py.get_type::<InvalidNzbError>())?;
    Ok(())
}
