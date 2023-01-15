import pygame
import random 
import math 

pygame.init() 

class DrawInformation: 
    #basic information for colors, fonts gradients, padding etc
    BLACK = 0,0,0
    WHITE = 255,255,255
    SORTING_COL1 = 64, 224, 208
    SORTING_COL2 = 142,75,180
    BACKGROUND_COL = 254,250,212 

    FONT = pygame.font.SysFont('system',25)
    LARGE_FONT = pygame.font.SysFont('system',35)
    SIDE_PAD = 40
    TOP_PAD = 150

    GRADIENTS = [ 
        (199,44,65),
        (238,69,64),
        (128,19,54)

    ]

    def __init__(self, width, height, lst): 
        self.width = width
        self.height = height

        #window for pygame
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst): 
        #Used to determine wtih of bars (based on num entries, screen size)
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        #bar dimensions
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height-self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending): 

    #fills screen with selected background color 
    draw_info.window.fill(draw_info.BACKGROUND_COL)
    
    #header 
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    #titles/basic commands
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 -controls.get_width()/2, 50))

    #ascending and descnending sorted algorithms
    sorting = draw_info.FONT.render("I - Insertion | B - Bubble ", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 80))

    #ascneding only algorithms 
    sorting = draw_info.FONT.render("H - Heap | Q - Quick", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 110))

    draw_algo(draw_info)

    pygame.display.update()

def draw_algo(draw_info, color_positions={}, clear_bg=False): 
    lst = draw_info.lst 

    #clears background 
    if clear_bg: 
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, 
                        draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COL, clear_rect)

    #getting height and length of list objects 
    for i, val in enumerate(lst): 
        x = draw_info.start_x  + i * draw_info.block_width 
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

    #keeps the gradient colors 
        color = draw_info.GRADIENTS[i % 3] 

    #changes colors of bars at a specific index (the ones being currently moved)
        if i in color_positions: 
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width,  draw_info.height))
    
    if clear_bg: 
        pygame.display.update()

# generates starting list by selecting heights in range and appending them to the list 
def generate_starting_list(n, min_val, max_val): 
    
    nums = list(range(min_val, max_val))
    random.shuffle(nums)
    return nums[:n] 

#bubble sort algorithm  
def bubble_sort(draw_info, ascending=True): 
    """
    This is a simple bubble sort algorithm that takes in the draw_info, and 
    a boolean for ascending 

    it compares two adjacent elements, and swaps them based on comparison 
    
    The function returns the sorted list
    """
    lst = draw_info.lst 

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i): 
            num1 = lst[j]
            num2 = lst[j + 1]

            #if in ascending and num to left > num to right, swap, opposite for desending 
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending): 

                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                
                #draws algorithm 
                draw_algo(draw_info, {j: draw_info.SORTING_COL1, j + 1: draw_info.SORTING_COL2}, True) 
                yield True 

    return lst 

#insertion sort algorithm 
def insertion_sort(draw_info, ascending=True):
    """
    This is a classic insertion sort algorithm, taking 2 parameters, draw_info, and whether 
    its ascending or descending (bool)

    Compares from left to right, and compares to previous items 
    Using this comparison, it "inserts" the novel element in the right position 

    The function returns the sorted list
    """
    
    #gets unsorted list
    lst = draw_info.lst

    #loops trough elements in array 
    for i in range(1, len(lst)): 

        #sets current to leftmost, unvisited point 
        current = lst[i]

        #repeats current value is placed in the right position 
        while True: 

            #compares current element to previous 
            ascending_sort = i > 0 and lst[i - 1] > current and ascending 
            descending_sort = i > 0 and lst[i - 1] < current and not ascending 

            #if element lower is smaller (for ascending) or if element below is larger (for descending)
            #continue, else break 
            if not ascending_sort and not descending_sort: 
                break 
            
            #assigns the value to the index below it 
            lst[i] = lst[i - 1]

            #moves down to the lower index 
            i = i - 1 
            lst [i] = current 

            #draws sorting algorithm 
            draw_algo(draw_info, {i-1: draw_info.SORTING_COL1, i: draw_info.SORTING_COL2}, True)
            yield True 

    return lst 

def quick_sort(draw_info, ascending=True):
    """
    This quick sort algorithm takes in draw_info and an ascending boolean 

    The implementation here is a 3 median pivot quick sorting system (see partition section for more info).
    Some advantages of a 3 median pivot quick sort is that you get a guaranteed O(nlogn) for a sorted 
    or reversed data. Although there is a slight increase in constant time to find the median, we always
    have at least one item on each side of pivot (better worst-case, with less cutoffs as well)

    Here we are getting help from the quick sort helper functoin, which yields to update the vizualization
    """
    yield from quick_sort_helper(draw_info, 0, len(draw_info.lst), ascending)

def quick_sort_helper(draw_info, start, end, ascending=True):
    #checks if the start index is less than the end
    if start < end:
        #gets pivot index pased on result from partition, yields to draw on screen 
        pivot_index = yield from partition(draw_info, start, end, ascending)

        #left and right side of pivot sorting (recursive call)
        yield from quick_sort_helper(draw_info, start, pivot_index, ascending)
        yield from quick_sort_helper(draw_info, pivot_index + 1, end, ascending)


