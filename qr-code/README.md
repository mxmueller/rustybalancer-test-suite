# QR Code Generator Stress Test

This project contains a Rust-based stress test for a QR Code Generator web service. The test can simulate a high number of concurrent requests and measure the service's performance under load.

## Prerequisites

- Rust (latest stable version)
- Cargo (comes with Rust)

## Installation

1. Clone this repository or copy the `stress_test.rs` and `Cargo.toml` files into a new directory.

2. Open a terminal and navigate to the directory containing the project files.

3. Build the release version of the stress test:

   ```
   cargo build --release
   ```

   This step compiles the stress test with optimizations for better performance.

## Usage

To run the stress test, use the following command:

```
cargo run --release -- <base_url> <requests_per_second> <test_duration_seconds> <intensity>
```

Where:

- `<base_url>`: The base URL of your QR Code Generator service (e.g., http://localhost:8080)
- `<requests_per_second>`: The target number of requests per second
- `<test_duration_seconds>`: The duration of the test in seconds
- `<intensity>`: The length of the random string to be encoded in the QR code (use 0 for root path requests)

Example:

```
cargo run --release -- http://localhost:8080 100 60 10
```

This will run a test against `http://localhost:8080` with 100 requests per second for 60 seconds, using random strings of length 10 for QR code generation.

## Output

The test will print real-time statistics every second, including:

- Current request rate
- Total requests
- Successful requests
- Failed requests
- Elapsed time

At the end of the test, it will display a summary with the total number of requests, success rate, and average request rate.

## Notes

- Always use the `--release` flag when running the stress test to ensure optimized performance.
- Ensure your QR Code Generator service is running before starting the stress test.
- Adjust the test parameters to match your service's expected load and capacity.
- For intensive testing, consider running the test from a separate machine to avoid resource contention with the service being tested.

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are correctly installed (`cargo build --release`).
2. Check that the provided base URL is correct and the service is running.
3. If you get a "address already in use" error, try changing the port in your service or wait a few moments for the previous instance to fully close.

For any other issues, please check the Rust and dependency documentation or open an issue in this project's repository.