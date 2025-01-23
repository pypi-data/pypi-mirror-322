import re, gzip, os
import requests, datetime, json
import adagenes.tools.parse_vcf as parse_vcf
import adagenes as ag
from adagenes.tools.json_mgt import generate_variant_data


class VCFProcessor:

    def get_connection(self,variants, url_pattern, genome_version):
        url = url_pattern.format(genome_version) + variants
        print(url)
        r = requests.get(url)
        return r.json()


    def query_service(self,vcf_lines, variant_dc, outfile, extract_keys, srv_prefix, url_pattern, genome_version, qid_key="q_id", error_logfile=None):
        variants = ','.join(variant_dc.values())

        try:
            json_body = self.get_connection(variants, url_pattern, genome_version)

            # for i, l in enumerate(variant_dc.keys()):
            for i, l in enumerate(json_body):
                if json_body[i]:
                    annotations = []

                    if qid_key not in json_body[i]:
                        continue
                    qid = json_body[i][qid_key]

                    for k in extract_keys:
                        if k in json_body[i]:
                            annotations.append('{}-{}={}'.format(srv_prefix, k, json_body[i][k]))

                    try:
                        splits = vcf_lines[qid].split("\t")
                        splits[7] = splits[7] + ";" + ';'.join(annotations)
                        vcf_lines[qid] = "\t".join(splits)
                    except:
                    # print("error in query response ",qid,'  ,',variant_dc)
                        if error_logfile is not None:
                            cur_dt = datetime.datetime.now()
                            date_time = cur_dt.strftime("%m/%d/%Y, %H:%M:%S")
                            print(cur_dt, ": error processing variant response: ", qid, file=error_logfile)

        except:
            # print("error in whole service query ",variant_dc)
            if error_logfile is not None:
                print("error processing request: ", variants, file=error_logfile)

        for line in vcf_lines:
            print(vcf_lines[line], file=outfile)


    def read_genomeversion(self,line):
        if not line.startswith('##reference'):
            return None
        p = re.compile('(##reference=).*GRCh([0-9]+).*')
        m = p.match(line)

        if m and len(m.groups()) > 1:
            genome_version = 'hg' + m.group(2)
            if genome_version == 'hg37':
                genome_version = 'hg19'
            return genome_version

        p = re.compile('(##reference=).*(hg[0-9]+).*')
        m = p.match(line)
        if m and len(m.groups()) > 1:
            return m.group(2)
        return None

    def process_file(self,
                     infile,
                     outfile,
                     magic_obj,
                     reader=None,
                     writer=None,
                     input_format='vcf',
                     output_format='vcf',
                     variant_batch_size=100,
                     line_batch_size=5000,
                     genome_version=None,
                     error_logfile=None,
                     output_type='file',
                     filter=None,
                     mapping=None,
                     labels=None,
                     ranked_labels=None):
        """

        :param infile:
        :param outfile:
        :param magic_obj:
        :param input_format:
        :param output_format:
        :param variant_batch_size:
        :param line_batch_size:
        :param genome_version:
        :param error_logfile:
        :param output_type:
        :param filter:
        :return:
        """
        infile_str = False
        outfile_str = False
        if isinstance(infile, str):
            infile = open(infile, "r")
            infile_str = True
        if isinstance(outfile, str):
            outfile = open(outfile, "w")
            outfile_str = True

        variants_written=False


        variants = {}
        if input_format == 'vcf':
            variant_count = 0
            line_count = 0
            vcf_lines = {}
            info_lines = {}
            first_chunk = True
            last_chunk=False

            header_lines = []
            c=0

            if writer is not None:
                writer.pre_process(outfile,ranked_labels=ranked_labels)


            first_chunk=True
            for line in infile:

                if reader is not None:
                    vcf_lines = reader.read_line(line, vcf_lines)
                    first_chunk = False
                else:
                    if line.startswith('##'):
                        print(line.strip(), file=outfile)
                        header_lines.append(line.strip())
                        if genome_version is None:
                            genome_version = self.read_genomeversion(line)
                        continue
                    elif line.startswith('#CHROM'):
                        if hasattr(magic_obj, "info_lines"):
                            header_lines += magic_obj.info_lines

                        header_lines.append(line.strip())
                        # if genome version has not set yet, use hg38 as default
                        if genome_version is None:
                            genome_version = 'hg38'

                        lines, genome_version = parse_vcf.process_vcf_headers(header_lines, genome_version)
                        #magic_obj.genome_version = "hg38"
                        for hline in lines:
                            print(hline, file=outfile)
                        continue
                    else:
                        variant_count += 1
                        line_count += 1

                    fields = line.strip().split('\t')

                    if len(fields) >= 7:
                        chromosome, pos, ref_base, alt_base = fields[0], fields[1], fields[3], fields[4]
                        info = fields[7]
                        chr_prefix = ""
                        if not chromosome.startswith("chr"):
                            chr_prefix = "chr"
                        variant = chr_prefix + '{}:{}{}>{}'.format(chromosome, pos, ref_base, alt_base)
                        if alt_base != '.':
                            variants[variant_count] = variant
                        #print(line)
                        vcf_lines[variant] = { "CHROM":chromosome,
                                               "POS": pos,
                                               "ID": fields[2],
                                               "REF": ref_base,
                                               "ALT": alt_base,
                                               "QUAL": fields[5],
                                               "FILTER": fields[6],
                                               "INFO": fields[7],
                                               "OPTIONAL": fields[8:]
                                               } #line.strip()
                                                # TODO: add samples columns
                        info_lines[variant] = info.strip()
                        #bframe = ag.BiomarkerFrame()
                        vcf_lines= ag.generate_variant_data(vcf_lines, variant, chromosome, pos, fields, ref_base, alt_base,
                                                         genome_version=genome_version)
                        vcf_lines = ag.TypeRecognitionClient(genome_version=genome_version).process_data(vcf_lines)


                # query the service either after 100 ("variant_batch_size") variants
                # or 5000 ("line_batch_size") lines are collected
                if (len(variants) >= variant_batch_size) or (len(vcf_lines) >= line_batch_size):
                        if output_format == 'json' and variants_written:
                            print(',', file=outfile, end='')


                        # Process
                        if magic_obj is not None:
                            vcf_lines = magic_obj.process_data(vcf_lines)


                        # Writer
                        if output_type == 'file':

                            c = 1
                            if writer is not None:
                                if magic_obj is None:
                                    srv_prefix=""
                                    extract_keys = []
                                else:
                                    srv_prefix = magic_obj.srv_prefix
                                    extract_keys = magic_obj.extract_keys
                                #writer.write_chunk_to_file(outfile, vcf_lines, c, srv_prefix, extract_keys,
                                #                           first_chunk=first_chunk, last_chunk=last_chunk)
                                writer.write_chunk_to_file(outfile, vcf_lines, c, srv_prefix, extract_keys,
                                                           mapping=mapping,
                                                           ranked_labels=ranked_labels,
                                                           labels=labels
                                                           )
                                first_chunk=False
                            else:
                                for var in vcf_lines.keys():
                                    if output_format == 'vcf':
                                        #for json_obj in vcf_lines:
                                        if hasattr(magic_obj, 'key_labels'):
                                            labels = magic_obj.key_labels
                                        else:
                                            labels = None
                                        if (not hasattr(magic_obj, 'srv_prefix')) and (magic_obj is not None):
                                            magic_obj.srv_prefix = None
                                        if (not hasattr(magic_obj, 'extract_keys')) and (magic_obj is not None):
                                            magic_obj.extract_keys = None
                                        print(self.to_single_vcf_line(vcf_lines[var], magic_obj.srv_prefix, magic_obj.extract_keys, labels), file=outfile)
                                        #to_vcf(vcf_lines, magic_obj.srv_prefix, magic_obj.extract_keys)
                                    elif output_format == 'json':
                                        #print(vcf_lines)
                                        #print(json.dumps(vcf_lines), file=outfile)
                                        json_str = json.dumps(vcf_lines[var])
                                        #json_str = json_str.lstrip('{').rstrip('}')
                                        json_str = "\"" + var + "\"" + ":" + json_str
                                        if c < len(vcf_lines):
                                            json_str = json_str + ','
                                        #else:
                                        #    json_str = json_str + '}'

                                        c += 1

                                        print(json_str, file=outfile)

                            #if output_format == 'vcf':
                            variants = {}
                            vcf_lines = {}
                            variant_count = 0
                            line_count = 0
                            info_lines = {}
                            #c=0
                            variants_written = True

        else:
            vcf_lines = json.load(infile)
            for i, key in enumerate(vcf_lines.keys()):
                variants[i] = key
            #print("loaded ",vcf_lines)

        # query the service with the remaining lines
        c=1
        if len(vcf_lines) > 0:
            #if genome_version != "hg38":
            #    vcf_lines = ag.LiftoverClient(genome_version=genome_version).process_data(vcf_lines, target_genome="hg38")

            if magic_obj is not None:
                vcf_lines = magic_obj.process_data(vcf_lines)
            #print("after process ",vcf_lines)

            if output_format == 'json' and variants_written :
                print(',', file=outfile, end='')
            for var in vcf_lines.keys():
                #print(vcf_lines[line])

                if output_type == 'file':
                    if writer is not None:
                        #writer.write_chunk_to_file(outfile, vcf_lines, c, magic_obj.srv_prefix, magic_obj.extract_keys,
                        #                           first_chunk=first_chunk, last_chunk=last_chunk)
                        writer.write_chunk_to_file(outfile, vcf_lines, c, srv_prefix, extract_keys,
                                                   mapping=mapping,
                                                   ranked_labels=ranked_labels,
                                                   labels=labels
                                                   )
                    else:
                        if output_format == 'vcf':
                            #for json_obj in vcf_lines:
                            if hasattr(magic_obj, 'key_labels'):
                                labels = magic_obj.key_labels
                            else:
                                labels = None
                            if not hasattr(magic_obj, 'srv_prefix'):
                                magic_obj.srv_prefix = None
                            if not hasattr(magic_obj, 'extract_keys'):
                                magic_obj.extract_keys = None
                            print(self.to_single_vcf_line(vcf_lines[var], magic_obj.srv_prefix, magic_obj.extract_keys, labels), file=outfile)
                            #to_vcf(vcf_lines, magic_obj.srv_prefix, magic_obj.extract_keys)
                        elif output_format == 'json':
                            json_str = json.dumps(vcf_lines[var])
                            #json_str = json_str.lstrip('{').rstrip('}')
                            json_str = "\"" + var + "\"" + ":" + json_str
                            if c < len(vcf_lines):
                                json_str = json_str + ','
                            #else:
                            #    json_str = json_str + '}'
                            #print(len(vcf_lines))
                            print(json_str, file=outfile)
                            #print(json.dumps(vcf_lines))
                            #print(json.dumps(vcf_lines), file=outfile)
                            #print(line, file=outfile)
                            c+=1

        #if writer is not None:
        #    last_chunk=True
        #    writer.write_chunk_to_file(outfile, vcf_lines, c, magic_obj.srv_prefix, magic_obj.extract_keys,
        #                               first_chunk=first_chunk, last_chunk=last_chunk)

        #if ((output_format == 'avf') or(output_format == 'json') and (output_type=='file')):
        #    print('}', file=outfile)
        #    #print("{", file=outfile)
        #    #if output_format == 'json':
        #    print(json.dumps(vcf_lines), file=outfile)
        #    #print("}", file=outfile)
        if writer is not None:
            writer.post_process(outfile)

        if infile_str is True:
            infile.close()
        if outfile_str is True:
            outfile.close()

        #print(vcf_lines)

        if output_type == 'obj':
            return vcf_lines

    def to_vcf(self,vcf_obj, srv_prefix, extract_keys, outfile):
        for json_obj in vcf_obj:
            print(self.to_single_vcf_line(json_obj, srv_prefix, extract_keys), file = outfile)

    def to_single_vcf_line(self,vcf_obj, srv_prefix, extract_keys, labels):
        """

        :param vcf_obj:
        :param srv_prefix:
        :param extract_keys:
        :return:
        """
        if srv_prefix is not None:
            annotations = generate_annotations(srv_prefix, vcf_obj, extract_keys, labels)
        else:
            annotations = []

        #splits = vcf_lines[qid].split("\t")
        #print(vcf_obj)
        if "INFO" not in vcf_obj.keys():
            if "INFO" in vcf_obj["variant_data"].keys():
                vcf_obj["INFO"] = vcf_obj["variant_data"]["INFO"]
                vcf_obj["OPTIONAL"] = vcf_obj["variant_data"]["OPTIONAL"]
                vcf_obj["ID"] = vcf_obj["variant_data"]["ID"]
                vcf_obj["QUAL"] = vcf_obj["variant_data"]["QUAL"]
                vcf_obj["FILTER"] = vcf_obj["variant_data"]["FILTER"]

        vcf_obj["INFO"] = vcf_obj["INFO"] + ";" + ';'.join(annotations)

        #vcf_lines[qid] = "\t".join(splits)
        vcf_obj["INFO"] = vcf_obj["INFO"].lstrip(";.")

        if vcf_obj["INFO"] == "":
            vcf_obj["INFO"] = "."

        optional_columns = '\t'.join(vcf_obj['OPTIONAL'])
        #vcfline = f"{vcf_obj['CHROM']}\t{vcf_obj['POS']}\t{vcf_obj['ID']}\t{vcf_obj['REF']}" \
        #    f"\t{vcf_obj['ALT']}\t{vcf_obj['QUAL']}\t{vcf_obj['FILTER']}\t{vcf_obj['INFO']}" \
        #    f"\t{optional_columns}"
        #print("obj ",vcf_obj)
        vcfline = f"{vcf_obj['variant_data']['CHROM']}\t{vcf_obj['variant_data']['POS']}\t{vcf_obj['ID']}\t{vcf_obj['variant_data']['REF']}" \
                  f"\t{vcf_obj['variant_data']['ALT']}\t{vcf_obj['QUAL']}\t{vcf_obj['FILTER']}\t{vcf_obj['INFO']}" \
                  f"\t{optional_columns}"

        return vcfline.rstrip("\t")

    def to_json(self, json_obj, outfile_str:str):
        outfile = open(outfile_str, 'rw')
        json.dumps(json_obj, file=outfile)
        outfile.close()

def generate_annotations(srv_prefix, vcf_obj, extract_keys, labels):
    """

    :param srv_prefix:
    :param vcf_obj:
    :param extract_keys:
    :return:
    """
    annotations = []
    if isinstance(srv_prefix, str):
        if srv_prefix in vcf_obj:
            service_output = vcf_obj[srv_prefix]
            for k in extract_keys:
                if k in service_output:
                    annotations.append('{}_{}={}'.format(srv_prefix, k, service_output[k]))
    elif isinstance(srv_prefix, list):
        for i,pref in enumerate(srv_prefix):
            if pref in vcf_obj.keys():
                service_output = vcf_obj[pref]
                k_list = extract_keys[i]
                if isinstance(k_list,list):
                    for k in k_list:
                        if k in service_output:
                            annotations.append('{}_{}={}'.format(pref, k, service_output[k]))
                elif isinstance(k_list, str):
                    for j,k in enumerate(extract_keys):
                        if k in service_output:
                            if labels is not None:
                                label = labels[j]
                                annotations.append('{}={}'.format(label, service_output[k]))
                            else:
                                annotations.append('{}_{}={}'.format(pref, k, service_output[k]))
    return annotations
