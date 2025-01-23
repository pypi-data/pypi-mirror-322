# rnzb

Python bindings to the [nzb-rs](https://github.com/ravencentric/nzb-rs) library - a [spec](https://sabnzbd.org/wiki/extra/nzb-spec) compliant parser for [NZB](https://en.wikipedia.org/wiki/NZB) files, written in Rust.

## Installation

### From PyPI (Recommended)

Pre-built wheels are available for Linux (glibc/musl), Windows and macOS, supporting CPython 3.9-3.13 and PyPy 3.9-3.10 (except Windows x86: CPython only).

```bash
pip install rnzb
```

### From Source

Building from source requires the [Rust toolchain](https://rustup.rs/) and [Python 3.9+](https://www.python.org/downloads/).
This project is managed by [uv](https://github.com/astral-sh/uv) so the instructions also use uv but you can use your tool of choice with slightly different commands.

```bash
git clone https://github.com/Ravencentric/rnzb
cd rnzb
uv sync
uv run maturin build --release
```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contributing

Contributions are welcome! Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.