from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
from typing import List, Dict, Generator, Tuple, Set
import logging
from collections import Counter, defaultdict
import shutil
import click

import pysam
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner
from rich.progress import track

logger = logging.getLogger(__name__)

@dataclass
class AmpliconRead:
    """Represents a processed amplicon read pair."""
    sequence: str
    mutations: int
    quality: float

class AmpliconProcessor:
    def __init__(self, 
                 reference_path: Path,
                 min_base_quality: int = 20,
                 min_mapping_quality: int = 30,
                 max_file_size: int = 10_000_000_000):  # 10GB default
        """Initialize the processor with reference genome and quality parameters."""
        self.reference_path = Path(reference_path)
        self.min_base_quality = min_base_quality
        self.min_mapping_quality = min_mapping_quality
        self.max_file_size = max_file_size
        self.reference = self._load_reference()
        
        # Initialize aligner for indel detection
        self.aligner = PairwiseAligner()
        self.aligner.mode = 'global'
        self.aligner.match_score = 2
        self.aligner.mismatch_score = -1
        self.aligner.open_gap_score = -2
        self.aligner.extend_gap_score = -0.5
        
        # Check for required executables and index files
        self._check_dependencies()
        self._check_and_create_bwa_index()

    def _load_reference(self) -> Dict[str, str]:
        """Load reference sequences."""
        try:
            reference_dict = {}
            with open(self.reference_path) as handle:
                for record in SeqIO.parse(handle, "fasta"):
                    reference_dict[record.id] = str(record.seq)
            if not reference_dict:
                raise ValueError(f"No sequences found in reference file: {self.reference_path}")
            return reference_dict
        except Exception as e:
            logger.error(f"Error loading reference sequence: {str(e)}")
            raise

    def _check_dependencies(self):
        """Check if required external programs are available."""
        for cmd in ['bwa', 'samtools']:
            if not shutil.which(cmd):
                raise RuntimeError(f"{cmd} not found in PATH. Please install {cmd}.")

    def _check_and_create_bwa_index(self):
        """Check if BWA index files exist, create them if they don't."""
        index_extensions = ['.amb', '.ann', '.bwt', '.pac', '.sa']
        missing_indices = [ext for ext in index_extensions 
                         if not (self.reference_path.parent / f"{self.reference_path.name}{ext}").exists()]
        
        if missing_indices:
            logger.info(f"Creating BWA index for {self.reference_path}")
            with click.progressbar(length=1, label='Indexing reference', show_eta=True) as bar:
                try:
                    # First check if reference file exists
                    if not self.reference_path.exists():
                        raise RuntimeError(f"Reference file not found: {self.reference_path}")
                    
                    # Check if reference file is empty
                    if self.reference_path.stat().st_size == 0:
                        raise RuntimeError(f"Reference file is empty: {self.reference_path}")
                    
                    # Run BWA index with detailed error capture
                    result = subprocess.run(
                        ['bwa', 'index', str(self.reference_path)],
                        check=True,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        text=True
                    )
                    
                    # Verify index creation
                    still_missing = [ext for ext in index_extensions 
                                   if not (self.reference_path.parent / f"{self.reference_path.name}{ext}").exists()]
                    
                    if still_missing:
                        raise RuntimeError(f"BWA indexing failed to create files: {', '.join(still_missing)}")
                    
                    bar.update(1)
                    logger.info("BWA index created successfully")
                    
                except subprocess.CalledProcessError as e:
                    error_msg = f"BWA indexing failed: {e.stderr}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
                except Exception as e:
                    error_msg = f"Error during BWA indexing: {str(e)}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)

    def _align_sequence_to_reference(self, sequence: str, ref_seq: str) -> str:
        """Align a sequence to reference to detect indels and mutations."""
        try:
            # Get the best alignment
            alignments = self.aligner.align(ref_seq, sequence)
            if len(alignments) == 0:
                logger.warning("No alignment found, returning original sequence")
                return sequence
                
            alignment = alignments[0]
            
            # Get the target and query sequences from the alignment
            target_seq = str(alignment.target)
            query_seq = str(alignment.query)
            
            # Process the alignment to mark mutations and gaps
            result = []
            for t, q in zip(target_seq, query_seq):
                if t == '-':  # Insertion relative to reference
                    result.append(q.lower())
                elif q == '-':  # Deletion relative to reference
                    result.append('-')
                elif t.upper() != q.upper():  # Mismatch
                    result.append(q.lower())
                else:  # Match
                    result.append(q.upper())
            
            return ''.join(result)
            
        except Exception as e:
            logger.error(f"Error in sequence alignment: {str(e)}")
            return sequence

    def _reconstruct_sequence(self,
                            read1: pysam.AlignedSegment,
                            read2: pysam.AlignedSegment,
                            ref_seq: str) -> str:
        """Reconstruct the amplicon sequence from paired reads."""
        sequence = list(ref_seq.upper())
        
        for read in (read1, read2):
            read_seq = read.query_sequence
            ref_pos = read.reference_start
            
            query_pos = 0
            for op, length in read.cigartuples:
                if op == 0:  # Match or mismatch
                    for i in range(length):
                        if (read.query_qualities[query_pos + i] >= self.min_base_quality and
                            ref_pos + i < len(sequence)):
                            base = read_seq[query_pos + i].upper()
                            if base != ref_seq[ref_pos + i].upper():
                                sequence[ref_pos + i] = base.lower()
                            else:
                                sequence[ref_pos + i] = base.upper()
                    query_pos += length
                    ref_pos += length
                elif op == 1:  # Insertion
                    if ref_pos < len(sequence):
                        sequence[ref_pos] = '-'
                    query_pos += length
                elif op == 2:  # Deletion
                    for i in range(length):
                        if ref_pos + i < len(sequence):
                            sequence[ref_pos + i] = '-'
                    ref_pos += length
                elif op == 4:  # Soft clip
                    query_pos += length
        
        reconstructed = ''.join(sequence)
        return self._align_sequence_to_reference(reconstructed, ref_seq)

    def _is_full_length(self, sequence: str, ref_seq: str) -> bool:
        """Check if a sequence covers the full reference length."""
        seq_no_indels = sequence.replace('-', '')
        ref_no_indels = ref_seq.replace('-', '')
        
        if len(seq_no_indels) != len(ref_no_indels):
            return False
            
        if sequence.startswith('-') or sequence.endswith('-'):
            return False
        if sequence.startswith('N') or sequence.endswith('N'):
            return False
            
        return True

    def _get_read_pairs(self, 
                       bam: pysam.AlignmentFile,
                       ref_name: str) -> Generator[Tuple[pysam.AlignedSegment, pysam.AlignedSegment], None, None]:
        """Generate properly paired reads."""
        reads = {}
        for read in bam.fetch(ref_name):
            if (not read.is_proper_pair or 
                read.is_secondary or 
                read.is_supplementary or 
                read.mapping_quality < self.min_mapping_quality):
                continue
                
            qname = read.query_name
            if qname in reads:
                pair = reads.pop(qname)
                yield (read, pair) if read.is_read1 else (pair, read)
            else:
                reads[qname] = read

    def _align_reads(self, 
                    fastq_r1: Path,
                    fastq_r2: Path, 
                    temp_dir: Path,
                    output_dir: Path,
                    threads: int) -> Path:
        """Align reads using BWA-MEM and convert to sorted BAM."""
        sample_name = fastq_r1.stem.replace("_R1_001.fastq", "")
        temp_sam = temp_dir / f"{sample_name}.sam"
        temp_bam = temp_dir / f"{sample_name}.temp.bam"
        final_bam = output_dir / f"{sample_name}.bam"
        
        try:
            # Check input file sizes
            total_size = fastq_r1.stat().st_size + fastq_r2.stat().st_size
            if total_size > self.max_file_size:
                raise ValueError(f"Input files too large: {total_size} bytes")
            
            # Run BWA-MEM
            bwa_cmd = [
                'bwa', 'mem',
                '-t', str(threads),
                str(self.reference_path),
                str(fastq_r1),
                str(fastq_r2)
            ]
            
            with open(temp_sam, 'w') as sam_out:
                logger.debug(f"Running BWA: {' '.join(bwa_cmd)}")
                subprocess.run(
                    bwa_cmd,
                    stdout=sam_out,
                    stderr=subprocess.PIPE,
                    check=True
                )
            
            # Convert SAM to BAM
            subprocess.run(
                ['samtools', 'view', '-b', '-@', str(threads), '-o', str(temp_bam), str(temp_sam)],
                check=True,
                stderr=subprocess.PIPE
            )
            
            # Sort BAM
            subprocess.run(
                [
                    'samtools', 'sort',
                    '-@', str(threads),
                    '-m', '1G',
                    '-T', str(temp_dir / f"{sample_name}.sort"),
                    '-o', str(final_bam),
                    str(temp_bam)
                ],
                check=True,
                stderr=subprocess.PIPE
            )
            
            # Index BAM
            subprocess.run(
                ['samtools', 'index', str(final_bam)],
                check=True,
                stderr=subprocess.PIPE
            )
            
            return final_bam
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"Alignment failed: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Alignment failed: {str(e)}")
        finally:
            for temp_file in [temp_sam, temp_bam]:
                try:
                    if temp_file.exists():
                        temp_file.unlink()
                except:
                    pass

    def _process_alignments(self, 
                          bam_path: Path,
                          ref_name: str) -> Generator[AmpliconRead, None, None]:
        """Process aligned reads for a reference sequence."""
        try:
            bam = pysam.AlignmentFile(bam_path, "rb")
            ref_seq = self.reference[ref_name]
            
            read_count = 0
            for read1, read2 in self._get_read_pairs(bam, ref_name):
                if not (read1 and read2):
                    continue
                    
                sequence = self._reconstruct_sequence(read1, read2, ref_seq)
                mutations = sum(1 for base in sequence if base.islower() or base == '-')
                quality = (read1.mapping_quality + read2.mapping_quality) / 2
                
                read_count += 1
                yield AmpliconRead(sequence, mutations, quality)
            
            if read_count == 0:
                logger.warning(f"No valid read pairs found for {ref_name}")
                
        except Exception as e:
            logger.error(f"Error processing alignments for {ref_name}: {str(e)}")
            raise
        finally:
            if 'bam' in locals():
                bam.close()

    def _analyze_amplicons(self,
                          amplicon_reads: List[AmpliconRead],
                          ref_name: str) -> List[Dict]:
        """Analyze processed amplicon reads."""
        results = []
        
        if not amplicon_reads:
            logger.warning(f"No valid reads found for reference {ref_name}")
            return results
        
        haplotype_counts = Counter(read.sequence for read in amplicon_reads)
        total_reads = sum(haplotype_counts.values())
        ref_seq = self.reference[ref_name].upper()
        
        for haplotype, count in haplotype_counts.most_common():
            frequency = (count / total_reads) * 100
            mutations = sum(1 for base in haplotype if base.islower() or base == '-')
            is_full_length = self._is_full_length(haplotype, ref_seq)
            
            results.append({
                'reference': ref_name,
                'haplotype': haplotype,
                'count': count,
                'frequency': frequency,
                'mutations': mutations,
                'is_full_length': is_full_length
            })
        
        return results

    def process_sample(self, 
                      fastq_r1: Path,
                      fastq_r2: Path,
                      output_dir: Path,
                      threads: int = 4) -> pd.DataFrame:
        """Process a single sample's FASTQ files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            try:
                bam_path = self._align_reads(fastq_r1, fastq_r2, temp_dir, output_dir, threads)
                
                results = []
                for ref_name in self.reference:
                    amplicon_reads = list(self._process_alignments(bam_path, ref_name))
                    if amplicon_reads:
                        results.extend(self._analyze_amplicons(amplicon_reads, ref_name))
                
                if not results:
                    return pd.DataFrame(columns=['reference', 'haplotype', 'count', 'frequency', 
                                              'mutations', 'is_full_length'])
                
                df = pd.DataFrame(results)
                
                # Save results
                sample_name = fastq_r1.stem.replace("_R1_001.fastq", "")
                csv_path = output_dir / f"{sample_name}_haplotypes.csv"
                df.to_csv(csv_path, index=False)
                
                return df
                
            except Exception as e:
                logger.error(f"Error processing sample: {str(e)}")
                return pd.DataFrame(columns=['reference', 'haplotype', 'count', 'frequency', 
                                          'mutations', 'is_full_length'])