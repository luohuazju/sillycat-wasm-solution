
use anyhow::{bail, Context as _, Result};
use std::path::Path;
use wasmtime::{Engine, Extern, Instance, Linker, Module, Store, Val, ValType};
use wasmtime_wasi::{old::snapshot_0::Wasi as WasiSnapshot0, Wasi};

use crate::calculator::calculator::Calculator;

mod calculator;

fn main() {
    //wasmtime Config
    let config = wasmtime::Config::new();
    //wasmtime Engine
    let engine = Engine::new(&config);
    //wasmtime Store
    let store = Store::new(&engine);
    //all arguments from command line
    let args: Vec<String> = std::env::args().collect();
    //arg1 -- Path
    let path = args.get(1).unwrap();
    let path = Path::new(path);
    //arg2 -- FunctionName
    let func_name = args.get(2).unwrap();
    //wasmtime Module
    let module_registry = ModuleRegistry::new(&store).unwrap();

    //instance the wasm file with  path
    let instance = instantiate_module(&store, &module_registry, path).unwrap();
    
    //all other args 1 and 99
    let x = args[3..args.len()].to_vec();
    invoke_export(instance, func_name, x).unwrap()
}

/**
 * instanciate module
 */
fn instantiate_module(
    store: &Store,
    module_registry: &ModuleRegistry,
    path: &Path,
) -> Result<Instance> {
    let data = wat::parse_file(path)?;
    let module = Module::new(store, &data)?;
    let mut linker = Linker::new(store);

    for (_, item) in module.imports().enumerate() {
        match item.module() {
            "wasi_snapshot_preview1" => {
                linker.define(
                    "wasi_snapshot_preview1",
                    item.name(),
                    Extern::Func(
                        module_registry
                            .wasi_snapshot_preview1
                            .get_export(item.name())
                            .unwrap()
                            .clone(),
                    ),
                )?;
            }
            "wasi_unstable" => {
                linker.define(
                    "wasi_unstable",
                    item.name(),
                    Extern::Func(
                        module_registry
                            .wasi_unstable
                            .get_export(item.name())
                            .unwrap()
                            .clone(),
                    ),
                )?;
            }
            _ => {}
        }
    }

    linker.func("calculator", "add", |x: i32, y: i32| {
        let ctx = calculator::CalculatorCtx {};
        ctx.add(x, y).unwrap()
    })?;

    linker.instantiate(&module)
}

fn invoke_export(instance: Instance, name: &str, args: Vec<String>) -> Result<()> {
    let func = if let Some(export) = instance.get_export(name) {
        if let Some(func) = export.into_func() {
            func
        } else {
            bail!("export of `{}` wasn't a function", name)
        }
    } else {
        bail!("failed to find export of `{}` in module", name)
    };

    let mut values = Vec::new();
    //all args
    let mut x = args.iter();
    for ty in func.ty().params() {
        let val = match x.next() {
            Some(s) => s,
            None => bail!("exception"),
        };
        values.push(match ty {
            ValType::I32 => Val::I32(val.parse()?),
            ValType::I64 => Val::I64(val.parse()?),
            ValType::F32 => Val::F32(val.parse()?),
            ValType::F64 => Val::F64(val.parse()?),
            t => bail!("unsupported argument type {:?}", t),
        });
    }

    let results = func
        .call(&values)
        .with_context(|| format!("failed to invoke `{}`", name))?;

    for result in results.into_vec() {
        match result {
            Val::I32(i) => println!("{}", i),
            Val::I64(i) => println!("{}", i),
            Val::F32(f) => println!("{}", f),
            Val::F64(f) => println!("{}", f),
            Val::FuncRef(_) => println!("<funcref>"),
            Val::AnyRef(_) => println!("<anyref>"),
            Val::V128(i) => println!("{}", i),
        }
    }

    Ok(())
}

struct ModuleRegistry {
    wasi_snapshot_preview1: Wasi,
    wasi_unstable: WasiSnapshot0,
}

impl ModuleRegistry {
    fn new(store: &Store) -> Result<ModuleRegistry> {
        let cx1 = wasi_common::WasiCtxBuilder::new()
            .inherit_stdin()
            .inherit_stdout()
            .inherit_stderr()
            .build()?;
        let cx2 = wasi_common::old::snapshot_0::WasiCtxBuilder::new()
            .inherit_stdin()
            .inherit_stdout()
            .inherit_stderr()
            .build()?;

        Ok(ModuleRegistry {
            wasi_snapshot_preview1: Wasi::new(store, cx1),
            wasi_unstable: WasiSnapshot0::new(store, cx2),
        })
    }
}
