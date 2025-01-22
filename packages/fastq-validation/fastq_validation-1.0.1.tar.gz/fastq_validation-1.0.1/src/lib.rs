use pyo3::prelude::*;
use std::{
    collections::HashMap,
    ffi::OsStr,
    fs::File,
    io::{BufRead, BufReader, BufWriter, Read, Write},
    path::Path,
};

use flate2::read::MultiGzDecoder;

const MAX_FILE_SIZE: u64 = 107374182400; // 100GB
const MAX_LINE_LENGTH: usize = 10485760; // 10MB

/// Given a string of a float, trim trailling `0` chars
/// Stolen from `grumpy`
///
/// # Arguments
/// - `float_string` - String representation of a float
///
/// # Returns
/// - Trimmed string
fn trim_float_string(mut float_string: String) -> String {
    while float_string.ends_with('0') {
        float_string.pop();
        if float_string.ends_with("1.0") {
            // Keep trailing 0 for 1.0
            return float_string;
        }
    }

    float_string
}

#[pyclass]
#[derive(Debug)]
/// Struct to hold data about a fastq file
pub struct FastqStats {
    #[pyo3(get, set)]
    /// Number of reads in the fastq
    pub num_reads: u64,

    #[pyo3(get, set)]
    /// Mean length of a read in the fastq
    pub mean_read_length: f64,

    #[pyo3(get, set)]
    /// Percentage of reads with the same length
    pub percentage_same_length: f64,
}

#[pymethods]
impl FastqStats {
    /// Check if the fastq has ONT read characteristics
    /// Requires that mean read length > 350 and percentage of reads with the same length < 0.9
    fn is_ont(&self) -> bool {
        self.mean_read_length > 350.0 && self.percentage_same_length < 0.9
    }

    /// Check if the fastq has Illumina read characteristics
    /// Requires that mean read length is between 50 and 350 and percentage of reads with the same length > 0.9
    fn is_illumina(&self) -> bool {
        self.mean_read_length > 50.0
            && self.mean_read_length < 350.0
            && self.percentage_same_length > 0.9
    }
}

/// Read normal or compressed files seamlessly
/// Uses the presence of a `gz` extension to choose between the two
/// https://users.rust-lang.org/t/write-to-normal-or-gzip-file-transparently/35561
///
/// # Arguments
/// - `filename` - Path to the file
///
/// # Returns
/// - BufRead object to read the file
pub fn get_reader(filename: &str) -> Box<dyn BufRead> {
    let path = Path::new(filename);
    let file = match File::open(path) {
        Err(why) => panic!("couldn't open {}: {}", path.display(), why),
        Ok(file) => file,
    };

    if path.extension() == Some(OsStr::new("gz")) {
        Box::new(BufReader::with_capacity(
            128 * 1024,
            MultiGzDecoder::new(file),
        ))
    } else {
        Box::new(BufReader::with_capacity(128 * 1024, file))
    }
}

