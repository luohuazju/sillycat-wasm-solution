Build and Run
```
cargo build

ls -l target/debug/     
total 59016
drwxr-xr-x   76 carl  staff      2432 Feb 22 21:28 build
drwxr-xr-x  621 carl  staff     19872 Feb 22 21:30 deps
drwxr-xr-x    2 carl  staff        64 Feb 22 21:12 examples
drwxr-xr-x    5 carl  staff       160 Feb 22 21:30 incremental
-rwxr-xr-x    1 carl  staff  30211928 Feb 22 21:30 wasi-impl
-rw-r--r--    1 carl  staff       219 Feb 22 21:30 wasi-impl.d

./target/debug/wasi-impl ../wasi-consumer-rust/target/wasm32-wasi/debug/wasi_consumer_rust.wasm consume_add 1 2
3

./target/debug/wasi-impl ../wasi-consumer-as/build/wasi-consumer-as.wasm consume_add 1 4
5

./target/debug/wasi-impl ../wasi-consumer-as/build/wasi-consumer-as.wat consume_add 1 4
5
```