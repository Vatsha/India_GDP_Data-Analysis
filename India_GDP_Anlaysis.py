"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal



def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    values = {}
    with open(filename, newline='')as csvfile:
        result = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in result:
            temporary_dict = {}
            for name in row:
                temporary_dict[name] = row[name]
                values[row[keyfield]] = temporary_dict
    return values
#print(read_csv_as_nested_dict('isp_gdp.csv', 'Country Name',',','"'))



def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    table = []
    gdpdat_v2 = {}
    for k, v in gdpdata.items():
        try:
            gdpdat_v2[int(k)] = float(v)
        except ValueError:
            pass

    min_max = [year for year in range(gdpinfo['min_year'], gdpinfo['max_year'] + 1)]

    for key in min_max:
        if key in gdpdat_v2:
            table.append((key, gdpdat_v2[key]))
    return table



def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    gdp_dat = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"],gdpinfo["quote"])

    country_fetch = [k for k in gdp_dat]
    table = {}


    for country in country_list:
        #if country in country_list:
        try:
            table[country] = build_plot_values(gdpinfo, gdp_dat[country])
        except KeyError:
            table[country] = []

    return table
gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }
#print(build_plot_dict({'min_year': 2000, 'country_name': 'Country Name', 'separator': ',', 'country_code': 'Code', 'gdpfile': 'isp_gdp.csv', 'quote': '"', 'max_year': 2005}, ['India']))
t=build_plot_dict(gdpinfo, ['India'])
x=list(t.values())
x=x[0]
x_vals=[]
y_vals=[]
for i in range (len(x)):
    x_vals.append(x[i][0])
    y_vals.append(x[i][1])
def draw_line(title, xvals, yvals):
    """
    Draw line plot with given x and y values.
    """
    lineplot = pygal.Line(height=400)
    lineplot.title = title
    lineplot.x_labels = x_vals
    lineplot.add("Data", yvals)
    lineplot.render_in_browser()

#xvals = [0, 1, 3, 5, 6, 7, 9, 11, 12, 15]
#yvals = [4, 3, 1, 2, 2, 4, 5, 2, 1, 4]

draw_line("My Line Plot", x_vals, y_vals)

def draw_xy(title, x_vals, y_vals):
    """
    Draw xy plot with given x and y values.
    """
    coords = [(xval, yval) for xval, yval in zip(xvals, yvals)]
    xyplot = pygal.XY(height=400)
    xyplot.title = title
    xyplot.add("Data", coords)
    xyplot.render_in_browser()

draw_xy("My XY Plot", x_vals, y_vals)



