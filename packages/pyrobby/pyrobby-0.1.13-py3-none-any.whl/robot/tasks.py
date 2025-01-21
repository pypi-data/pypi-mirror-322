import random
algo_task_1_text = """
Робот должен закрасить клетку 3, двигаясь влево от клетки 2.
"""
# Алгоритмические задания (algo_tasks)
def algo_task_1(app, input_value):
    app.clear_task()
    app.field(5, 5)
    app.robot.start_pos(1,1)
    app.add_end_position(1,2)    
    app.save_environment_to_memory()
    
      # Вызов функции проверки задания

def algo_task_2(app, input_value): 
    app.clear_task()
    app.field(5, 5)
    app.robot.start_pos(3,3)
    app.add_end_position(5,3)    
    app.save_environment_to_memory()
    

def algo_task_3(app, input_value):
    app.clear_task()
    app.field(5, 5)
    app.robot.start_pos(5,5)
    app.add_end_position(5,3) 
    app.add_wall('left',5,4)
    app.add_wall('left',4,4)   
    app.save_environment_to_memory()
    

def algo_task_4(app, input_value):
    app.clear_task()
    app.field(5, 5)
    app.robot.start_pos(5,1)
    app.add_end_position(3,3) 
    app.add_wall('left',5,2)
    app.add_wall('left',4,2)
    app.mark_cell_to_fill(3,2)   
    app.save_environment_to_memory()

def algo_task_5(app, input_value):
    app.clear_task()
    app.field(5, 5)
    app.robot.start_pos(2,3)
    app.add_end_position(1,5)
    for i in range(3,6): 
        app.add_wall('down',1,i)
        app.mark_cell_to_fill(1,i)   
    app.save_environment_to_memory()

def algo_task_6(app, input_value):
    app.clear_task()
    app.field(5, 7)
    app.robot.start_pos(3, 2)
    app.add_end_position(3, 6)
    app.add_wall('left',3,2)
    app.add_wall('right',3,6)
    for i in range(2,7):
        app.mark_cell_to_fill(3,i)
        app.add_wall('up',3,i)
        app.add_wall('down',3,i)    
    app.save_environment_to_memory()

def algo_task_7(app, input_value):
    app.clear_task()
    app.field(5,5)
    app.robot.start_pos(1,1)
    for i in range(2,6):
        app.mark_cell_to_fill(i,i)
    app.add_end_position(5,5)
    app.save_environment_to_memory()

def algo_task_8(app, input_value):
    app.clear_task()
    app.field(4, 4)
    app.robot.start_pos(1, 1)
    app.add_end_position(1, 1)
    for i in range(1,5):
        app.mark_cell_to_fill(i,1)
        app.mark_cell_to_fill(1,i)
        app.mark_cell_to_fill(i,4)
        app.mark_cell_to_fill(4,i)
    app.save_environment_to_memory()
    

def algo_task_9(app, input_value):
    app.clear_task()
    app.field(5,5)
    app.robot.start_pos(1, 1)
    app.add_end_position(5, 5)
    for i in range(1,6):
        if i%2==0:
            app.add_wall('down',i, 5)
            app.add_wall('down',i, 4)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 2)
        else:
            app.add_wall('down',i, 1) 
            app.add_wall('down',i, 2)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 4)
    app.save_environment_to_memory()

def algo_task_10(app, input_value):
    app.clear_task()
    app.field(8, 8)    # Сначала устанавливаем размер поля
    
    # Устанавливаем стартовую позицию робота после установки размера поля
    app.robot.start_pos(8, 8)  # Теперь это будет работать, так как поле 8x8
    app.mark_cell_to_fill(5,1)

    app.add_wall('down',2,4)
    app.add_wall('down',4,4)
    app.add_wall('down',4,1)
    app.add_wall('down',4,6)
    app.add_wall('down',7,6)
    app.add_wall('down',6,5)
    app.add_wall('down',6,8)

    app.add_wall('right',3,1)
    app.add_wall('right',2,2)
    app.add_wall('right',2,4)
    app.add_wall('right',4,2)
    app.add_wall('right',2,2)
    app.add_wall('right',5,4)
    app.add_wall('right',3,3)
    app.add_wall('right',8,7)

    for i in range(4):
        app.add_wall('right',4+i,2)
        app.add_wall('down',3,i+2)
        app.add_wall('down',5,i+4)
    for i in range(3):
        app.add_wall('down',1,i+1)
        app.add_wall('right',5+i,1)
        app.add_wall('left',6+i,4)
    for i in range(2):                
        app.add_wall('right',1+i,4)
        app.add_wall('right',7+i,4)
        app.add_wall('right',2+i,5)
        app.add_wall('right',3+i,6)
        app.add_wall('right',6+i,6)
        app.add_wall('down',1,6+i)
        app.add_wall('down',2,7+i)
        app.add_wall('right',4+i,7) 
        
    app.add_end_position(1, 1)
    app.save_environment_to_memory()

