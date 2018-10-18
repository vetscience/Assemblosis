#!/usr/bin/env python

import os, sys, optparse
from base import Base

#################################################
def options():
    parser = optparse.OptionParser('usage: python %prog -i filename -n size')
    parser.add_option('-r', '--ref', dest='ref', help='FASTA file of reference genome', metavar='REF', default='')
    parser.add_option('-f', '--gff', dest='gff', help='GFF file of reference genome', metavar='REF', default='')
    parser.add_option('-a', '--asms', dest='asms', help='FASTA files for the assemblies to evaluate.', metavar='ASMS', default='')
    parser.add_option('-g', '--gages', dest='gages', help='GAGE reports', metavar='GAGE', default='')
    parser.add_option('-q', '--quasts', dest='quasts', help='QUAST reports', metavar='QUAST', default='')
    parser.add_option('-m', '--quastMisAsms', dest='quastMisAsms', help='QUAST misassembly report', metavar='QUASTMISASMS', default='')
    parser.add_option('-s', '--quastSnpsZipped', dest='quastSnpsZipped', help='QUAST nucleotide differences (gzipped)', metavar='QUASTSNPS', default='')
    parser.add_option('-b', '--busco', dest='busco', help='BUSCO report', metavar='BUSCO', default='')
    parser.add_option('-l', '--labels', dest='labels', help='Labels for the reference and the assemblies', metavar='LABELS', default='')
    options, args = parser.parse_args()
    return options


