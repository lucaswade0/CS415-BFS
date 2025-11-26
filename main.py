from PIL import Image
from collections import deque
import heapq
import sys

def is_valid_vertex(img, x, y):
    """Check if pixel at (x,y) is a valid vertex (R > 100 or G > 100 or B > 100)"""
    color = img.getpixel((x, y))
    r = color[0]
    g = color[1]
    b = color[2]
    return r > 100 or g > 100 or b > 100

def bfs(img, vertexStart, vertexDest):
    """Breadth-First Search algorithm"""
    width = img.width
    height = img.height

    # Check if start and dest are within bounds
    if not (0 <= vertexStart[0] < width and 0 <= vertexStart[1] < height):
        print(f"ERROR: Start point {vertexStart} is out of bounds!")
        return -1
    if not (0 <= vertexDest[0] < width and 0 <= vertexDest[1] < height):
        print(f"ERROR: Dest point {vertexDest} is out of bounds!")
        return -1

    # Check if start and dest are valid vertices
    if not is_valid_vertex(img, vertexStart[0], vertexStart[1]):
        print(f"ERROR: Start point {vertexStart} is not a valid vertex!")
        return -1
    if not is_valid_vertex(img, vertexDest[0], vertexDest[1]):
        print(f"ERROR: Dest point {vertexDest} is not a valid vertex!")
        return -1

    # Initialize data structures
    visited = {}
    distance = {}
    prev = {}

    for i in range(width):
        for j in range(height):
            distance[(i, j)] = sys.maxsize
            visited[(i, j)] = False

    # Initialize queue
    Q = deque()
    Q.append(vertexStart)
    visited[vertexStart] = True
    distance[vertexStart] = 0
    img.putpixel(vertexStart, (0, 0, 255))  # Start Blue

    #(up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # BFS
    while Q and not visited[vertexDest]:
        currentU = Q.popleft()

        for direction in directions:
            neighborX, neighborY = currentU[0] + direction[0], currentU[1] + direction[1]

            if 0 <= neighborX < width and 0 <= neighborY < height:
                if not visited[(neighborX, neighborY)]:
                    # Check if neighbor is a valid vertex
                    if is_valid_vertex(img, neighborX, neighborY):
                        visited[(neighborX, neighborY)] = True
                        img.putpixel((neighborX, neighborY), (0, 255, 0))  # Green
                        distance[(neighborX, neighborY)] = distance[currentU] + 1
                        prev[(neighborX, neighborY)] = currentU
                        Q.append((neighborX, neighborY))

    # Check if destination was reached
    if not visited[vertexDest]:
        print("ERROR: Destination is unreachable!")
        return -1

    # Trace back the path and color it red
    v = vertexDest
    while v != vertexStart:
        img.putpixel(v, (255, 0, 0))  # Red
        v = prev[v]

    return distance[vertexDest]

def calculateH(p, t):
    """Calculate heuristic (Manhattan distance)"""
    return abs(p[0] - t[0]) + abs(p[1] - t[1])

