#########################################
##       Written by Dale Julson        ##
##     Dale.A.Julson@Vanderbilt.edu    ##
##     feel free to modify as needed   ##
#########################################

## This script can be used to make +1sigma/-1sigma variation plots.
## This is useful when performing systematic uncertainty studies.

import ROOT
import array

name  = "Pile_UP/tbar.root" #Input root file or path to root file here.
output = "Pile_UP/tbar_Systematic_output.root" #This will be the output root file that you will open with a TBrowser.
systematic = "Pileup_weight" #This will be the title of the systematic. Jet_Scale, Pileup_weight, Jet_Res
plot_name = "largest m(jj) [GeV]" #This will be the plot name in the lower right.
upper_left_title = "Systematic: Pile Up" #This will be the title in the upper left.
upper_right_title = "TTBar (2016)" #This will be the title in the upper right. Virtual WZ, m(N2) 300 GeV, dM 50 GeV

orig_histo_name = "orig/LargestDiJetMass"
up_histo_name = systematic + "_Up/LargestDiJetMass"
down_histo_name = systematic + "_Down/LargestDiJetMass"

srbinedges = array.array('d',[500,750,1000,1500,2000,2500,5000])
nbins = len(srbinedges)-1

input_root_file = ROOT.TFile.Open(name,"UPDATE")
output_root_file = ROOT.TFile.Open(output,"RECREATE")

orig_histo = input_root_file.Get(orig_histo_name)
up_histo = input_root_file.Get(up_histo_name)
down_histo = input_root_file.Get(down_histo_name)

orig_histo.SetLineColor(ROOT.kBlue)
orig_histo.SetMarkerStyle(20)
orig_histo.SetMarkerColor(ROOT.kBlue)
up_histo.SetLineColor(ROOT.kGreen-2)
up_histo.SetMarkerStyle(25)
up_histo.SetMarkerColor(ROOT.kGreen-2)
down_histo.SetLineColor(ROOT.kOrange-3)
down_histo.SetMarkerStyle(46)
down_histo.SetMarkerColor(ROOT.kOrange-3)

rebinned_orig = orig_histo.Clone()
rebinned_up = up_histo.Clone()
rebinned_down = down_histo.Clone()

rebinned_orig = rebinned_orig.Rebin(nbins, "rebinned_orig", srbinedges)
rebinned_up = rebinned_up.Rebin(nbins, "rebinned_up", srbinedges)
rebinned_down = rebinned_down.Rebin(nbins, "rebinned_down", srbinedges)


normalized_orig = rebinned_orig.Clone()
normalized_up = rebinned_up.Clone()
normalized_down = rebinned_down.Clone()

normalized_orig.Scale(1/normalized_orig.Integral(-10000,10000))
normalized_up.Scale(1/normalized_up.Integral(-10000,10000))
normalized_down.Scale(1/normalized_down.Integral(-10000,10000))

c = ROOT.TCanvas("","",600,500)
c.Draw()


top_pad = ROOT.TPad("top", "top", 0, 0.25, 1, 1, 0)
top_pad.SetLogy()
top_pad.SetGrid(1,0)
top_pad.SetBottomMargin(-1)
top_pad.Draw()
top_pad.cd()

hs = ROOT.THStack()
hs.Add(normalized_orig)
hs.Add(normalized_up)
hs.Add(normalized_down)
hs.Draw("NOSTACK")
hs.GetYaxis().SetTitle("a.u.")
hs.GetYaxis().SetTitleOffset(0.5)
hs.GetYaxis().SetTitleSize(0.05)
hs.GetXaxis().SetLabelSize(0.035)

legend = ROOT.TLegend(0.75,0.65,0.88,0.85)
legend.SetBorderSize(0)
legend.Draw()
legend.AddEntry(normalized_orig, "nominal")
legend.AddEntry(normalized_up, "shift up")
legend.AddEntry(normalized_down, "shift down")

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

c.cd(0)
bottom_pad = ROOT.TPad("bottom", "bottom", 0, 0.0, 1, 0.28, 0)
bottom_pad.SetGrid(1,1)
bottom_pad.SetTitle("")
bottom_pad.SetTopMargin(0.05)
bottom_pad.SetBottomMargin(0.25)
bottom_pad.Draw()
bottom_pad.cd()

unity = [1 for i in range(len(srbinedges)-1)]
zeroes = [0 for i in range(len(srbinedges)-1)]
bin_location = []
nominal_error = []
x_error = []
y_error = []
up_over_nominal = []
down_over_nominal = []

for i in range(nbins):
    j=i+1
    nominal_bin_content = rebinned_orig.GetBinContent(j)
    if (nominal_bin_content < 0.0000000001):
        nominal_error.append(0)
        up_over_nominal.append(0)
        down_over_nominal.append(0)
    else:
        nominal_error.append((rebinned_orig.GetBinError(j))/(rebinned_orig.GetBinContent(j)))
        up_over_nominal.append((rebinned_up.GetBinContent(j)/rebinned_orig.GetBinContent(j)))
        down_over_nominal.append((rebinned_down.GetBinContent(j)/rebinned_orig.GetBinContent(j)))
    bin_location.append(rebinned_orig.GetBinCenter(j))
    x_error.append(rebinned_orig.GetBinWidth(j)*0.5)
    

unity = array.array('d', unity)
zeroes = array.array('d', zeroes)
bin_location = array.array('d', bin_location)
nominal_error = array.array('d', nominal_error)
x_error = array.array('d', x_error)
y_error = array.array('d', y_error)
up_over_nominal = array.array('d', up_over_nominal)
down_over_nominal = array.array('d', down_over_nominal)

ratio_plot = ROOT.TGraphErrors(nbins,bin_location,unity,x_error,nominal_error)
ratio_plot.GetXaxis().SetRangeUser(min(srbinedges),max(srbinedges))
ratio_plot.GetXaxis().SetTitle(plot_name)
ratio_plot.GetXaxis().SetTitleSize(0.1)
ratio_plot.GetYaxis().SetTitle("Ratio")
ratio_plot.GetYaxis().SetTitleOffset(0.35)
ratio_plot.GetYaxis().SetTitleSize(0.1)
ratio_plot.SetTitle("")
ratio_plot.SetLineWidth(1)
ratio_plot.SetFillColor(ROOT.kMagenta+1)
ratio_plot.SetFillStyle(3002)
ratio_plot.GetXaxis().SetLabelSize(0.10)
ratio_plot.GetYaxis().SetLabelSize(0.10)
ratio_plot.Draw("a2")

line = ROOT.TLine(min(srbinedges),1,max(srbinedges),1)
line.SetLineColor(2)
line.SetLineWidth(1)
line.Draw("same")

ratio_plot_up = ROOT.TGraphErrors(nbins,bin_location,up_over_nominal,zeroes,zeroes)
ratio_plot_up.SetLineColor(ROOT.kGreen-2)
ratio_plot_up.SetMarkerStyle(21)
ratio_plot_up.SetMarkerColor(ROOT.kGreen-2)
ratio_plot_up.Draw("same P")

ratio_plot_down = ROOT.TGraphErrors(nbins,bin_location,down_over_nominal,zeroes,zeroes)
ratio_plot_down.SetLineColor(ROOT.kOrange-3)
ratio_plot_down.SetMarkerStyle(47)
ratio_plot_down.SetMarkerColor(ROOT.kOrange-3)
ratio_plot_down.Draw("same P")

output_root_file.cd()
c.Write()

input_root_file.Purge()
input_root_file.Close()
output_root_file.Close()