# Задания на циклы For (for_tasks)
def for_task_1(app, task_number):
    app.clear_task()
    app.field(5, 9)
    app.robot.start_pos(3, 2)
    app.add_end_position(3, 8)
    app.add_wall('left',3,2)
    app.add_wall('right',3,8)
    for i in range(7):        
        app.add_wall('up',3,i+2)
        app.add_wall('down',3,i+2)    
    app.save_environment_to_memory()
    

def for_task_2(app, input_value):
    app.clear_task()
    app.field(5, 9)
    app.robot.start_pos(3, 2)
    app.add_end_position(3, 8)
    app.add_wall('left',3,2)
    app.add_wall('right',3,8)
    app.add_wall('up',3,2)
    app.add_wall('down',3,2)
    for i in range(3,9):
        app.mark_cell_to_fill(3,i)
        app.add_wall('up',3,i)
        app.add_wall('down',3,i)    
    app.save_environment_to_memory()

def for_task_3(app, input_value):
    app.clear_task()
    app.field(5, 9)
    app.robot.start_pos(3, 2)
    app.add_end_position(3, 8)
    app.add_wall('left',3,2)
    app.add_wall('right',3,8)
    app.add_wall('up',3,8)
    app.add_wall('down',3,8)
    for i in range(2,8):
        app.mark_cell_to_fill(3,i)
        app.add_wall('up',3,i)
        app.add_wall('down',3,i)    
    app.save_environment_to_memory()

def for_task_4(app, input_value):
    app.clear_task()
    app.field(5, 9)
    app.robot.start_pos(3, 2)
    app.add_end_position(3, 8)
    app.add_wall('left',3,2)
    app.add_wall('right',3,8)    
    for i in range(2,9):
        app.mark_cell_to_fill(3,i)
        app.add_wall('up',3,i)
        app.add_wall('down',3,i)    
    app.save_environment_to_memory()

def for_task_5(app, input_value):
    app.clear_task()
    app.field(7,7)
    app.robot.start_pos(1,1)
    for i in range(2,7):
        app.mark_cell_to_fill(i,i)
    app.add_end_position(7,7)
    app.save_environment_to_memory()

def for_task_6(app, input_value):
    app.clear_task()
    app.field(4, 4)
    app.robot.start_pos(1, 1)
    app.add_end_position(1, 1)
    for i in range(1,5):
        app.mark_cell_to_fill(i,1)
        app.mark_cell_to_fill(1,i)
        app.mark_cell_to_fill(i,4)
        app.mark_cell_to_fill(4,i)
    app.save_environment_to_memory()

def for_task_7(app, input_value):
    app.clear_task()
    app.field(7,5)
    app.robot.start_pos(1, 1)
    app.add_end_position(7, 5)
    for i in range(1,7):
        if i%2==0:
            app.add_wall('down',i, 5)
            app.add_wall('down',i, 4)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 2)
        else:
            app.add_wall('down',i, 1) 
            app.add_wall('down',i, 2)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 4)
    app.save_environment_to_memory()

def for_task_8(app, input_value):
    app.clear_task()
    app.field(7, 7)
    app.robot.start_pos(1, 1)
    for i in range(1, 8):
        for j in range(1, 8):
            if (i + j) % 2 == 0:
                app.mark_cell_to_fill(i, j)
    app.add_end_position(7, 7)
    app.save_environment_to_memory()

def for_task_9(app, input_value):
    app.clear_task()
    app.field(12, 7)
    app.robot.start_pos(2,4)
    app.add_end_position(2,4)
    app.add_wall('up',12,4)
    for i in range(2,12):
        app.add_wall('up',i,4)
        app.mark_cell_to_fill(i,4)
        if i%2==0:
            app.add_wall('right',i,4)            
        else:
            app.add_wall('left',i,4)           
    app.save_environment_to_memory()

