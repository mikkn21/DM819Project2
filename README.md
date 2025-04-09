## Second Project of the Course DM819 Computational Geometry

This project was developed together with my fellow student [@jonas-bork](https://github.com/jonas-bork).

The project implements **Fortune's algorithm** as described in *Computational Geometry: Algorithms and Applications (3rd Edition)* to compute Voronoi diagrams in time $O(n \log n)$.

To simplify the problem, we assume the input points are in *general position*. Specifically, the input points satisfy the following conditions:

- All points are distinct.
- No four points lie on a common circle.
- No two points share the same $x$-coordinate.
- No two points share the same $y$-coordinate.
- All points are in the plane.

As we assume the input is in general position, we do not have any *special cases* to consider.

> [!IMPORTANT]
> Please note that the git commit history might not fully reflect the individual contributions, as we pair programmed using the [VS Code Live Share extension](https://marketplace.visualstudio.com/items/?itemName=MS-vsliveshare.vsliveshare).


> **Citation:**  
> de Berg, M., Cheong, O., van Kreveld, M., & Overmars, M. (2008). *Computational Geometry: Algorithms and Applications* (3rd ed.). Springer.
