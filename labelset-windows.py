#!/usr/bin/env python -O
#-*-coding:big5-*-
#Author:chen, chien-ting
#Updated Day:2011-04-26
#license: GPL (http://www.gnu.org/licenses/gpl.html)
'''
WARNING:
The usage of the program MAY NOT violate the laws, and the author of the
program DOES NOT have the responsibility for the usage of other users.
'''

import re #regular expression
import sys #used to control system
import os #used to detect the system information

os_name = os.name #the type of operating system (posix, nt, and so on).


'''funtcion to quit the program'''
def quit_program():
        a = raw_input("請按 Enter 鍵繼續...")
        exit()

'''open data file'''
raw_data_file = open('in.txt','r').readlines() #open the data file(in.txt) and spilt it by line.
raw_database = [] #raw_database


'''transfer raw_data_file to raw_database'''
for i in range(len(raw_data_file)):
	line = raw_data_file[i] #content of line i of raw_data_file.

	#ignore empty line.
	if re.match ('^\s*$', line):
		pass
	
	#ignore lines with unnacessary data.
	elif re.match('^\S+$',line):
		pass
	
	elif re.match('^\s*[^#]', line): #avoid import commends (starts with #) and null line
		line = re.split('#', line)[0] #ignore commend (starts with #)
		line_splitted = re.split('\s+', line) #split it with space, tab, and linefeed.
                
                '''delete the null string splitted improperly by linefeed character.'''
                if line_splitted[-1] == '':
			del line_splitted[-1]
		
		'''if the data item is/are too many or too few, print the error.'''
		if len(line_splitted) != 3:
			print "第 %d 行的資料不足或過多，請檢查資料內容是否正確。"\
							  % (i + 1)
			print line_splitted
			quit_program()
				
                '''try to convert the distance to float'''
                try:
		       	line_splitted[2] = float(line_splitted[2])

	       	#If the distance can't be floated, print the error.
		except ValueError:
			print "第 %d 行的距離（或其他成本）之資料錯誤！請檢查該資料是否有誤。" % (i + 1)
			quit_program()
		else:
			raw_database.append(line_splitted) #append the line to the raw_database

	else:
		pass


'''convert the raw files.'''
origin = [""] #all the origin points are stored here
all_point = [""] #all the points are stored here
origin_pointer = [""] #pointer for origin points.
destination_and_distance = [] #destination and distance point table of star forward format

for i in range(len(raw_database)):
	for j in range(len(origin)):
		if raw_database[i][0] == origin[j]:
					break
		elif raw_database[i][0] != origin[j] and j == len(origin) - 1:
					if origin == [""]:
						origin = [raw_database[i][0]]
					else:
						origin.append(raw_database[i][0])
		else:
		    pass

'''create all point list'''
for i in range(len(raw_database)):
	for j in [0, 1]:
		for k in range(len(all_point)):
			if raw_database[i][j] == all_point[k]:
				break
			elif (raw_database[i][j] != all_point[k] \
			and k == len(all_point) - 1): 
				if all_point == [""]:
					all_point = [raw_database[i][j]]
				else:
					all_point.append(raw_database[i][j])
			else:
				pass



'''create destination and distance data for forward_star form'''

for i in range(len(origin)):
	
	#create template list storing destination and distace of a origin.
	template_dest_dist = []
	
	for j in range (len(raw_database)):
		if raw_database[j][0] == origin[i]:
			
			#add the destination and distance data in the template
			#list.
			template_dest_dist.append(raw_database[j][1:])
	
	#key in the origin pointer
	if origin_pointer == [""]:
		origin_pointer = [1]
	
	origin_pointer.append(origin_pointer[-1] + len(template_dest_dist))
	
	for i in range(len(template_dest_dist)):
		destination_and_distance.append(template_dest_dist[i])

del(origin_pointer[-1]) #delete one pointer not needed.

print "star forward的形式如下（自1起算）："

'''Print Start'''
print "起點序列如下："

for i in range(len(origin)):
     #print i and comma without creating newline
    sys.stdout.write(origin[i])
    
    #don't print comma in front of last item.
    if i != len(origin)-1 :
        sys.stdout.write(', ')

print '\n'

print "起點指標如下："
print origin_pointer, '\n'

'''Print destination and distance'''
print "迄點與距離如下："
print "迄點", "\t", "距離或成本"
print "-------------------------------"

for i in destination_and_distance:
    print i[0], "\t", i[1]

print "\n"

'''find the shortest_path'''
choice = "" #user's choice to find hte shortest path or not

while (re.match("^yes\s*$",choice) == None) and (re.match("^no\s*$",choice) == None): #\n = linefeed
        print "您想要求得最短路徑嗎？(yes or no)"
        choice = raw_input("\n>>>") #user's choice

if re.match("^no\s*$",choice):
    pass

