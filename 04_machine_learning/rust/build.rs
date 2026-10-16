#![forbid(unsafe_code)]

use std::{env, process::Command};

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    for (name, key) in [
        ("ASSAY_BUILD_PROFILE", "PROFILE"),
        ("ASSAY_OPT_LEVEL", "OPT_LEVEL"),
        ("ASSAY_RUSTFLAGS", "CARGO_ENCODED_RUSTFLAGS"),
    ] {
        println!(
            "cargo:rustc-env={name}={}",
            env::var(key).unwrap_or_default()
        );
    }
    let output = Command::new(env::var_os("RUSTC").expect("Cargo supplies RUSTC"))
        .arg("--version")
        .output()
        .expect("Read compiler version");
    assert!(output.status.success(), "Compiler version command failed");
    let version = String::from_utf8(output.stdout).expect("UTF-8 compiler version");
    println!("cargo:rustc-env=ASSAY_RUSTC_VERSION={}", version.trim());
    println!(
        "cargo:rustc-env=ASSAY_BUILD_TARGET={}",
        env::var("TARGET").expect("Cargo supplies TARGET")
    );
}
