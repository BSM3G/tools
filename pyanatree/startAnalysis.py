#! /usr/bin/env python
from analysis import *
import os
import multiprocessing
import optparse
from datetime import datetime


def getSampleInfo(configfile):
    lumi=1.
    sampleInfo={}

    with open(configfile) as configFile:
        for line in configFile:
            if line[0]=="#" or line[0:1]=="//":
                continue
            elif "luminosity" in line:
                lumi=float(line.split()[1])
                continue
            elif ".root" in line and "output" not in line:
                tmp=line.strip().split()
                if(len(tmp)<2):
                    continue
                sample=tmp[0]
                sampleCombine=tmp[1]
                if "Data" in sampleCombine:
                    sampleInfo[sample]={
                                        "output":sampleCombine,
                                        "lumi":1.,
                                        "xs":1.,
                                        "eff":1.,
                                        "type":"data",
                                        }
                elif(len(tmp)>4):
                    sampleInfo[sample]={
                                        "output":sampleCombine,
                                        "lumi":lumi,
                                        "xs":float(tmp[2]),
                                        "eff":float(tmp[3]),
                                        "type":tmp[4],
                                        }
    return sampleInfo


def worker(item):
    infiles, outfile, info, treeName=item
    ana=Analysis(infiles, outfile, info, treeName)
    ana.loop()

def main():

    date_time = datetime.now()
    usage = '%prog [options]'
    parser = optparse.OptionParser( usage = usage )
    parser.add_option( '-c', '--config', default = "CONFIG_FILE",
                            help = 'which configfile do you want to run over')
    parser.add_option( '-i', '--infile', default = '', metavar = 'in',
                            help = 'Define the input directory. [default = %default]')
    parser.add_option( '-o', '--out', default = "output%s_%s_%s_%s_%s"%(date_time.year,
                                                                        date_time.month,
                                                                        date_time.day,
                                                                        date_time.hour,
                                                                        date_time.minute), metavar = 'DIRECTORY',
                            help = 'Define name of the output folder [default = %default]')
    parser.add_option('-j','--parallel', default=multiprocessing.cpu_count(),
                            help = "set the number of parallel processes. [default= %default]")
    parser.add_option('-t','--tree', default="METCut/zboost",
                            help = "set the tree you want to process. [default= %default]")

    ( options, args ) = parser.parse_args()
    if len( args ) >= 1:
        options.config=args[0]

    if options.config=="CONFIG_FILE" and options.infile=="":
        parser.error( 'Exactly one CONFIG_FILE required!' )

    if options.infile=="":
        sampleInfo=getSampleInfo(options.config)
    else:
        #dummy info
        sampleInfo={}
        sampleInfo[options.infile]={
                                        "output":"dummy.root",
                                        "lumi":1.,
                                        "xs":1.,
                                        "eff":1.,
                                        "type":"bg",
                                        }

    if not os.path.exists(options.out):
        os.makedirs(options.out)
    #do some multiprocessing
    q=[]
    for sample,info in sampleInfo.items():
        outfile=os.path.join(options.out,info["output"])
        infile=sample
        q.append([infile, outfile, info,options.tree])
    if int(options.parallel)>1:
        pool = multiprocessing.Pool(int(options.parallel))
        result = pool.map_async(worker, q)
        result.wait()
        pool.close()
        while pool._cache:
            time.sleep(1)
        res = result.get()
    else:
        for i in q:
            worker(i)







if __name__ == '__main__':
    main()
