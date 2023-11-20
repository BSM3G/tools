#########################################
##       Written by Dale Julson        ##
##     Dale.A.Julson@Vanderbilt.edu    ##
##     feel free to modify as needed   ##
#########################################

#########################################
##    This script only procceses one   ##
##    year at a time. For generating   ##
##        "full lumi" plots, see       ##
##        "Full_lumi_plotter.py"       ##
#########################################

## This script can be used to make histograms which corretly propagate scale factor uncertainties

import math, array, argparse
import ROOT as r

output_root_name = "SF_corrected_output.root"

#Set to true if you would like data to be included in the plot
include_Data = True

if (include_Data):

	#Gotta provide the data files if they're going to be run over 
	data_file = "data.root"

#Set to true if you would like to generate Data/MC ratio plots
generate_data_MC_ratio_plot = include_Data and True

#Signal sample will be ignored if set to False. If set to true, provide signal sample info below
include_signal_sample = True

if (include_signal_sample):

	signal_sample_name = "WZ_mN2_300_dM_50"
	signal_file = f"{signal_sample_name}.root"
	signal_name = "#tilde{#chi}_{1}^{0}=300 GeV, #Deltam=50 GeV"

#If True, this will output latex code in the terminal that you can copy and paste into the AN
produce_latex_output = False
verbose_print = False
#If you want the histo saved as a pdf. You can always do this later in a TBrowser
save_as_PDF = False
output_PDF_name = "Signal_region_plot"

#Format is Cut_folder/plot_name
input_plot = "NDiJetCombinations/LargestDiJetMass"

#Provide the desired binning below:
srbinedges = array.array('d',[500,750,1000,1500,2000,2500,5000])
nBins = len(srbinedges)-1

upper_left_title = "OS #mu#mu channel"

plot_designator = "Largest m(jj) [GeV]"

list_of_histos = [] #Do not delete or change

#DY+Jets Scale Factor
DY_SF1 = 1.0
DY_SF1_err = 0.0
DY_SF2 = 1.0
DY_SF2_err = 0.0
DY_tot_SF = DY_SF1 * DY_SF2
DY_tot_SF_err = DY_tot_SF * math.sqrt((DY_SF1_err/DY_SF1)**2+(DY_SF2_err/DY_SF2)**2)
DY_input_file = "Z+Jets.root"
list_of_histos.append(DY_input_file)

#W+Jets Scale Factor
W_SF1 = 1.0
W_SF1_err = 0.0
W_SF2 = 1.0
W_SF2_err = 0.0
W_tot_SF = W_SF1 * W_SF2
W_tot_SF_err = W_tot_SF * math.sqrt((W_SF1_err/W_SF1)**2+(W_SF2_err/W_SF2)**2)
W_input_file = "W+Jets.root"
list_of_histos.append(W_input_file)

#EWK_V Scale Factor
EWK_V__SF1 = 1.0
EWK_V__SF1_err = 0.0
EWK_V__SF2 = 1.0
EWK_V__SF2_err = 0.0
EWK_V__tot_SF = EWK_V__SF1 * EWK_V__SF2
EWK_V__tot_SF_err = EWK_V__tot_SF * math.sqrt((EWK_V__SF1_err/EWK_V__SF1)**2+(EWK_V__SF2_err/EWK_V__SF2)**2)
EWK_V_input_file = "EWK_V.root"
list_of_histos.append(EWK_V_input_file)

#Rares Scale Factor
Rares_SF1 = 1.0
Rares_SF1_err = 0.0
Rares_SF2 = 1.0
Rares_SF2_err = 0.0
Rares_tot_SF = Rares_SF1 * Rares_SF2
Rares_tot_SF_err = Rares_tot_SF * math.sqrt((Rares_SF1_err/Rares_SF1)**2+(Rares_SF2_err/Rares_SF2)**2)
Rares_input_file = "Rares.root"
list_of_histos.append(Rares_input_file)