#################################################
def main():
    '''
    '''
    opts = options()
    base = Base()
    refGff = opts.gff
    buscoFiles = opts.busco.strip().strip('"').strip("'").split(',')
    asms = opts.asms.strip().strip('"').strip("'").split(',')
    gages = opts.gages.strip().strip('"').strip("'").split(',')
    quasts = opts.quasts.strip().strip('"').strip("'").split(',')
    quastMisAsms = opts.quastMisAsms.strip().strip('"').strip("'").split(',')
    quastSnpFiles = opts.quastSnpsZipped.strip().strip('"').strip("'").split(',')
    base.createDir("TablesDir")
    genomeLabels = opts.labels.strip().strip('"').strip("'").split(',')
    metricOrder = ["Genome size (nt)", "Sequence count", "Quast genome fraction (%)", "Quast aligned length (nt)", "Number of Ns (nt)", "Gap count", "N90 (nt)", "L90", "N50 (nt)", "L50", "NG90 (nt)", "LG90", "NG50 (nt)", "Quast NG50 (nt)", "LG50", "GC content (%)", "Longest sequence (nt)", "Shortest sequence (nt)", "Quast number of misassemblies", "Quast relocations","Quast translocations","Quast inversions", "Quast number of local misassemblies", "Quast duplication ratio", "Quast mismatches","Quast indels (<=5bp)","Quast indels (>5bp)","Quast indels length", "Quast mismatches per 100 kbp", "Quast indels per 100 kbp", "GAGE missing reference bases (nt / %)","GAGE missing assembly bases (nt / %)","GAGE duplicated reference bases","GAGE compressed reference bases","GAGE average identity (%)","GAGE nucleotide mismatches","GAGE indels (<=5bp)","GAGE indels (>5bp)","GAGE inversions","GAGE relocations","GAGE translocations","Complete BUSCOs","Complete single-copy BUSCOs","Complete duplicated BUSCOs","Fragmented BUSCOs","Missing BUSCOs","Expected BUSCOs","Number of nucleotide differences in CDSs","Number of indels in CDSs","Number of affected CDSs","Number of affected mRNAs","Number of nucleotide differences outside CDSs","Number of indels outside CDSs","Number of all anomalies","Number of non-synonymous mutations","Number of synonymous mutations","Number of in-frame indels","Number of mutated proteins"]

    dGenomes = {}
    for i in xrange(len(asms)):
        dGenomes[asms[i]] = []
    for i in xrange(len(asms)):
        base.shell("python /root/genomeInfo.py -s %s -r %s > genome%d.info" %(asms[i], asms[0], i + 1))
        with open("genome%d.info" %(i + 1)) as handle:
            for line in handle:
                line = line.strip()
                items = line.split()
                if "Number of sequences:" in line:
                    dGenomes[asms[i]].append(("Sequence count", items[-1]))
                if "are Ns" in line:
                    dGenomes[asms[i]].append(("Number of Ns (nt)", items[1]))
                if "CG content" in line:
                    dGenomes[asms[i]].append(("GC content (%)", items[3].strip('%')))
                if "Number of gaps" in line:
                    dGenomes[asms[i]].append(("Gap count", "{:,}".format(int(items[-1]))))
                if "N90" in line:
                    dGenomes[asms[i]].append(("N90 (nt)", "{:,}".format(int(items[1].strip(',')))))
                    dGenomes[asms[i]].append(("L90", "{:,}".format(int(items[-1]))))
                if "N50" in line:
                    dGenomes[asms[i]].append(("N50 (nt)", "{:,}".format(int(items[1].strip(',')))))
                    dGenomes[asms[i]].append(("L50", "{:,}".format(int(items[-1]))))
                if "NG90" in line:
                    dGenomes[asms[i]].append(("NG90 (nt)", "{:,}".format(int(items[1].strip(',')))))
                    dGenomes[asms[i]].append(("LG90", "{:,}".format(int(items[-1]))))
                if "NG50" in line:
                    dGenomes[asms[i]].append(("NG50 (nt)", "{:,}".format(int(items[1].strip(',')))))
                    dGenomes[asms[i]].append(("LG50", "{:,}".format(int(items[-1]))))
                if "Length of the genome" in line:
                    dGenomes[asms[i]].append(("Genome size (nt)", "{:,}".format(int(items[-1]))))
                if "Longest sequence" in line:
                    dGenomes[asms[i]].append(("Longest sequence (nt)", "{:,}".format(int(items[-1]))))
                if "Shortest sequence" in line:
                    dGenomes[asms[i]].append(("Shortest sequence (nt)", "{:,}".format(int(items[-1]))))

    for i in xrange(len(asms)):
        with open("%s" %quasts[i]) as handle:
            for line in handle:
               line = line.strip()
               items = line.split()
               if "NG50" in line:
                   dGenomes[asms[i]].append(("Quast NG50 (nt)", "{:,}".format(int(items[-1]))))
               if "# misassemblies" in line:
                   dGenomes[asms[i]].append(("Quast number of misassemblies", "{:,}".format(int(items[-1]))))
               if "local misassemblies" in line:
                   dGenomes[asms[i]].append(("Quast number of local misassemblies", "{:,}".format(int(items[-1]))))
               if "Duplication ratio" in line:
                   dGenomes[asms[i]].append(("Quast duplication ratio", items[-1]))
               if "mismatches per 100 kbp" in line:
                   dGenomes[asms[i]].append(("Quast mismatches per 100 kbp", items[-1]))
               if "indels per 100 kbp" in line:
                   dGenomes[asms[i]].append(("Quast indels per 100 kbp", items[-1]))
               if "Genome fraction (%)" in line:
                   dGenomes[asms[i]].append(("Quast genome fraction (%)", items[-1]))
               if "Total aligned length" in line:
                   dGenomes[asms[i]].append(("Quast aligned length (nt)", "{:,}".format(int(items[-1]))))

    for i in xrange(len(asms)):
        with open("%s" %quastMisAsms[i]) as handle:
            for line in handle:
                line = line.strip()
                items = line.split()
                if "relocations" in line:
                    count = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast relocations", "%s" %count))
                if "translocations" in line:
                    count = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast translocations", "%s" %count))
                if "inversions" in line:
                    count = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast inversions", "%s" %count))
                if "mismatches" in line:
                    bases = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast mismatches", "%s" %bases))
                if "indels (<= 5" in line:
                    bases = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast indels (<=5bp)", "%s" %bases))
                if "indels (> 5" in line:
                    bases = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast indels (>5bp)", "%s" %bases))
                if "Indels length" in line:
                    bases = "{:,}".format(int(items[-1]))
                    dGenomes[asms[i]].append(("Quast indels length", "%s" %bases))

    for i in xrange(len(asms)):
        with open("%s" %gages[i]) as handle:
            for line in handle:
               line = line.strip()
               items = line.split()
               if "Missing reference bases" in line:
                   bases, percentage = items[-1].strip(")").replace("(", "/").strip('%').split('/')
                   bases = "{:,}".format(int(bases))
                   dGenomes[asms[i]].append(("GAGE missing reference bases (nt / %)", "%s / %s" %(bases, percentage)))
               if "Missing assembly bases" in line:
                   bases, percentage = items[-1].strip(")").replace("(", "/").strip('%').split('/')
                   bases = "{:,}".format(int(bases))
                   dGenomes[asms[i]].append(("GAGE missing assembly bases (nt / %)", "%s / %s" %(bases, percentage)))
               if "Duplicated reference bases" in line:
                   dGenomes[asms[i]].append(("GAGE duplicated reference bases", "{:,}".format(int(items[-1]))))
               if "Compressed reference bases" in line:
                   dGenomes[asms[i]].append(("GAGE compressed reference bases", "{:,}".format(int(items[-1]))))
               if "Avg idy" in line:
                   dGenomes[asms[i]].append(("GAGE average identity (%)", items[-1]))
               if "SNPs" in line:
                   dGenomes[asms[i]].append(("GAGE nucleotide mismatches", "{:,}".format(int(items[-1]))))
               if "Indels < 5bp" in line:
                   dGenomes[asms[i]].append(("GAGE indels (<=5bp)", "{:,}".format(int(items[-1]))))
               if "Indels >= 5" in line:
                   dGenomes[asms[i]].append(("GAGE indels (>5bp)", items[-1]))
               if "Inversions" in line:
                   dGenomes[asms[i]].append(("GAGE inversions", items[-1]))
               if "Relocation" in line:
                   dGenomes[asms[i]].append(("GAGE relocations", items[-1]))
               if "Translocation" in line:
                   dGenomes[asms[i]].append(("GAGE translocations", items[-1]))

    for i in xrange(len(asms)):
        with open("%s" %buscoFiles[i]) as handle:
            for line in handle:
               line = line.strip()
               items = line.split()
               if "Complete BUSCOs" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Complete BUSCOs", "%s" %buscos))
               if "Complete and single" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Complete single-copy BUSCOs", "%s" %buscos))
               if "Complete and duplicated" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Complete duplicated BUSCOs", "%s" %buscos))
               if "Fragmented BUSCOs" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Fragmented BUSCOs", "%s" %buscos))
               if "Missing BUSCOs" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Missing BUSCOs", "%s" %buscos))
               if "Total BUSCO" in line:
                   buscos = "{:,}".format(int(items[0]))
                   dGenomes[asms[i]].append(("Expected BUSCOs", "%s" %buscos))

    for i in xrange(len(asms)):
        if i > 0:
            base.shell("python /root/snpCoding.py -i %s -n %s > snpIndel%d.info 2> indel%d.ids" %(refGff, quastSnpFiles[i], i + 1, i + 1))
            with open("snpIndel%d.info" %(i + 1)) as handle:
                for line in handle:
                    items = line.strip().split('\t')
                    snpCoding, indelCoding, cdsCnt, mRnaCnt, totalCnt, indelNonCoding, snpNonCoding = items[0], items[1], items[2], items[3], items[4], items[5], items[6]
                    dGenomes[asms[i]].append(("Number of nucleotide differences in CDSs", snpCoding))
                    dGenomes[asms[i]].append(("Number of indels in CDSs", indelCoding))
                    dGenomes[asms[i]].append(("Number of affected CDSs", cdsCnt))
                    dGenomes[asms[i]].append(("Number of affected mRNAs", mRnaCnt))
                    dGenomes[asms[i]].append(("Number of nucleotide differences outside CDSs", snpNonCoding))
                    dGenomes[asms[i]].append(("Number of indels outside CDSs", indelNonCoding))
                    dGenomes[asms[i]].append(("Number of all anomalies", totalCnt))
                    break
        else:
            dGenomes[asms[i]].append(("Number of nucleotide differences in CDSs", '0'))
            dGenomes[asms[i]].append(("Number of indels in CDSs", '0'))
            dGenomes[asms[i]].append(("Number of affected CDSs", '0'))
            dGenomes[asms[i]].append(("Number of affected mRNAs", '0'))
            dGenomes[asms[i]].append(("Number of nucleotide differences outside CDSs", '0'))
            dGenomes[asms[i]].append(("Number of indels outside CDSs", '0'))
            dGenomes[asms[i]].append(("Number of all anomalies", '0'))

    base.shell("python /root/rmSpliceVars.py -i %s > noSpliceVars.gff" %refGff)
    for i in xrange(len(asms)):
        if i > 0:
            base.shell("python /root/compileSnpsToRef.py -i %s -n %s > scafs.snpref%d.fa && rm -f scafs.snpref%d.fa.*" %(asms[0], quastSnpFiles[i], i + 1, i + 1))
            base.shell("gffread noSpliceVars.gff -g scafs.snpref%d.fa -x scafs.snpref.cds%d.fa" %(i + 1, i + 1))
            base.shell("gffread noSpliceVars.gff -g scafs.snpref%d.fa -y scafs.snpref.pts%d.fa" %(i + 1, i + 1))
            base.shell("python /root/countDiffs.py -1 scafs.snpref.cds.fa -2 scafs.snpref.cds%d.fa > cdsDiffs%d.txt 2> cdsDiffs%d.ids" %(i + 1, i + 1, i + 1))
            base.shell("python /root/countDiffs.py -1 scafs.snpref.pts.fa -2 scafs.snpref.pts%d.fa > ptsDiffs%d.txt 2> ptsDiffs%d.ids" %(i + 1, i + 1, i + 1))
            ptsIds, indelMrnaIds = [], []
            with open("ptsDiffs%d.ids" %(i + 1)) as handle:
                ptsIds = handle.readline().strip().split('\t')
            with open("indel%d.ids" %(i + 1)) as handle: # mRNA ids with indels
                indelMrnaIds = handle.readline().strip().split('\t')
            modPtsIds = set(ptsIds) | set(indelMrnaIds)
            snpCnt, nonSynCnt, synCnt, inFramCnt = 0, 0, 0, 0
            with open("cdsDiffs%d.txt" %(i + 1)) as handle:
                for line in handle:
                    snpCnt = int(line.strip())
                    break
            with open("ptsDiffs%d.txt" %(i + 1)) as handle:
                for line in handle:
                    nonSynCnt = int(line.strip())
                    break
            synCnt = snpCnt - nonSynCnt
            base.shell("python /root/compileIndelsToRef.py -i %s -g noSpliceVars.gff -n %s > indelDiffs%d.txt" %(asms[0], quastSnpFiles[i], i + 1))
            with open("indelDiffs%d.txt" %(i + 1)) as handle:
                for line in handle:
                    items = line.strip().split()
                    inFrameCnt = int(items[2])
                    break
            dGenomes[asms[i]].append(("Number of non-synonymous mutations", "%d" %nonSynCnt))
            dGenomes[asms[i]].append(("Number of synonymous mutations", "%d" %synCnt))
            dGenomes[asms[i]].append(("Number of in-frame indels", "%d" %inFrameCnt))
            dGenomes[asms[i]].append(("Number of mutated proteins", "%d" %len(modPtsIds)))
        else:
            base.shell("gffread noSpliceVars.gff -g %s -x scafs.snpref.cds.fa" %asms[0])
            base.shell("gffread noSpliceVars.gff -g %s -y scafs.snpref.pts.fa" %asms[0])
            dGenomes[asms[i]].append(("Number of non-synonymous mutations", '0'))
            dGenomes[asms[i]].append(("Number of synonymous mutations", '0'))
            dGenomes[asms[i]].append(("Number of in-frame indels", '0'))
            dGenomes[asms[i]].append(("Number of mutated proteins", '0'))

    dMetrics = {}
    print "Metrics\t%s" %'\t'.join(genomeLabels)
    for metricName in metricOrder:
        dMetrics[metricName] = []
    for i in xrange(len(asms)):
        for j in xrange(len(dGenomes[asms[i]])):
            metricName, metric = dGenomes[asms[i]][j]
            dMetrics[metricName].append(metric)
    for metricName in metricOrder:
        print "%s\t%s" %(metricName, '\t'.join(dMetrics[metricName]))


#################################################
if __name__ == "__main__":
    main()
