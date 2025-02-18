# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Chapter 3.4 Three Variables and Beyond
#
# So far in this chapter, we have seen a few ways to summarize and visualize the relationship between two variables. But what if we are working with three or more variables? This section discusses some strategies for dealing with multivariate data.
#
# Let's first read in the Ames housing data set, which will be a working example throughout this section.

# +
# %matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd

housing_df = pd.read_csv("https://raw.githubusercontent.com/dlsun/data-science-book/master/data/AmesHousing.txt", sep="\t")
housing_df.head()
# -

# ## Mapping Aesthetics to Variables
#
# In Section 3.3, we made a scatterplot showing the relationship between living area and sale price. What if we also want to understand how number of bedrooms enters into the equation?
#
# One possibility is to make a three-dimensional scatterplot. However, 3D plots are often misleading when represented in two dimensions, and they don't generalize well to even higher dimensions. A better approach is to use other _aesthetics_ of the plot, such as the color or size of the points, to represent additional variables. 
#
# The `.plot.scatter()` function in `pandas` allows us to control four aesthetics of a scatterplot. We've seen two already:
#
# - `x=`: the variable on the $x$-axis
# - `y=`: the variable on the $y$-axis
#
# but there are two more:
#
# - `c=`: the colors of the points (either the name of a variable in the `DataFrame` or an array specifying the color of each point)
# - `s=`: the sizes of the points (must be an array specifying the size of each point)
#
# For example, to use color to represent the number of bedrooms, we could do the following:

housing_df.plot.scatter(x="Gr Liv Area", y="SalePrice", 
                        c="Bedroom AbvGr", alpha=.5)

# Notice how the colors become darker as you move down the plot. This means that, holding living area constant, a house is less expensive the _more_ bedrooms it has. (Why do you think this is?)
#
# Now, number of bedrooms is a quantitative variable. What if we wanted to visualize how a categorical variable, such as building type, interacts with these two quantitative variables (living area and sale price)? We have to manually construct the array of colors using the `.map()` function we learned in Chapter 1.

# +
cols = housing_df["Bldg Type"].map({
    "1Fam": "blue",
    "TwnhsE": "green",
    "Twnhs": "green",
    "Duplex": "red",
    "2fmCon": "orange"
})

housing_df.plot.scatter(x="Gr Liv Area", y="SalePrice", 
                        c=cols, alpha=.3)
# -

# ## Small Multiples
#
# Rather than try to pack all of the variables into a single plot, we can juxtapose several plots or "facets", each showing the data from a slightly different angle. Edward Tufte coined the term "small multiples" for this type of graphic.
#
# For example, rather than use color to represent building type, we could have made 5 separate scatterplots, one for each building type, and arranged them in a row for easy comparison.

# +
# Specifies a 1 x 5 grid of plots, figsize in inches
fig, axes = plt.subplots(1, 5, figsize=(10, 4))

bldg_types = housing_df["Bldg Type"].unique()
for ax, bldg_type in zip(axes, bldg_types):
    housing_type = housing_df[housing_df["Bldg Type"] == bldg_type]
    housing_type.plot.scatter(x="Gr Liv Area", y="SalePrice", ax=ax)
    ax.set_title(bldg_type)
# -

# Of course, the goal of such a graphic is to facilitate comparison, which is difficult when the $x$- and $y$-axes of the facets are so different. Since the facets are aligned horizontally, it makes sense to use a common $y$-axis for all of them. We can do this by specifying `sharey=True` in `plt.subplots()`. (There is also a corresponding `sharex=` argument.)

# +
fig, axes = plt.subplots(1, 5, figsize=(10, 4), sharey=True)

bldg_types = housing_df["Bldg Type"].unique()
for ax, bldg_type in zip(axes, bldg_types):
    housing_type = housing_df[housing_df["Bldg Type"] == bldg_type]
    housing_type.plot.scatter(x="Gr Liv Area", y="SalePrice", ax=ax)
    ax.set_title(bldg_type)
# -

# Sharing the $y$-axes between the facets also resolved another issue---the colliding $y$-axis labels---since now only the first plot in the figure has an $y$-axis label.