else:
        point_number_of_start_in_all_point = None #an interger start from 0!

        while point_number_of_start_in_all_point == None:
            
                start = raw_input("請輸入起點：")
                
                for i in range(len(all_point)):
                        if start == all_point[i]:
                                point_number_of_start_in_all_point = i
                                break

        point_number_of_goal_in_all_point = None #an interger start from 0!
        
        while point_number_of_goal_in_all_point == None:

                goal = raw_input("請輸入終點：")

                for i in range(len(all_point)):
                        if goal == all_point[i]:
                                point_number_of_goal_in_all_point = i
                                break
        inf = float("infinity") #define inf as +infinity.
        
        distance_from_start_to_all_point = [inf] * len(all_point) #d(x). inf = infinite
        distance_from_start_to_all_point[point_number_of_start_in_all_point] = 0 #when x = s, d(x) = 0

        previous_point_from_start_to_above = ["unknown"] * len(all_point)
        previous_point_from_start_to_above[point_number_of_start_in_all_point] = None #when x = s, path(x) = none

        y = [start] #y[-1] = real y; other item of y = historical y.

        while y[-1] != goal:
                
                for i in range(len(all_point)):
                        if y[-1] == all_point[i]:
                                point_number_of_y_in_all_point = i
                                break
                
                point_number_of_y_in_origin = None
                
                for i in range(len(origin)):
                        if y[-1] == origin[i]:
                                point_number_of_y_in_origin = i #starts from 0
                                break

                '''refreshing d(x)'''
                for x in range(len(all_point)):
                        '''find a(y,x) of each x'''
                        a_of_y_x = inf #value of a(y,x)
                        if   point_number_of_y_in_origin != None:              
                                index_begin = (origin_pointer[point_number_of_y_in_origin]-1)

                                if point_number_of_y_in_origin == len(origin_pointer) - 1:
                                        index_end = len(destination_and_distance) - 1
                                else:
                                        index_end = (origin_pointer[(point_number_of_y_in_origin)+1]-1)
                                        
                                for i in range(index_begin, index_end):
                                        if x == destination_and_distance[i][1]:
                                                a_of_y_x = destination_and_distance[i][1]
                        
                        '''refreshing d(x)'''
                        distance_from_s_to_y = distance_from_start_to_all_point[point_number_of_y_in_all_point] #d(y)
                        
                        d_of_y_plus_a_of_y_x = distance_from_s_to_y + a_of_y_x #d(y)+a(y,x)

                        '''min{d(x),d(y)+a(y,x)}'''
                        if distance_from_start_to_all_point[x] >= d_of_y_plus_a_of_y_x:
                                distance_from_start_to_all_point[x] = d_of_y_plus_a_of_y_x
                                
                                '''refresh path(x)'''
                                if a_of_y_x != inf:
                                    previous_point_from_start_to_above[x] = all_point[point_number_of_y_in_all_point] 
                        else:
                                pass
                        
                
                '''refreshing y[-1]'''
                number_of_template_y_in_all_points = 0
                min_of_d_x_and_x_not_y = inf #use an infinite and used it to decrease some time to find the min.
                
                for i in range(len(distance_from_start_to_all_point)):
                        for j in y:
                                if all_point[i] == j:
                                        #print "i = %d break"% i
                                        #print "min_of_d_x_and_x_not_y %f" % min_of_d_x_and_x_not_y
                                        break
                                elif all_point[i] != j and j == y[len(y)-1]:
                                        #print "i %d" % i
                                        #print "min_of_d_x_and_x_not_y %f" % min_of_d_x_and_x_not_y
                                        if min_of_d_x_and_x_not_y >= distance_from_start_to_all_point[i]:
                                                min_of_d_x_and_x_not_y = distance_from_start_to_all_point[i]
                                                number_of_template_y_in_all_points = i
                                                #print "number_of_template_y_in_all_points %s" % number_of_template_y_in_all_points
                                else:
                                        pass

                y.append(all_point[number_of_template_y_in_all_points])
                #print y  
                #print 'path', previous_point_from_start_to_above
                                
        else:
                print "找到 %s 到 %s 的最短路徑，" % (start, goal)
                
                '''Print the shortest length. However, if it\'s infinity, print "infinitely long"'''
                if distance_from_start_to_all_point[point_number_of_goal_in_all_point] != inf:
                    print "長度： %s" % distance_from_start_to_all_point[point_number_of_goal_in_all_point]
                else:
                    print "長度： 無限長"
                print "路徑如下："
                
                previous_point = previous_point_from_start_to_above[point_number_of_goal_in_all_point]

                if distance_from_start_to_all_point[point_number_of_goal_in_all_point] != inf:
                    route_path = [previous_point, goal]

                    while previous_point != start:
                        
                        for i in range(len(all_point)):
                            if all_point[i] == previous_point:
                                previous_point = previous_point_from_start_to_above[i]
                                route_path.insert(0, previous_point)
                                
                    for i in range(len(route_path)):
                        sys.stdout.write(route_path[i])
                        
                        if i != len(route_path) - 1:
                            sys.stdout.write(" -> ") #sys.stdout.write means print something without creating newline.
                        else:
                            sys.stdout.write("\n")
                else:
                    print "找不到連絡的路徑！"

quit_program()