def partition(draw_info, start, end, ascending=True):
    """
    This function takes the drawing info, the start, the end, and whether the sort is in ascending or 
    descending order
    
    This partition algorithm uses a median of 3 function to find the pivot, to split array as evenly as possible
    It first moves the pivot out of the way by swapping it with the start point 
    Then it runs calculations, swapping values before and after pivot location if they meet the requirements 
    (everything before location of pivot must be smaller than pivot and vice vera)
    3 median allows us to skip the start and the end, as we already know those 2 are in the right positions 
    The function draws at every swap, yielding to update the display.

    The function returns the pivot index
    """
    lst = draw_info.lst

    # choose pivotusing mkedian of 3 
    pivot = median_of_three(lst, start, end)

    #find index of pivot to move it out of the way 
    pivot_index = lst.index(pivot)
    lst[start], lst[pivot_index] = lst[pivot_index], lst[start]
    i = start + 1

    #swaps if right side is higher and left side is lower (ascending) and vice versa for descending 
    for j in range(start + 1, end):
        if (ascending and lst[j] < pivot) or (not ascending and lst[j] > pivot):
            lst[i], lst[j] = lst[j], lst[i]

            #draws 
            draw_algo(draw_info, {i: draw_info.SORTING_COL1, j: draw_info.SORTING_COL2}, True)
            yield True

            #increments counter 
            i += 1

    #swaps the pivot with the i-1 position, putting it back in its correct place 
    lst[start], lst[i - 1] = lst[i - 1], lst[start]
    draw_algo(draw_info, {start: draw_info.SORTING_COL1, i-1: draw_info.SORTING_COL2}, True)
    yield True

    #returns the index of the pivot 
    pivot_index = i-1
    return pivot_index

    #quick sort median of 3 
def median_of_three(lst, start, end):

    #finds the middle, first and last entries
    first = lst[start]
    middle = lst[(start + end - 1) // 2]
    last = lst[end - 1]

    #sorts using prebuilt function and finds median 
    median = sorted([first, middle, last])[1]
    return median

    
#heap sort algorithm 
def heap_sort(draw_info, ascending =True):
    """
    This is a heap sort function, that takes in thte draw_info and ascneding (bool)

    First it finds the length of the list, and then created a max heap using the heapify 
    function. Once the heap has been made, the largest element of the heap is placed 
    at the end of the array, and this process repeats until the array has been sorted. 

    In this case, the implementation is using a max heap, that sorts in ascending order. 
    To make a descedning order array, a min heap can be created instead of a max heap. 
    Going through the binary tea has a time complexity of logn, and then moving the 
    the max value to the end of the array has a complexity of n, giving the the total 
    time complexity to be of O(nlogn)

    It returns the sorted array at the end
    """
    lst = draw_info.lst 
    n = len(lst)


    for i in range(n // 2 -1, -1, -1):
        heapify(lst, n, i, draw_info)
        draw_algo(draw_info, {i: draw_info.SORTING_COL1, 0: draw_info.SORTING_COL2}, True)
        yield True
        
        
    for i in range(n-1, 0, -1): 
        lst[i], lst[0] = lst[0], lst[i]
        draw_algo(draw_info, {i: draw_info.SORTING_COL1, 0: draw_info.SORTING_COL2}, True)
        yield True

        heapify(lst, i, 0, draw_info)
        draw_algo(draw_info, {i: draw_info.SORTING_COL1, 0: draw_info.SORTING_COL2}, True)
        yield True
        
    return lst

    #for heap sort 
def heapify(lst, n, parent_idx, draw_info):

    #creates max heap 
    largest = parent_idx
    left = 2*parent_idx + 1
    right = 2*parent_idx + 2 

    if left < n and lst[left] > lst[largest]: 
        largest = left
    
    if right < n and lst[right] > lst[largest]:
        largest = right 

    if largest != parent_idx: 
        lst[largest], lst[parent_idx] =  lst[parent_idx], lst[largest]

        #recursive call
        heapify(lst, n, largest, draw_info)

#main 
def main(): 
    run = True
    clock = pygame.time.Clock() 

    #number of elements, min and max vals 
    n =  50
    min_val = 10
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst) 
    sorting = False 
    ascending = True

    #default setting 
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    #loop mandatory in pygame (app will immediately end if not there)
    while run: 

        #speed 
        CLOCK = 30
        clock.tick(CLOCK)

        #uses generator to choose sorting algo 
        if sorting:
            try: 
                next(sorting_algorithm_generator)
            except StopIteration: 
                sorting = False
        
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        #returns list of all events occured since previous call 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False

            if event.type != pygame.KEYDOWN: 
                continue

            #reset screen 
            if event.key == pygame.K_r:
                   lst = generate_starting_list(n, min_val, max_val)
                   draw_info.set_list(lst)
                   sorting == False

            #start sorting 
            elif event.key == pygame.K_SPACE and sorting == False: 
                  sorting = True 
                  sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            #ascneding and descending (apply's to insertion and bubble)
            elif event.key == pygame.K_a and not sorting: 
                  ascending = True 
            elif event.key == pygame.K_d and not sorting: 
                  ascending = False 

             #algorithm key commands
            elif event.key == pygame.K_b and not sorting: 
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort - Average Case O(n2)"
            elif event.key == pygame.K_i and not sorting: 
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort - Average Case O(n2)"
            elif event.key == pygame.K_h and not sorting: 
                ascending = True 
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort - Average Case O(nlogn)"
            elif event.key == pygame.K_q and not sorting: 
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort - Average Case O(nlogn)"

            # speed  controls
            

                
    pygame.quit() 

if __name__ == "__main__": 
    main()