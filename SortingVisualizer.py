import pygame
import math
import random
pygame.init()  


class DrawInformation:
    LIGHT = 0XEFEBE0
    
    PURPLE = 0X603F8B
    GREEN = 0XB4FEE7
    PINK = 0XFD49A0
    LIGHT_PURPLE = 0XA16AE8
    
    GREEN2 = 0X00FF00
    RED = 0XFF0000
    BLACK = 0X000000
    
    BACKGROUND_COLOR = 0X16215A
    
    GRADIENTS = [PINK, LIGHT_PURPLE, GREEN, PURPLE]
    
    SIDE_PAD = 100
    TOP_PAD = 150
    
    FONT = pygame.font.SysFont('sans-serif', 30)
    LARGE_FONT = pygame.font.SysFont('sans-serif', 40)
    
    # creating an initializer/ constructor
    def __init__(self, width, height, list):
        self.width = width
        self.height = height
        
        # creating a window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(list) #calling a method which will be defined later
        
    def set_list(self, list):
    # we need our bars to adjust according to the number of elements in the list and height of the bar according to the magnitude of each element in the list
    # so in order to make it dynamic we need to calculate the height and the width
        self.list = list
        self.min_value = min(list)
        self.max_value = max(list)
        
        self.bar_width = round((self.width - self.SIDE_PAD) / len(list)) 
        self.bar_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value)) 
        self.start_x = self.SIDE_PAD // 2
        
        
def draw(draw_info, sorting_algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    heading = draw_info.LARGE_FONT.render("SORTING ALGORITHM VISUALIZER", 1, 0XB4FEE7)
    draw_info.window.blit(heading, (draw_info.width/2 - heading.get_width()/2, 10))
    
    control = draw_info.FONT.render("PRESS: R - RESET | A - ASCENDING | D - DESCENDING | SPACE - START SORT", 1, 0XEFEBE0)
    draw_info.window.blit(control, (draw_info.width/2 - control.get_width()/2, 50))
    
    sorting = draw_info.FONT.render("B - BUBBLE SORT | I - INSERTION SORT | S - SELECTION SORT", 1, 0XEFEBE0)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 80))
    
    sorting2 = draw_info.FONT.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}" , 1, 0XFD49A0)
    draw_info.window.blit(sorting2, (draw_info.width/2 - sorting2.get_width()/2, 120))
    
    draw_list(draw_info)
    pygame.display.update()
    
def draw_list(draw_info, color_positions={}, clear_bg = False):
    #1-Look for every single element in the list
    list = draw_info.list
    
    # to avoid redrawing of the text portion we'll only clear list and redraw it
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
        
        
    for i, val in enumerate(list):
        #2-Determine the height of the element
        #3-Determine the x-coordinate of the element
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.bar_height
        #4-Make sure to draw rectangle's in a slightly different color
        color = draw_info.GRADIENTS[i%4]
        
        # The index will map the color in the dictionary and then we'll manually override the color
        if i in color_positions:
            color = color_positions[i]
            
        #5-Draw a rectangle  representing it
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()    
    

def generate_random_list(n, min_val, max_val):
    list = []
    for _ in range(n): 
        val = random.randint(min_val, max_val) 
        list.append(val)
        
    return list


def bubble_sort(draw_info, ascending=True):
    list = draw_info.list
    
    for i in range(len(list) - 1):
        for j in range(len(list) - 1 - i):
            num1 = list[j]
            num2 = list[j+1]
            
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                list[j], list[j+1] = list[j+1], list[j]
                draw_list(draw_info, {j: draw_info.RED, j+1: draw_info.GREEN2}, True)
                yield True  
                
    return list

 
def insertion_sort(draw_info, ascending=True):
    list = draw_info.list
    
    for i in range(1, len(list)):
        current = list[i]
        
        while True:
            ascending_sort = i > 0 and list[i-1] > current and ascending
            descending_sort = i > 0 and list[i-1] < current and not ascending
            
            if not ascending_sort and not descending_sort:
                break
            
            list[i] = list[i-1]
            i = i-1
            list[i] = current
            draw_list(draw_info, {i-1: draw_info.RED, i: draw_info.GREEN2}, True)
            yield True
            
    return list

def selection_sort(draw_info, ascending=True):
    list = draw_info.list
    
    for i in range(len(list)):
        current = i
        for j in range(i+1, len(list)):
            if list[current] > list[j] and ascending:
                current = j
            elif list[current] < list[j] and not ascending:
                current = j
            
        list[i], list[current] = list[current], list[i]
        draw_list(draw_info, {i: draw_info.RED, current: draw_info.GREEN2}, True)
        yield True 
        
    return list
    

    
# Driver function

def main():
    run = True
    clock = pygame.time.Clock() 
    
    # creating a list 
    
    n = 60
    min_val = 10
    max_val = 100
    
    list = generate_random_list(n, min_val, max_val)
    
    # Drawing the window on the screen
    
    draw_info = DrawInformation(950, 630, list)
    sorting = False
    ascending = True
    
    sorting_algorithm = bubble_sort
    sorting_algo_name = "CURRENT SORTING ORDER"
    sorting_algo_generator = None
    

    while run:
        clock.tick(60)
        
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # If no key pressed then keep on executing whatever is inside of loop
            if event.type != pygame.KEYDOWN:
                continue
            
            # Reset functionality/ Regenerate the list
            if event.key == pygame.K_r:
                list = generate_random_list(n, min_val, max_val)
                draw_info.set_list(list)
                sorting = False
                
            # Start the sort
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)
                
            # Ascending order
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            
            # Descending order
            elif event.key == pygame.K_d and not sorting:
                ascending = False
                
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "BUBBLE SORT"
                
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "INSERTION SORT"
                
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "SELECTION SORT"
            
                
    pygame.quit()

if __name__ == "__main__":
    main()