#Diboson Scale Factor
VV_SF1 = 1.0
VV_SF1_err = 0.0
VV_SF2 = 1.0
VV_SF2_err = 0.0
VV_tot_SF = VV_SF1 * VV_SF2
VV_tot_SF_err = VV_tot_SF * math.sqrt((VV_SF1_err/VV_SF1)**2+(VV_SF2_err/VV_SF2)**2)
VV_input_file = "VV.root"
list_of_histos.append(VV_input_file)

#TTBar Scale Factor
TT_SF1 = 1.0
TT_SF1_err = 0.0
TT_SF2 = 1.0
TT_SF2_err = 0.0
TT_tot_SF = TT_SF1 * TT_SF2
TT_tot_SF_err = TT_tot_SF * math.sqrt((TT_SF1_err/TT_SF1)**2+(TT_SF2_err/TT_SF2)**2)
TT_input_file = r"tbar{t}.root"
list_of_histos.append(TT_input_file)

#SingleTop Scale Factor
ST_SF1 = 1.0
ST_SF1_err = 0.0
ST_SF2 = 1.0
ST_SF2_err = 0.0
ST_tot_SF = ST_SF1 * ST_SF2
ST_tot_SF_err = ST_tot_SF * math.sqrt((ST_SF1_err/ST_SF1)**2+(ST_SF2_err/ST_SF2)**2)
ST_input_file = "SingleTop.root"
list_of_histos.append(ST_input_file)

#QCD Tranfer Factor
QCD_TF1 = 1.0
QCD_TF1_err = 0.0
QCD_TF2 = 1.0
QCD_TF2_err = 0.0
QCD_CRA = 1.0
QCD_CRA_err = 0.0
QCD_tot_TF = QCD_TF1 * QCD_TF2 * QCD_CRA
QCD_tot_TF_err = QCD_tot_TF * math.sqrt((QCD_TF1_err/QCD_TF1)**2+(QCD_TF2_err/QCD_TF2)**2+(QCD_CRA_err/QCD_CRA)**2)
QCD_input_file = "QCD.root"
list_of_histos.append(QCD_input_file)

##################################
##################################
##################################

#This defines the parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", dest="year", help="Year being run over")
args = parser.parse_args()

#This will set the correct lumi value
acceptable_years = [2016,2017,2018]
set_year = int(args.year)
if (set_year not in acceptable_years):
	print("Please input acceptable year (2016, 2017, or 2018) with option -y.")
	sys.exit()

years = [2016, 2017, 2018]
lumi = [35.9, 41.5, 59.7]

legend_nColumn = 3

nBins_for_integral = 1
srbinedges_for_integral = array.array('d',[min(srbinedges),max(srbinedges)])

output_root_file = r.TFile.Open(output_root_name,"RECREATE")

r.gDirectory.mkdir(f"rebinned")
r.gDirectory.mkdir(f"SF_corr")

Total_event_yield = []
Total_event_yield_err = []
Total_event_yield_for_Latex = []

Total_event_yield_no_SF = []
Total_event_yield_no_SF_err = []

##################################
#######  Various functions  ######
##################################

def propagate_err(err_list):
	total_err = 0
	for i in err_list:
		total_err = math.sqrt(total_err**2+i**2)
	return total_err