#[pyfunction]
/// Given a filepath, determine if the file is gzipped or not.
/// If gzipped, read it with a maximum decompressed file size of 10GB
///
/// # Arguments
/// - `filepath` - Path to the fastq
///
/// # Returns
/// - FastqStats struct containing the number of reads, mean read length, and percentage of reads with the same length
///
/// # Panics
/// - If the file is invalid FASTQ or shows signs of a zip bomb
fn safe_parse_fastq(filepath: &str) -> FastqStats {
    let mut reader = get_reader(filepath);
    let mut file_size: u64 = 0;

    let mut seq = String::new();

    let mut num_reads: u64 = 0;
    let mut total_read_length: u64 = 0;
    let mut line_idx = 0;
    let mut length_counter: HashMap<usize, u64> = HashMap::new();

    let mut line = String::new();
    let mut buf = vec![0u8; MAX_LINE_LENGTH];
    let mut file_empty = false;
    while !file_empty {
        let res = reader.read_exact(&mut buf);
        if res.is_err() {
            // Read exact returns error if EOF exists in buffer
            // So let the loop finish and check if the line is empty
            // Catches last chunk of file
            file_empty = true;
        }
        let mut matched_line = false;
        for byte in buf.iter() {
            if *byte == b'\0' {
                file_empty = true;
                matched_line = true;
                break;
            }
            if *byte == b'\n' {
                // End of line, so process and continue
                matched_line = true;
                // Skip empty lines
                if line.is_empty() {
                    continue;
                }

                file_size += line.len() as u64;
                if file_size > MAX_FILE_SIZE {
                    panic!("File {:} exceeds 100GB decompressed limit!", filepath);
                }
                match line_idx % 4 {
                    0 => {
                        if !line.starts_with('@') {
                            panic!(
                                "1 Invalid header line {:} in {:}\n{:}",
                                line_idx, filepath, line
                            );
                        }
                    }
                    1 => {
                        seq = line.clone();
                        for c in seq.chars() {
                            if c != 'A' && c != 'C' && c != 'G' && c != 'T' && c != 'N' {
                                panic!(
                                    "Invalid sequence line {:} in {:} with character {:}",
                                    line_idx, filepath, c
                                );
                            }
                        }
                        total_read_length += line.len() as u64;
                        num_reads += 1;

                        if let std::collections::hash_map::Entry::Vacant(e) =
                            length_counter.entry(line.len())
                        {
                            e.insert(1);
                        } else {
                            *length_counter.get_mut(&line.len()).unwrap() += 1;
                        }
                    }
                    2 => {
                        if !line.starts_with('+') {
                            panic!("Invalid field 3 on line {:} in {:}", line_idx, filepath);
                        }
                    }
                    3 => {
                        if line.len() != seq.len() {
                            panic!(
                                "Quality line {:} does not match sequence line {:} in {:}",
                                line_idx,
                                line_idx - 1,
                                filepath
                            );
                        }
                        for c in line.chars() {
                            if !('!'..='~').contains(&c) {
                                panic!(
                                    "Invalid quality line {:} in {:} with character {:}",
                                    line_idx, filepath, c
                                );
                            }
                        }
                    }
                    _ => panic!("Invalid line index!"),
                }
                line_idx += 1;
                line = String::new();
            } else if *byte != b'\r' {
                line.push(*byte as char);
            }
        }
        if !matched_line {
            panic!(
                "Line number {:} of {:} exceeds 10MB limit!",
                line_idx, filepath
            );
        }
        // Ensure that we start from a clean buffer each time we read
        buf.fill(0);
    }

    let most_common_read_length = length_counter.iter().max_by_key(|x| x.1).unwrap().0;
    let percentage_same_length =
        *length_counter.get(most_common_read_length).unwrap() as f64 / num_reads as f64;

    FastqStats {
        num_reads,
        mean_read_length: (total_read_length / num_reads) as f64,
        percentage_same_length,
    }
}

#[pyfunction]
#[pyo3(signature = (reads1, reads2, output=None))]
/// Given two fastq files, determine if they are Illumina reads
///
/// # Arguments
/// - `reads1` - Path to the first fastq
/// - `reads2` - Path to the second fastq
/// - `output` - Path to write the output JSON
///
/// # Returns
/// - Tuple of FastqStats structs containing the number of reads, mean read length, and percentage of reads with the same length
pub fn check_illumina(
    reads1: String,
    reads2: String,
    output: Option<String>,
) -> (FastqStats, FastqStats) {
    let stats1 = safe_parse_fastq(&reads1);
    let stats2 = safe_parse_fastq(&reads2);

    if let Some(output) = output {
        let reads_match = stats1.num_reads == stats2.num_reads;

        let reads1 = reads1.split("/").last().unwrap().to_string();
        let reads2 = reads2.split("/").last().unwrap().to_string();
        let to_write = [
            "{\n".to_string(),
            format!("\t\"{}\": {{\n", reads1),
            format!("\t\t\"num_reads\": {},\n", stats1.num_reads),
            format!("\t\t\"mean_read_length\": {},\n", stats1.mean_read_length),
            format!(
                "\t\t\"percentage_same_length\": {}\n",
                trim_float_string(stats1.percentage_same_length.to_string())
            ),
            "\t},\n".to_string(),
            format!("\t\"{}\": {{\n", reads2),
            format!("\t\t\"num_reads\": {},\n", stats2.num_reads),
            format!("\t\t\"mean_read_length\": {},\n", stats2.mean_read_length),
            format!(
                "\t\t\"percentage_same_length\": {}\n",
                trim_float_string(stats2.percentage_same_length.to_string())
            ),
            "\t},\n".to_string(),
            "\t\"Illumina\": {\n".to_string(),
            format!("\t\t\"Number of reads match\": {},\n", reads_match),
            format!(
                "\t\t\"{} is Illumina\": {},\n",
                reads1,
                stats1.is_illumina()
            ),
            format!("\t\t\"{} is Illumina\": {}\n", reads2, stats2.is_illumina()),
            "\t}\n".to_string(),
            "}".to_string(),
        ];

        let mut writer = BufWriter::new(File::create(output).unwrap());
        writer.write_all(to_write.join("").as_bytes()).unwrap();
        writer.flush().unwrap();
    }

    (stats1, stats2)
}

