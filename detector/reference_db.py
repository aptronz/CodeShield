REFERENCE_SOLUTIONS = {
    "python": [
        """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""",
        """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
""",
        """
def linear_search(items, target):
    for idx in range(len(items)):
        if items[idx] == target:
            return idx
    return -1
""",
        """
def is_palindrome(text):
    left = 0
    right = len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True
""",
        """
def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result
""",
        """
if __name__ == "__main__":
    number = int(input())
    print(number * number)
""",
    ],
    "javascript": [
        """
function bubbleSort(arr) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr.length - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        const tmp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = tmp;
      }
    }
  }
  return arr;
}
""",
        """
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
""",
        """
function showMessage() {
  alert("Hello, JavaScript!");
}
""",
        """
<!DOCTYPE html>
<html>
<head>
  <title>Simple JS</title>
</head>
<body>
  <button onclick="showMessage()">Click Me</button>
  <script>
    function showMessage() {
      alert("Hello, JavaScript!");
    }
  </script>
</body>
</html>
""",
    ],
    "java": [
        """
class Factorial {
    static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
""",
        """
class Search {
    static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
}
""",
        """
public class Main {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 0; i < n; i++) {
            System.out.println(i);
        }
    }
}
""",
        """
class Fibonacci {
    static int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
}
""",
    ],
    "cpp": [
        """
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
""",
        """
int linear_search(int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}
""",
        """
#include <iostream>
using namespace std;

int main() {
    int n = 5;
    for (int i = 0; i < n; i++) {
        cout << i << endl;
    }
    return 0;
}
""",
        """
int gcd(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
""",
    ],
}
