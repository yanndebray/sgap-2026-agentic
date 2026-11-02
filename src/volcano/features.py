"""Feature functions and transformers.

Owns: pure-Python feature functions (stateless, attached to the
pipeline via `.skb.apply_func`) and sklearn-compatible transformers
(stateful, attached via `.skb.apply`). Composition into the learner
happens in `pipeline.py`.
"""

from __future__ import annotations

import pandas as pd

# Major oxides (raw, then normalized to 100%), trace elements and their
# ratios, and isotope ratios, in file order. The isotope columns and
# `Fe2O3T` are empty in the training table, so the imputer drops them.
CHEMISTRY_COLUMNS = [
    "SiO2", "TiO2", "Al2O3", "FeO", "Fe2O3", "Fe2O3T", "FeOT", "MnO", "MgO",
    "CaO", "Na2O", "K2O", "P2O5", "Cl", "LOI", "Total",
    "SiO2_normalized", "TiO2_normalized", "Al2O3_normalized",
    "FeOT_normalized", "MnO_normalized", "MgO_normalized", "CaO_normalized",
    "Na2O_normalized", "K2O_normalized", "P2O5_normalized", "Cl_normalized",
    "Total_normalization",
    "Rb", "Sr", "Y", "Zr", "Nb", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Sm",
    "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "Pb",
    "Th", "U", "La_Yb", "Zr_Nb",
    "Sr87_Sr86", "Sr87_Sr86_2SE", "Nd143_Nd144", "Nd143_Nd144_2SE",
]  # fmt: skip
TECHNIQUE_COLUMN = "AnalyticalTechnique"
FEATURE_COLUMNS = [*CHEMISTRY_COLUMNS, TECHNIQUE_COLUMN]


def select_features(table: pd.DataFrame) -> pd.DataFrame:
    """Keep the chemistry and analytical-technique columns of each row.

    Identifiers, provenance, flags, coordinates and dating columns are
    dropped: they identify the volcano or are unknown for a new sample.
    """
    return table[FEATURE_COLUMNS]