def for_task_10(app, input_value):
    app.clear_task()
    app.field(8, 8)
    app.robot.start_pos(1, 2)
    app.add_end_position(1, 2)
    app.add_wall('down',7,2)
    app.add_wall('left',2,2)
    app.add_wall('right',2,7)
    app.mark_cell_to_fill(7,2)
    app.mark_cell_to_fill(2,7)
    app.mark_cell_to_fill(2,2)
    app.mark_cell_to_fill(7,7)
    for i in range(3,8):
        app.add_wall('up',2,i)
        app.add_wall('down',7,i)
        app.add_wall('left',i,2)
        app.add_wall('right',i,7)  
        app.mark_cell_to_fill(i,2)
        app.mark_cell_to_fill(i,7)
        app.mark_cell_to_fill(2,i)
        app.mark_cell_to_fill(7,i)
    for i in range(3,8):
        app.add_wall('up',i,2)
        app.add_wall('up',i,7)
    for i in range(3,6):
        app.add_wall('right',7,i)
        app.add_wall('right',2,i)
    app.save_environment_to_memory()

# Задания на условия If (if_tasks)
def if_task_1(app, input_value):
    app.clear_task()
    app.field(3,3)
    app.robot.start_pos(2,2)
    app.add_end_position(2,2)
    if random.random()>0.5:
        app.add_wall('right',2,2)
        app.mark_cell_to_fill(2,2)
    app.save_environment_to_memory()

def if_task_2(app, input_value):
    app.clear_task()
    app.field(3,5)
    app.robot.start_pos(2,4)
    app.add_end_position(2,2)
    if random.random()>0.3:
        app.add_wall('left',2,2)
        app.mark_cell_to_fill(2,2)
    app.save_environment_to_memory()
    
def if_task_3(app, input_value):
    app.clear_task()
    app.field(3,3)
    app.robot.start_pos(2,2)
    app.add_end_position(2,2)
    if random.random()>0.3:
        app.add_wall('left',2,2)
        app.add_wall('right',2,2)
        app.mark_cell_to_fill(1,2)
    else:
        if random.random()>0.5:
            app.add_wall('left',2,2)
        else:
            app.add_wall('right',2,2)
    app.save_environment_to_memory()

def if_task_4(app, input_value):
   app.clear_task()
   app.field(3, 3)
   app.robot.start_pos(2,2)
   dir = random.randint(1, 2)
   if dir==1:
       app.add_wall('left',2,2)
       app.add_end_position(2,3)
   else:
       app.add_wall('right',2,2)
       app.add_end_position(2,1)
   
   app.save_environment_to_memory()

def if_task_5(app, input_value):
    """
    Задача 2 для if: Робот появляется в одной из верхних ячеек (1 или 2)
    и должен приехать в противоположную нижнюю ячейку (4 или 3 соответственно).
    """
    app.clear_task()
    app.field(2, 2)  # Создаем поле 2x2
    
    # Случайно выбираем начальную позицию (1 или 2 ячейка)
    start_cell = random.choice([1, 2])
    if start_cell == 1:
        end_cell = 4  # Правая нижняя ячейка
    else:
        end_cell = 3  # Левая нижняя ячейка
    
    # Устанавливаем начальную позицию робота
    app.robot.start_pos(start_cell)
    
    # Устанавливаем конечную позицию
    app.add_end_position(end_cell)
    
    app.save_environment_to_memory()