def rebin_histo(input_plot, input_file):

	#######################################
	### This function opens each file,  ###
	### creates a rebinned clone of the ###
	### values and errors.              ###
	#######################################

	f = r.TFile.Open(input_file, "read")
	histo = f.Get(input_plot)
	name = input_file.split(".")[0]

	#pyroot cant handle the {} in the name, so this is a work around
	if name == f"tbar{{t}}": name = "tbart" 
	
	rebinned_histo = histo.Clone()
	rebinned_histo = rebinned_histo.Rebin(nBins,"Orig_"+name,srbinedges)
	
	rebinned_histo_for_integral = histo.Clone()
	rebinned_histo_for_integral = rebinned_histo_for_integral.Rebin(nBins_for_integral,"Integral_"+name,srbinedges_for_integral)
	
	only_histo_value = rebinned_histo.Clone()
	only_histo_value.SetName("only_val_"+name)
	
	only_histo_err = rebinned_histo.Clone()
	only_histo_err.SetName("only_err_"+name)
	
	for i in range(1,nBins+1):
		only_histo_value.SetBinError(i,0)
		# only_histo_err.SetBinContent(i,0)
	output_root_file.cd(f"rebinned")
	rebinned_histo.Write()
	rebinned_histo_for_integral.Write()
	only_histo_value.Write()
	only_histo_err.Write()
	output_root_file.cd()

