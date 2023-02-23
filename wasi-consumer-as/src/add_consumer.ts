@external("calculator", "add")
declare function calculator_add(left: i32, right: i32): i32


function consume_add(left: i32, right: i32): i32 {
    return calculator_add(left, right);
}

export {
    consume_add
}