def if_task_6(app, input_value):
    """
    Задача 3 для if: Робот появляется в точке (3,3), рядом со стеной.
    Нужно определить положение стены и закрасить клетку с противоположной стороны.
    """
    
    app.field(5, 5)  # Создаем поле 5x5
    
    # Устанавливаем робота в центр поля (3,3)
    center_m, center_n = 3, 3
    app.robot.start_pos(center_m, center_n)
    
    # Словарь противоположных направлений и соответствующих клеток для закраски
    opposite_directions = {
        'up': {'wall_dir': 'down', 'wall_pos': (center_m - 1, center_n),
               'fill_pos': (center_m + 1, center_n)},
        'down': {'wall_dir': 'up', 'wall_pos': (center_m + 1, center_n),
                'fill_pos': (center_m - 1, center_n)},
        'left': {'wall_dir': 'right', 'wall_pos': (center_m, center_n - 1),
                'fill_pos': (center_m, center_n + 1)},
        'right': {'wall_dir': 'left', 'wall_pos': (center_m, center_n + 1),
                 'fill_pos': (center_m, center_n - 1)}
    }
    
    # Случайно выбираем направление для стены
    wall_direction = random.choice(list(opposite_directions.keys()))
    direction_info = opposite_directions[wall_direction]
    
    # Добавляем стену
    wall_m, wall_n = direction_info['wall_pos']
    app.add_wall(direction_info['wall_dir'], wall_m, wall_n)
    
    
    # Отмечаем клетку для закраски с противоположной стороны
    fill_m, fill_n = direction_info['fill_pos']
    app.add_end_position(fill_m, fill_n)
    app.mark_cell_to_fill(fill_m, fill_n)
    
    app.save_environment_to_memory()


def if_task_7(app, input_value):
    app.clear_task()
    app.field(3, 3)
    rand = random.randint(1, 4) 
    match rand:
        case 1:
            app.robot.start_pos(2,2)
            app.add_wall('up',2,2)
            app.add_wall('left',2,2)
            app.add_wall('down',2,2)
            app.add_end_position(2,3)
            app.mark_cell_to_fill(2,3)
        case 2:
            app.robot.start_pos(2,2)
            app.add_wall('up',2,2)
            app.add_wall('right',2,2)
            app.add_wall('down',2,2)
            app.add_end_position(2,1)
            app.mark_cell_to_fill(2,1)
        case 3:
            app.robot.start_pos(2,2)
            app.add_wall('down',2,2)
            app.add_wall('left',2,2)
            app.add_wall('right',2,2)
            app.add_end_position(1,2)
            app.mark_cell_to_fill(1,2)
        case 4:
            app.robot.start_pos(2,2)
            app.add_wall('up',2,2)
            app.add_wall('left',2,2)
            app.add_wall('right',2,2)
            app.add_end_position(3,2)
            app.mark_cell_to_fill(3,2)
                
    app.save_environment_to_memory()


def if_task_8(app, input_value):
    app.clear_task()
    app.field(4, 4)
    rand = random.randint(1, 4) 
    match rand:
        case 1:
            app.robot.start_pos(2,2)
            app.add_wall('up',2,2)
            app.add_wall('left',2,2)
            app.add_end_position(3,3)
        case 2:
            app.robot.start_pos(2,3)
            app.add_wall('up',2,3)
            app.add_wall('right',2,3)
            app.add_end_position(3,2)
        case 3:
            app.robot.start_pos(3,2)
            app.add_wall('down',3,2)
            app.add_wall('left',3,2)
            app.add_end_position(2,3)
        case 4:
            app.robot.start_pos(3,3)
            app.add_wall('down',3,3)
            app.add_wall('right',3,3)
            app.add_end_position(2,2)

    app.save_environment_to_memory()

def if_task_9(app, input_value): 

    app.clear_task()
    app.field(5, 5)  # Создаем поле 5x5
    
    # Устанавливаем робота в центр поля (3,3)
    center_m, center_n = 3, 3
    app.robot.start_pos(center_m, center_n)
    app.add_end_position(center_m, center_n)
    
    # Случайно добавляем стены
    directions = ['up', 'down', 'left', 'right'] # Вычисляем номер центральной ячейки
    
    # Словарь для связи направления и соответствующей ячейки для закраски
    cells_to_mark = {
        'up': (center_m - 1, center_n),     # Клетка сверху
        'down': (center_m + 1, center_n),   # Клетка снизу
        'left': (center_m, center_n - 1),   # Клетка слева
        'right': (center_m, center_n + 1)   # Клетка справа
    }
    
    # Случайно выбираем, какие стены будут присутствовать
    for direction in directions:
        if random.choice([True, False]):  # 50% шанс для каждой стены
            if direction == 'down':
                app.add_wall('down', 3+1, 3)  # Стена снизу
            elif direction == 'up':
                app.add_wall('up', 3-1, 3)    # Стена сверху
            elif direction == 'right':
                app.add_wall('right', 3, 3+1) # Стена слева
            elif direction == 'left':
                app.add_wall('left', 3, 3-1)  # Стена справа
            
            # Отмечаем клетку для закраски
            m, n = cells_to_mark[direction]
            app.mark_cell_to_fill(m, n)
    
    # Добавляем центральную клетку для закраски
    app.mark_cell_to_fill(center_m, center_n)
    
    # Устанавливаем конечную позицию в центре
    
    
    app.save_environment_to_memory()