def apply_SF(sample, print_results):

	sample_name = sample.split(".")[0]

	#pyroot cant handle the {} in the name, so this is a work around
	if sample_name == f"tbar{{t}}": sample_name = "tbart"
	
	output_root_file.cd()

	only_histo_value = output_root_file.Get(f"rebinned/only_val_"+sample_name) #Open Desired Plot
	only_histo_err = output_root_file.Get(f"rebinned/only_err_"+sample_name)
	histo_for_integral = output_root_file.Get(f"rebinned/Integral_"+sample_name)

	#This is the brute force way to do it, but oh well...
	if "QCD" in sample_name:

		SF1 = QCD_TF1
		SF1_err = QCD_TF1_err
		SF2 = QCD_TF2
		SF2_err = QCD_TF2_err
		SF = QCD_tot_TF
		SF_err = QCD_tot_TF_err

		color = r.kOrange+1
		histo_title = "QCD"
		if print_results: print(f"QCD SF used: {SF} ± {round(SF_err,4)}")

	elif "EWK_V" in sample_name:

		SF1 = EWK_V__SF1
		SF1_err = EWK_V__SF1_err
		SF2 = EWK_V__SF2
		SF2_err = EWK_V__SF2_err
		SF = EWK_V__tot_SF
		SF_err = EWK_V__tot_SF_err

		color = r.kRed
		histo_title = "EWK_V"
		if print_results: print(f"EWK_V SF used: {SF} ± {round(SF_err,4)}")

	elif "Rares" in sample_name:

		SF1 = Rares_SF1
		SF1_err = Rares_SF1_err
		SF2 = Rares_SF2
		SF2_err = Rares_SF2_err
		SF = Rares_tot_SF
		SF_err = Rares_tot_SF_err

		color = r.kYellow-7
		histo_title = "Rares"
		if print_results: print(f"Rares SF used: {SF} ± {round(SF_err,4)}")

	elif "SingleTop" in sample_name:

		SF1 = ST_SF1
		SF1_err = ST_SF1_err
		SF2 = ST_SF2
		SF2_err = ST_SF2_err
		SF = ST_tot_SF
		SF_err = ST_tot_SF_err

		color = r.kGreen+1
		histo_title = "SingleTop"
		if print_results: print(f"SingleTop SF used: {SF} ± {round(SF_err,4)}")

	elif "Z+Jets" in sample_name:

		SF1 = DY_SF1
		SF1_err = DY_SF1_err
		SF2 = DY_SF2
		SF2_err = DY_SF2_err
		SF = DY_tot_SF
		SF_err = DY_tot_SF_err

		color = r.kMagenta+1
		histo_title = "Z+Jets"
		if print_results: print(f"Z+Jets SF used: {SF} ± {round(SF_err,4)}")

	elif "W+Jets" in sample_name:

		SF1 = W_SF1
		SF1_err = W_SF1_err
		SF2 = W_SF2
		SF2_err = W_SF2_err
		SF = W_tot_SF
		SF_err = W_tot_SF_err

		color = r.kViolet-9
		histo_title = "W+Jets"
		if print_results: print(f"W+Jets SF used: {SF} ± {round(SF_err,4)}")

	elif "VV" in sample_name:

		SF1 = VV_SF1
		SF1_err = VV_SF1_err
		SF2 = VV_SF2
		SF2_err = VV_SF2_err
		SF = VV_tot_SF
		SF_err = VV_tot_SF_err

		color = r.kBlue-4
		histo_title = "VV"
		if print_results: print(f"VV SF used: {SF} ± {round(SF_err,4)}")

	elif "tbar" in sample_name:

		SF1 = TT_SF1
		SF1_err = TT_SF1_err
		SF2 = TT_SF2
		SF2_err = TT_SF2_err
		SF = TT_tot_SF
		SF_err = TT_tot_SF_err

		color = r.kAzure+10
		histo_title = "tbart"
		if print_results: print(f"bar{{t}} SF used: {SF} ± {round(SF_err,4)}")

	else:
		SF1 = 1.0
		SF1_err = 0.0
		SF2 = 1.0
		SF2_err = 0.0
		SF = 1.0
		SF_err = 0.0

		color = r.kGray
		histo_title = "No_title"
		if print_results: print("No SF used (SF=1)")

	#Get histos that will be SF corrected
	SF_corr_value_histo = only_histo_value.Clone()
	SF_corr_err_histo = only_histo_err.Clone()
	SF_Corr_integral = histo_for_integral.Clone()

	pre_SF_yield = SF_Corr_integral.GetBinContent(1)
	Total_event_yield_no_SF.append(pre_SF_yield)

	pre_SF_yield_err = SF_Corr_integral.GetBinError(1)
	Total_event_yield_no_SF_err.append(pre_SF_yield_err)

	str_pre_SF_Yield = "{} $\\pm$ {}".format(round(pre_SF_yield,1),round(pre_SF_yield_err,2))
	str_SF1 = "{} $\\pm$ {}".format(SF1,SF1_err)
	str_SF2 = "{} $\\pm$ {}".format(SF2,SF2_err)

	output_root_file.cd(f"SF_corr")
	SF_corr_value_histo.SetFillColor(color)
	SF_corr_value_histo.SetLineColor(color)

	SF_histo_value = r.TH1D(f"SF_value_{str(histo_title)}",f"SF_value_{str(histo_title)}",nBins,srbinedges)
	SF_histo_err = r.TH1D(f"SF_err_{str(histo_title)}",f"SF_err_{str(histo_title)}",nBins,srbinedges)

	for i in range(1,nBins+1):
		SF_histo_value.SetBinContent(i,SF)
		SF_histo_value.SetBinError(i,0)
		SF_histo_err.SetBinContent(i,1)
		SF_histo_err.SetBinError(i,SF_err)

	SF_value_for_integral = r.TH1D(f"{histo_title}_SF_for_integral",f"{histo_title}_SF_for_integral",nBins_for_integral,srbinedges_for_integral)
	SF_value_for_integral.SetBinContent(1,SF)
	SF_value_for_integral.SetBinError(1,SF_err)

	SF_histo_value.Write()
	SF_histo_err.Write()

	SF_corr_value_histo.Multiply(SF_histo_value)
	SF_corr_err_histo.Multiply(SF_histo_err)
	SF_Corr_integral.Multiply(SF_value_for_integral)

	SF_corr_value_histo.SetName(f"SF_Corr_{histo_title}")
	SF_corr_value_histo.Write()

	SF_corr_err_histo.SetName(f"SF_err_Corr_{histo_title}")
	SF_corr_err_histo.Write()

	SF_Corr_integral.SetName(f"SF_corr_Integral_{histo_title}")
	SF_Corr_integral.Write()

	tot_yield = SF_Corr_integral.GetBinContent(1)
	Total_event_yield.append(tot_yield)

	tot_yield_error = SF_Corr_integral.GetBinError(1)
	Total_event_yield_err.append(tot_yield_error)

	str_Total_event_yield = "{} ± {}".format(round(tot_yield,1),round(tot_yield_error,2))
	print(f"{sample_name} yield: {str_Total_event_yield}")

	if ((SF == 1) and (SF_err < 0.00000001)):
		Total_event_yield_for_Latex.append([histo_title,str_pre_SF_Yield,"---","---",str_Total_event_yield])
	else:
		Total_event_yield_for_Latex.append([histo_title,str_pre_SF_Yield,str_SF1,str_SF2,str_Total_event_yield])

