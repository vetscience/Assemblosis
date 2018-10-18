#! /usr/bin/env python

'''
Can read tree structure from .keg files:
E.g. ko00194.keg

'''
import sys
from tree import Tree

class Gene:
    '''
    '''
    def __init__(self, scafId, geneId, start, end, strand):
        '''
        '''
        self.type = "gene"
        self.id = geneId
        self.start, self.end = start, end
        self.scafId = scafId
        self.strand = strand

class Mrna:
    '''
    '''
    def __init__(self, geneId, start, end, strand, aed, eAed, qi):
        '''
        '''
        self.type = "mRNA"
        self.id = geneId
        self.start, self.end = start, end
        self.strand = strand
        self.aed, self.eAed, self.qi = aed, eAed, qi

class ExonUnique:
    '''
    '''
    def __init__(self, exonId, start, end):
        '''
        '''
        self.type = "exonUnique"
        self.id = exonId
        self.start, self.end = start, end


class Exon:
    '''
    '''
    def __init__(self, exonId, start, end, strand):
        '''
        '''
        self.type = "exon"
        self.id = exonId
        self.start, self.end = start, end
        self.strand = strand


class Intron:
    '''
    '''
    def __init__(self, intronId, start, end):
        '''
        '''
        self.type = "intron"
        self.id = intronId
        self.start, self.end = start, end


class Cds:
    '''
    '''
    def __init__(self, cdsId, start, end, strand, offset):
        '''
        '''
        self.type = "cds"
        self.id = cdsId
        self.start, self.end = start, end
        self.strand = strand
        self.offset = offset


class CdsUnique:
    '''
    '''
    def __init__(self, cdsId, start, end):
        '''
        '''
        self.type = "cdsUnique"
        self.id = cdsId
        self.start, self.end = start, end


