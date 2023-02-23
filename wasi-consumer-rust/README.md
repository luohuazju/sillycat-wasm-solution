
```
cargo install -f cargo-wasi
cargo wasi build

ls -l target/wasm32-wasi/debug
total 11648
drwxr-xr-x  2 carl  staff       64 Feb 22 21:20 build
drwxr-xr-x  4 carl  staff      128 Feb 22 21:20 deps
drwxr-xr-x  2 carl  staff       64 Feb 22 21:20 examples
drwxr-xr-x  3 carl  staff       96 Feb 22 21:20 incremental
-rw-r--r--  1 carl  staff      174 Feb 22 21:20 wasi_consumer_rust.d
-rwxr-xr-x  1 carl  staff  1986497 Feb 22 21:20 wasi_consumer_rust.rustc.wasm
-rw-r--r--  2 carl  staff  1986521 Feb 22 21:20 wasi_consumer_rust.wasi.wasm
-rw-r--r--  2 carl  staff  1986521 Feb 22 21:20 wasi_consumer_rust.wasm
```