def sortStack(list_of_histos):

	item_dict = {}

	output_root_file.cd()

	for item in list_of_histos:

		sample_name = item.split(".")[0]

		#pyroot cant handle the {} in the name, so this is a work around
		if sample_name == f"tbar{{t}}": sample_name = "tbart"
			
		histo_name = f"SF_corr/SF_Corr_{str(sample_name)}"

		histo = output_root_file.Get(histo_name)

		histo_size = histo.Integral()

		if sample_name not in item_dict:
			item_dict[sample_name] = histo_size
		elif sample_name in item_dict:
			item_dict[sample_name] += histo_size

	sorted_items = sorted(item_dict, key=item_dict.get, reverse=True)

	total_sum = sum(item_dict.values())

	return sorted_items, total_sum

#########################
#### Start of script ####
#########################

#Rebin all the histograms
for obj in list_of_histos:
	rebin_histo(input_plot, obj)

#Apply the SFs to all histograms
for obj in list_of_histos:
	apply_SF(obj, verbose_print)

print("Total yield: {} ± {}".format(round(sum(Total_event_yield),1),round(propagate_err(Total_event_yield_err),2)))

#This makes it so the legend is in descending order of total event yield
list_of_sorted_histo, max_value = sortStack(list_of_histos)

output_root_file.cd()

canvas_name = input_plot.split("/")[1]
c = r.TCanvas(canvas_name,canvas_name,600,500)

c.Draw()
c.cd()

#This separates the canvas into top and bottom pads
if (generate_data_MC_ratio_plot):

	top_pad = r.TPad("top", "top", 0, 0.25, 1, 1, 0)
	top_pad.SetBottomMargin(-1)
	top_pad.Draw()
	top_pad.cd()

leg = r.TLegend(0.58,0.58,0.83,0.88,"brNDC")
leg.SetHeader("")
leg.SetBorderSize(0)
leg.SetTextSize(0.035)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetNColumns(1)

#Stacked plot which will have all samples added to
Stacked_plot = r.THStack("","")
Stacked_plot.Draw()

#if including data samples, this will add them together and add to the stack 
if (include_Data):

	rebin_histo(input_plot, data_file)

	histo_data_name= f"rebinned/Orig_data"

	histo_data = output_root_file.Get(histo_data_name)

	histo_data.SetMarkerColor(r.kBlack)
	histo_data.SetLineColor(r.kBlack)
	histo_data.SetMarkerStyle(20)
	histo_data.SetMarkerSize(1.0)

	# histo_data.Draw("same2")
	leg.AddEntry(histo_data, "Data", "lep")

#cycle over all samples
for name in list_of_sorted_histo:

	#Get the initial 2016 value, which will then have 2017 & 2018 added to it. 	
	histo_name = f"SF_corr/SF_Corr_{name}"
	histo = output_root_file.Get(histo_name)

	#Due to pyroot not handling {} well
	legend_name = name
	if legend_name == "tbart":
		legend_name = "t#bar{t}"
	
	histo.SetMarkerSize(0)
	Stacked_plot.Add(histo)
	leg.AddEntry(histo, legend_name, "f")

Total_yields_bin_content_x = []
Total_yields_bin_content_y = []
Total_yields_bin_content_err_x = []
Total_yields_bin_content_err_y = []
Total_yields_histo = Stacked_plot.GetStack().Last().Clone()