def if_task_10(app, input_value):
    app.clear_task()
    app.field(5, 5)
    center_m, center_n = 3, 3
    app.robot.start_pos(center_m, center_n)
    
    # Случайно добавляем стены в углах
    corners = [(2,2), (2,4), (4,2), (4,4)]
    for m, n in random.sample(corners, 2):
        app.add_wall('up' if m < 3 else 'down', m, n)
        app.add_wall('left' if n < 3 else 'right', m, n)
        app.mark_cell_to_fill(m, n)
    
    app.add_end_position(center_m, center_n)
    app.save_environment_to_memory()





# Задания на сложные условия (cif_tasks)
def cif_task_1(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 9)
    required_width = 1 + corridor_length
    app.field(3, required_width)  
    app.robot.start_pos(2, 1)  # m=3, n=2
    app.add_end_position(2,corridor_length)
    app.add_wall('right',2,corridor_length)
    for i in range(1,corridor_length):
        if random.random() < 0.5:  # 50% шанс на выполнение команды
            # Добавляем верхнюю стену коридора
            app.add_wall('up', 2, 1 + i)
            app.mark_cell_to_fill(2, 1 + i)           
    app.save_environment_to_memory()

def cif_task_2(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 9)
    required_width = 1 + corridor_length
    app.field(3, required_width)  
    app.robot.start_pos(2, 1)
    app.add_end_position(2, corridor_length)
    app.add_wall('right', 2, corridor_length)
    
    for i in range(1, corridor_length):
        if random.random() < 0.5:  # 50% шанс на выполнение команды
            # Случайно выбираем верхнюю или нижнюю стену
            wall_position = random.choice(['up', 'down'])
            app.add_wall(wall_position, 2, 1 + i)
            app.mark_cell_to_fill(2, 1 + i)
            
    app.save_environment_to_memory()
   

def cif_task_3(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 9)
    required_width = 1 + corridor_length
    app.field(3, required_width)  
    app.robot.start_pos(2, 1)
    app.add_end_position(2, corridor_length)
    app.add_wall('right', 2, corridor_length)
    
    for i in range(1, corridor_length):
        has_up_wall = random.random() < 0.7    # 50% шанс на верхнюю стену
        has_down_wall = random.random() < 0.7   # 50% шанс на нижнюю стену
        
        # Добавляем стены если они выпали
        if has_up_wall:
            app.add_wall('up', 2, 1 + i)
        if has_down_wall:
            app.add_wall('down', 2, 1 + i)
            
        # Закрашиваем клетку только если есть обе стены
        if has_up_wall and has_down_wall:
            app.mark_cell_to_fill(2, 1 + i)
            
    app.save_environment_to_memory()
    

def cif_task_4(app, input_value):
    app.clear_task()
    rand = random.randint(3,9)
    app.field(rand+2,5)
    app.robot.start_pos(2,3)
    app.add_end_position(rand+1,3)
    app.add_wall('down',rand+1,3)
    for i in range(2,rand+2):
        if random.random()>0.4:
            app.add_wall('left',i,3)
        else:
            app.mark_cell_to_fill(i,2)


    app.save_environment_to_memory()

def cif_task_5(app, input_value):
    app.clear_task()
    rand = random.randint(3,9)
    app.field(rand+2,5)
    app.robot.start_pos(2,3)
    app.add_end_position(rand+1,3)
    app.add_wall('down',rand+1,3)
    for i in range(2,rand+2):
        if random.random()>0.4:
            app.add_wall('left',i,3)
        else:
            app.mark_cell_to_fill(i,2)
        if random.random()>0.4:
            app.add_wall('right',i,3)
        else:
            app.mark_cell_to_fill(i,4)


    app.save_environment_to_memory()

def cif_task_6(app, input_value):
    app.clear_task()
    rand = random.randint(3,9)
    app.field(rand+2,5)
    app.robot.start_pos(2,3)
    app.add_end_position(rand+1,3)
    app.add_wall('down',rand+1,3)
    for i in range(2,rand+2):
        if random.random()>0.4:
            app.add_wall('left',i,3)
            app.mark_cell_to_fill(i,4)
        else:            
            app.add_wall('right',i,3)        
            app.mark_cell_to_fill(i,2)


    app.save_environment_to_memory()