def bestFS(img, vertexStart, vertexDest):
    """Best-First Search (A*) algorithm"""
    width = img.width
    height = img.height

    # Check if start and dest are within bounds
    if not (0 <= vertexStart[0] < width and 0 <= vertexStart[1] < height):
        print(f"ERROR: Start point {vertexStart} is out of bounds!")
        return -1
    if not (0 <= vertexDest[0] < width and 0 <= vertexDest[1] < height):
        print(f"ERROR: Dest point {vertexDest} is out of bounds!")
        return -1

    # Check if start and dest are valid vertices
    if not is_valid_vertex(img, vertexStart[0], vertexStart[1]):
        print(f"ERROR: Start point {vertexStart} is not a valid vertex! (Pixel Too Dark)")
        return -1
    if not is_valid_vertex(img, vertexDest[0], vertexDest[1]):
        print(f"ERROR: Dest point {vertexDest} is not a valid vertex! (Pixel Too Dark)")
        return -1

    # Initialize data structures
    visited = {}
    fScore = {}
    distance = {}
    prev = {}

    for i in range(width):
        for j in range(height):
            distance[(i, j)] = sys.maxsize
            fScore[(i,j)] = sys.maxsize
            visited[(i, j)] = False

    # Initialize priority queue
    Q = []

    # g(s) = 0
    distance[vertexStart] = 0

    # f(s) = g(s) + h(s) = 0 + h(s)
    hStart = calculateH(vertexStart, vertexDest)
    fScore[vertexStart] = hStart
    
    # PQ stores (f-score, vertex)
    heapq.heappush(Q, (fScore[vertexStart], vertexStart))
    img.putpixel(vertexStart, (0, 0, 255))  # Start Blue

    #(up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Best-First Search
    while Q:
        # u = vertex with the minimum f-score
        f, currentU = heapq.heappop(Q)

        if visited[currentU]:
            continue

        visited[currentU] = True

        # Color the visited node (GREEN)
        # Only color if not the start/end and not already colored
        if currentU != vertexStart and currentU != vertexDest:
            img.putpixel(currentU, (0, 255, 0))

        if currentU == vertexDest:
            break

        for direction in directions:
            neighbor = (currentU[0] + direction[0], currentU[1] + direction[1])
            neighborX, neighborY = neighbor

            if 0 <= neighborX < width and 0 <= neighborY < height:
                # Check if neighbor is a valid vertex
                if is_valid_vertex(img, neighborX, neighborY):
                    
                    # Tentative g-score (distance from start) to neighbor
                    tentative_g_score = distance[currentU] + 1
                    
                    # If this path is better than any previously found path to neighbor
                    if tentative_g_score < distance[neighbor]:
                        # Update the path and g-score
                        prev[neighbor] = currentU
                        distance[neighbor] = tentative_g_score

                        # Calculate and update f-score
                        hValue = calculateH(neighbor, vertexDest)
                        fScore[neighbor] = tentative_g_score + hValue
                        
                        # Add or update in the priority queue
                        heapq.heappush(Q, (fScore[neighbor], neighbor))


    # Check if destination was reached
    if not visited[vertexDest]:
        print("ERROR: Destination is unreachable!")
        return -1

    # Trace back the path and color it red
    v = vertexDest
    path_length = 0
    while v in prev:
        img.putpixel(v, (255, 0, 0))  # Red
        v = prev[v]
        path_length += 1

    return distance[vertexDest]

def main():
    # Get input from user
    filename = input("Enter input image name (BMP file): ")

    try:
        img1 = Image.open(filename)
        img2 = Image.open(filename)
    except Exception as e:
        print(f"ERROR: Could not open image file '{filename}': {e}")
        return

    # Display valid coordinate ranges
    print(f"\nImage dimensions: {img1.width} x {img1.height}")
    print(f"Valid row range: 0 to {img1.height - 1}")
    print(f"Valid column range: 0 to {img1.width - 1}\n")


    startRow = int(input("Enter start row: "))
    startCol = int(input("Enter start column: "))
    destRow = int(input("Enter destination row: "))
    destCol = int(input("Enter destination column: "))


    startPoint = (startCol, startRow)
    destPoint = (destCol, destRow)

    # Run BFS
    print("\nRunning Breadth-First Search...")
    resultBFS = bfs(img1, startPoint, destPoint)

    if resultBFS == -1:
        print("BFS failed to find a path.")
        return

    # Run Best-First Search
    print("Running Best-First Search...")
    resultBestFS = bestFS(img2, startPoint, destPoint)

    if resultBestFS == -1:
        print("Best-First Search failed to find a path.")
        return

    # Display the shortest path length
    print(f"\nShortest path length: {resultBFS}")

    print("Start Vertex will be colored Blue in output images to indicate the starting point.")

    # Get output file names
    outputFile1 = input("\nEnter output file name for BFS result (no file extension needed, defaults to .bmp): ")
    outputFile2 = input("Enter output file name for Best-First Search result (no file extension needed, defaults to .bmp): ")

    # Automatically append .bmp extension
    outputFile1 = outputFile1 + ".bmp"
    outputFile2 = outputFile2 + ".bmp"

    # Save output images
    try:
        img1.save(outputFile1)
        print(f"BFS result saved to {outputFile1}")
    except Exception as e:
        print(f"ERROR: Could not save BFS result: {e}")

    try:
        img2.save(outputFile2)
        print(f"Best-First Search result saved to {outputFile2}")
    except Exception as e:
        print(f"ERROR: Could not save Best-First Search result: {e}")

if __name__ == "__main__":
    main()
