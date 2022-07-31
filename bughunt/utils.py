"""Module."""
import logging
import math
from dataclasses import dataclass


class State:
    """State."""

    # TODO serialize this class
    # TODO deserialize this class
    ...


@dataclass
class SpriteState:
    """Sprite State."""

    rotation: float = 0.
    x: int = 0
    y: int = 0

    def as_tuple(self):
        """As tuple."""
        return (self.x, self.y, self.rotation)


def is_convex(poly):
    """Check if polygon is convex."""
    if len(poly) < 4:
        return True

    sign = False
    n = len(poly)

    for i in range(n):
        dx1 = poly[(i + 2) % n][0] - poly[(i + 1) % n][0]
        dy1 = poly[(i + 2) % n][1] - poly[(i + 1) % n][1]
        dx2 = poly[i][0] - poly[(i + 1) % n][0]
        dy2 = poly[i][1] - poly[(i + 1) % n][1]
        zcrossproduct = dx1 * dy2 - dy1 * dx2

        if i == 0:
            sign = zcrossproduct > 0
        elif sign != (zcrossproduct > 0):
            return False

    return True


def convex_polygons_overlap(r1, r2):
    """Check if two convex polygons overlap."""
    poly1 = [(i[0], i[1]) for i in r1]
    poly2 = [(i[0], i[1]) for i in r2]

    for shape in range(2):
        if shape == 1:
            poly1 = [(i[0], i[1]) for i in r2]
            poly2 = [(i[0], i[1]) for i in r1]

        for a in range(len(poly1)):
            b = (a + 1) % len(poly1)
            axisProj = (-poly1[b][1] + poly1[a][1], poly1[b][0] - poly1[a][0])
            d = math.sqrt(axisProj[0] * axisProj[0] + axisProj[1] * axisProj[1])
            axisProj = (axisProj[0] / d, axisProj[1] / d)

            # Work out min and max 1D points for r1
            min_r1 = float('inf')
            max_r1 = -float('inf')
            for p in range(len(poly1)):
                q = (poly1[p][0] * axisProj[0] + poly1[p][1] * axisProj[1])
                min_r1 = min(min_r1, q)
                max_r1 = max(max_r1, q)

            # Work out min and max 1D points for r2
            min_r2 = float('inf')
            max_r2 = -float('inf')
            for p in range(len(poly2)):
                q = (poly2[p][0] * axisProj[0] + poly2[p][1] * axisProj[1])
                min_r2 = min(min_r2, q)
                max_r2 = max(max_r2, q)

            if not (max_r2 >= min_r1 and max_r1 >= min_r2):
                return False

    return True


def main():
    """Main function."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Main.")


if __name__ == "__main__":
    main()
