# Exploratory Visualization of Football Match Dynamics

This repository contains the code and final report developed for an exploratory data visualization project in the context of football analytics. The objective of the project is to investigate how contextual factors influence match outcomes and on-field behaviour, using event-level data from Spanish LaLiga football matches.

The work focuses on visual exploration, data preparation and interpretation rather than predictive modelling or causal inference. Several analytical paths were explored; some led to meaningful insights, while others resulted in dead ends that are briefly mentioned as part of the exploratory process.

## Project scope and research questions

The project addresses three main research questions:

1. **Disciplinary behaviour in heavy defeats**  
   How does the frequency of yellow cards change in situations where a team is losing by a large goal difference? Is disciplinary behaviour different in heavy defeats compared to normal match situations?

2. **Team age, experience and performance**  
   Do particularly young teams perform worse than more experienced teams? Is team age associated with match outcomes in balanced matches, and does this relationship change when teams face stronger or weaker opponents?

3. **Short-term impact of VAR-disallowed goals (exploratory dead end)**  
   Does having a goal disallowed by the Video Assistant Referee (VAR) affect a team’s likelihood of conceding shortly afterwards? This analysis is included as an example of an exploratory path that did not lead to conclusive results due to data limitations.

## Repository structure

- `data/`  
  JSON files containing season-level match data.

- `analysis/`  
  Modules implementing the logic for each research question.

- `match/`  
  Utilities for match state reconstruction (scoreline, time intervals, player counts).

- `viz/`  
  Plotting functions used to generate the figures included in the report.

- `main_experience.py`  
  Entry point for the analysis of team age and experience.

- `main_fairplay.py`  
  Entry point for the analysis of disciplinary behaviour in heavy defeats.

- `main_var.py`  
  Entry point for the exploratory VAR analysis.

- `report/`  
  Final written report including motivation, data preparation, visual findings, discussion of dead ends, and conclusions.

## How to reproduce the analyses

Each research question can be reproduced independently by executing the corresponding script:

```bash
python main_experience.py
python main_fairplay.py
python main_var.py
```

All scripts assume that the required datasets are located in the `data/` directory.  
The necessary Python dependencies can be installed using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Running the scripts generates the figures used in the final report.

## Notes

This project is intended for exploratory and educational purposes. The visual patterns shown in the figures are not meant to imply causal relationships; instead, they serve as a basis for discussion and for outlining potential directions for more rigorous statistical analysis.
