//! Test driver for the generated pure workspace root; one hex request per line.
use std::io::{self, BufRead};
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        assert_eq!(line.len() % 2, 0);
        let bytes = (0..line.len()).step_by(2)
            .map(|i| u8::from_str_radix(&line[i..i + 2], 16).unwrap()).collect();
        let result = prism_legal_matter::workspaceDispatch(bytes).unwrap();
        println!("{}", result.iter().map(|b| format!("{b:02x}")).collect::<String>());
    }
}
