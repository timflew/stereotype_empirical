import csv
import numpy as np
import matplotlib.pyplot as plt
import os


def main():
	
	all_count_male,all_count_female=load_csv()
	all_count=all_count_male+all_count_female

	all_prop=convert2prop(all_count)
	
	plot_prop(all_prop)

	compare_prop(all_prop)

	return None


def load_csv():
	# Get raw counts of male and female
	# Columns-white,black,asian,hispanic
	# Rows-Different income brackets
	stereo_file=open('income_freq_male.csv','rU')
	stereo_read=csv.reader(stereo_file)
	
	all_freq=[]
	for row in stereo_read:
		to_int=map(int,row)
		all_freq.append(to_int)
		
	all_count_male=np.array(all_freq)


	stereo_file=open('income_freq_female.csv','rU')
	stereo_read=csv.reader(stereo_file)
	# white,black,asian,hispanic
	all_freq=[]
	for row in stereo_read:
		to_int=map(int,row)
		all_freq.append(to_int)
		
	all_count_female=np.array(all_freq)
	
	return all_count_male,all_count_female


def convert2prop(all_count):
	# Convert counts to proportions
	total_count = np.sum(all_count,0)

	all_prop=np.divide(all_count.astype(float),total_count.astype(float))
	return all_prop


def plot_prop(all_prop):
	# Plot proportions in heatmap
	fig1 = plt.figure(1)
	rect = fig1.patch
	fig1.set_facecolor('white')
	plt.clf()
	prop_plot=plt.imshow(all_prop, aspect='auto', interpolation='nearest')
	prop_plot.set_cmap('rainbow')
	xlabels = ['White', 'Black', 'Asian', 'Hispanic']
	plt.xticks([0,1,2,3], xlabels, rotation='vertical')

	ylabels = ['Under $2,500', '$250,000 and above']
	plt.yticks([0,43], ylabels, rotation='horizontal')

	plt.colorbar()
	plt.show()
	return None

def compare_prop(all_prop):
	# Compare proportions across races
	num_race = np.size(all_prop,1)

	race_comp=np.zeros((num_race,num_race))
	
	for race1 in range(0,num_race):
		for race2 in range(0,num_race):
			if race1 != race2:
				curr_race1=all_prop[:,race1]
				curr_race2=all_prop[:,race2]
				race_comp[race1,race2]=np.mean(compare_race(curr_race1,curr_race2,race1,race2))
			else:
				race_comp[race1,race2]=None

	fig1 = plt.figure(2)
	fig1.set_facecolor('white')
	plt.clf()
	prop_plot=plt.imshow(race_comp, aspect='auto', interpolation='nearest')
	prop_plot.set_cmap('rainbow')
	xlabels = ['White', 'Black', 'Asian', 'Hispanic']
	plt.xticks([0,1,2,3], xlabels, rotation='horizontal')

	ylabels = ['White', 'Black', 'Asian', 'Hispanic']
	plt.yticks([0,1,2,3], ylabels, rotation='vertical')

	plt.title('Probability Row greater than Column')

	plt.colorbar()
	plt.show()


	return None

def compare_race(race1,race2,n1,n2):
	# Pairwise race comparison
	fold_name='comp_race'
	if not os.path.exists(fold_name):
		os.makedirs(fold_name)

	fname='comp_race'+str(n1)+'_'+str(n2)+'.npy'

	full_fname=os.path.join(fold_name,fname)

	if not os.path.isfile(full_fname):
		print 'Fitting '+fname
		num_income=range(0,len(race1))
		num_samp=20000
		race_comp=[]
		for its in range(0,num_samp):
			race1_choice=np.random.choice(num_income,p=race1)
			race2_choice=np.random.choice(num_income,p=race2)
			if race1_choice>race2_choice:
				race_comp.append(1)
			elif race1_choice<race2_choice:
				race_comp.append(0)
		race_comp_array=np.array(race_comp)
		np.save(full_fname,race_comp_array)
	else:
		race_comp_array=np.load(full_fname)

	return race_comp_array





if __name__=='__main__':
	main()

