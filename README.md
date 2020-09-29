## Project Overview:

Story Squad is an interactive game where children create stories and illustrations, and compete with other children based on their individual scores.

## Data Sources

Due to COPPA compliance, all data scources are private. Contact the project stakeholder for access.


PDF files containing images of stories and illustrations are analyzed using the Google Vision API, which returns a text string. 

The string is analyzed using a variety of metrics, and a score is returned. 

Player's scores are matched up to their nearest neighbors, and teams of 3 or 4 are created . 

## Endpoints

We should receive either a PDF, or a URL, not both. In the case of PDF files, they will be deconstructed into text files and added to a dictionary where they will be compiled, connected to each other, and from this dictionary, a string of text will be returned. 

In the case of a URL, the URL will be directly fed into the Google Vision API and a string of text will be returned. 
