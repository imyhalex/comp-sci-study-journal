# Closest Pair of Points using Divide and Conquer algorithm

- __Details__[[Link](https://www.geeksforgeeks.org/closest-pair-of-points-using-divide-and-conquer-algorithm/)]

## A typical data structure
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y  = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
```

## Brute-Force Search Method
- simply calculate distances between every pair of points
- keep track of the minimum distance and the pair of points that distance

```python
def closest_pair_brute_force(points):
    n = len(points)

    if n < 2:
        return float('inf), (None, None)
    
    min_dist = float('inf)
    closest_pair = (None, None)

    for i in range(n):
        for j in range(i + 1, n):
            distance = Point.dist(points[i], points[j])
            if distance < min_dist:
                min_dist = distance
                closest_pair = (points[i], points[j])
    
    return min_dist, closest_pair
```

## Divide-and-Conquer

- Video Explaination[[Link](https://www.youtube.com/watch?v=6u_hWxbOc7E)]

```java
import java.util.Comparator;

public class ClosestPairDC {

    // -----------------------
    // 1) Point Class
    // -----------------------
    public static class Point {
        public double x, y;
        
        public Point(double x, double y) {
            this.x = x;
            this.y = y;
        }

        // Optional: for debugging/printing
        @Override
        public String toString() {
            return "(" + x + ", " + y + ")";
        }
    }

    // -----------------------
    // 2) Comparators for Merge Sort
    // -----------------------
    // Sort by X-coordinate
    public static Comparator<Point> cmpX = new Comparator<Point>() {
        @Override
        public int compare(Point p1, Point p2) {
            return Double.compare(p1.x, p2.x);
        }
    };

    // Sort by Y-coordinate
    public static Comparator<Point> cmpY = new Comparator<Point>() {
        @Override
        public int compare(Point p1, Point p2) {
            return Double.compare(p1.y, p2.y);
        }
    };

    // -----------------------
    // 3) Custom Merge Sort Implementation
    // -----------------------
    public static void mergeSort(Point[] arr, int left, int right, Comparator<Point> comp) {
        if (left >= right) {
            return; // zero or one element => already sorted
        }
        int mid = (left + right) / 2;
        mergeSort(arr, left, mid, comp);
        mergeSort(arr, mid + 1, right, comp);
        merge(arr, left, mid, right, comp);
    }

    private static void merge(Point[] arr, int left, int mid, int right, Comparator<Point> comp) {
        int n1 = mid - left + 1;
        int n2 = right - mid;

        // Temporary arrays
        Point[] leftArr = new Point[n1];
        Point[] rightArr = new Point[n2];

        // Copy data
        for (int i = 0; i < n1; i++) {
            leftArr[i] = arr[left + i];
        }
        for (int j = 0; j < n2; j++) {
            rightArr[j] = arr[mid + 1 + j];
        }

        // Merge
        int i = 0, j = 0;
        int k = left;
        while (i < n1 && j < n2) {
            if (comp.compare(leftArr[i], rightArr[j]) <= 0) {
                arr[k] = leftArr[i];
                i++;
            } else {
                arr[k] = rightArr[j];
                j++;
            }
            k++;
        }

        // Copy remaining elements
        while (i < n1) {
            arr[k++] = leftArr[i++];
        }
        while (j < n2) {
            arr[k++] = rightArr[j++];
        }
    }

    // -----------------------
    // 4) Entry point for Closest Pair
    // -----------------------
    public static double closestPair(Point[] points) {
        int n = points.length;
        if (n < 2) {
            return 0;  // or Double.POSITIVE_INFINITY if you prefer
        }

        // Create copies sorted by X and by Y
        Point[] px = new Point[n];
        Point[] py = new Point[n];
        System.arraycopy(points, 0, px, 0, n);
        System.arraycopy(points, 0, py, 0, n);

        // Sort each array (custom merge sort)
        mergeSort(px, 0, n - 1, cmpX);
        mergeSort(py, 0, n - 1, cmpY);

        // Now run the recursive divide-and-conquer
        return closestPairRec(px, py, 0, n - 1);
    }

    // -----------------------
    // 5) Recursive Function
    // -----------------------
    private static double closestPairRec(Point[] px, Point[] py, int left, int right) {
        int n = right - left + 1;

        // Base case: if small, use brute force
        if (n <= 3) {
            return bruteForce(px, left, right);
        }

        // Midpoint
        int mid = (left + right) / 2;
        Point midPoint = px[mid];

        // Build py_left and py_right
        // We'll separate points in py according to the x of midPoint
        Point[] pyLeft = new Point[n];
        Point[] pyRight = new Point[n];
        int leftCount = 0;
        int rightCount = 0;

        for (Point p : py) {
            if (p == null) {
                continue;
            }
            if (p.x <= midPoint.x) {
                pyLeft[leftCount++] = p;
            } else {
                pyRight[rightCount++] = p;
            }
        }

        // Recursively find the smallest distances in left and right subarrays
        double dl = closestPairRec(px, pyLeft, left, mid);
        double dr = closestPairRec(px, pyRight, mid + 1, right);
        double d = Math.min(dl, dr);

        // Build strip (points within d of midPoint.x)
        // We'll reuse py to keep them sorted by y
        Point[] strip = new Point[n];
        int sCount = 0;
        for (Point p : py) {
            if (p == null) continue;
            if (Math.abs(p.x - midPoint.x) < d) {
                strip[sCount++] = p;
            }
        }

        // Check points in strip for potentially smaller distance
        double stripDist = stripClosest(strip, sCount, d);
        return Math.min(d, stripDist);
    }

    // -----------------------
    // 6) Brute Force for small subarray
    // -----------------------
    private static double bruteForce(Point[] px, int left, int right) {
        double minDist = Double.POSITIVE_INFINITY;
        for (int i = left; i < right; i++) {
            for (int j = i + 1; j <= right; j++) {
                double dist = distance(px[i], px[j]);
                if (dist < minDist) {
                    minDist = dist;
                }
            }
        }
        return minDist;
    }

    // -----------------------
    // 7) Checking strip (sorted by y)
    // -----------------------
    private static double stripClosest(Point[] strip, int size, double d) {
        double minDist = d;
        // strip is already sorted by y (in practice) because we took it from py
        // For each point, compare with next points while y-distance < d
        for (int i = 0; i < size; i++) {
            // Compare up to 6-7 points after i
            for (int j = i + 1; j < size && (strip[j].y - strip[i].y) < minDist; j++) {
                double dist = distance(strip[i], strip[j]);
                if (dist < minDist) {
                    minDist = dist;
                }
            }
        }
        return minDist;
    }

    // -----------------------
    // 8) Distance Function
    // -----------------------
    public static double distance(Point p1, Point p2) {
        double dx = p1.x - p2.x;
        double dy = p1.y - p2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // -----------------------
    // Main Method - Demo
    // -----------------------
    public static void main(String[] args) {
        Point[] points = {
            new Point(2, 3),
            new Point(12, 30),
            new Point(40, 50),
            new Point(5, 1),
            new Point(12, 10),
            new Point(3, 4)
        };

        double minDist = closestPair(points);
        System.out.println("Minimum distance found: " + minDist);
    }
}
```