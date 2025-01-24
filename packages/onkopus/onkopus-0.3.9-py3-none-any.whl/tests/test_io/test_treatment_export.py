
import unittest,os
import adagenes
import onkopus as op


class TreatmentExportTestCase(unittest.TestCase):

    def test_export_treatment_data(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = op.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        outfile=__location__ + "/../test_files/test_writer.out.csv"
        op.ClinSigWriter().write_evidence_data_to_file(bf,outfile,sep="\t")

        file = open(outfile, 'r')
        contents = file.read()
        contents_expected = """biomarker\tcitation_i"""
        self.assertEqual(contents[0:20], contents_expected, "")
        file.close()



    def test_export_treatment_data_opened_file(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = op.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        #print(bf.data["chr7:140753336A>T"]["oncokb"])

        outfile_str=__location__ + "/../test_files/test_writer.out.stream.csv"
        outfile = open(outfile_str, "w")
        op.ClinSigWriter().write_evidence_data_to_file_all_features(bf,outfile=outfile,sep="\t")
        outfile.close()

        file = open(outfile_str)
        contents = file.read()
        contents_expected = """biomarker\tcitation_i"""
        self.assertEqual(contents[0:20], contents_expected, "")
        file.close()

    def test_export_treatment_data_filestream(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        oncokb_key = os.getenv("ONCOKB_KEY")

        data = {"chr7:140753336A>T":{}, "chr17:7673776G>A":{}}
        genome_version = "hg38"
        bf = adagenes.BiomarkerFrame(genome_version=genome_version,data=data)
        bf = op.annotate(bf, genome_version="hg38",oncokb_key=oncokb_key)

        #print(bf.data["chr7:140753336A>T"]["oncokb"])

        import io
        import pandas as pd
        outfile_str=__location__ + "/../test_files/test_writer.out.stream.csv"
        outfile = io.StringIO()
        op.ClinSigWriter().write_evidence_data_to_file_all_features(bf,outfile=outfile,sep="\t")

        outfile.seek(0)
        df = pd.read_csv(outfile, sep="\t", names=range(12))
        print("TREATMENTS ",df)

        outfile.close()

        self.assertEqual(df.columns, [], "")