#####################################################
class WbTree(Tree):
    '''
    '''
    #################################################
    def __init__(self, label = "Genome", myObject = None):
        '''
        '''
        Tree.__init__(self, label, myObject)
        self.exonCnt, self.intronCnt, self.cdsCnt = 0, 0, 0
        self.splices = True # Print out splicing variants by default

    #################################################
    def _createIntrons(self, geneParent, dExons):
        ''' geneParent is the tree node to add the introns to
        '''
        dSeq = {}
        start, end = geneParent.object.start, geneParent.object.end
        for i in xrange(start, end + 1): dSeq[i] = 0
        for mRnaId in dExons.iterkeys(): # Fetch coordinates from all mRNAs
            for exon in dExons[mRnaId]:
                for i in xrange(exon.start, exon.end + 1): dSeq[i] = 1
        idxs = sorted(dSeq.iterkeys())
        if idxs[0] == 0 or idxs[-1] == 0:
            print "Exons expected at the ends of the genes. Exiting..."
            sys.exit(0)
        inIntron = False
        exonStart, exonEnd = geneParent.object.start, 0
        for i in idxs:
            if dSeq[i] == 0 and inIntron == False:
                inIntron, start = True, i # Concerns introns
                exonEnd = i - 1
                self.exonCnt += 1
                exonId = "Exon%d" %self.exonCnt
                exon = ExonUnique(exonId, exonStart, exonEnd)
                self.addChild(geneParent, exonId, exon)
            if dSeq[i] == 1 and inIntron == True:
                inIntron, end = False, i - 1
                self.intronCnt += 1
                intronId = "Intron%d" %self.intronCnt
                #print "%s\t%d\t%d" %(intronId, start, end)
                intron = Intron(intronId, start, end)
                self.addChild(geneParent, intronId, intron)
                exonStart = i # Concerns exons
        exonEnd = geneParent.object.end
        self.exonCnt += 1
        exonId = "Exon%d" %self.exonCnt
        exon = ExonUnique(exonId, exonStart, exonEnd)
        self.addChild(geneParent, exonId, exon)
        
    #################################################
    def _createUniqueCdss(self, geneParent, dCdss):
        ''' geneParent is the tree node to add the CDSs to
        '''
        dSeq = {}
        start, end = geneParent.object.start, geneParent.object.end
        for i in xrange(start, end + 1): dSeq[i] = 0
        for mRnaId in dCdss.iterkeys(): # Fetch coordinates from all mRNAs
            for cds in dCdss[mRnaId]:
                for i in xrange(cds.start, cds.end + 1): dSeq[i] = 1
        # Create intron object
        idxs = sorted(dSeq.iterkeys())
        inIntron, start = False, 0
        cdsStart, cdsEnd = geneParent.object.start, 0
        for i in xrange(len(idxs)):
            if dSeq[idxs[i]] == 1:
                cdsStart = idxs[i]
                start = i
                break
        for i in idxs[start:]:
            if dSeq[i] == 0 and inIntron == False:
                inIntron, start = True, i # Concerns introns
                cdsEnd = i - 1
                self.cdsCnt += 1
                cdsId = "Cds%d" %self.cdsCnt
                cds = CdsUnique(cdsId, cdsStart, cdsEnd)
                self.addChild(geneParent, cdsId, cds)
            if dSeq[i] == 1 and inIntron == True:
                inIntron, end = False, i - 1
                cdsStart = i # Concerns CDSs
        if dSeq[idxs[-1]] == 1:
            cdsEnd = geneParent.object.end
            self.cdsCnt += 1
            cdsId = "Cds%d" %self.cdsCnt
            cds = CdsUnique(cdsId, cdsStart, cdsEnd)
            self.addChild(geneParent, cdsId, cds)

        
    #################################################
    def parse(self, makerGffFilename, createAggregates = True):
        '''
        '''
        dMrnas, dExons, dCdss = {}, {}, {}
        geneParent = None
        handle = open(makerGffFilename, 'r')
        root = self.root
        for line in handle:
            items = line.strip().split('\t')
            if len(items) > 1:
                if len(items) > 2 and items[2] == "gene":
                    geneId = items[8].split(';')[0].split('=')[1]
                    start, end = int(items[3]), int(items[4])
                    strand = items[6]
                    scafId = items[0]
                    gene = Gene(scafId, geneId, start, end, strand)
                    if geneParent != None and createAggregates == True:
                        self._createIntrons(geneParent, dExons)
                        self._createUniqueCdss(geneParent, dCdss)
                    geneParent = self.addChild(root, geneId, gene)
                    dMrnas, dExons, dCdss = {}, {}, {}
                    mRnaParent = None
                elif len(items) > 2 and items[2] == "mRNA":
                    mRnaId = items[8].split(';')[0].split('=')[1]
                    aed, eAed, qi = "-", "-", "-"
                    start, end = int(items[3]), int(items[4])
                    strand = items[6]
                    mRna = Mrna(mRnaId, start, end, strand, aed, eAed, qi)
                    mRnaParent = self.addChild(geneParent, mRnaId, mRna)
                    dMrnas[mRnaId] = mRnaParent # Add mRNA identifier to sort exons right
                    dExons[mRnaId] = [] # Repository for exons to sort introns out
                    dCdss[mRnaId] = [] 
                elif len(items) > 2 and items[2] == "exon":
                    if mRnaParent == None: continue
                    exonId = items[8].split(';')[0].split('=')[1]
                    parentIds = []
                    # Next line is needed only for the rare case of exon line not having parent info
                    try:
                        parentIds.append(mRnaParent.label)
                    except UnboundLocalError:
                        continue
                    subItems = items[8].split(';')
                    if len(subItems[1]) > 1:
                        try:
                            parentIds = subItems[1].split('=')[1].split(',')
                        except IndexError:
                            print >> sys.stderr, "FATAL ERROR 1: %s" %line
                            print >> sys.stderr, subItems
                            sys.exit(0)
                    start, end = int(items[3]), int(items[4])
                    strand = items[6]
                    exon = Exon(exonId, start, end, strand)
                    for parentId in parentIds: # Add exon to all mRNAs which are parents to the exon
                        try:
                            mRnaParent = dMrnas[parentId]
                        except KeyError:
                            print >> sys.stderr, "FATAL ERROR 2: %s" %line
                            print >> sys.stderr, mRnaParent
                            print >> sys.stderr, parentIds
                            sys.exit(0)
                        self.addChild(mRnaParent, exonId, exon)
                        dExons[parentId].append(exon) # Introns can be deducted from this information
                elif len(items) > 2 and items[2] == "CDS":
                    if mRnaParent == None: continue
                    cdsId = items[8].split(';')[0].split('=')[1]
                    parentIds.append(mRnaParent.label)
                    subItems = items[8].split(';')
                    if len(subItems[1]) > 1:
                        try:
                            parentIds = subItems[1].split('=')[1].split(',')
                        except IndexError:
                            print >> sys.stderr, "FATAL ERROR 3: %s" %line
                            print >> sys.stderr, subItems
                            sys.exit(0)
    
                    start, end = int(items[3]), int(items[4])
                    strand, offset = items[6], items[7]
                    cds = Cds(cdsId, start, end, strand, offset)
                    for parentId in parentIds: # Add CDS to all mRNAs which are parents to the CDS
                        try:
                            mRnaParent = dMrnas[parentId]
                        except KeyError:
                            print >> sys.stderr, "FATAL ERROR 4: %s" %line
                            print >> sys.stderr, mRnaParent
                            print >> sys.stderr, parentIds
                            sys.exit(0)
                        self.addChild(mRnaParent, cdsId, cds)
                        dCdss[parentId].append(cds) # CDS introns can be deducted from this information
                elif len(items) > 2 and (items[2] in ["pseudogene", "transcript", "tRNA", "snoRNA", "region"]):
                    mRnaParent = None
        if geneParent != None and createAggregates == True:
            self._createIntrons(geneParent, dExons)
            self._createUniqueCdss(geneParent, dCdss)
        handle.close()


    #################################################
    def createScafs(self, makerGffFilename):
        ''' Creates scaffold sequences and fills in exon areas in there
        '''
        handle = open(makerGffFilename)
        fastaFound, scafId, scafLen = False, None, 0
        dScafs = {}
        for line in handle:
            if line[0] == ">":
                if fastaFound == True:
                    dScafs[scafId] = [0 for i in xrange(scafLen)]
                fastaFound = True
                scafId, scafLen = line[1:].strip(), 0
            if fastaFound == True:
                scafLen += len(line.strip())
        handle.close()

        scafId = None
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                scafId = item.scafId
            if item.type == "exon":
                start, end = item.start, item.end
                seq = dScafs[scafId]
                for i in xrange(start, end + 1):
                    seq[i] = 1
        return dScafs

    #################################################
    def splicingVars(self, switch = True):
        '''
        '''
        self.splices = switch        


    #################################################
    def __repr__(self):
        '''
        '''
        myStr = ""
        geneId, mRnaId, scafId = None, None, None
        mRnas, dExons, dCdss = [], {}, {}
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                if len(mRnas) > 0:
                    for mRna in sorted(mRnas, key = lambda item: item.id):
                        myStr += "%s\tmaker\tmRNA\t%d\t%d\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" %(scafId, mRna.start, mRna.end, mRna.strand, mRna.id, geneId, mRna.id)
                        sortedExons = sorted(dExons[mRna.id], key = lambda item: item.start)
                        if mRna.strand == '-': sortedExons = sortedExons[::-1]
                        for exon in sortedExons:
                            myStr += "%s\tmaker\t%s\t%d\t%d\t.\t%s\t.\tID=%s;Parent=%s\n" %(scafId, exon.type, exon.start, exon.end, exon.strand, exon.id, mRna.id)
                        sortedCdss = sorted(dCdss[mRna.id], key = lambda item: item.start)
                        if mRna.strand == '-': sortedCdss = sortedCdss[::-1]
                        for cds in sortedCdss:
                            myStr += "%s\tmaker\tCDS\t%d\t%d\t.\t%s\t%s\tID=%s;Parent=%s\n" %(scafId, cds.start, cds.end, cds.strand, cds.offset, cds.id, mRna.id)
                        if self.splices == False: break # Print out only first mRNA
                mRnas, dExons, dCdss = [], {}, {}
                geneId, scafId = item.id, item.scafId
                myStr += "%s\tmaker\t%s\t%d\t%d\t.\t%s\t.\tID=%s;Name=%s\n" %(item.scafId, item.type, item.start, item.end, item.strand, item.id, item.id)
            if item.type == "mRNA":
                mRnaId = item.id
                mRnas.append(item)
            if item.type == "exon":
                try:
                    dExons[mRnaId].append(item)
                except KeyError:
                    dExons[mRnaId] = []
                    dExons[mRnaId].append(item)
            if item.type == "cds":
                try:
                    dCdss[mRnaId].append(item)
                except KeyError:
                    dCdss[mRnaId] = []
                    dCdss[mRnaId].append(item)
        if len(mRnas) > 0:
            for mRna in sorted(mRnas, key = lambda item: item.id):
                myStr += "%s\tmaker\tmRNA\t%d\t%d\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" %(scafId, mRna.start, mRna.end, mRna.strand, mRna.id, geneId, mRna.id)
                sortedExons = sorted(dExons[mRna.id], key = lambda item: item.start)
                if mRna.strand == '-': sortedExons = sortedExons[::-1]
                for exon in sortedExons:
                    myStr += "%s\tmaker\t%s\t%d\t%d\t.\t%s\t.\tID=%s;Parent=%s\n" %(scafId, exon.type, exon.start, exon.end, exon.strand, exon.id, mRna.id)
                sortedCdss = sorted(dCdss[mRna.id], key = lambda item: item.start)
                if mRna.strand == '-': sortedCdss = sortedCdss[::-1]
                for cds in sortedCdss:
                    myStr += "%s\tmaker\tCDS\t%d\t%d\t.\t%s\t%s\tID=%s;Parent=%s\n" %(scafId, cds.start, cds.end, cds.strand, cds.offset, cds.id, mRna.id)
        return myStr.strip()
        

    #################################################
    def _fixGaps(self, genes, poss, dNs):
        '''
        '''
        # Fixing splicing variants (transcripts and CDSs)
        for item in poss:
            geneItem, mRnaItem, sExon, eExon, sCds, eCds = item[0], item[1], item[2], item[3], item[4], item[5]
            frontCnt, backCnt = dNs[mRnaItem.id]
            print >> sys.stderr, "## %s: %s (%d, %d) %s" %(geneItem.id, mRnaItem.id, frontCnt, backCnt, mRnaItem.strand)
            mRnaFirst, cdsFirst = int(sExon.start), int(sCds.start)
            mRnaLast, cdsLast = int(eExon.end), int(eCds.end)
            if mRnaItem.strand == '+':
                mRnaFirst += frontCnt
                delta = int(frontCnt / 3) * 3 + 3
                if cdsFirst - mRnaFirst < 0: cdsFirst += delta
                mRnaLast -= backCnt
                if mRnaLast - cdsLast < 0: cdsLast -= delta
            else:
                mRnaFirst += backCnt
                delta = int(backCnt / 3) * 3 + 3
                if cdsFirst - mRnaFirst < 0: cdsFirst += delta
                mRnaLast -= frontCnt
                if mRnaLast - cdsLast < 0: cdsLast -= delta
            mRnaItem.start, mRnaItem.end = mRnaFirst, mRnaLast
            sExon.start, eExon.end, sCds.start, eCds.end = mRnaFirst, mRnaLast, cdsFirst, cdsLast # This is the fix
        trStart, trEnd = None, None
        # Checking the gene limits (if having more splicing variants)
        for item in genes:
            geneItem, mRnaItem, sExon, eExon, sCds, eCds = item[0], item[1], item[2], item[3], item[4], item[5]
            mRnaFirst, mRnaLast = int(mRnaItem.start), int(eExon.end)
            if trStart == None or mRnaFirst < trStart: trStart = mRnaFirst
            if trEnd == None or mRnaLast > trEnd: trEnd = mRnaLast
        geneItem.start, geneItem.end = trStart, trEnd


    #################################################
    def findAndFixPoss(self, dNs):
        '''
        '''
        dMrnas, dGene = {}, {}
        found = False
        exons, cdss = [], []
        genes, poss = [], []
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                if len(poss) > 0: # Fix the changes
                    self._fixGaps(genes, poss, dNs)
                geneItem = item
                genePos = "%s-%s" %(item.start, item.end)
                dGene = node.dict # Anchor point for positional changes in exons and CDSs
                dMrnas = {}
                for mRnaId in sorted([node.dict[key].label for key in node.dict.iterkeys() if node.dict[key].object.type == "mRNA"]):
                    dMrnas[mRnaId] = True
                found = False
                for mRnaId in dNs.iterkeys():
                    try:
                        dMrnas[mRnaId]
                        found = True
                    except KeyError:
                        pass
                genes, poss = [], []
            if item.type == "mRNA":
                if found == True:
                    mRnaId = item.id
                    exons = sorted([node.dict[key].object for key in node.dict.iterkeys() if node.dict[key].object.type == "exon"], key=lambda exon: exon.start)
                    cdss = sorted([node.dict[key].object for key in node.dict.iterkeys() if node.dict[key].object.type == "cds"], key=lambda exon: exon.start)
                    sExon, eExon = exons[0], exons[-1]
                    sCds, eCds = cdss[0], cdss[-1]
                    genes.append((geneItem, item, sExon, eExon, sCds, eCds))
                    try:
                        dNs[mRnaId]
                        poss.append((geneItem, item, sExon, eExon, sCds, eCds))
                    except KeyError:
                        pass
        if len(poss) > 0: # Fix the changes
            self._fixGaps(genes, poss, dNs)

    ######################
    def rmShortIntrons(self, lenLimit, dMrnasPreserve, preserveOne = True):
        ''' Removes the genes and/or splicing variants having short introns.
            Not valid: First splicing variant is preserved if preserveOne is True, otherwise they are all removed.
        '''
        # Read in the GFF file to clarify the relationships between geneIds and mRnaIds
        dGeneIds, geneId = {}, None
        dExons = {}
        dShortIntronsMrna = {}
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                geneId = item.id
                dGeneIds[geneId] = []
            if item.type == "mRNA":
                mRnaId = item.id
                dGeneIds[geneId].append(mRnaId)
                exons = sorted([node.dict[key].object for key in node.dict.iterkeys() if node.dict[key].object.type == "exon"], key=lambda exon: exon.start)
                dExons[mRnaId] = exons
                prevEnd = None
                for exon in exons:
                    if prevEnd != None:
                        if abs(int(exon.start) - prevEnd) - 1 < lenLimit:
                            dShortIntronsMrna[mRnaId] = True
                            break
                    prevEnd = int(exon.end)
    
        dMrnaIds = {}
        for geneId in dGeneIds:
            for mRnaId in dGeneIds[geneId]:
                dMrnaIds[mRnaId] = geneId
    
        preserveGeneIds = set()
        print >> sys.stderr, "## Preserving %d mRNAs when removing introns" %len(list(dMrnasPreserve.iterkeys()))
        for mRnaId in dMrnasPreserve.iterkeys():
            try:
                geneId = dMrnaIds[mRnaId]
                preserveGeneIds.add(geneId)
            except KeyError:
                pass
        print >> sys.stderr, "## Preserving %d mRNAs when removing introns" %len(preserveGeneIds)
        rmGeneIds = set()
        for mRnaId in dShortIntronsMrna.iterkeys():
            geneId = dMrnaIds[mRnaId]
            rmGeneIds.add(geneId)
        rmMrnaLabels = set(rmGeneIds) - set(preserveGeneIds)
        rmFinal = set()
        for geneId in rmMrnaLabels: # Remove genes, which are non in list of preserved gene ids
            rmFinal.add(geneId)
        for mRnaId in dShortIntronsMrna.iterkeys():
            geneId = dMrnaIds[mRnaId]
            if preserveOne == False:
                rmFinal.add(geneId)

        print >> sys.stderr, "# mRNA count having short introns: %d" %len(list(dShortIntronsMrna.iterkeys()))
        genes = set()
        for mRnaId in dShortIntronsMrna.iterkeys():
            genes.add(dMrnaIds[mRnaId])
        print >> sys.stderr, "# Gene count having Short introns: %d" %len(genes)
        genes = set()
        for myId in rmFinal:
             try:
                 genes.add(dMrnaIds[myId])
             except KeyError:
                 pass
             try:
                 dGeneIds[myId]
                 genes.add(myId)
             except KeyError:
                 pass
        print >> sys.stderr, "# Gene count having short introns to remove: %d" %len(genes)
        self.rmNodes(rmFinal)


    ######################
    def rmShortExons(self, lenLimit, dMrnasPreserve, preserveAll = True):
        ''' Removes the genes and/or splicing variants having short exons.
            Splicing variants are preserved if preserveAll is True, otherwise they are all removed.
        '''
        dGeneIds, geneId = {}, None
        dExons = {}
        dShortExonsMrna = {}
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                geneId = item.id
                dGeneIds[geneId] = []
            if item.type == "mRNA":
                mRnaId = item.id
                dGeneIds[geneId].append(mRnaId)
                exons = sorted([node.dict[key].object for key in node.dict.iterkeys() if node.dict[key].object.type == "exon"], key=lambda exon: exon.start)
                dExons[mRnaId] = exons
                for exon in exons:
                    if abs(int(exon.end) - int(exon.start)) + 1 < lenLimit:
                        dShortExonsMrna[mRnaId] = True
                        break
    
        dMrnaIds = {}
        for geneId in dGeneIds:
            for mRnaId in dGeneIds[geneId]:
                dMrnaIds[mRnaId] = geneId
    
        preserveGeneIds = set()
        print >> sys.stderr, "## Preserving %d mRNAs when removing exons" %len(list(dMrnasPreserve.iterkeys()))
        for mRnaId in dMrnasPreserve.iterkeys():
            try:
                geneId = dMrnaIds[mRnaId]
                preserveGeneIds.add(geneId)
            except KeyError:
                pass
        print >> sys.stderr, "## Preserving %d mRNAs when removing exons" %len(preserveGeneIds)
        rmGeneIds = set()
        for mRnaId in dShortExonsMrna.iterkeys():
            geneId = dMrnaIds[mRnaId]
            rmGeneIds.add(geneId)
        rmMrnaLabels = set(rmGeneIds) - set(preserveGeneIds)
        print >> sys.stderr, "## Remove (%d), preserve (%d) and final remove (%d) gene ids." %(len(rmGeneIds), len(preserveGeneIds), len(rmMrnaLabels))
        rmFinal = set()
        for geneId in rmMrnaLabels:
            rmFinal.add(geneId)
        for mRnaId in dShortExonsMrna.iterkeys():
            geneId = dMrnaIds[mRnaId]
            if preserveAll == False:
                rmFinal.add(geneId)

        print >> sys.stderr, "# mRNA count having short exons: %d" %len(list(dShortExonsMrna.iterkeys()))
        genes = set()
        for mRnaId in dShortExonsMrna.iterkeys():
            genes.add(dMrnaIds[mRnaId])
        print >> sys.stderr, "# Gene count having short exons: %d" %len(genes)
        genes = set()
        for myId in rmFinal:
             try:
                 genes.add(dMrnaIds[myId])
             except KeyError:
                 pass
             try:
                 dGeneIds[myId]
                 genes.add(myId)
             except KeyError:
                 pass
        print >> sys.stderr, "# Gene count having short exons to remove: %d" %len(genes)
        self.rmNodes(rmFinal)


    ######################
    def rmVars(self, longest = False):
        ''' Preserve the first or the longest one.
        '''
        dGeneIds, geneId = {}, None
        dExons = {}
        for node in self.depthFirst():
            item = node.object
            if item == None: continue
            if item.type == "gene":
                geneId = item.id
                dGeneIds[geneId] = []
            if item.type == "mRNA":
                mRnaId = item.id
                dGeneIds[geneId].append(mRnaId)
                exons = sorted([node.dict[key].object for key in node.dict.iterkeys() if node.dict[key].object.type == "exon"], key=lambda exon: exon.start)
                dExons[mRnaId] = exons
                mRnaLen = 0
                for exon in exons:
                    mRnaLen += abs(int(exon.end) - int(exon.start)) + 1
                dExons[mRnaId] = mRnaLen
    
        dMrnaIds = {}
        for geneId in dGeneIds:
            for mRnaId in dGeneIds[geneId]:
                dMrnaIds[mRnaId] = geneId
    
        rmLabels = []
        for geneId in dGeneIds.iterkeys():
            if len(dGeneIds[geneId]) == 0: rmLabels.append(geneId)
            if len(dGeneIds[geneId]) > 1:
                myList = sorted(dGeneIds[geneId])
                if longest == False:
                    for item in myList[1:]:
                        rmLabels.append(item)
                else:
                    lens = [dExons[mRnaId] for mRnaId in myList]
                    maxIdx = lens.index(max(lens))
                    for i in xrange(len(myList)):
                        if i != maxIdx: rmLabels.append(myList[i])
        self.rmNodes(rmLabels)
