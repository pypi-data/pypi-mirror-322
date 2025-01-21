import os, gzip, csv
import adagenes.clients.reader as reader
import adagenes
#from adagenes.tools.parse_dataframes import parse_dataframe_biomarkers, is_dragen_file


def parse_csv_line(line, sep=",", quote_char='"', remove_quotes=True):
    fields = []        # List to store the parsed fields
    field = []         # List to collect characters for the current field
    inside_quotes = False  # Flag to track if we are inside a quoted field

    i = 0
    while i < len(line):
        char = line[i]

        if char == quote_char:  # Handle quote characters
            if inside_quotes:
                # Look ahead to see if the next character is also a quote
                if i + 1 < len(line) and line[i + 1] == quote_char:
                    # Double quote inside quoted field; add a single quote to field
                    field.append(quote_char)
                    i += 1  # Skip the next quote character
                else:
                    # Closing quote, toggle inside_quotes off
                    inside_quotes = False
            else:
                # Opening quote, toggle inside_quotes on
                inside_quotes = True

        elif char == sep and not inside_quotes:
            # If we encounter a comma outside of quotes, end of field
            fields.append(''.join(field))
            field = []  # Reset the field for the next entry

        else:
            # Add character to the current field
            field.append(char)

        i += 1

    # Add the last field to the list (if there's anything left)
    fields.append(''.join(field))
    return fields


class CSVReader(reader.Reader):

    def read_file(self,
                  infile,
                  sep=',',
                  genome_version='hg38',
                  batch_size=100,
                  columns=None,
                  mapping=None,
                  header=True,
                  remove_quotes=True,
                  start_row=None, end_row=None
                  ) -> adagenes.BiomarkerFrame:
        """
        Loads a tab or comma-separated file in a variant data object

        :param batch_size:
        :param sep:
        :param genome_version:
        :param infile:
        :return:
        """
        if genome_version is None:
            genome_version = self.genome_version

        fileopen = False
        if isinstance(infile, str):
            fileopen = True
            file_name, file_extension = os.path.splitext(infile)
            input_format_recognized = file_extension.lstrip(".")
            if input_format_recognized == "gz":
                infile = gzip.open(infile, 'rt')
            else:
                infile = open(infile, 'r')

        #reader = csv.reader(infile, quotechar='"', delimiter=',', skipinitialspace=True)
        lines = []
        columns = None
        for i,line in enumerate(infile):
            if line.startswith("#"):
                columns = line.replace("#","").strip().split(sep)
            elif (i==0) and (header is True):
                columns = parse_csv_line(line.strip(), remove_quotes=remove_quotes, sep=sep)# .split(sep)
            else:
                lines.append(parse_csv_line(line.strip(), sep=sep))

        json_obj = adagenes.BiomarkerFrame(preexisting_features=columns)
        row = 0
        #dragen_file = adagenes.is_dragen_file(df.columns)
        #if dragen_file:
        #    json_obj.data_type = "g"

        #print("columns ",columns, ":: ",json_obj.preexisting_features)
        #print("lines ",lines)
        json_obj = adagenes.tools.parse_dataframes.parse_csv_lines(lines,columns,json_obj, mapping=mapping,
                                                                   genome_version=genome_version,sep=sep, header=header,
                                                                   remove_quotes=remove_quotes)

        if fileopen is True:
            infile.close()

        return json_obj

    def read_file_chunk(self, infile, json_obj: adagenes.BiomarkerFrame, genome_version="hg38") -> adagenes.BiomarkerFrame:
        """
        Reads a defined number of lines from a file object, adds them to the given biomarker set and returns the extended biomarker list

        :param genome_version:
        :param infile:
        :type infile:
        :param json_obj:
        :type json_obj: BiomarkerSet
        :return: json_obj
        """

        json_obj_new = self.read_file(infile,genome_version=genome_version)
        json_obj.data = json_obj_new.data

        return json_obj
