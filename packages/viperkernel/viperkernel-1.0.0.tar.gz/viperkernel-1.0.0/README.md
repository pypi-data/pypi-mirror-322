# VIPERKernel

This package can be installed as follows:
```
pip install git+https://github.com/califano-lab/VIPERKernel.git@main
```

VIPERKernel is an algorithm that builds on CellRank (Weiler et al., 2024) to compute velocity based on the TFs and CoTFs identified using the VIPER algorithm. In this approach, we assume that as samples differentiate, the top TFs and CoTFs defining their cell state will increase in activity (while the lowest ones will decrease). Velocity is computed by identifying the top 50 and bottom 50 top regulators of each sample from its VIPER activity, along with its 15 nearest neighbors (NN) using Scanpy. NN with greater increases of the top regulators and greater decreases of bottom regulators receive a higher score. These scores are converted into probabilities, giving us a transition matrix.

This protein velocity algorithm assumes that undifferentiated populations are differentiating, with the MRs defining populations increasing as they become more differentiated and stable in their cell states. However, this assumption may not hold true in cases where normal or cancer populations change from one clearly defined differentiated state into another differentiated state.

## Dependencies:
- cellrank
- tqdm
- numpy

## References:
Weiler, P., Lange, M., Klein, M., Pe’er, D., & Theis, F. (2024). CellRank 2: unified fate mapping in multiview single-cell data. Nature Methods, 1-10.