#This will propagate all the errors together
for i in range(1,nBins+1):
	Total_yields_bin_content_x.append(Total_yields_histo.GetBinCenter(i))
	Total_yields_bin_content_err_x.append(Total_yields_histo.GetBinWidth(i)*0.5)
	Total_yields_bin_content_y.append(Total_yields_histo.GetBinContent(i))
	err_y = 0
	for name in list_of_sorted_histo:
		histo = output_root_file.Get(f"SF_corr/SF_err_Corr_{str(name)}")
		err_value = histo.GetBinError(i)
		err_y = math.sqrt(err_y**2+err_value**2)
	Total_yields_bin_content_err_y.append(err_y)

Total_yields_bin_content_x = array.array('d',Total_yields_bin_content_x)
Total_yields_bin_content_y = array.array('d',Total_yields_bin_content_y)
Total_yields_bin_content_err_x = array.array('d',Total_yields_bin_content_err_x)
Total_yields_bin_content_err_y = array.array('d',Total_yields_bin_content_err_y)

Errors_histo = r.TGraphErrors(nBins,Total_yields_bin_content_x,Total_yields_bin_content_y,Total_yields_bin_content_err_x,Total_yields_bin_content_err_y)
Errors_histo.SetLineWidth(1)
Errors_histo.SetFillColor(r.kMagenta+1)
Errors_histo.SetFillStyle(3004)
Errors_histo.SetLineColor(r.kMagenta+1)

Stacked_plot.Draw()

if (generate_data_MC_ratio_plot): Stacked_plot.GetXaxis().SetTitle(plot_designator)

Stacked_plot.GetXaxis().SetLabelSize(0.0375)
Stacked_plot.GetXaxis().SetTitleSize(0.0375)

Stacked_plot.GetYaxis().SetTitle("Events")
Stacked_plot.GetYaxis().SetLabelSize(0.0375)
Stacked_plot.GetYaxis().SetTitleSize(0.0375)
Stacked_plot.GetYaxis().SetRangeUser(0.00001, max_value*1.2);

Errors_histo.Draw("same2")

if (include_Data):
	histo_data.Draw("same2")

#if including signal samples, this will add them together and add to the stack 
if (include_signal_sample):

	rebin_histo(input_plot, signal_file)

	histo_name = f"rebinned/only_val_{signal_sample_name}"

	histo = output_root_file.Get(histo_name)

	histo.SetMarkerSize(0)
	histo.SetLineColor(r.kBlack)
	histo.SetLineWidth(4)
	histo.SetLineStyle(4)

	histo.Draw("same")
	leg.AddEntry(histo, signal_name, "l")

leg.AddEntry(Errors_histo, "BG stat. uncer", "f")
leg.Draw()

pt0 = r.TPaveText(0.76,0.885,0.91,0.945,"NBNDC")
pt0.SetBorderSize(0)
pt0.SetFillStyle(0)
pt0.SetTextAlign(32)
pt0.SetTextFont(42)
pt0.AddText("{} fb^{} (13 TeV)".format(lumi[abs(2018-(set_year+2))],"{-1}"))
pt0.Draw();

pt1 = r.TPaveText(0.09,0.88,0.24,0.98,"NBNDC")
pt1.AddText(upper_left_title)
pt1.SetTextFont(42)
pt1.SetTextAlign(12)
pt1.SetFillStyle(0)
pt1.SetBorderSize(0)
pt1.SetTextSize(0.04)
pt1.Draw()

pt2 = r.TPaveText(0.11,0.83,0.23,0.90,"NBNDC")
pt2.SetBorderSize(0)
pt2.SetFillStyle(0)
pt2.SetTextAlign(12)
pt2.AddText("CMS ")
pt2.Draw()

pt3 = r.TPaveText(0.11,0.79,0.23,0.83,"NBNDC")
pt3.SetBorderSize(0)
pt3.SetFillStyle(0)
pt3.SetTextAlign(12)
pt3.SetTextFont(52)
pt3.AddText("Preliminary")
pt3.Draw() 

