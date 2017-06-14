#! /usr/bin/env python

import ROOT
import sys

from math import sin,sqrt,acos,sin,cos
from numpy import fabs
from array import array
from rootpy.io import root_open
from rootpy.tree import TreeChain


# Create histograms, etc.
ROOT.gROOT.SetBatch()        # don't pop up canvases

class Analysis(object):
    def __init__(self, infile, outfile, info,treeName):
        if type(infile)==type([]):
            self.inFile=infile
        else:
            self.inFile=[infile]
        self.outfile=outfile
        self.sampleInfo=info
        self.treeName=treeName
        self.plots={}
        self.profiles={}
        self.weight=1.

        #some examples
        self.CreateHisto(0,"chargeStudy",["qMt","mDM"],[10000,5000],[-5000,0],[5000,5000])

        for i in range(2):
            self.CreateProfile(i,"test_profile","x-axis","y-axis",100,0,100)
            self.CreateHisto1D(i,"jet_mass","M [GeV]",10000,0,10000)
            self.CreateHisto1D(i,"zp_mass","M [GeV]",10000,0,10000)
            self.CreateHisto1D(i,"zp_pt","p_{T} (Z') [GeV]",10000,0,10000)
            self.CreateHisto1D(i,"zp_eta","#eta (Z')",1000,-7,7)
            self.CreateHisto1D(i,"jet_eta","#eta (jet)",1000,-7,7)

    def CreateHisto(self,nhist,name,title,nbin,nmin,nmax):
        if type(title)==type(""):
            self.CreateHisto1D(nhist,name,title,nbin,nmin,nmax)
            return
        if type(nhist)==type(""):
            histString="h%d_%s_%s"
        else:
            histString="h%d_%d_%s"
        tmphist =  ROOT.THnSparseF(histString %(len(nbin),nhist, name), histString %(len(nbin),nhist, name), len(nbin), array("i",nbin), array("d",nmin), array("d",nmax))
        for i in range(len(nbin)):
            tmphist.GetAxis(i).SetTitle(title[i])
        tmphist.Sumw2()
        self.plots.update({histString %(len(nbin),nhist, name): tmphist})

    def CreateHisto1D(self,nhist,name,title,nbin,nmin,nmax):
        tmphist = ROOT.TH1D("h1_%d_%s" %(nhist, name), "h1_%d_%s" %(nhist, name), nbin, nmin, nmax)
        tmphist.SetXTitle(title)
        tmphist.Sumw2()
        self.plots.update({"h1_%d_%s" %(nhist, name): tmphist})

    def CreateProfile(self,nhist,name,xtitle,ytitle,sbin,xmin,xmax):
        if type(nhist)==type(0):
            profieString="p_%d_%s"
        else:
            profieString="p_%s_%s"
        tmphist = ROOT.TProfile(profieString %(nhist, name), profieString %(nhist, name), sbin, xmin, xmax)
        tmphist.SetXTitle(xtitle)
        tmphist.SetYTitle(ytitle)
        tmphist.Sumw2()
        self.profiles.update({profieString %(nhist, name): tmphist})

    def CreateProfile2D(self,nhist,name,xtitle,ytitle,ztitle,xbin,xmin,xmax,ybin,ymin,ymax):
        tmphist = ROOT.TProfile2D("p2_%d_%s" %(nhist, name), "p2_%d_%s" %(nhist, name), xbin, xmin, xmax,ybin,ymin,ymax)
        tmphist.SetXTitle(xtitle)
        tmphist.SetYTitle(ytitle)
        tmphist.SetZTitle(ztitle)
        tmphist.Sumw2()
        self.profiles.update({"p2_%d_%s" %(nhist, name): tmphist})

    ##fill anything that comes in
    def Fill(self,nhist,name,value):

        if type(nhist)==int and "h1_%d_%s" %(nhist, name) in self.plots:
            self.plots["h1_%d_%s" %(nhist, name)].Fill(value,self.weight)
        elif len(value)>1:
            if type(nhist)==str:
                histString="h%d_%s_%s"
            else:
                histString="h%d_%d_%s"
            if histString %(len(value),nhist, name) in self.plots:
                self.plots[histString %(len(value),nhist, name)].Fill(array("d",value),self.weight)
            else:
                print(("hist "+histString%(len(value),nhist, name)+" not in plots" ))
        else:
            print("Strange things happened")

    def Profile(self, nhist, name, x, y):
        if type(nhist)==type(0):
            profieString="p_%d_%s"
        else:
            profieString="p_%s_%s"
        if profieString %(nhist, name) in self.profiles:
            self.profiles[profieString %(nhist, name)].Fill(x,y,self.weight)
        else:
            print((profieString %(nhist, name)), self.profiles)
            print("Strange things happened /\ ")

    def Profile2D(self, nhist, name, x, y, z):
        if "p2_%d_%s" %(nhist, name) in self.profiles:
            self.profiles["p2_%d_%s" %(nhist, name)].Fill(x,y,z,self.weight)
        else:
            print(("p2_%d_%s" %(nhist, name)))
            print("Strange things happened /\ ")

    def getCharge(self,p):
        quarkq=self.chargeMap[fabs(p.pdgId)]
        if (p.pdgId<0):
            quarkq*=-1.
        return quarkq


    def writeFile(self):
        f = ROOT.TFile(self.outfile,"RECREATE")
        f.SetCompressionLevel(9)
        f.cd()
        for i in self.plots:
            #we will do the scaling afterwards
            #self.plots[i].Scale(self.sampleInfo["xs"]*self.sampleInfo["lumi"]*self.sampleInfo["eff"]/self.Nev)
            self.plots[i].Write()
        f.mkdir("profiles","profiles")
        f.cd("profiles")
        for i  in list(self.profiles.values()):
            #no do not scale profiles
            #self.plots[i].Scale(self.sampleInfo["xs"]*self.sampleInfo["lumi"]*self.sampleInfo["eff"]/self.Nev)
            i.Write()
        f.Close()

    def loop(self):

        tree=TreeChain(self.treeName, self.inFile)
        self.Nev=0
        for f in self.inFile:
            tmpf=root_open(f)

            for path, dirs, objects in tmpf.walk():
                if "Events" in objects:
                    evHist=tmpf.Get(path+"/Events")
                    self.Nev+=evHist.GetBinContent(1)
                    break
            tmpf.close()



        counter=0
        for e in tree:
            self.Fill(0,"zp_pt",e.mu1_pt)

            #just profile stuff
            self.Profile( 0, "test_profile",e.mu1_pt , e.mu1_pt/14)
            if(e.mu1_pt>30):
                #make cuts
                self.Fill(1,"zp_pt",e.mu1_pt/15)


        self.writeFile()