def cif_task_7(app, input_value):
    app.clear_task()
    rand = random.randint(3,9)
    app.field(rand+2,5)
    app.robot.start_pos(2,3)
    app.add_end_position(rand+1,3)
    app.add_wall('down',rand+1,3)
    for i in range(2,rand+2):
        if random.random()>0.4:
            if random.random()>0.4:
                app.add_wall('left',i,3)
                app.mark_cell_to_fill(i,4)
            else:            
                app.add_wall('right',i,3)        
                app.mark_cell_to_fill(i,2)
        else:
            app.add_wall('left',i,3)
            app.add_wall('right',i,3) 
            app.mark_cell_to_fill(i,3)
    app.save_environment_to_memory()

def cif_task_8(app, input_value):
    app.clear_task()
    rand = random.randint(2,9)
    app.field(rand, rand)  # Создаем поле 2x2
    if random.random()>0.5:
        app.robot.start_pos(1,1)
        app.add_end_position(rand,rand)
    else:
        app.robot.start_pos(rand,rand)
        app.add_end_position(1,1)
    
    app.save_environment_to_memory()

def cif_task_9(app, input_value):
    app.clear_task()
    a = random.randint(2,6)
    b = random.randint(2,6)
    app.field(8,13)
    dir = random.choice(['left', 'right']) 
    app.robot.start_pos(a+1,b+1)
    if dir=='left':        
        app.add_end_position(2,2)
        for i in range(2,b+1):
            app.add_wall('up',2,i) 
            app.add_wall('down',2,i)
        for i in range(3,a+2):
            app.add_wall('left',i,b+1)
            app.add_wall('right',i,b+1)
        app.add_wall('up',2,b+1)
        app.add_wall('right',2,b+1)
        app.add_wall('left',2,2)
    else:        
        app.add_end_position(2,b*2)
        for i in range(b+2,b*2+1):
            app.add_wall('up',2,i) 
            app.add_wall('down',2,i)
        for i in range(3,a+2):
            app.add_wall('left',i,b+1)
            app.add_wall('right',i,b+1)
        app.add_wall('up',2,b+1)
        app.add_wall('right',2,b*2)
        app.add_wall('left',2,b+1)
    app.save_environment_to_memory()


def cif_task_10(app, input_value):
    app.clear_task()
    a=0
    b=0
    while a==b:
        a=random.randint(2,7)
        b=random.randint(2,7)
    maximum = max(a,b)
    app.field(9,4)
    app.robot.start_pos(2,2)
    for i in range(2,a+2):
        app.add_wall('left',i,2)
    for i in range(2,b+2):
        app.add_wall('right',i,3)
    if a>b:
        app.add_end_position(maximum+1,2)
    else:
        app.add_end_position(maximum+1,3)
    app.save_environment_to_memory()

# Задания на циклы While (while_tasks)
def while_task_1(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 7)
    required_width = 2 + corridor_length
    app.field(5, required_width)  
    app.robot.start_pos(3, 2)  # m=3, n=2
    app.add_end_position(3,2+corridor_length-1)
    app.add_wall('left', 3,2)
    app.add_wall('right',3,2+corridor_length-1)
    # Добавляем стены для формирования коридора
    for i in range(corridor_length ):   
        # Добавляем верхнюю стену коридора
        app.add_wall('up',3, 2+i)        
        app.add_wall('down',3, 2+i)
    app.save_environment_to_memory()

def while_task_2(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 7)
    required_width = 2 + corridor_length
    app.field(5, required_width)  
    app.robot.start_pos(3, 2)  # m=3, n=2
    app.add_end_position(3,2+corridor_length-1)
    app.add_wall('left', 3,2)
    app.add_wall('right',3,2+corridor_length-1)
    # Добавляем стены для формирования коридора
    for i in range(corridor_length):    
        # Добавляем верхнюю стену коридора
        app.add_wall('up',3, 2+i)
        app.add_wall('down',3, 2+i)
    for i in range(corridor_length-1):   
        # Добавляем верхнюю стену коридора        
        app.mark_cell_to_fill(3,2+i)
        
    app.save_environment_to_memory()