if (generate_data_MC_ratio_plot):
	
	top_pad.Modified()

	c.cd(0)

	bottom_pad = r.TPad("bottom", "bottom", 0, 0.0, 1, 0.28, 0)
	bottom_pad.SetGrid(0,0)
	bottom_pad.SetTitle("")
	bottom_pad.SetTopMargin(0.05)
	bottom_pad.SetBottomMargin(0.25)
	bottom_pad.Draw()
	bottom_pad.cd()

	unity = array.array('d', [1 for i in range(len(srbinedges)-1)])
	# zeroes = array.array('d',  [0 for i in range(len(srbinedges)-1)])
	nominal_error = []

	data_ratio = histo_data.Clone()
	MC_ratio_no_err = r.TH1D("MC_ratio_no_err", "MC_ratio_no_err", nBins, srbinedges)

	for i in range(nBins):

		MC_ratio_no_err.SetBinContent(i+1, Total_yields_bin_content_y[i])
		MC_ratio_no_err.SetBinError(i+1,0.0)

		#Make sure you arent dividing by zero in the MC yield
		if Total_yields_bin_content_y[i] > 0.00000001:
			nominal_error.append(Total_yields_bin_content_err_y[i]/Total_yields_bin_content_y[i])
		else:
			nominal_error.append(0)

	data_ratio.Divide(MC_ratio_no_err)
	data_ratio.SetStats(0)
	data_ratio.GetXaxis().SetTitle(plot_designator)
	data_ratio.GetXaxis().SetRangeUser(min(srbinedges),max(srbinedges))
	data_ratio.GetXaxis().SetTitleSize(0.1)
	data_ratio.GetYaxis().SetTitleOffset(0.12)
	data_ratio.GetXaxis().SetLabelSize(0.10)

	data_ratio.GetYaxis().SetTitle("Data/MC")
	data_ratio.GetYaxis().SetTitleOffset(0.35)
	data_ratio.GetYaxis().SetTitleSize(0.1)
	data_ratio.GetYaxis().SetLabelSize(0.10)

	data_ratio.SetTitle("")
	data_ratio.SetLineWidth(1)
	data_ratio.SetFillColor(r.kMagenta+1)
	data_ratio.SetFillStyle(1001)
	
	data_ratio.Draw("")

	nominal_error_array = array.array('d', nominal_error)
	MC_ratio_with_err = r.TGraphErrors(nBins, Total_yields_bin_content_x, unity, Total_yields_bin_content_err_x, nominal_error_array)
	MC_ratio_with_err.SetLineWidth(1)
	MC_ratio_with_err.SetLineColor(r.kMagenta+1)
	MC_ratio_with_err.SetFillStyle(3004)
	MC_ratio_with_err.SetFillColor(r.kMagenta+1)
	MC_ratio_with_err.Draw("same2")

	line = r.TLine(min(srbinedges),1,max(srbinedges),1)
	line.SetLineColor(2)
	line.SetLineWidth(1)
	line.Draw("same")

c.Write()

if (save_as_PDF):
	c.SaveAs("{}.pdf".format(output_PDF_name))

output_root_file.Close()

if (produce_latex_output):
	Total_yield_no_SF = round(sum(Total_event_yield_no_SF),1)
	Total_yield_no_SF_err = round(propagate_err(Total_event_yield_no_SF_err),2)
	Total_yield_with_SF = round(sum(Total_event_yield),1)
	Total_yield_with_SF_err = round(propagate_err(Total_event_yield_err),2)
	for i in Total_event_yield_for_Latex:
		print(i[0]+" & "+i[1]+" & "+i[2]+" & "+i[3]+" & "+i[4]+" \\\\")
	print("SR BG Prediction & {} $\\pm$ {} & --- & --- & {} $\\pm$ {} \\\\".format(Total_yield_no_SF,Total_yield_no_SF_err,Total_yield_with_SF,Total_yield_with_SF_err))