#[pyfunction]
#[pyo3(signature = (reads, output=None))]
/// Given a fastq file, determine if it is ONT reads
///
/// # Arguments
/// - `reads` - Path to the fastq
/// - `output` - Path to write the output JSON
///
/// # Returns
/// - FastqStats struct containing the number of reads, mean read length, and percentage of reads with the same length
pub fn check_ont(reads: String, output: Option<String>) -> FastqStats {
    let stats = safe_parse_fastq(&reads);

    if let Some(output) = output {
        let reads = reads.split("/").last().unwrap().to_string();
        let to_write = [
            "{\n".to_string(),
            format!("\t\"{}\": {{\n", reads),
            format!("\t\t\"num_reads\": {},\n", stats.num_reads),
            format!("\t\t\"mean_read_length\": {},\n", stats.mean_read_length),
            format!(
                "\t\t\"percentage_same_length\": {}\n",
                trim_float_string(stats.percentage_same_length.to_string())
            ),
            "\t},\n".to_string(),
            "\t\"ONT\": {\n".to_string(),
            format!("\t\t\"{} is ONT\": {}\n", reads, stats.is_ont()),
            "\t}\n".to_string(),
            "}".to_string(),
        ];

        let mut writer = BufWriter::new(File::create(output).unwrap());
        writer.write_all(to_write.join("").as_bytes()).unwrap();
        writer.flush().unwrap();
    }

    stats
}