# ## Grammar of Graphics
#
# The **grammar of graphics** organizes the ideas above into a coherent philosophy. The key insight is that a graphic can be specified by mapping its "aesthetics" (e.g., color, size, $x$-axis, column facet) to variables in a data set. Although `pandas` provides some support for this philosophy (as we have seen above), the process is tedious and often requires writing boilerplate code. For example, in order to use color to represent building type, we had to manually map each building type to a color. Libraries based on the grammar of graphics provide a more friendly interface and hide this complexity from the user.
#
# Software packages that implement the grammar of graphics include `ggplot2` in R and [Altair](https://altair-viz.github.io/) in Python. Since we are working in Python, we will use Altair. The first step is to import the package.

from altair import *

# Now, let's use Altair to recreate the scatterplot from earlier, where each point was colored according to the number of bedrooms.
#
# Every Altair command starts with `Chart(your_data_frame)`, followed by the two main elements of the graphic:
# - the mark (i.e., the geometric object being plotted, which for a scatterplot, is a circle)
# - the encoding channels (i.e., mappings between aesthetics and variables)

Chart(housing_df).mark_circle().encode(
    x="Gr Liv Area",
    y="SalePrice",
    color="Bedroom AbvGr"
)

# Now, what if we replace the number of bathrooms, a quantitative variable, with building type, a categorical variable?

Chart(housing_df).mark_circle().encode(
    x="Gr Liv Area",
    y="SalePrice",
    color="Bldg Type"
)

# Notice how Altair automatically inferred that building type was a categorical variable and chose a coloring scheme accordingly. (Compare the color schemes of the two plots above. For quantitative variables, Altair uses a color gradient, while for categorical variables, it uses distinct colors.)

# On the other hand, if we had wanted to have building type be a column facet, using small multiples to show the different building types, we would map the `column` aesthetic to building type:

Chart(housing_df).mark_circle().encode(
    x="Gr Liv Area",
    y="SalePrice",
    column="Bldg Type"
)

# In the examples above, we mapped variables to aesthetics by simply specifying the column names. Although this is convenient, it does not allow the aesthetics to be customized any further. To customize an aesthetic, we have to specify the aesthetic as an object.
#
# Every aesthetic in Altair has an associated Python class. The name of the class is usually just the name of the aesthetic, but with the first letter capitalized. For example, the `x` aesthetic is associated with the `X` class and the `color` aesthetic with the `Color` class. The first argument of the constructor is always the name of the variable to map to the aesthetic, but there are additional arguments that allow for customization.
#
# For example, suppose we wanted the $x$-axis limits to range from 0 to 4000 and the tick labels on the $y$-axis to display numbers in scientific notation (i.e., 2e+5 instead of 200,000). Here's how we could achieve those customizations in Altair:

Chart(housing_df).mark_circle().encode(
    x=X("Gr Liv Area", scale=Scale(domain=(0, 4000))),
    y=Y("SalePrice", axis=Axis(format="e")),
    column="Bldg Type"
)

# ## Summary Statistics
#
# When there are three or more variables, summarizing the relationships can be difficult, so it is usually more fruitful to produce a visualization. That said, there are a few commonly used summary statistics for multivariate data.
#
# The **covariance matrix** is exactly what its name implies; it is a matrix whose $(i, j)$th entry is the correlation between variable $i$ and variable $j$. It is obtained by calling `.cov()` on a `DataFrame`.

# +
variables = ["Gr Liv Area", 
             "Bedroom AbvGr", 
             "Full Bath", 
             "SalePrice"]

housing_df[variables].cov()
# -

# Likewise, the **correlation matrix** is just the corresponding matrix of correlations. All of its entries are between $-1$ and $+1$. It is obtained by calling `.corr()` on a `DataFrame`.

housing_df[variables].corr()

# Why does it make sense that all of the diagonal entries of this matrix are equal to $1.0$?

# # Exercises

# Exercises 1-3 deal with the Tips data set (`https://raw.githubusercontent.com/dlsun/data-science-book/master/data/tips.csv`).

# **Exercise 1.** Make a scatterplot (using `pandas` and `matplotlib`) showing the relationship between the tip and the total bill. Use color to indicate whether the tipper was male or female and the size of each point to represent the party size.

# +
# TYPE YOUR CODE HERE
# -

# **Exercise 2.** Repeat Exercise 1, but using Altair. Can you incorporate even more variables into this figure?

# +
# TYPE YOUR CODE HERE
# -

# **Exercise 3.** Calculate the correlation matrix summarizing the pairwise relationships between the quantitative variables in this data set. Interpret what you see.

# +
# TYPE YOUR CODE HERE
