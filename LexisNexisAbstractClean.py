#! usr/bin/env python3
# LXNXAbstractClean.py - Takes LexisNexis Abstracts and cleans them in preparation
# for text mining

import re, os, linecache

# Gets file name from user
file_name = input("Enter base name for all files: ")

# Makes a new folder for cleaned files
new_folder = 'LXNX_' + file_name + '_Clean'
os.makedirs(new_folder)

# Identifies and pulls text file number from filename
ssbfilepattern = re.compile (r"""^(SSBs_)
							(\d*)
							(.txt)
							""", re.VERBOSE)



# Sets count, whitelist characters for cleaning
count = 0
whitelist = set('abcdefghijklmnopqrstuvwxyz-_ ')

#Dictionary to find terms that need to be combined with underscores
repldict = {'ssb':'sugar_sweetened_beverage',
	'SSB':'sugar_sweetened_beverage',
	'ssbs':'sugar_sweetened_beverage',
	'sugar sweetened beverage':'sugar_sweetened_beverage',
	'sugar sweetened beverages':'sugar_sweetened_beverage',
	'sugarsweetened beverage':'sugar_sweetened_beverage',
	'sugarsweetened beverages':'sugar_sweetened_beverage',
	'newyork':'new_york',
	'new york':'new_york',
	'new york city':'new_york_city',
	'newyork city':'new_york_city',
	'-':' '
	}

def replfunc(match):
	return repldict[match.group(0)]

# Creates regex based on dictionary
ssbregex = re.compile('|'.join(re.escape(x) for x in repldict))

# Goes through files in folder, strings them into one line and cleans them
for file in os.listdir('.'):
	mo = ssbfilepattern.search(file)

	if file.endswith('.txt'):
		with open(file) as myfile:
			count = count + 1
			number = mo.group(2)
			abstract=" ".join(line.rstrip() for line in myfile)
			abstract = abstract.lower()
			abstract = ''.join(filter(whitelist.__contains__, abstract))
			abstract = ssbregex.sub(replfunc, abstract)
			f_write = open(os.path.join(new_folder, file_name + '_' + number + '.txt'), 'w')
			f_write.write(abstract)
			f_write.close()

print('Done cleaning '+ str(count)+' documents.')