def while_task_3(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 7)
    required_width = 2 + corridor_length
    app.field(5, required_width)  
    app.robot.start_pos(3, 2)  # m=3, n=2
    app.add_end_position(3,2+corridor_length-1)
    app.add_wall('left', 3,2)
    app.add_wall('right',3,2+corridor_length-1)
    # Добавляем стены для формирования коридора
    for i in range(corridor_length ):    
        # Добавляем верхнюю стену коридора
        app.add_wall('up',3, 2+i)        
        app.add_wall('down',3, 2+i)
    for i in range(3,corridor_length+2):               
        app.mark_cell_to_fill(3,i)
        
    app.save_environment_to_memory()    

def while_task_4(app, input_value):
    app.clear_task()
    corridor_length = random.randint(2, 7)
    required_width = 2 + corridor_length
    app.field(5, required_width)  
    app.robot.start_pos(3, 2)  # m=3, n=2
    app.add_end_position(3,2+corridor_length-1)
    app.add_wall('left', 3,2)
    app.add_wall('right',3,2+corridor_length-1)
    # Добавляем стены для формирования коридора
    for i in range(corridor_length ):    
        # Добавляем верхнюю стену коридора
        app.add_wall('up',3, 2+i)        
        app.add_wall('down',3, 2+i)
    for i in range(2,corridor_length+2):               
        app.mark_cell_to_fill(3,i)
        
    app.save_environment_to_memory()

def while_task_5(app, input_value):
    app.clear_task()
    length = random.randint(2, 9)
    app.field(length+1, length+1)
    app.robot.start_pos(1,1)
    app.add_end_position(length+1,length+1)
    for i in range(1,length+1):
        app.mark_cell_to_fill(i+1,i+1)
    app.save_environment_to_memory()

def while_task_6(app, input_value):
    app.clear_task()
    length = random.randint(2, 9)
    app.field(length, length)
    app.robot.start_pos(1, 1)
    app.add_end_position(1,1)
    for i in range(1,length+1):
        app.mark_cell_to_fill(i,1)
        app.mark_cell_to_fill(1,i)
        app.mark_cell_to_fill(i,length)
        app.mark_cell_to_fill(length,i)
    app.save_environment_to_memory()

def while_task_7(app, input_value):
    app.clear_task()
    length = 2
    while length%2==0:
        length = random.randint(3, 11)
    app.field(length,5)
    app.robot.start_pos(1, 1)
    app.add_end_position(length, 5)
    for i in range(1,length+1):
        if i%2==0:
            app.add_wall('down',i, 5)
            app.add_wall('down',i, 4)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 2)
        else:
            app.add_wall('down',i, 1) 
            app.add_wall('down',i, 2)
            app.add_wall('down',i, 3)
            app.add_wall('down',i, 4)
    app.save_environment_to_memory()

def while_task_8(app, input_value):
    app.clear_task()
    length = random.randint(2, 9)
    app.field(length, length)
    app.robot.start_pos(1, 1)
    for i in range(1, length+1):
        for j in range(1, length+1):
            app.mark_cell_to_fill(i,j)        
    app.add_end_position(length, length)
    app.save_environment_to_memory()

def while_task_9(app, input_value):
    app.clear_task()
    length = random.randint(5, 10)
    end = random.randint(2, 4)
    app.field(length,5)
    app.robot.start_pos(2, 3)
    app.add_end_position(length-end+1, 3)
    for i in range(2,length-end+2):
        app.mark_cell_to_fill(i,3)
        app.add_wall('down',i,3)
    app.save_environment_to_memory()

def while_task_10(app, input_value):
    app.clear_task()
    length = random.randint(5, 14)
    app.field(length, length)
    app.robot.start_pos(length, 1)
    app.add_end_position(length, length)
    app.add_wall('up',length,length)    
    # Создаем стены с интервалом в 3 клетки
    wall_positions = [3, 6, 9, 12]      
    for wall_x in wall_positions:
        if wall_x<length-1:
            height = random.randint(3, length-2)
            for i in range(height):
                app.add_wall('right', length-i, wall_x)
                app.mark_cell_to_fill(length-i, wall_x)
                app.mark_cell_to_fill(length-i, wall_x+1)
            app.mark_cell_to_fill(length-i-1, wall_x)
            app.mark_cell_to_fill(length-i-1, wall_x+1)
    app.save_environment_to_memory()


