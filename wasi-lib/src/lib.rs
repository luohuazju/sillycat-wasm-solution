wiggle::from_witx!({
    witx: ["../wasi-interface/calculator.witx"],
    ctx: CalculatorCtx,
});

pub struct CalculatorCtx {}

impl calculator::Calculator for CalculatorCtx {
    fn add(&self, lh: i32, rh: i32) -> Result<i32, types::Errno> {
        //this is the implementation of the witx trait from wiggle
        Ok(lh + rh)
    }
}

impl wiggle::GuestErrorType for types::Errno {
    fn success() -> Self {
        unimplemented!()
    }
}

impl types::GuestErrorConversion for CalculatorCtx {
    fn into_errno(&self, _e: wiggle::GuestError) -> types::Errno {
        unimplemented!()
    }
}