#[pymodule]
/// Module to check if a fastq file is Illumina or ONT
fn fastq_validation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FastqStats>()?;

    m.add_function(wrap_pyfunction!(check_illumina, m)?)?;
    m.add_function(wrap_pyfunction!(check_ont, m)?)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    macro_rules! assert_panics {
        ($expression:expr) => {
            let result = std::panic::catch_unwind(|| $expression);
            assert!(result.is_err());
        };
    }

    #[test]
    fn test_single_line_zip_bomb() {
        // 20GB of 0s decompressed (20MB compressed)
        // But all on 1 line (so fails on single line limit)
        // if multi line, would need to be valid FASTQ

        // Technically not a proper zip bomb (as just a large valid zip file)
        // but the premise is the same
        assert_panics!(safe_parse_fastq("test_data/bomb.fastq.gz"));
    }

    #[test]
    fn test_fastq_format_checks() {
        // Non-gzipped invalid fastq should fail
        assert_panics!(safe_parse_fastq("test_data/not_fastq.fastq"));

        // Non-gzipped valid fastq should be fine
        safe_parse_fastq("test_data/basic_illumina_1.fastq");

        // Gzipped but non-fastq data should fail
        assert_panics!(safe_parse_fastq("test_data/not_fastq.fastq.gz"));

        // Invalid FASTQ data should fail
        assert_panics!(safe_parse_fastq("test_data/bad_header.fastq.gz"));
        assert_panics!(safe_parse_fastq("test_data/bad_seq.fastq.gz"));
        assert_panics!(safe_parse_fastq("test_data/bad_plus.fastq.gz"));
        assert_panics!(safe_parse_fastq("test_data/bad_qual.fastq.gz"));
        assert_panics!(safe_parse_fastq("test_data/bad_qual2.fastq.gz"));
    }

    #[test]
    fn test_valid_illumina() {
        let (stats1, stats2) = check_illumina(
            "test_data/basic_illumina_1.fastq.gz".to_string(),
            "test_data/basic_illumina_2.fastq.gz".to_string(),
            None,
        );

        assert_eq!(stats1.num_reads, 5);
        assert_eq!(stats1.mean_read_length, 151.0);
        assert_eq!(stats1.percentage_same_length, 1.0);

        assert_eq!(stats2.num_reads, 5);
        assert_eq!(stats2.mean_read_length, 151.0);
        assert_eq!(stats2.percentage_same_length, 1.0);
    }

    #[test]
    fn test_valid_decompressed_illumina() {
        let (stats1, stats2) = check_illumina(
            "test_data/basic_illumina_1.fastq".to_string(),
            "test_data/basic_illumina_2.fastq".to_string(),
            None,
        );

        assert_eq!(stats1.num_reads, 5);
        assert_eq!(stats1.mean_read_length, 151.0);
        assert_eq!(stats1.percentage_same_length, 1.0);

        assert_eq!(stats2.num_reads, 5);
        assert_eq!(stats2.mean_read_length, 151.0);
        assert_eq!(stats2.percentage_same_length, 1.0);
    }

    #[test]
    fn test_valid_ont() {
        let stats = check_ont("test_data/basic_ont.fastq.gz".to_string(), None);

        assert_eq!(stats.num_reads, 5);
        assert_eq!(stats.mean_read_length, 5177.0);
        assert_eq!(stats.percentage_same_length, 0.2);
    }

    #[test]
    fn test_invalid_ont() {
        let stats = check_ont("test_data/basic_illumina_1.fastq.gz".to_string(), None);

        assert_eq!(stats.num_reads, 5);
        assert_eq!(stats.mean_read_length, 151.0);
        assert_eq!(stats.percentage_same_length, 1.0);
        assert!(!stats.is_ont());
        assert!(stats.is_illumina());
    }

    #[test]
    fn test_invalid_illumina() {
        let (stats1, stats2) = check_illumina(
            "test_data/basic_ont.fastq.gz".to_string(),
            "test_data/basic_illumina_2.fastq.gz".to_string(),
            None,
        );

        assert_eq!(stats1.num_reads, 5);
        assert_eq!(stats1.mean_read_length, 5177.0);
        assert_eq!(stats1.percentage_same_length, 0.2);
        assert!(!stats1.is_illumina());
        assert!(stats1.is_ont());

        assert_eq!(stats2.num_reads, 5);
        assert_eq!(stats2.mean_read_length, 151.0);
        assert_eq!(stats2.percentage_same_length, 1.0);
        assert!(stats2.is_illumina());
        assert!(!stats2.is_ont());
    }

    #[test]
    fn test_valid_illumina_with_output() {
        let (stats1, stats2) = check_illumina(
            "test_data/basic_illumina_1.fastq.gz".to_string(),
            "test_data/basic_illumina_2.fastq.gz".to_string(),
            Some("test_data/actual/basic_illumina_output.json".to_string()),
        );

        assert_eq!(stats1.num_reads, 5);
        assert_eq!(stats1.mean_read_length, 151.0);
        assert_eq!(stats1.percentage_same_length, 1.0);
        assert!(stats1.is_illumina());
        assert!(!stats1.is_ont());

        assert_eq!(stats2.num_reads, 5);
        assert_eq!(stats2.mean_read_length, 151.0);
        assert_eq!(stats2.percentage_same_length, 1.0);
        assert!(stats2.is_illumina());
        assert!(!stats2.is_ont());

        let mut expected_buf = Vec::new();
        let _ = File::open("test_data/expected/basic_illumina_output.json")
            .unwrap()
            .read_to_end(&mut expected_buf);

        let mut actual_buf = Vec::new();
        let _ = File::open("test_data/actual/basic_illumina_output.json")
            .unwrap()
            .read_to_end(&mut actual_buf);
        assert_eq!(expected_buf, actual_buf);
    }

    #[test]
    fn test_valid_ont_with_output() {
        let stats = check_ont(
            "test_data/basic_ont.fastq.gz".to_string(),
            Some("test_data/actual/basic_ont_output.json".to_string()),
        );

        assert_eq!(stats.num_reads, 5);
        assert_eq!(stats.mean_read_length, 5177.0);
        assert_eq!(stats.percentage_same_length, 0.2);
        assert!(stats.is_ont());
        assert!(!stats.is_illumina());

        let mut expected_buf = Vec::new();
        let _ = File::open("test_data/expected/basic_ont_output.json")
            .unwrap()
            .read_to_end(&mut expected_buf);

        let mut actual_buf = Vec::new();
        let _ = File::open("test_data/actual/basic_ont_output.json")
            .unwrap()
            .read_to_end(&mut actual_buf);
        assert_eq!(expected_buf, actual_buf);
    }
}
