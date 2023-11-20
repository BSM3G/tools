#########################################
##       Written by Dale Julson        ##
##     Dale.A.Julson@Vanderbilt.edu    ##
##     feel free to modify as needed   ##
#########################################

## This script can be used to compare the kinematics of bakground samples to signal samples.
## This is useful when performing optimization studies.

import ROOT
import array

output = "Kinematics_output.root" #This will be the output root file that you will open with a TBrowser.
plot_name = "largest m(jj) [GeV]" #This will be the plot name in the lower right.
upper_left_title = "Upper Left Title" #This will be the title in the upper left.
upper_right_title = "(2016)" #This will be the title in the upper right.
backgrounds = ["tbar.root","Z+Jets.root","W+Jets.root"] #place the background root files to be includded in "Background" here.
signal_name = "mN2_300_dM_30.root" #Place signal ROOt file here
histo_name = "NDiJetCombinations/LargestDiJetMass" #Cut folder and histogram of interest
binEdges = list(range(0,4000,100)) #Rebinning parameters. This says "rebin from 0 to 4000 in steps of 100".

nbins = len(binEdges)-1
rebinnededges = array.array('d',binEdges)

signal_root_file = ROOT.TFile.Open(signal_name,"UPDATE")

opened_root_files = []
for i in backgrounds:
    opened_root_files.append(ROOT.TFile.Open(i,"UPDATE"))

output_root_file = ROOT.TFile.Open(output,"RECREATE")

signal_histo = signal_root_file.Get(histo_name)

opened_histos = []
for i in opened_root_files:
    opened_histos.append(i.Get(histo_name))


signal_histo = signal_histo.Rebin(nbins, "rebinned", rebinnededges)
for indx,elem in enumerate(opened_histos):
    opened_histos[indx] = elem.Rebin(nbins, "rebinned", rebinnededges)

for indx,elem in enumerate(opened_histos):
    if indx == 0:
        pass
    else:
        opened_histos[0].Add(elem)

BG_histo = opened_histos[0]


signal_histo.Scale(1/signal_histo.Integral(-10000,10000))
BG_histo.Scale(1/BG_histo.Integral(-10000,10000))


signal_histo.SetLineColor(ROOT.kBlue)
signal_histo.SetMarkerStyle(20)
signal_histo.SetMarkerColor(ROOT.kBlue)

BG_histo.SetLineColor(ROOT.kGreen-2)
BG_histo.SetMarkerStyle(25)
BG_histo.SetMarkerColor(ROOT.kGreen-2)

c = ROOT.TCanvas(plot_name,plot_name,600,500)
c.Draw()

top_pad = ROOT.TPad("top", "top", 0, 0.05, 1, 1, 0)
top_pad.SetLogy()
# top_pad.SetGrid(1,0)
top_pad.SetBottomMargin(0.1)
top_pad.Draw()
top_pad.cd()

hs = ROOT.THStack()
hs.Add(signal_histo)
hs.Add(BG_histo)
hs.Draw("NOSTACK")
hs.GetYaxis().SetTitle("a.u.")
hs.GetYaxis().SetTitleOffset(1.2)
hs.GetYaxis().SetTitleSize(0.04)
hs.GetXaxis().SetRangeUser(500,5000)
hs.GetXaxis().SetTitle(plot_name)
hs.GetXaxis().SetTitleSize(0.04)

legend = ROOT.TLegend(0.65,0.79,0.88,0.89)
legend.SetBorderSize(0)
legend.Draw()
legend.AddEntry(signal_histo, "signal")
legend.AddEntry(BG_histo, "#sum Background")

pt1 = ROOT.TPaveText(0.76,0.88,0.91,0.98,"NBNDC")
pt1.AddText(upper_right_title)
pt1.SetTextFont(42)
pt1.SetTextAlign(32)
pt1.SetFillStyle(0)
pt1.SetBorderSize(0)
pt1.SetTextSize(0.04)
pt1.Draw()

pt2 = ROOT.TPaveText(0.09,0.88,0.24,0.98,"NBNDC")
pt2.AddText(upper_left_title)
pt2.SetTextFont(42)
pt2.SetTextAlign(12)
pt2.SetFillStyle(0)
pt2.SetBorderSize(0)
pt2.SetTextSize(0.04)
pt2.Draw()


output_root_file.cd()
c.Write()

signal_root_file.Purge()
signal_root_file.Close()

for i in opened_root_files:
        i.Purge()
        i.Close()

output_root_file.Close()
