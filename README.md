# Mood-Learning
Solving health with regression using Emoods as a base dataset!

# Dependencies
* Make
* unzip
* Python 3

Python packages are listed in `requirements.txt`. Make installs them into a local `.venv` on the first run and again whenever `requirements.txt` changes.

# Start
* Place the `export.emoodsw` file in the root of the project
* Run ```make``` to build every figure into `finished/`
* Make only rebuilds what changed: a new export reruns everything, an edited script reruns only its figure
* Run ```make clean``` to remove `data/` and `finished/`, and ```rm -rf .venv``` to reinstall the packages

# Next-day mood forecast
* Run ```make forecast```
* Predicts tomorrow's DEPRESSED, ANXIOUS and MOTIVATION from the last 7 days and compares against guessing the mean and guessing yesterday's value
* Summary figure (errors, strongest features, actual vs predicted) is saved to `finished/forecast.png`

# Lagged correlation
* Run ```make lagged_correlation```
* Left: how each value today relates to each value tomorrow
* Right: for each mood, how a habit relates on the same day, the next day, and the next day after removing the effect of today's mood
* Saved to `finished/lagged_correlation.png`

# Long-term patterns
* Run ```make long_term```
* Top: 3-month averages over all years for mood, caffeine and alcohol, and sleep. The mood chart marks antidepressant start and stop (a gap over 14 days counts as a stop, runs under 7 days are ignored)
* Middle: average by month of year, to show seasons
* Bottom: same-day correlation of key pairs for each year, to show which relationships are stable
* Saved to `finished/long_term.png`

# Correlation matrix
* Run ```make correlation_matrix```
* Same-day correlation between every pair of values
* Saved to `finished/correlation_matrix.png`
