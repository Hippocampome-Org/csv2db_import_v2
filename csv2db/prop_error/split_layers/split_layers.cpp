// Split neuron pair layer entries into multiple rows
// This changes e.g., layers column:"DG:SMi; DG:H" into "DG:SMi" and "DG:H"
// being on seperate rows.
// Author: Nate Sutton, 2023
// Reference: https://stackoverflow.com/questions/216823/how-to-trim-an-stdstring

#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <functional> 
#include <cctype>
#include <locale>

using namespace std;

static inline string &trim_string(string &s) {
    s.erase(s.begin(), find_if(s.begin(), s.end(),
            not1(ptr_fun<int, int>(isspace))));
    return s;
}

void tokenize(string const &str, const char delim, vector<string> &layer_entries)
{
    stringstream ss(str);
	string s;

    while (getline(ss, s, delim)) {layer_entries.push_back(s);}
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
    	cout << "please include parameters ./split_layers <input_file> <output_file>\n";
    	exit(0);
    }
	string noc_filepath = argv[1]; //"../number_of_contacts.csv";
	string noc_new_filepath = argv[2]; //"../number_of_contacts_reformat.csv";
	fstream noc_file(noc_filepath, ios::in);
	fstream noc_new_file(noc_new_filepath, ios::out);
	vector<vector<string>> content;
	vector<string> row;
	string line, word;
	const char delim = ';';	
	vector<string> layer_entries;
	int layer_index = 8; // column index that layer is stored in

	if(noc_file.is_open())
	{
		while(getline(noc_file, line))
		{
			row.clear();
			stringstream str(line);
			while(getline(str, word, ',')) {row.push_back(word);}
			content.push_back(row);
		}
	}
	else {cout << "Could not open the file\n";}

	for (int i = 0; i < content.size(); i++) {
		layer_entries.clear();
		tokenize(content[i][layer_index], delim, layer_entries);
		if (layer_entries.size() > 1) {
			for (int k = 0; k < layer_entries.size(); k++) {
				for (int j = 0; j < content[i].size(); j++) {
					// skip first column because auto-id will be added in the column
					if (j == 0) { /* skip */ }
					// add parsed layer entry
					else if (j == layer_index) {noc_new_file << trim_string(layer_entries[k]);}
					else {noc_new_file << content[i][j];}
					if (j < (content[i].size())) {noc_new_file << ",";}
				}
				noc_new_file << "\n";
			}
		}
		else {
			for (int j = 0; j < content[i].size(); j++) {
				if (j == 0) { /* skip */ }
				else {noc_new_file << content[i][j];}
				if (j < (content[i].size())) {noc_new_file << ",";}
			}
			noc_new_file << "\n";
		}
	}

	noc_file.close();
	noc_new_file.close();

	cout << "completed\n";

	return 0;
}