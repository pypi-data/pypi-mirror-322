use clap::Parser;
use fastq_validation::{check_illumina, check_ont};

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Path to the first read file
    #[arg(long)]
    reads1: String,

    /// Path to the second read file
    #[arg(long, default_value = "")]
    reads2: String,

    #[arg(long, default_value=None)]
    output: Option<String>,
}

fn main() {
    let args = Args::parse();

    if args.reads2.is_empty() {
        check_ont(args.reads1, args.output);
    } else {
        check_illumina(args.reads1, args.reads2, args.output);
    }
}
