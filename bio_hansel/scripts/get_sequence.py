from Bio import Entrez, SeqIO
import pandas as pd
import os
from typing import Dict


def get_sequences(output_directory: str, reference_genome_path: str,
                  results_dict: Dict[str, pd.DataFrame]):
    """Collects the sequences from the from the reference genome by going through the dataframe and finding the appropriate SNV location
    Args: 
    output_directory:directory where the schema would be located as indicated by the user
    data_frame: filtered data frame with list of SNVs and their location
    group: specific group in which the SNV belongs to
    random_id: id that is assigned to the schema file
    output_directory: directory in which output files are stored
    reference_genome_path: file path to where the reference genome is located

    Output:
    Creates schema file in the output directory


    """
    for key, value in results_dict.items():
        group = key
        max_sequence = value.loc[value['POS'].idxmax()]
        gb_file = reference_genome_path
        max_sequence_value = max_sequence['POS']
        with open(f"{output_directory}/schema.fasta", "a+") as file:
            for gb_record in SeqIO.parse(open(gb_file, "r"), "genbank"):
                for index, row in value.iterrows():
                    position = row['POS']
                    reference_snv = row['REF']
                    alternate_snv = row['ALT']

                    seq_start1 = max(0, position - 16) - 1
                    seq_stop1 = position - 1

                    seq_start2 = position
                    seq_stop2 = min(max_sequence_value, position + 16)

                    record_1 = gb_record.seq[seq_start1:seq_stop1]
                    record_2 = gb_record.seq[seq_start2:seq_stop2]
                    attribute_value = row.iloc[3]
                    # if the ratio is above 1, then it means that it is positive and takes the alternate snv form
                    if (attribute_value > 0):
                        file.write('>' + str(position) + '-' + str(group) +
                                   '\n')
                        file.write(
                            str(record_1) + alternate_snv + str(record_2) +
                            '\n')
                        file.write('>negative' + str(position) + '-' +
                                   str(group) + '\n')
                        file.write(
                            str(record_1) + reference_snv + str(record_2) +
                            '\n')

                    # if the ratio is below 1, then it means that it remains negative
                    else:
                        file.write('>' + str(position) + '-' + str(group) +
                                   '\n')
                        file.write(
                            str(record_1) + reference_snv + str(record_2) +
                            '\n')
                        file.write('>negative' + str(position) + '-' +
                                   str(group) + '\n')
                        file.write(
                            str(record_1) + alternate_snv + str(record_2) +
                            '\n')